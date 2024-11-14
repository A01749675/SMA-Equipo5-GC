# Description: Clase que define a los agentes de tipo StreetDir, que son calles con múltiples direcciones.

#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 10/11/2024



import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors


class AgentStreetDir(mesa.Agent):
    """Clase que define calles especiales en las que un agente puede moverse en dos direcciones.

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
        street (int): id de la calle en la que se encuentra el agente
        directions (dict): diccionario con las direcciones en las que se puede mover el agente
    """
    def __init__(self,uniqueId,model, street, directions):
        super().__init__(uniqueId,model)
        self.street = street
        self.availableDirections = {
            "N":directions["N"],
            "S":directions["S"],
            "E":directions["E"],
            "W":directions["W"]
            }
        
        self.direction = []
        self.currentDirection()
        self.movementEquivalence = {
                "N":(0,1),
                "S":(0,-1),
                "E":(1,0),
                "W":(-1,0)
            }
    def currentDirection(self):
        """
        Método que guarda las direcciones en las que se puede mover el agente de tipo Car/SmartCar que se encuentre en la misma casilla
        que el agente actual 
        """
        for dir, value in self.availableDirections.items():
            if value:
                self.direction.append(dir)
                
    def step(self):
        """
        Método que ejecuta las acciones de un agente Street.
        """
        pass