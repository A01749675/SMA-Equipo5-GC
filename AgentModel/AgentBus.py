
#CLase que declara los agentes de tipo carro Inteligentes, que tienen acceso a un manejador de rutas que les permite revisar si ya existe una ruta de 
#un estacionamiento a otro y si no, generar una nueva ruta.

#Esta clase combina el comportamiento de movimiento aleatorio con una heurística simple (reducir distancia) junto con la construcción de rutas directas entre 
#estacionamientos.

#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 13/11/2024

import math
from collections import deque

import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors

from AgentStreet import Street
from AgentStoplights import Stoplight
from AgentParking import Parking
from AgentBuilding import Building
from AgentStreetDir import AgentStreetDir
import random
from pprint import pprint

class AgentBus(mesa.Agent):
    
    def __init__(self,unique_id,model,bus,busStop):
        """Constructor de la clase AgentBus

        Args:
            unique_id (int): Identificador único del agente
            pos (tuple): Posición del agente
            model (ModelCity): Modelo de la ciudad
            stoplight (Stoplight): Semáforo al que pertenece el agente
        """
        super().__init__(unique_id,model)
        self.bus = bus
