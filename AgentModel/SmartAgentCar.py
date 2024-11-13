import math

import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

from AgentStreet import Street
from AgentStoplights import Stoplight
from AgentParking import Parking
from AgentBuilding import Building
from AgentStreetDir import AgentStreetDir
import random

class SmartCar(mesa.Agent):
    def __init__(self, uniqueId, model, car, targetDestination, targetParking,startParking,Waze):
        super().__init__(uniqueId, model)
        
        self.carId = car
        self.target = targetDestination
        self.targetParking = targetParking
        
        self.currentDir = ""
        
        self.movementEquivalence = {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "W": (-1, 0)
        }
        self.oppositeDir = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }
        
        self.inDestination = False
        self.justStarted = True
       
        self.prevPos = None
        

        self.multipleDir = False
        self.directions = []
        self.positionHistory = []
        self.visits = {}
        
        self.waze = Waze
        
        self.start = startParking
        self.previousParking = startParking
        self.path = []
        self.foundRoute = False


    def getCurrentDirection(self):
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for c in cell:
            if isinstance(c, Street):
                for dir, value in c.availableDirections.items():
                    if value:
                        self.currentDir = dir
        return (0, 0)  # Default to no movement if no direction is found

    def exitParkingLot(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        for neighbor in neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Street):
                    self.model.grid.move_agent(self, neighbor)
                    self.justStarted = False
                    return

    def checkStoplight(self):
        if self.justStarted:
            self.exitParkingLot()
            
        # Range of positions where there could be a stoplight
        if self.currentDir == "N":
            positions = [(self.pos[0], self.pos[1] + i) for i in range(6) if self.pos[1] + i < self.model.grid.height - 1]
        elif self.currentDir == "S":
            positions = [(self.pos[0], self.pos[1] - i) for i in range(6) if self.pos[1] - i > 0]
        elif self.currentDir == "E":
            positions = [(self.pos[0] + i, self.pos[1]) for i in range(6) if self.pos[0] + i < self.model.grid.width - 1]
        elif self.currentDir == "W":
            positions = [(self.pos[0] - i, self.pos[1]) for i in range(6) if self.pos[0] - i > 0]
        else:
            positions = []
        
        spotlightFound = False
        spotLightPos = None
        
        # Check if there is a stoplight in the range of positions
        if not positions:
            spotlightFound = True
        
        for position in positions:
            cell = self.model.grid.get_cell_list_contents([position])
            # Check if there is a stoplight in the cell
            for agent in cell:
                if isinstance(agent, Stoplight):
                    spotLightPos = position
                    print(self.currentDir)
                    if agent.state == "Green" or agent.state == "Yellow":
                        spotlightFound = True
                    else:
                        spotlightFound = False
                    break
                else:
                    spotlightFound = True
                    
        if spotlightFound:
            self.basicMovementChecker()
            if spotLightPos is not None:
                stopCell = self.model.grid.get_cell_list_contents([spotLightPos])
                for agent in stopCell:
                    if isinstance(agent, Stoplight):
                        agent.carMessage(math.dist(self.pos, spotLightPos))

    def bestPosition(self, positions):
        bestPos = None
        bestDistance = 1000
        for position in positions:
            if position in self.visits:
                visit_count = self.visits[position]
            else:
                visit_count = 0 
            distance = abs(position[0] - self.target[0]) + abs(position[1] - self.target[1])
            effective_distance = distance + (visit_count * 10)
            if (effective_distance < bestDistance and position != self.prevPos
                and position[0] >= 0 and position[0] <= self.model.grid.width - 1 and position[1] >= 0 and position[1] <= self.model.grid.height - 1):
                bestDistance = effective_distance
                bestPos = position
        return bestPos

    def basicMovementChecker(self):
        possibleSteps = []
        
        if self.multipleDir:
            for direction in self.directions:
                cellEquivalence = self.movementEquivalence[direction]
                possibleNextPos = (self.pos[0] + cellEquivalence[0], self.pos[1] + cellEquivalence[1])
                
                if possibleNextPos == self.pos:
                    continue
                if possibleNextPos[0] < 0 or possibleNextPos[0] > self.model.grid.width - 1 or possibleNextPos[1] < 0 or possibleNextPos[1] > self.model.grid.height - 1:
                    continue
                possibleSteps.append(possibleNextPos)
            self.multipleDir = False

        else:
            self.getCurrentDirection()
            
            currentDir = self.movementEquivalence[self.currentDir]
            predefinedMovement = (self.pos[0] + currentDir[0], self.pos[1] + currentDir[1])
            
            neighbors = [(self.pos[0] + 1, self.pos[1]),  # Right
                         (self.pos[0] - 1, self.pos[1]),  # Left
                         (self.pos[0], self.pos[1] + 1),  # Up
                         (self.pos[0], self.pos[1] - 1)]
            
            if (predefinedMovement[0] >= 0 or predefinedMovement[0] <= self.model.grid.width - 1 and predefinedMovement[1] >= 0 or predefinedMovement[1] <= self.model.grid.height - 1):
                possibleSteps.append(predefinedMovement)
 
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                    continue
                
                cell = self.model.grid.get_cell_list_contents([neighbor])
                
                for c in cell:
                    if isinstance(c, SmartCar):
                        continue
                    
                    if isinstance(c, AgentStreetDir):
                        possibleSteps.append(neighbor)
                    
                    if isinstance(c, Parking):

                            if self.previousParking is None:
                                self.previousParking = c.parkingId
                                continue
                            if self.waze.routeExists(self.previousParking,c.parkingId):
                                self.foundRoute = True
                            if self.previousParking != c.parkingId:
    
                                route = str(self.previousParking) + "-" + str(c.parkingId)
                                self.waze.addDirection(route,[self.pos]+[p for p in self.path if p is not None])
                                self.waze.addParkingNeighbors(self.previousParking,c.parkingId,[self.pos]+[p for p in self.path if p is not None])
                                self.path = []
                                self.previousParking = c.parkingId
                                
                            if c.parkingId == self.targetParking:
                                self.inDestination = True
                                route = str(self.previousParking) + "-" + str(c.parkingId)
                                self.waze.addDirection(route,[self.pos]+[p for p in self.path if p is not None])
                                self.waze.addParkingNeighbors(self.previousParking,c.parkingId,[self.pos]+[p for p in self.path if p is not None])
                                self.path = []
                                self.previousParking = c.parkingId
                                self.model.grid.move_agent(self, neighbor)
                                return
                    
                    if isinstance(c, Street):
                        cellDirection = c.currentDirection()
                        cellEquivalence = self.movementEquivalence[cellDirection]
                        possibleNextPos = (neighbor[0] + cellEquivalence[0], neighbor[1] + cellEquivalence[1])
                        if cellDirection == self.oppositeDir[self.currentDir]:
                            continue
                        if possibleNextPos == self.pos:
                            continue
                        possibleSteps.append(neighbor)

        if len(set(self.positionHistory)) < 8:  # Detect a small repeated loop
            if random.random() < 0.5:  # 50% chance to pick a random next step
                nextPos = random.choice(possibleSteps)
            else:
                nextPos = self.bestPosition(possibleSteps)
        else:
            nextPos = self.bestPosition(possibleSteps)
        
        nextCell = self.model.grid.get_cell_list_contents([nextPos])
        for c in nextCell:
            if isinstance(c, SmartCar):
                return
            if isinstance(c,Stoplight):
                if c.state == "Red":
                    return
            if isinstance(c, Building):
                return
            if isinstance(c, AgentStreetDir):
                self.multipleDir = True
                self.directions = c.direction  # Ensure this is correctly set
            else:
                self.multipleDir = False
                self.directions = []
        
        if nextPos == self.target:
            self.inDestination = True
            
        self.prevPos = self.pos        
        self.model.grid.move_agent(self, nextPos)
        self.visits[nextPos] = self.visits.get(nextPos, 0) + 1
        
        self.getCurrentDirection()
        self.path.append(nextPos)

    def step(self):
        if not self.inDestination:
            self.positionHistory.append(self.pos)
            if len(self.positionHistory) > 10:  # Keep only recent history
                self.positionHistory.pop(0)
            self.checkStoplight()
            print("----------------")
            print(self.previousParking)
            print(self.waze.graphDirections)
            print(self.waze.parkingGraph)
        else:
            print("I am in destination")
            self.waze.bestRouteToParking(self.start,self.targetParking)