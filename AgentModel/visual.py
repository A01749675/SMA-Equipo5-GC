import signal
import sys

from mesa.visualization.modules import ChartModule, BarChartModule
import mesa
import random

from AgentPerson import Persona
from ModelCity import CityModel
from AgentBuilding import Building
from AgentParking import Parking
from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentCar import Car
from AgentStreetDir import AgentStreetDir
from SmartAgentCar import SmartCar
from AgentBusStop import BusStop
from AgentBus import AgentBus

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
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "blue"
        if agent.walkable:
            portrayal["text"] = "W"
            portrayal["text_color"] = "black"
    if isinstance(agent, Parking):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "yellow"
        portrayal["text"] = str(agent.parkingId)
        portrayal["text_color"] = "black"
    if isinstance(agent, Stoplight):
        portrayal["Shape"] = "rect"
        if agent.state == "Red":
            portrayal["Color"] = "red"
            portrayal["text"] = agent.stoplightId
            portrayal["text_color"] = "black"
        elif agent.state == "Green":
            portrayal["Color"] = "green"
            portrayal["text"] = agent.stoplightId
            portrayal["text_color"] = "black"
        else:
            portrayal["Color"] = "yellow"
            portrayal["text"] =agent.stoplightId
            portrayal["text_color"] = "black"
            
    if isinstance(agent,AgentStreetDir):
        portrayal["Shape"] ="rect"
        portrayal["Color"] = "purple"
    if isinstance(agent, Street):
        portrayal["Shape"] = "arrowHead"
        portrayal["Color"] = "black"
        portrayal["scale"] = 0.5  # Adjust the scale as needed
        if agent.walkable:
            portrayal["text"] = "w"
            portrayal["text_color"] = "red"
        agentDirection = ""
        for dir, value in agent.availableDirections.items():
            if value:
                agentDirection = dir
                break
            
        if agentDirection == "N":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = 1
        elif agentDirection == "S":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = -1
        elif agentDirection == "E":
            portrayal["heading_x"] = 1
            portrayal["heading_y"] = 0
        elif agentDirection == "W":
            portrayal["heading_x"] = -1
            portrayal["heading_y"] = 0
    if isinstance(agent, Car) or isinstance(agent, SmartCar):
        possible = ["car.jpeg"]
        portrayal["Shape"] = random.choice(possible)
        portrayal["Color"] = "red"
        portrayal["text_color"] = "black"

    if isinstance(agent, Persona):
        portrayal["Color"] = "red"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "black"
        
    if isinstance(agent, BusStop):
        portrayal["Color"] = "green"
        portrayal["Shape"] = "rect"
        portrayal["text"] = agent.busStop
        portrayal["text_color"] = "black"
        
    if isinstance(agent, AgentBus):
        portrayal["Color"] = "blue"
        portrayal["Shape"] = "bus.jpeg"
        portrayal["r"] = 0.5
        portrayal["text"] = agent.bus
        portrayal["text_color"] = "black"


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
    {"numAgents": 20}
    {"numAgents": 5}
)

server.port = 3900

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

server.launch()