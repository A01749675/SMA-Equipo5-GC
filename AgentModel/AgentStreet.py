import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors


class Street(mesa.Agent):
    
    def __init__(self,uniqueId,model, street, directions):
        super().__init__(uniqueId,model)
        self.street = street
        self.availableDirections = {
            "N":directions["N"],
            "S":directions["S"],
            "E":directions["E"],
            "W":directions["W"]
            }
        self.movementEquivalence = {
                "N":(0,1),
                "S":(0,-1),
                "E":(1,0),
                "W":(-1,0)
            }

    def step(self):
        """
        Método que ejecuta las acciones de un agente Street.
        """
        pass