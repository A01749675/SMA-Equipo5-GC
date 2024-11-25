import mesa

from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentBuilding import Building
from AgentParking import Parking
from AgentBusStop import BusStop


class Persona(mesa.Agent):
    """Clase que define los agentes que representan a las personas en el modelo de la simulación.

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
    """
    def __init__(self, uniqueId, model, inBus = False):
        super().__init__(uniqueId,model)
        self.unique_id = uniqueId
        self.in_Bus = inBus

    def caminar(self):
        """
        Método que simula el movimiento de la persona en la simulación.
        """
        direccion = None
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        cell1 = self.model.grid.get_cell_list_contents([neighbors[0]])
        cell2 = self.model.grid.get_cell_list_contents([neighbors[1]])
        cell3 = self.model.grid.get_cell_list_contents([neighbors[2]])
        cell4 = self.model.grid.get_cell_list_contents([neighbors[3]])
        cellPos = self.model.grid.get_cell_list_contents([self.pos])

        for c in cell3:
            if isinstance(c, Street) or isinstance(c, Stoplight):
                direccion = "der"

        for c in cell2:
            if isinstance(c, Street) or isinstance(c, Stoplight):
                direccion = "izq"

        for c in cell4:
            if isinstance(c, Street) or isinstance(c, Stoplight):
                direccion = "down"
                for c in cell2:
                    if isinstance(c, Street) or isinstance(c, Stoplight):
                        direccion = "izq"
                        print("esquins inf der")

        for c in cell1:
            if isinstance(c, Street) or isinstance(c, Stoplight):
                direccion = "up"
                print("up normal")
                for c in cell3:
                    if isinstance(c, Stoplight) or isinstance(c, Street):
                        direccion = "der"
                        print("esquins sup izq")

        if self.checarSemaforo(neighbors) != None:
            print("Semaforo")

        for c in cellPos:
            if isinstance(c, BusStop):
                # direccion = None
                print("BusStop")

        if direccion == "der":
            self.model.grid.move_agent(self, neighbors[3])
        elif direccion == "izq":
            self.model.grid.move_agent(self, neighbors[0])
        elif direccion == "up":
            self.model.grid.move_agent(self, neighbors[2])
        elif direccion == "down":
            self.model.grid.move_agent(self, neighbors[1])

    def checarSemaforo(self, neighbors):
        """
        Método que checa si hay un semáforo en la dirección de la persona.

        Args:
            neighbors (list): lista de vecinos de la persona
        """
        for n in neighbors:
            cell = self.model.grid.get_cell_list_contents([n])
            for c in cell:
                if isinstance(c, Stoplight):
                    return c
        return None

    def cruzarCalle(self):
        """
        Método que simula el cruce de la persona en la simulación.
        """
        pass

    def step(self):
        """
        Método que simula el paso de la persona en la simulación.
        """
        self.caminar()