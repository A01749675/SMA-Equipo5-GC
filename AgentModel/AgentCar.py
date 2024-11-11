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

class Car(mesa.Agent):
    def __init__(self, uniqueId, model, car,targetDestination):
        super().__init__(uniqueId, model)
        self.carId = car
        self.currentDir = ""
        self.movementEquivalence = {
                "N":(0,1),
                "S":(0,-1),
                "E":(1,0),
                "W":(-1,0)
            }
        self.target = targetDestination
        self.inDestination = False
        self.oppositeDir = {
            "N":"S",
            "S":"N",
            "E":"W",
            "W":"E"
        }
    
    def getCurrentDirection(self):
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for c in cell:
            if isinstance(c, Street):
                for dir, value in c.availableDirections.items():
                    if value:
                        self.currentDir = dir
        return (0, 0)  # Default to no movement if no direction is found

    def checkNeighbors(self):
        positions = [(self.pos[0] + 1, self.pos[1]),  # Right
                     (self.pos[0] - 1, self.pos[1]),  # Left
                     (self.pos[0], self.pos[1] + 1),  # Up
                     (self.pos[0], self.pos[1] - 1)]  # Down
        possibleSteps = []
        for position in positions:
            if 0 <= position[0] < self.model.grid.width and 0 <= position[1] < self.model.grid.height:
                cell = self.model.grid.get_cell_list_contents([position])
                for c in cell:
                    if isinstance(c, Street):
                        for dir, value in c.availableDirections.items():
                            if value:
                                possibleSteps.append(position)
        if possibleSteps:
            self.model.grid.move_agent(self, self.random.choice(possibleSteps))
            
    def basicMovement(self):
        currentDirectionMovement = self.getCurrentDirection()
        new_pos = (self.pos[0] + currentDirectionMovement[0], self.pos[1] + currentDirectionMovement[1])
        if 0 <= new_pos[0] < self.model.grid.width and 0 <= new_pos[1] < self.model.grid.height:
            self.model.grid.move_agent(self, new_pos)
    
    def randomBasicMovement(self):
        self.getCurrentDirection()
        forbiddenDirection = ""
        if self.currentDir == "N":
            forbiddenDirection = "S"
        elif self.currentDir == "S":
            forbiddenDirection = "N"
        elif self.currentDir == "E":
            forbiddenDirection = "W"
        elif self.currentDir == "W":
            forbiddenDirection = "E"
        
        steps = [
            (self.pos[0] + 1, self.pos[1]),  # Right
            (self.pos[0] - 1, self.pos[1]),  # Left
            (self.pos[0], self.pos[1] + 1),  # Up
            (self.pos[0], self.pos[1] - 1)  # Down
        ]
        possibleSteps = []
        for step in steps:
            if step[0] < 0 or step[0] >= self.model.grid.width-1 or step[1] < 0 or step[1] >= self.model.grid.height-1:
                continue
            if self.pos == self.movementEquivalence[forbiddenDirection]:
                continue
            cell = self.model.grid.get_cell_list_contents([step])
            for c in cell: 
                if isinstance(c, Street):
                    possibleSteps.append(step)
            
        nextPos = self.random.choice(possibleSteps)
        if nextPos == self.target:
            self.inDestination = True
        self.model.grid.move_agent(self, nextPos)
        
    def checkStoplight(self):
        #Range of positions where there could be a stoplight
        if self.currentDir == "N":
            positions = [(self.pos[0],self.pos[1]+i) for i in range(5) if self.pos[1]+i < self.model.grid.height-1]
        elif self.currentDir == "S":
            positions = [(self.pos[0],self.pos[1]-i) for i in range(5) if self.pos[1]-i > 0]
        elif self.currentDir == "E":
            positions = [(self.pos[0]+i,self.pos[1]) for i in range(5) if self.pos[0]+i < self.model.grid.width-1]
        else:
            positions = [(self.pos[0]-i,self.pos[1]) for i in range(5) if self.pos[0]+i < self.model.grid.width-1]
        
        spotlightFound = False
        spotLightPos = None
        #Check if there is a stoplight in the range of positions
        if not positions:
            spotlightFound = True
        
        for position in positions:
            cell = self.model.grid.get_cell_list_contents([position])
            #Check if there is a stoplight in the cell
            for agent in cell:
                if isinstance(agent, Stoplight):

                    spotLightPos = position
                    print(self.currentDir)
                    if agent.state == "Green":
                        spotlightFound = True
                        print("Green at", position)
                    else:
                        
                        print("Red at", position)
                        spotlightFound = False
                    break
                else:
                    spotlightFound = True
        if spotlightFound:
            self.basicMovementChecker()
        else:
            print(positions)
            print(spotLightPos)
            print("Stop")
        
                    
                    
        
        
    def basicMovementChecker(self):
        if self.inDestination:
            return
        self.getCurrentDirection()
        print(f"I am {self.carId} and I am at {self.pos} and I am going {self.currentDir}")
        currentDir = self.movementEquivalence[self.currentDir]
        predefinedMovement = (self.pos[0] + currentDir[0], self.pos[1] + currentDir[1])
        neighbors = [(self.pos[0] + 1, self.pos[1]),  # Right
                     (self.pos[0] - 1, self.pos[1]),  # Left
                     (self.pos[0], self.pos[1] + 1),  # Up
                     (self.pos[0], self.pos[1] - 1)]
        
        if (predefinedMovement[0] >= 0 or predefinedMovement[0] <= self.model.grid.width-1
                and predefinedMovement[1] >= 0 or predefinedMovement[1] <= self.model.grid.height-1):
            possibleSteps = [predefinedMovement]
        else:
            possibleSteps = []
            
        for neighbor in neighbors:
            if neighbor[0] < 0 or neighbor[0] >= self.model.grid.width-1 or neighbor[1] < 0 or neighbor[1] >= self.model.grid.height-1:
                continue
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Street):
                    cellDirection = c.currentDirection()
                    cellEquivalence = self.movementEquivalence[cellDirection]
                    possibleNextPos = (neighbor[0] + cellEquivalence[0],neighbor[1] + cellEquivalence[1])
                    if cellDirection == self.currentDir:
                        continue
                    if cellDirection == self.oppositeDir[self.currentDir]:
                        continue
                    if possibleNextPos == self.pos:
                        continue
                    possibleSteps.append(neighbor)
        nextPos = self.random.choice(possibleSteps)
        
        print(f"These are the possible steps {possibleSteps}, for the current position of {self.pos}")
        if nextPos == self.target:
            self.inDestination = True
            print("arrived")
        else:
            print(f"Current: {self.pos} Next: {nextPos}")
            print(f"Distance to target {abs(nextPos[0]-self.target[0]) + abs(nextPos[1]-self.target[1])}: target {self.target}")
        self.model.grid.move_agent(self, nextPos)
        self.getCurrentDirection()
        
    def step(self):
        self.checkStoplight()
        print("Move")