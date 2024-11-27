# Description: Clase que define a los agentes de tipo Street.
#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 10/11/2024

import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors


class Street(mesa.Agent):
    """
    Clase que define a los agentes de tipo Street. Representan las calles y almacenan valores de las direcciones en las que puede moverse un agente 
    de tipo Car o SmartCar.

    Args:
       uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
        street (int): id de la calle en la que se encuentra el agente
        directions (dict): diccionario con las direcciones en las que se puede mover el agente
        
    """
    def __init__(self,uniqueId,model, street, directions, walkable = False):
        super().__init__(uniqueId,model)
        self.street = street
        self.availableDirections = {
            "N":directions["N"],
            "S":directions["S"],
            "E":directions["E"],
            "W":directions["W"]
            }
        self.direction = self.currentDirection()
        self.movementEquivalence = {
                "N":(0,1),
                "S":(0,-1),
                "E":(1,0),
                "W":(-1,0)
            }
        self.walkable = walkable
    def currentDirection(self):
        """Método que regresa la dirección del agente.

        Returns:
            dir (str): dirección del agente
        """
        for dir, value in self.availableDirections.items():
            if value:
                return dir
    def step(self):
        """
        Método que ejecuta las acciones de un agente Street.
        """
        pass