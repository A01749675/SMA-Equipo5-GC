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
    def __init__(self, uniqueId, model, car):
        super().__init__(uniqueId, model)
        self.carId = car
        self.currentDir = ""
        self.movementEquivalence = {
                "N":(0,1),
                "S":(0,-1),
                "E":(1,0),
                "W":(-1,0)
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
            if step[0] < 0 or step[0] >= self.model.grid.width or step[1] < 0 or step[1] >= self.model.grid.height:
                continue
            if self.pos == self.movementEquivalence[forbiddenDirection]:
                continue
            cell = self.model.grid.get_cell_list_contents([step])
            for c in cell: 
                if isinstance(c, Street):
                    possibleSteps.append(step)
            

        self.model.grid.move_agent(self, self.random.choice(possibleSteps))
        
        
    def basicMovementChecker(self):
        self.getCurrentDirection()
        currentDir = self.movementEquivalence[self.currentDir]
        predefinedMovement = (self.pos[0] + currentDir[0], self.pos[1] + currentDir[1])
        neighbors = [(self.pos[0] + 1, self.pos[1]),  # Right
                     (self.pos[0] - 1, self.pos[1]),  # Left
                     (self.pos[0], self.pos[1] + 1),  # Up
                     (self.pos[0], self.pos[1] - 1)]
        
        possibleSteps = [predefinedMovement]
        for neighbor in neighbors:
            if neighbor[0] < 0 or neighbor[0] >= self.model.grid.width or neighbor[1] < 0 or neighbor[1] >= self.model.grid.height:
                continue
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Street):
                    cellDirection = c.currentDirection()
                    if cellDirection == self.currentDir:
                        continue
                    else:
                        possibleSteps.append(neighbor)
        self.model.grid.move_agent(self, self.random.choice(possibleSteps))
        
    def step(self):
        self.basicMovementChecker()
        print("Move")