import mesa
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
        self.inBus = inBus
        self.waiting = False
        self.waitingTime = 0
        
        self.Bus = None
        self.justExited = False
        
    def is_agent_bus(self, obj):
        from AgentBus import AgentBus  # Lazy import here
        return isinstance(obj, AgentBus)
    
    def is_agent_car(self, obj):
        from SmartAgentCar import SmartCar  # Lazy import here
        return isinstance(obj, SmartCar)
    
    def caminar(self):
        """
        Método que simula el movimiento de la persona en la simulación.
        """
        if not self.waiting:
            current_cell = self.model.grid.get_cell_list_contents(self.pos)
            
            if not self.justExited:
                for c in current_cell:
                    if isinstance(c,BusStop):
                        self.waiting = True
                        self.waitingTime = 20
                        return
                    
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
                        if self.is_agent_bus(c):
                            continue
                        if self.is_agent_car(c):
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
                
            else:
                
                neighbors = [(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]+1),(self.pos[0],self.pos[1]-1)]
                
                for neighbor in neighbors:
                    if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                        continue
                    cell = self.model.grid.get_cell_list_contents(neighbor)
                    for c in cell:
                        if self.is_agent_bus(c):
                            if not self.inBus:
                                self.model.grid.move_agent(self,neighbor)
                                self.Bus = c
                                c.board(self)
                                self.inBus = True
        else:
            neighbors = [(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]+1),(self.pos[0],self.pos[1]-1)]
            possible_steps = []
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                    continue
                cell = self.model.grid.get_cell_list_contents(neighbor)
                for c in cell:
                    if isinstance(c,BusStop):
                        continue
                    if self.is_agent_bus(c):
                        continue
                    if self.is_agent_car(c):
                        continue
                    if isinstance(c,Building):
                        if c.walkable:
                            possible_steps.append(neighbor)
            self.justExited = False
            self.model.grid.move_agent(self,self.random.choice(possible_steps))

    def subscribeToBus(self):
        """
        Método que simula la suscripción de la persona al bus en la simulación.
        """
        if self.Bus.waiting:
            neighbors = [(self.pos[0]+1,self.pos[1]),(self.pos[0]-1,self.pos[1]),(self.pos[0],self.pos[1]+1),(self.pos[0],self.pos[1]-1)]
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] > self.model.grid.width - 1 or neighbor[1] < 0 or neighbor[1] > self.model.grid.height - 1:
                    continue
                cell = self.model.grid.get_cell_list_contents(neighbor)
                for cellContent in cell:
                    if isinstance(cellContent,BusStop):
                        choices = [True,False]
                        choice = self.random.choice(choices)
                        if choice:
                            self.inBus = False
                            self.Bus = None
                            self.model.grid.move_agent(self,neighbor)
                            print("I am out of the bus")
                            self.justExited = True
                            return 
            self.Bus.board(self)
            self.inBus = True
        self.model.grid.move_agent(self,self.Bus.pos)

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
        if not self.inBus:
            
            if self.waiting:
                self.waitingTime -= 1
                if self.waitingTime == 0:
                    self.waiting = False
            self.caminar()
        else:
            self.subscribeToBus()
