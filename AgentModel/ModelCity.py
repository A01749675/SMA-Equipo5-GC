#Simulación de la ciudad del reto
# Este código instancia el modelo de la ciudad, generando una matriz de 24x24 celdas en la que se colocan los diferentes agentes y elementos de la ciudad.
# Se crean edificios, estacionamientos, semáforos, calles y carros. Colocandolos según la imagen de referencia del reto.


#Author Carlos Iker Fuentes Reyes A01749675, Cesár Augusto Flores Reyes A01751101
#Fecha de creación: 10/11/2024

import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

from AgentBuilding import Building
from AgentPerson import Persona
from AgentParking import Parking
from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentCar import Car
from SmartAgentCar import SmartCar
from AgentStreetDir import AgentStreetDir

from Waze import Waze

class CityModel(mesa.Model):
    """Clase principal del modelo CityModel en el que se construye la distribución de la ciudad, se colocan los elementos, instancian los agentes y
            se ejecuta la simulación.
            

    Args:
        numAgents (int): número de agentes que se instanciarán en la simulación. De momento los únicos agentes instanciados son los carros.
                        Los demás elementos, de momento están manejados como parte del ambiente (edificios, estacionamientos, semáforos y calles).
    """
    def __init__(self, numAgents):
        super().__init__()
        self.numAgents = numAgents
        
        self.WIDTH = 24
        self.HEIGHT = 24
        
        self.grid = mesa.space.MultiGrid(self.WIDTH, self.HEIGHT, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        
        self.buildingRanges = {
            "BuildingOne": ((3,3), (6,12)),
            "BuildingTwo": ((9,3), (12,5)),
            "BuildingThree": ((9,8), (12,12)),
            "BuildingFour": ((3,17), (6,18)),
            "BuildingFive": ((9,17), (12,18)),
            "BuildingSix": ((3,21), (6,22)),
            "BuildingSeven": ((9,21), (12,22)),
            "BuildingEight": ((17,3), (22,6)),
            "BuildingNine": ((17,9), (22,12)),
            "BuildingTen": ((17,17), (18,22)),
            "BuildingEleven": ((21,17), (22,22)),
            "Glorieta": ((14,14), (15,15))
        }
        
        self.parkings = {
            1: (3,10),
            2: (4,3),
            3: (4,18),
            4: (5,12),
            5: (5,21),
            6: (6,7),
            7: (9,9),
            8: (10,22),
            9: (11,5),
            10: (11,12),
            11: (11,17),
            12: (18,3),
            13: (18,18),
            14: (18,20),
            15: (21,6),
            16: (21,9),
            17: (21,20)
        }
        self.walkableBuildings = [
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3),

            (2, 6),
            (3, 6),
            (4, 6),
            (5, 6),
            (2, 7),
            (3, 7),
            (4, 7),
            (5, 7),

            (8, 2),
            (9, 2),
            (10, 2),
            (11, 2),
            (8, 3),
            (9, 3),
            (10, 3),
            (11, 3),

            (8, 6),
            (9, 6),
            (10, 6),
            (11, 6),
            (8, 7),
            (9, 7),
            (10, 7),
            (11, 7),

            (16, 2),
            (16, 3),
            (16, 4),
            (16, 5),
            (16, 6),
            (16, 7),
            (17, 2),
            (17, 3),
            (17, 4),
            (17, 5),
            (17, 6),
            (17, 7),

            (20, 2),
            (20, 3),
            (20, 4),
            (20, 5),
            (20, 6),
            (20, 7),
            (21, 2),
            (21, 3),
            (21, 4),
            (21, 5),
            (21, 6),
            (21, 7),

            (2, 12),
            (3, 12),
            (4, 12),
            (5, 12),
            (2, 21),
            (3, 21),
            (4, 21),
            (5, 21),
            (2, 13),
            (2, 14),
            (2, 15),
            (2, 16),
            (2, 17),
            (2, 18),
            (2, 19),
            (2, 20),
            (5, 13),
            (5, 14),
            (5, 15),
            (5, 16),
            (5, 17),
            (5, 18),
            (5, 19),
            (5, 20),

            (8, 19),
            (9, 19),
            (10, 19),
            (11, 19),
            (8, 21),
            (9, 21),
            (10, 21),
            (11, 21),
            (8, 20),
            (11, 20),

            (8, 16),
            (9, 16),
            (10, 16),
            (11, 16),
            (8, 12),
            (9, 12),
            (10, 12),
            (11, 12),
            (8, 13),
            (8, 14),
            (8, 15),
            (11, 13),
            (11, 14),
            (11, 15),

            (16, 15),
            (17, 15),
            (18, 15),
            (19, 15),
            (20, 15),
            (21, 15),
            (16, 12),
            (17, 12),
            (18, 12),
            (19, 12),
            (20, 12),
            (21, 12),
            (16, 14),
            (16, 13),
            (21, 14),
            (21, 13),

            (16, 18),
            (17, 18),
            (18, 18),
            (19, 18),
            (20, 18),
            (21, 18),
            (16, 21),
            (17, 21),
            (18, 21),
            (19, 21),
            (20, 21),
            (21, 21),
            (16, 19),
            (16, 20),
            (21, 19),
            (21, 20)
        ]

        self.stoplights = {
            1: ((1,18), (2,18)),
            2: ((3,19), (3,20)),
            3: ((6,23), (6,24)),
            4: ((7,22), (8,22)),
            5: ((7,8), (8,8)),
            6: ((7,3), (8,3)),
            7: ((9,1), (9,2)),
            8: ((9,6), (9,7)),
            9: ((18,15), (18,16)),
            10: ((19,17), (20,17))
        }
        
        self.stoplightNeighbors = {
            1: ((2, 4), (2, 5)),
            2: ((0, 6), (1, 6)),
            3: ((6, 2), (7, 2)),
            4: ((5, 0), (5, 1)),
            5: ((8, 17), (8, 18)),
            6: ((8, 22), (8, 23)),
            7: ((6, 21), (7, 21)),
            8: ((6, 16), (7, 16)),
            9: ((19, 7), (18, 7)),
            10: ((17, 8), (17, 9))
        }

        self.stoplightScync = [
            (2, 4),
            #(0, 6),
            (6, 2),
            #(5, 0),
            (8, 17),
            #(8, 22),
            (6, 21),
            #(6, 16),
            (19, 7),
            #(17, 8)
        ]
        
        self.streets = {
            1: ((1,1), (2,22)),
            2: ((1,23), (22,24)),
            3: ((23,1), (24,24)),
            4: ((3,1), (22,2)),
            5: ((15,17), (16,22)),
            6: ((13,17), (14,22)),
            7: ((7,3), (8,12)),
            8: ((7,17), (8,22)),
            9: ((4,19), (6,20)),
            10: ((9,19), (12,20)),
            11: ((19,17), (20,22)),
            12: ((13,3), (14,12)),
            13: ((15,3), (16,12)),
            14: ((3,13), (12,14)),
            15: ((3,15), (12,16)),
            16: ((17,15), (22,16)),
            17: ((17,13), (22,14)),
            18: ((17,7), (22,8)),
            19: ((9,6), (12,7)),
            20: ((14,13), (15,13)),
            21 : ((13,14), (13,15)),
            22: ((14,16), (15,16)),
            23: ((16,14), (16,15)),
        }
        
        self.streetDirections = {
            1: {"N": False, "S": True, "E": False, "W": False},
            2: {"N": False, "S": False, "E": True, "W": False},
            3: {"N": True, "S": False, "E": False, "W": False},
            4: {"N": False, "S": False, "E": False, "W": True},
            5: {"N": True, "S": False, "E": False, "W": False},
            6: {"N": False, "S": True, "E": False, "W": False},
            7: {"N": True, "S": False, "E": False, "W": False},
            8: {"N": False, "S": True, "E": False, "W": False},
            9: {"N": False, "S": False, "E": False, "W": True},
            10: {"N": False, "S": False, "E": True, "W": False},
            11: {"N": True, "S": False, "E": False, "W": False},
            12: {"N": False, "S": True, "E": False, "W": False},
            13: {"N": True, "S": False, "E": False, "W": False},
            14: {"N": False, "S": False, "E": False, "W": True},
            15: {"N": False, "S": False, "E": True, "W": False},
            16: {"N": False, "S": False, "E": True, "W": False},
            17: {"N": False, "S": False, "E": False, "W": True},
            18: {"N": False, "S": False, "E": False, "W": True},
            19: {"N": False, "S": False, "E": False, "W": True},
            20: {"N": False, "S": False, "E": False, "W": True},
            21: {"N": False, "S": True, "E": False, "W": False},
            22: {"N": False, "S": False, "E": True, "W": False},
            23: {"N": True, "S": False, "E": False, "W": False},
        }
        self.twoDirSteets = {
            1 : (13,13),
            2: (13,16),
            3: (16,16),
            4:(16,13)
        }
        
        self.twoDirSteetsDirections = {
            1 : {"N":False, "S":True,"E":False,"W":True},
            2: {"N":False, "S":True,"E":True,"W":False},
            3: {"N":True, "S":False,"E":True,"W":False},
            4: {"N":True, "S":False,"E":False,"W":True}
        }
        self.waze = Waze()
        
        self.cars = []
        self.stoplightsData = []
        self.addBuilding()
        self.addStreet()
        self.addParking()
        self.addStoplights()
        self.addCar()
        self.addTwoDirStreet()
        self.addPedestrians(10)
        
    def addBuilding(self):
        """Añadir edificios a la cuadrícula."""
        for building, coords in self.buildingRanges.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Building(self.next_id(), self, building)
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))

        for buildingPos in self.walkableBuildings:
            cell = self.grid.get_cell_list_contents([buildingPos])
            for c in cell:
                if isinstance(c, Building):
                    c.walkable = True

    def addParking(self):
        """Añadir estacionamientos a la cuadrícula."""
        for parking, (x,y) in self.parkings.items():
            agent = Parking(self.next_id(), self, parking)
            self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
            
    def addStoplights(self):
        """Añadir semáforos a la cuadrícula."""
        for stoplight, coords in self.stoplights.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Stoplight(self.next_id(), self, stoplight, self.stoplightNeighbors[stoplight])
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
                    self.schedule.add(agent)  # Add the stoplight to the scheduler
                    self.stoplightsData.append(agent)

        for stoplight in self.stoplightScync:
            cell = self.grid.get_cell_list_contents([stoplight])
            for c in cell:
                if isinstance(c, Stoplight):
                    c.sync = True
            
    def addStreet(self):
        """Añadir calles a la cuadrícula."""
        for street, coords in self.streets.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Street(self.next_id(), self, street, self.streetDirections[street])
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
    
    def addCar(self):
        """Añadir carros a la cuadrícula."""
        for i in range(self.numAgents):
            startingParking = self.random.choice(list(self.parkings.keys()))
            targetParking = self.random.choice(list(self.parkings.keys()))
            
            parkingLot = self.parkings[startingParking]
            destination = (self.parkings[targetParking][0]-1,(self.HEIGHT)- self.parkings[targetParking][1])
            
            car = SmartCar(self.next_id(), self, i+1,destination,targetParking,startingParking,self.waze)
            self.grid.place_agent(car, (parkingLot[0]-1, (self.HEIGHT)-parkingLot[1]))
            self.schedule.add(car)
            self.cars.append(car)

        #car = Car(self.next_id(), self, 0, (1,1),1)
        #self.grid.place_agent(car, (1,10))
        #self.schedule.add(car)

        #car = Car(self.next_id(), self, 1, (1, 1), 1)
        #self.grid.place_agent(car, (5, 5))
        #self.schedule.add(car)

    def addTwoDirStreet(self):
        """Añadir calles de doble dirección a la cuadrícula."""
        for street, coords in self.twoDirSteets.items():
            (x,y) = coords
            agent = AgentStreetDir(self.next_id(),self,street,self.twoDirSteetsDirections[street])
            self.grid.place_agent(agent,(x-1,self.HEIGHT-y))

    def addPedestrians(self, numPedestrians):
        for i in range (numPedestrians):
            agent = Persona(self.next_id(), self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, self.random.choice(self.walkableBuildings))
    
    def step(self):
        """Avanzar un paso en la simulación."""
        self.schedule.step()
        
    def getCarData(self):
        result = {"cars":[]}
        for car in self.cars:
            result["cars"].append({"id":car.unique_id,"x":car.pos[0],"z":car.pos[1],"direction":car.currentDir})
        return result
    def getStopLight(self):
        result = {"stoplights":[]}
        for stop in self.stoplightsData:
            result["stoplights"].append({"id":stop.stoplightId,"state":stop.state})
        return result
    
    def getAllData(self):
        result = {"cars":[],"stoplights":[]}
        for car in self.cars:
            result["cars"].append({"id":car.unique_id,"x":car.pos[0],"z":car.pos[1],"direction":car.currentDir})
        for stop in self.stoplightsData:
            result["stoplights"].append({"id":stop.stoplightId,"state":stop.state})
        
        return result