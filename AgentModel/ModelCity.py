import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

from AgentBuilding import Building
from AgentParking import Parking
from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentCar import Car

class CityModel(mesa.Model):
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
            "BuildingEleven": ((21,17), (22,22))
        }
        
        self.parkings = {
            "1": (3,10),
            "2": (4,3),
            "3": (4,18),
            "4": (5,12),
            "5": (5,21),
            "6": (6,7),
            "7": (9,9),
            "8": (10,22),
            "9": (11,5),
            "10": (11,12),
            "11": (11,17),
            "12": (18,3),
            "13": (18,18),
            "14": (18,20),
            "15": (21,6),
            "16": (21,9),
            "17": (21,20)
        }
        
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
        
        self.stoplightState = {
            1: "Green",
            2: "Red",
            3: "Red",
            4: "Green",
            5: "Green",
            6: "Green",
            7: "Red",
            8: "Red",
            9: "Red",
            10: "Green"
        }
        
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
            19: ((9,6), (12,7))
        }
        
        self.streetDirections = {
            1: {"N": False, "S": True, "E": False, "W": False},
            2: {"N": False, "S": False, "E": True, "W": False},
            3: {"N": True, "S": False, "E": True, "W": False},
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
            19: {"N": False, "S": False, "E": False, "W": True}
        }
        
        self.addBuilding()
        self.addStreet()
        self.addParking()
        self.addStoplights()
        self.addCar()
        
    def addBuilding(self):
        for building, coords in self.buildingRanges.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Building(self.next_id(), self, building)
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y)) 

    def addParking(self):
        for parking, (x,y) in self.parkings.items():
            agent = Parking(self.next_id(), self, parking)
            self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
            
    def addStoplights(self):
        for stoplight, coords in self.stoplights.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Stoplight(self.next_id(), self, stoplight, self.stoplightState[stoplight])
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
            
    def addStreet(self):
        for street, coords in self.streets.items():
            (xmin, ymin), (xmax, ymax) = coords
            for x in range(xmin, xmax+1):
                for y in range(ymin, ymax+1):
                    agent = Street(self.next_id(), self, street, self.streetDirections[street])
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
    
    def addCar(self):
        car = Car(self.next_id(), self, 1)
        self.grid.place_agent(car, (1, 23))
        self.schedule.add(car)  # Add the car to the scheduler
    
    def step(self):
        self.schedule.step()