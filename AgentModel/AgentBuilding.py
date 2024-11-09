
import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors



class Building(mesa.Agent):
    
    def __init__(self,uniqueId,model, building):
        super().__init__(uniqueId,model)
        self.building = building