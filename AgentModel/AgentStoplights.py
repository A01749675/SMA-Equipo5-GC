import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors


class Stoplight(mesa.Agent):
    
    def __init__(self,uniqueId,model, stoplight,state):
        super().__init__(uniqueId,model)
        self.stoplightId = stoplight
        self.state = state

    def step(self):
        """
        Método que ejecuta las acciones de un agente Stoplight.
        """
        pass