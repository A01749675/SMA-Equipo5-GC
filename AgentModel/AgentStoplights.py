import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

class Stoplight(mesa.Agent):

    def __init__(self,uniqueId,model, stoplight, neighbors):
        super().__init__(uniqueId,model)
        self.stoplightId = stoplight
        self.countSteps = 0
        self.TIME = 10
        self.noCars = 0
        self.state = "Yellow"
        self.on = False
        self.neighbors = neighbors
        self.neighborETA = 1000
        self.active = False
        self.stopLights = []
        self.sync = False
        self.partner = None

    def setPartner(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        for neighbor in neighborhood:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Stoplight):
                    self.partner = c
                    c.partner = self

    def carMessage(self, eta):
        if self.partner is None:
            self.setPartner()

        if not self.active:
            neighbors = []
            for neighbor in self.neighbors:
                cell = self.model.grid.get_cell_list_contents([neighbor[0], neighbor[1]])
                for c in cell:
                    if isinstance(c, Stoplight):
                        c.neighborETA = eta
                        neighbors.append(c)
            self.stopLights = neighbors
            self.stopLights.append(self.partner)
            print("Stoplights: ", self.stopLights, self.pos)

            if eta < self.neighborETA:
                self.state = "Green"
                self.on = True
                for neighbor in neighbors:
                    neighbor.state = "Red"
                    neighbor.on = False
                    neighbor.active = True
            else:
                self.state = "Red"
                self.on = False
            for light in self.model.stoplights[self.stoplightId]:
                cell = self.model.grid.get_cell_list_contents([light[0]-1, self.model.HEIGHT-light[1]])
                for c in cell:
                    if isinstance(c, Stoplight):
                        if c.state != self.state:
                            c.carMessage(eta)

        self.active = True
        self.noCars = 0
        print("Stoplights2: ", self.stopLights, self.pos)


    def step(self):
        print("lights", self.stopLights, self.pos)
        if self.sync:
            print("lightsSync", self.stopLights)
            for light in self.stopLights:
                light.noCars = self.noCars
                light.countSteps = self.countSteps
                light.active = self.active
        #print("Stoplight: ", self.pos, " State: ", self.state, "noCars: ", self.noCars, "countSteps: ", self.countSteps)
        if self.active:
            self.noCars += 1
            if self.noCars%20==0:
                self.active = False
                self.state = "Yellow"
            self.countSteps += 1
            if self.countSteps%self.TIME==0:
                self.on = not self.on
                self.state = "Red" if self.on else "Green"

        else:
            self.noCars = 0
            self.countSteps = 0
            self.state = "Yellow"
            #for light in self.stopLights:
            #    print("Light: ", light.pos)
            #    light.state = "Yellow"
            #    light.noCars = self.noCars
            #    light.countSteps = self.countSteps
            #    light.active = self.active

