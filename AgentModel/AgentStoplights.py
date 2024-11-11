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
        self.countSteps = 0
        self.TIME = 10
        self.on = False if self.state == "Red" else True

    def step(self):

        self.countSteps += 1
        if self.countSteps%self.TIME==0:
            self.on = not self.on
            self.state = "Red" if self.on else "Green"