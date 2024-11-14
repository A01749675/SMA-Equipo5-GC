

#Clase carro de tipo agente reactivo que va de un estacionamiento a otro, siguiendo una heurisitca simple


#DE MOMENTO NO SE ESTÁ UTILZIANDO

#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 10/11/2024
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


class Car(mesa.Agent):
    """
    Clase que define a los agentes de tipo Car. Representan los autos que se mueven en el modelo de agentes.
    Esta implementación es de agentes reactivos con memoria que evitan ciclarse, al llevar registro de sus últimas posiciones. 

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
        car (int): id del auto
        targetDestination (tuple): coordenadas del destino del auto
        targetParking (int): id del estacionamiento al que se dirige el auto
        
    """
    def __init__(self, uniqueId, model, car, targetDestination, targetParking):
        super().__init__(uniqueId, model)
        
        self.carId = car
        self.currentDir = ""
        self.movementEquivalence = {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "W": (-1, 0)
        }
        
        self.target = targetDestination
        self.inDestination = False
        self.justStarted = True
        self.targetParking = targetParking
        self.prevPos = None
        
        self.oppositeDir = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }
        self.multipleDir = False
        self.directions = []
        self.positionHistory = []
        self.visits = {}


    def getCurrentDirection(self):
        """ Método que obtiene la dirección actual del agente.

        Returns:
            str: dirección actual del agente
        """
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for c in cell:
            if isinstance(c, Street):
                for dir, value in c.availableDirections.items():
                    if value:
                        self.currentDir = dir
        return (0, 0)  # Default to no movement if no direction is found

    def exitParkingLot(self):
        """
            Método que permite a un agente salir de un estacionamiento.
        """
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        for neighbor in neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Street):
                    self.model.grid.move_agent(self, neighbor)
                    self.justStarted = False
                    return

    def checkStoplight(self):
        """
            Método que verifica si hay un semáforo en la dirección del agente.
        """
        if self.justStarted:
            print("Exiting")
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
                        print("Green or Yellow at", position)
                    else:
                        print("Red at", position)
                        spotlightFound = False
                    break
                else:
                    spotlightFound = True
        if spotlightFound:
            self.basicMovementChecker()
            print("Spotlight found at", spotLightPos)
            if spotLightPos is not None:
                stopCell = self.model.grid.get_cell_list_contents([spotLightPos])
                for agent in stopCell:
                    if isinstance(agent, Stoplight):
                        agent.carMessage(math.dist(self.pos, spotLightPos))

    def bestPosition(self, positions):
        """
        Método que regresa la mejor posición a la que puede moverse el agente, usando una heurística simple que considera la distancia al destino y el número de visitas a la posición.

        Args:
            positions (list[tuple[int,int]]): lista de posiciones a las que puede moverse el agente

        Returns:
            tuple[int,int]: mejor posición a la que puede moverse el agente
        """
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
        """
        Método que declara el movimiento básico del agente, considerando las direcciones en las que puede moverse.
        
        """
        
        possibleSteps = []
        if self.multipleDir:
            tempPossibleSteps = []
            print("I can go to multiple directions")
            print(self.directions)

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
            
            print(f"I am {self.carId} and I am at {self.pos} and I am going {self.currentDir}")
            print(f"My target parking is {self.targetParking}")
            currentDir = self.movementEquivalence[self.currentDir]
            predefinedMovement = (self.pos[0] + currentDir[0], self.pos[1] + currentDir[1])
            neighbors = [(self.pos[0] + 1, self.pos[1]),  # Right
                         (self.pos[0] - 1, self.pos[1]),  # Left
                         (self.pos[0], self.pos[1] + 1),  # Up
                         (self.pos[0], self.pos[1] - 1)]
            
            if (predefinedMovement[0] >= 0 or predefinedMovement[0] <= self.model.grid.width - 1
                    and predefinedMovement[1] >= 0 or predefinedMovement[1] <= self.model.grid.height - 1):
                possibleSteps.append(predefinedMovement)
 
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                    continue
                cell = self.model.grid.get_cell_list_contents([neighbor])
                for c in cell:
                    if isinstance(c, Parking):
                        if c.parkingId == self.targetParking:
                            self.inDestination = True
                            self.model.grid.move_agent(self, neighbor)
                            return
                    
                    if isinstance(c, Car):
                        continue
                    
                    if isinstance(c, AgentStreetDir):
                        possibleSteps.append(neighbor)
                    
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
        print("AAAAAAAAAAAAAAAa")
        print(self.positionHistory)
        for c in nextCell:
            if isinstance(c, Car):
                print(f"Car {c.carId} is at {nextPos}")
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

    def step(self):
        """
        Método que ejecuta las acciones de un agente Car.
        """
        if not self.inDestination:
            self.positionHistory.append(self.pos)
            if len(self.positionHistory) > 10:  # Keep only recent history
                self.positionHistory.pop(0)
            self.checkStoplight()
        else:
            print("I am in destination")