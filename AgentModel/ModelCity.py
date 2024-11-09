
import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors


from AgentBuilding import Building
from AgentParking import Parking
from AgentStoplights import Stoplight

class CityModel(mesa.Model):
    
    def __init__(self,numAgents):
        
        super().__init__()
        self.numAgents = numAgents
        
        self.WIDTH = 24
        self.HEIGHT = 24
        
        self.grid = mesa.space.MultiGrid(self.WIDTH, self.HEIGHT, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        self.buildingRanges = {
            
            "BuildingOne":((3,3),(6,12)),
            "BuildingTwo":((9,3),(12,5)),
            "BuildingThree2":((9,8),(12,12)),
            "BuildingThree":((3,17),(6,18)),
            "BuildingFour":((9,17),(12,18)),
            "BuildingFive":((3,21),(6,22)),
            "BuildingSix":((9,21),(12,22)),
            "BuildingSeven":((17,3),(22,6)),
            "BuildingEight":((17,9),(22,12)),
            "BuildingNine":((17,17),(18,22)),
            "BuildingTen":((21,17),(22,22))
            }
        
        self.parkings = {
            "1":(3,10),
            "2":(4,3),
            "3":(4,18),
            "4":(5,12),
            "5":(5,21),
            "6":(6,7),
            "7":(9,9),
            "8":(10,22),
            "9":(11,5),
            "10":(11,12),
            "11":(11,17),
            "12":(18,3),
            "13":(18,18),
            "14":(18,20),
            "15":(21,6),
            "16":(21,9),
            "17":(21,20)
                
        }
        self.stoplights = {
            "1":((1,18),(2,18)),
            "2":((3,19),(3,20)),
            "3":((6,23),(6,24)),
            "4":((7,22),(8,22)),
            "5":((7,8),(8,8)),
            "6":((7,3),(8,3)),
            "7":((9,1),(9,2)),
            "8":((9,6),(9,7)),
            "9":((18,15),(18,16)),
            "10":((19,17),(20,17)),
            
        }
        self.addBuilding()
        self.addParking()
        self.addStoplights()
        
        
    def addBuilding(self):
        for building, coords in self.buildingRanges.items():
            (xmin, ymin), (xmax, ymax) = coords
            print(xmin, xmax, ymin, ymax)
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
                    agent = Stoplight(self.next_id(), self, stoplight)
                    self.grid.place_agent(agent, (x-1, (self.HEIGHT)-y))
            
    def step(self):
        self.schedule.step()