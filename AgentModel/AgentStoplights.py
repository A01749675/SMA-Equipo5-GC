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
        self.sync = False
        self.partners = []
        self.syncLight = None

    def setPartner(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        for neighbor in neighborhood:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c not in self.partners:
                        self.partners.append(c)
                    if self not in c.partners:
                        c.partners.append(self)

        for neighbor in self.neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor[0], neighbor[1]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c not in self.partners:
                        self.partners.append(c)

    def carMessage(self, eta):

        if not self.active:
            print("neighborsA: ", self.neighbors)
            print("Stoplights: ", (self.partners), self.pos)
            for agent in self.partners:
                print("Agent: ", agent.pos)

            if eta < self.neighborETA:
                self.state = "Green"
                self.on = True
                for partner in self.partners:
                    partner.state = "Red"
                    partner.on = False
                    partner.active = True
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
        print("Stoplights2: ", self.partners, self.pos)

    def turnOff(self):
        self.active = False
        self.state = "Yellow"
        self.noCars = 0
        self.countSteps = 0
        for partner in self.partners:
            partner.active = False
            partner.state = "Yellow"
            partner.noCars = 0
            partner.countSteps = 0


    def step(self):
        if len(self.partners) < 2:
            self.setPartner()

        if self.sync:
            print("neighbors: ", self.neighbors)
            print("lightsSync", self.partners, self.pos)
            for light in self.partners:
                print("LightSync: ", light.pos)
                light.noCars = self.noCars
                print("noCars: ", light.noCars, "self.noCars: ", self.noCars)
                light.countSteps = self.countSteps
                light.active = self.active
                if self.active == False:
                    light.turnOff()
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
            self.turnOff()

            #for light in self.stopLights:
            #    print("Light: ", light.pos)
            #    light.state = "Yellow"
            #    light.noCars = self.noCars
            #    light.countSteps = self.countSteps
            #    light.active = self.active

