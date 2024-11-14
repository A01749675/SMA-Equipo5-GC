
#Clase que define los estacionamientos en el modelo de agentes


#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 10/11/2024




import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors



class Parking(mesa.Agent):
    """Clase que define los agentes de estacionamientos en el modelo de agentes. Son los espacios de los estacionamientos que se van a generar en el modelo de agentes.
        Sirven de referencia para el estacionamiento de los autos en el modelo de agentes. 
        Son el origen y destino de los autos en el modelo de agentes.
    

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente 
        parking (int): id del estacionamiento que representa el agente
    """
    def __init__(self,uniqueId,model, parking):
        super().__init__(uniqueId,model)
        self.parkingId = parking