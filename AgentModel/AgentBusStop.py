
#Clase que define los edificios en el modelo de agentes


#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 10/11/2024


import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors



class BusStop(mesa.Agent):
    """Clase que define los elementos del ambiente de la simulación. Son los espacios de los edificios que se van a agenerar en el modelo de agentes.

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
        building (int): id del edificio en el que se encuentra el agente
        walkable (bool): indica si el edificio es transitable por peatones
    """
    def __init__(self,uniqueId,model, busStop, walkable=True):
        super().__init__(uniqueId,model)
        self.busStop = busStop
        self.walkable = walkable