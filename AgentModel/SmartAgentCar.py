
#CLase que declara los agentes de tipo carro Inteligentes, que tienen acceso a un manejador de rutas que les permite revisar si ya existe una ruta de 
#un estacionamiento a otro y si no, generar una nueva ruta.

#Esta clase combina el comportamiento de movimiento aleatorio con una heurística simple (reducir distancia) junto con la construcción de rutas directas entre 
#estacionamientos.

#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 13/11/2024

import math
from collections import deque

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
from AgentPerson import Persona
from AgentBusStop import BusStop

import random
from pprint import pprint

class SmartCar(mesa.Agent):
    """Clase de tipo carro inteligente que tiene acceso a un manejador de rutas que le permite revisar si ya existe una ruta de un estacionamiento a otro y si no, generar una nueva ruta.
    Declara agentes de tipo carro inteligente, que puede interactuar con su entorno y moverse de un lugar a otro en el modelo de agentes.
    Declara los comportamientos esperados a la hora de ir de punto a punto, evitando obstáculos y siguiendo las reglas de tránsito. (No subir a la banqueta, no chocar con otros autos, respetar los semáforos, etc.)
    Declara los métodos necesarios para que el carro pueda moverse de un punto a otro en el modelo de agentes.

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
        car (int): id del carro en el que se encuentra el agente
        targetDestination (tuple): coordenadas del destino al que se dirige el agente
        targetParking (int): id del estacionamiento al que se dirige el agente
        startParking (int): id del estacionamiento en el que se encuentra el agente
        Waze (Waze): manejador de rutas que tiene acceso el agente
    """
    
    def __init__(self, uniqueId, model, car, targetDestination, targetParking, startParking, Waze):
        super().__init__(uniqueId, model)
        
        self.carId = car
        self.target = targetDestination
        self.targetParking = targetParking
        
        self.currentDir = ""
        self.busInFront = False
        
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
        self.bestPath: deque = deque()

    def getCurrentDirection(self):
        """
        Método que obtiene la dirección en la que se puede mover el agente de tipo Car

        Returns:
            str : dirección en la que se puede mover el agente
        """
        cell = self.model.grid.get_cell_list_contents([self.pos])
        for c in cell:
            if isinstance(c, Street):
                for dir, value in c.availableDirections.items():
                    if value:
                        self.currentDir = dir
        return ""  # Default to no movement if no direction is found

    def exitParkingLot(self):
        """
        Método que saca al agente de un estacionamiento.
        """
        neighbors = [(self.pos[0] + 1, self.pos[1]),  # Right
                         (self.pos[0] - 1, self.pos[1]),  # Left
                         (self.pos[0], self.pos[1] + 1),  # Up
                         (self.pos[0], self.pos[1] - 1)]
        
        for neighbor in neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, SmartCar):
                    break
                if isinstance(c, Street):
                    self.model.grid.move_agent(self, neighbor)
                    self.justStarted = False
                    #print("Entering streer from parking lot")
                    #print("The dir is: "+c.currentDirection())
                    return

    def checkStoplight(self):
        """
        Método que verifica si hay un semáforo en la dirección en la que se dirige el agente y determina si puede avanzar o no.
        Esta función a su vez llama a los métodos basicMovementChecker y followBestPath para que el agente pueda moverse de un punto a otro.
        """
        if self.justStarted:
            self.exitParkingLot()
            
        if self.pos == self.target:
            self.inDestination = True
            return
            
        # Range of positions where there could be a stoplight
        cellsAhead = 3
        if self.currentDir == "N":
            positions = [(self.pos[0], self.pos[1] + i) for i in range(cellsAhead) if self.pos[1] + i < self.model.grid.height - 1]
        elif self.currentDir == "S":
            positions = [(self.pos[0], self.pos[1] - i) for i in range(cellsAhead) if self.pos[1] - i > 0]
        elif self.currentDir == "E":
            positions = [(self.pos[0] + i, self.pos[1]) for i in range(cellsAhead) if self.pos[0] + i < self.model.grid.width - 1]
        elif self.currentDir == "W":
            positions = [(self.pos[0] - i, self.pos[1]) for i in range(cellsAhead) if self.pos[0] - i > 0]
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
                    if agent.state == "Green" or agent.state == "Yellow":
                        spotlightFound = True
                    else:
                        spotlightFound = False
                    break
                else:
                    spotlightFound = True
                    
        if spotlightFound:
            if not self.foundRoute:
                self.basicMovementChecker()
            else:
                self.followBestPath()
            if spotLightPos is not None:
                stopCell = self.model.grid.get_cell_list_contents([spotLightPos])
                for agent in stopCell:
                    if isinstance(agent, Stoplight):
                        agent.carMessage(math.dist(self.pos, spotLightPos))

    def bestPosition(self, positions):
        """Método de heurística simple que regresa la mejor posición a la que se puede mover el agente tomando en cuenta su distancia manhattan al destino 
        y el número de veces que ha visitado la posición.
        
        Esto último se hace para evitar ciclos. 

        Args:
            positions (list[tuple[int,int]]): lista de posiciones a las que se puede mover el agente

        Returns:
            tuple[int,int]: mejor posición a la que se puede mover el agente
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
            Método que verifica si el agente puede moverse a una posición. 
            Este método filtra los posibles movimientos siguiendo los criterios: 
                1. No moverse a la posición anterior
                2. No moverse a una posición fuera de los límites del grid
                3. No moverse a una posición que ya ha visitado [depende de los ciclos, si puede visitarla, pero verifica si no la ha vistidado numerosas veces ya]
                4. No moverse a una posición que contenga un semáforo en rojo
                5. No moverse a una posición que contenga un edificio
                6. No moverse a una posición que contenga otro carro
                7. Si se tiene una calle con múltiples direcciones, añade ambas direcciones a su lista de posibles movimientos
            Asimismo plantea las siguientes alternativas:
                1. Pregunta si existe una ruta de un estacionamiento a otro
                2. Si no existe una ruta, genera una nueva ruta
                3. Si existe una ruta, sigue la mejor ruta
               
        """
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
            
            neighbors = [(self.pos[0] + 1, self.pos[1]),  # East
                         (self.pos[0] - 1, self.pos[1]),  # West
                         (self.pos[0], self.pos[1] + 1),  # North
                         (self.pos[0], self.pos[1] - 1)] # South
            equivalence = ["E", "W", "N", "S"]
            count = 0
            if (predefinedMovement[0] >= 0 or predefinedMovement[0] <= self.model.grid.width - 1 and predefinedMovement[1] >= 0 or predefinedMovement[1] <= self.model.grid.height - 1):
                possibleSteps.append(predefinedMovement)
 
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                    continue
                
                cell = self.model.grid.get_cell_list_contents([neighbor])
                
                for c in cell:
                    if c is self:
                        return
                    if isinstance(c, Parking):
                        if c.parkingId == self.targetParking:
                            #self.inDestination = True
                            route = str(self.previousParking) + "-" + str(c.parkingId)
                            self.waze.addDirection(route, [p for p in self.path if p is not None]+[neighbor])
                            self.waze.addParkingNeighbors(self.previousParking, c.parkingId, [p for p in self.path if p is not None] + [neighbor])
                            self.path = []
                            self.previousParking = c.parkingId
                            self.model.grid.move_agent(self, neighbor)
                            return
                        if self.previousParking is None:
                            self.previousParking = c.parkingId
                            continue
 
                        if self.previousParking != c.parkingId:
                            route = str(self.previousParking) + "-" + str(c.parkingId)
                            self.waze.addDirection(route, [p for p in self.path if p is not None]+ [neighbor])
                            self.waze.addParkingNeighbors(self.previousParking, c.parkingId, [p for p in self.path if p is not None]+[neighbor])
                            self.path = []
                            self.previousParking = c.parkingId
                            
                        if self.waze.routeExists(c.parkingId, self.targetParking) and c.parkingId != self.targetParking:
                            #print("There is a route from", c.parkingId, "to", self.targetParking)
                            self.foundRoute = True
                            self.bestPath = self.waze.shortestPath(c.parkingId, self.targetParking)
                            return 

                    if isinstance(c, SmartCar):
                        continue
                    if isinstance(c, Persona):
                        if c.inBus:
                            continue
 
                    if self.is_agent_bus(c):
                        continue
                    
                    
                    if isinstance(c, AgentStreetDir):
                        possibleSteps.append(neighbor)
                        
                    if isinstance(c, Street):
                        cellDirection = c.currentDirection()
                        cellEquivalence = self.movementEquivalence[cellDirection]
                        possibleNextPos = (neighbor[0] + cellEquivalence[0], neighbor[1] + cellEquivalence[1])
                        possibleNextDir = equivalence[count]
                        if cellDirection == self.oppositeDir[self.currentDir]:
                            continue
                        if possibleNextPos == self.pos:
                            continue
                        if possibleNextDir == self.oppositeDir[self.currentDir]:
                            continue
                        possibleSteps.append(neighbor)
                count += 1

        if len(set(self.positionHistory)) < 8:  # Detect a small repeated loop
            if random.random() < 0.5:  # 50% chance to pick a random next step
                nextPos = random.choice(possibleSteps)
            else:
                nextPos = self.bestPosition(possibleSteps)
        else:
            nextPos = self.bestPosition(possibleSteps)
            
        try: 
            nextCell = self.model.grid.get_cell_list_contents([nextPos])
            for c in nextCell:
                if nextCell is self:
                    continue
                if isinstance(c, SmartCar):
                    return
                if isinstance(c,BusStop):
                    return
                if self.is_agent_bus(c):
                    return
                if isinstance(c, Persona):
                    if not c.inBus:
                        return
                if isinstance(c, Stoplight):
                    if c.state == "Red":
                        return
                if isinstance(c, Building):
                    return
                if isinstance(c, AgentStreetDir):
                    self.multipleDir = True
                    self.directions = c.direction
                else:
                    self.multipleDir = False
                    self.directions = []
                    
            if nextPos == self.target:
                #self.inDestination = True
                self.model.grid.move_agent(self, nextPos)
                return
                
            self.prevPos = self.pos        
            self.model.grid.move_agent(self, nextPos)
            self.visits[nextPos] = self.visits.get(nextPos, 0) + 1
            
            self.getCurrentDirection()
            if self.path: 
                if self.path[-1] != self.pos:
                    self.path.append(self.pos)
            else:
                self.path.append(self.pos)
        except:
            print("Error: No path to destination")

    def is_agent_bus(self, obj):
        from AgentBus import AgentBus  # Lazy import here
        return isinstance(obj, AgentBus)
        
    def followBestPath(self):
        """
        Follow the best path to reach the target destination. Handle obstacles dynamically and retry blocked positions.
        """
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        for neighbor in neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Parking) and c.parkingId == self.targetParking:
                    #self.inDestination = True
                    self.model.grid.move_agent(self, neighbor)
                    return  
                
        if not hasattr(self, 'blockedPositions'):
            self.blockedPositions = {}

        if self.bestPath and not self.inDestination:
            print("My position is ", self.pos)
            print("Following best path ", self.bestPath, " to ", self.targetParking)

            nextPos = self.bestPath.popleft()

            # If the target position is reached
            if nextPos == self.target:
                #self.inDestination = True
                self.model.grid.move_agent(self, nextPos)
                return

            # Check the next position for obstacles
            nextCell = self.model.grid.get_cell_list_contents([nextPos])
            blocked = False
            

            for c in nextCell:
                
                if isinstance(c, Parking):
                    if c.parkingId == self.targetParking:
                        #self.inDestination = True
                        self.model.grid.move_agent(self, nextPos)
                        return
                
                if isinstance(c, (SmartCar, Building, Stoplight)) and not (isinstance(c, Stoplight) and c.state == "Green"):
                    blocked = True
                    break

            if blocked:
                # Add position back to the path and track blocked positions with a cooldown
                self.bestPath.appendleft(nextPos)
                self.blockedPositions[nextPos] = self.blockedPositions.get(nextPos, 0) + 1

                # If a position has been retried too many times, consider it permanently blocked
                if self.blockedPositions[nextPos] > 10:
                    print(f"Position {nextPos} is permanently blocked. Recomputing path...")
                    
                    neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                    for neighbor in neighbors:
                        cell = self.model.grid.get_cell_list_contents([neighbor])
                        for c in cell:
                            if isinstance(c, Parking) and c.parkingId == self.targetParking:
                                #self.inDestination = True
                                self.model.grid.move_agent(self, neighbor)
                                return  
                    self.foundRoute = False
                    

                return

            # If the position is clear, move the agent
            if nextPos in self.blockedPositions:
                del self.blockedPositions[nextPos]  # Clear it from blocked positions

            self.model.grid.move_agent(self, nextPos)

        # If no path remains, check neighbors heuristically
        if not self.bestPath and not self.inDestination:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            for neighbor in neighbors:
                cell = self.model.grid.get_cell_list_contents([neighbor])
                for c in cell:
                    if isinstance(c, Parking) and c.parkingId == self.targetParking:
                        #self.inDestination = True
                        self.model.grid.move_agent(self, neighbor)
                        return
            if not self.inDestination:
                print("Error: No path to destination")
                self.foundRoute = False

    def step(self):
        """
        Método que ejecuta las acciones de un agente SmartCar
        
        """
        if not self.inDestination:
            self.positionHistory.append(self.pos)
            if len(self.positionHistory) > 10:  # Keep only recent history
                self.positionHistory.pop(0)
            self.checkStoplight()
            if not self.foundRoute:
                self.bestPath = self.waze.shortestPath(self.start, self.target)
                if self.bestPath:
                    self.foundRoute = True
            # print("----------------")
            # print(self.previousParking)
            # print(self.waze.graphDirections)
            # print(self.waze.parkingGraph)
        else:
            print("Agent has reached destination")
