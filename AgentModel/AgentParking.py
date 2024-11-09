import mesa
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.colors as mcolors



class Parking(mesa.Agent):
    
    def __init__(self,uniqueId,model, parking):
        super().__init__(uniqueId,model)
        self.parking = parking