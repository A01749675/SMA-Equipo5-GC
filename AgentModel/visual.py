# Roomba Cleaning Simulation. 

#Este código es la representacón gráfica del modelo simulado en la lase Rooomba.py
#Despliega la simulación en una interfaz gráfica para una mejor visualización de la simulación, ésta corre en un servidor local,
#muestra un grid con celdas sucias y limpias, y agentes Roomba que se mueven y limpian las celdas sucias.
#Además, muestra gráficas en tiempo real de los datos importantes como el porcentaje de celdas limpias, el tiempo de ejecución,
# y los pasos requeridos para completar la simulación

# Autor: Carlos Iker Fuentes Reyes A01749675 && Santiago Chevez Trejo A01749887
# Fecha de creación: 7/11/2024


from mesa.visualization.modules import ChartModule,BarChartModule

import mesa
import random

from ModelCity import CityModel
from AgentBuilding import Building
from AgentParking import Parking
from AgentStoplights import Stoplight

def agentPortrayal(agent):
    """
    Instancia un agente Roomba y lo representa en la interfaz gráfica.

    Args:
        agent (Agent): un agente que puede ser de tipo RoombaAgent o Cell.

    Returns:
        dict: diccionario con las propiedades del agente.
    """
    portrayal = {"Shape": "",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1.0,
                    "h": 1.0}
    
    if isinstance(agent, Building):
        print("Building")
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
    if isinstance(agent, Parking):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
    if isinstance(agent, Stoplight):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "red"
        
    return portrayal

def generateRandomGridSize():
    """
    Genera un tamaño aleatorio para el grid.

    Returns:
        tuple: regresa una tupla con dos valores enteros 
                aleatorios para el ancho y alto del grid.
    """
    return (24,24)

def generateRandomAgents():
    """
    Genera un número aleatorio de agentes Roomba.

    Returns:
        int: número entero aleatorio de agentes Roomba.
    """
    return random.randint(1, 20)

width , height = generateRandomGridSize()


grid = mesa.visualization.CanvasGrid(agentPortrayal, 24, 24, 500, 500)




server = mesa.visualization.ModularServer(
    CityModel,
    [grid],
    "City",
    {"numAgents": random.randint(1, 20)}
)

server.port = 3145
server.launch()