
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
import random
from SmartAgentCar import SmartCar
from pprint import pprint

busRoutes = {
    "1-2": [(8,8),(9,8),(10,8),(11,8),(12,8),(12,7),(12,6),(12,5),(12,4),(12,3),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(22,2),(22,3),(22,3)],
    "2-3": [(22,3),(22,4),(22,5),(22,6),(22,7),(22,8),(22,9),(22,10),(22,11),(22,12),(22,13)],
    "3-4":[(22,13),(22,14),(22,15),(22,16),(22,17),(22,18),(22,19),(22,20),(22,21),(22,22),(21,22),(20,22),(19,22)],
    "4-5":[(19,22),(18,22),(17,22),(16,22),(15,22),(14,22),(13,22),(12,22),(11,22),(10,22),(9,22),(8,22),(7,22),(6,22),(5,22),(4,22),(3,22),(2,22),(1,22),(1,21),(1,20)],
    "5-1":[(1,20),(1,19),(1,18),(1,17),(1,16),(1,15),(1,14),(1,13),(1,12),(1,11),(1,10),(1,9),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)],
    
}


busStops = {
            1: (8,7),
            2: (21,3),
            3: (21,13),
            4: (19,21),
            5: (2,20),
        }

class AgentBus(mesa.Agent):
    
    def __init__(self,unique_id,model,initialBus):
        """Constructor de la clase AgentBus

        Args:
            unique_id (int): Identificador único del agente
            pos (tuple): Posición del agente
            model (ModelCity): Modelo de la ciudad
            stoplight (Stoplight): Semáforo al que pertenece el agente
        """
        super().__init__(unique_id,model)
        self.bus = initialBus
        self.route = []
        self.routeIndex = 0
        self.currentDir = ""
        self.waitTime = 20
        self.waiting = False
        self.people = []
        
        
    def board(self,Persona):
        self.people.append(Persona)
    def exit(self,Persona):
        self.people.remove(Persona)
        
    def travel(self):

        if self.bus!=5:
            target = self.bus+1
        else:
            target = 1
        if self.route == []:
            self.route = busRoutes[f"{self.bus}-{target}"]
            self.routeIndex = 0
        else:

            nextPos = self.route[self.routeIndex]
            cell = self.model.grid.get_cell_list_contents(nextPos)
            for cellContent in cell:

                if isinstance(cellContent,Building):
                    print("Building")
                    return
                if isinstance(cellContent,AgentBus):
                    print("Bus")
                    return
                if isinstance(cellContent,Parking):
                    print("Parking")
                    return
                
                if isinstance(cellContent,SmartCar):
                    return
                if isinstance(cellContent,Persona):
                    print("Person")
                    return

                if isinstance(cellContent,Street):
                    print("Street")
                    self.currentDir = cellContent.direction
                    self.model.grid.move_agent(self,nextPos)
                    self.routeIndex+=1
                    if self.routeIndex == len(self.route):
                        self.routeIndex = 0
                        self.waiting = True
                        self.route = []
                        self.bus+=1
                        if(self.bus>5):
                            self.bus = 1
                    return
                if isinstance(cellContent,AgentStreetDir):
                    self.currentDir = cellContent.direction
                    self.model.grid.move_agent(self,nextPos)
                    self.routeIndex+=1
                    if self.routeIndex == len(self.route):
                        self.routeIndex = 0
                        self.waiting = True
                        self.route = []
                        self.bus+=1
                        if(self.bus>5):
                            self.bus = 1
                        return
                    
    def checkStoplight(self):
        """
        Método que verifica si hay un semáforo en la dirección en la que se dirige el agente y determina si puede avanzar o no.
        Esta función a su vez llama a los métodos basicMovementChecker y followBestPath para que el agente pueda moverse de un punto a otro.
        """
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
            self.travel()
            if spotLightPos is not None:
                stopCell = self.model.grid.get_cell_list_contents([spotLightPos])
                for agent in stopCell:
                    if isinstance(agent, Stoplight):
                        agent.carMessage(math.dist(self.pos, spotLightPos))

    def step(self):
        if self.waiting:
            self.route=[]
            self.waitTime -= 1
            if self.waitTime == 0:
                self.waiting = False
                self.waitTime = 20
        else:
            print("Bus",self.bus)
            print("-------------------------------")
            self.checkStoplight()
        # for person in self.people:
        #     person.step()
                
                
        
