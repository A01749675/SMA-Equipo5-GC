#Este código implementa la funcionalidad de los agentes de tipo semáforo en 
# la simulación. Se encargan de regular el tráfico en la intersección de calles.


#Author: César Augusto Flores Reyes A01751101
#Date: 13/11/2024
import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

class Stoplight(mesa.Agent):

    def __init__(self,uniqueId,model, stoplight, neighbors):
        """
        Constructor de la clase Stoplight para la simulación de tráfico.

        Args:
            uniqueId (int): identificador único del agente
            model (mesa.Model): modelo de la simulación
            stoplight (id): identificador del semáforo
            neighbors (semáforos vecinos): semáforos  de la intersección vecina
        """
        super().__init__(uniqueId,model)
        self.stoplightId = stoplight
        self.countSteps = 0
        self.TIME = 10
        self.noCars = 0
        self.state = "Yellow"
        self.on = False
        self.neighbors = neighbors
        self.neighborAgents = []
        self.active = False
        self.sync = False
        self.partners = []
        self.syncLight = None

    def setPartner(self):
        """
        Método que establece listas los semáforos vecinos de un semáforo y de la intersección vecina.
        """
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        for neighbor in neighborhood:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c not in self.partners and c != self:
                        self.partners.append(c)
                    if self not in c.partners:
                        c.partners.append(self)

        for neighbor in self.neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor[0], neighbor[1]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c not in self.partners:
                        self.partners.append(c)

        for neighbor in self.neighbors:
            cell = self.model.grid.get_cell_list_contents([neighbor])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c not in self.neighborAgents:
                        self.neighborAgents.append(c)

    def carMessage(self, eta):
        """
        Método que recibe un mensaje de un carro indicando que el carro etá cerca.

        Args:
            eta (int): Distancia entre el carro y el semáforo
        """
        if not self.active:

            self.state = "Green"
            self.on = True

            for neighbor in self.neighborAgents:
                neighbor.turnOn("Red")

            for partner in self.partners:
                if partner not in self.neighborAgents:
                    partner.turnOn("Green")

        self.active = True
        self.noCars = 0

    def turnOff(self):
        """
        Método que apaga un semáforo, lo vuelve amarillo y detiene las cuentas.
        """
        self.active = False
        self.state = "Yellow"
        self.noCars = 0
        self.countSteps = 0
        for partner in self.partners:
            partner.active = False
            partner.state = "Yellow"
            partner.noCars = 0
            partner.countSteps = 0

    def turnOn(self, state):
        """
        Método que enciende un semáforo y comeinza las cuentas.

        Args:
            state (str): Estado en el que enciende verde o rojo
        """
        self.active = True
        self.state = state
        if state == "Green":
            self.on = True
        else:
            self.on = False

    def flip(self):
        self.on = not self.on
        self.state = "Green" if self.on else "Red"

    def step(self):
        """
        Método que ejecuta un paso de la simulación.
        
        """
        if len(self.partners) < 2:
            self.setPartner()

        if self.sync:
            for light in self.partners:
                light.noCars = self.noCars
                light.countSteps = self.countSteps
                light.active = self.active
                if self.active == False:
                    light.turnOff()

            self.countSteps += 1
            if self.countSteps%self.TIME==0:
                self.flip()
                for light in self.partners:
                    light.flip()

            self.noCars += 1
            if self.noCars%20==0:
                self.turnOff()
