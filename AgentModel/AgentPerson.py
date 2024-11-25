import mesa
from AgentStreet import Street
from AgentBuilding import Building
from AgentParking import Parking


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
        neighbors = [(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]+1),(self.pos[0],self.pos[1]-1)]
        possible_steps = []
        for neighbor in neighbors:
            if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                continue
            cell = self.model.grid.get_cell_list_contents(neighbor)
            for c in cell:
                if isinstance(c,Persona):
                    continue
                if isinstance(c,Parking):
                    continue
                # if isinstance(c,Street):
                #     if c.walkable:
                #         possible_steps.append(neighbor)
                #         continue
                if isinstance(c,Building):
                    if c.walkable:
                        possible_steps.append(neighbor)
                        continue
                
        nextPos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self,nextPos)

    def girar(self):
        """
        Método que simula el giro de la persona en la simulación.
        """
        pass

    def esquinaCheck(self):
        """
        Método que simula el cruce de la persona en la simulación.
        """
        pass

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