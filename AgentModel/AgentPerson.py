import mesa

from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentBuilding import Building
from AgentParking import Parking
from AgentBusStop import BusStop
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

        self.crossing = False
        self.streetDir = None
        self.onStreet = False
        
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
                                #print("esquins inf der")

                for c in cell1:
                    if isinstance(c, Street) or isinstance(c, Stoplight):
                        direccion = "up"
                        #print("up normal")
                        for c in cell3:
                            if isinstance(c, Stoplight) or isinstance(c, Street):
                                direccion = "der"
                                #print("esquins sup izq")

                calleCruzar = self.checarCalle(neighbors)

                if calleCruzar != None:
                    print("Calle a cruzar")
                    coin = self.random.choice([1, 2])
                    if coin == 1:
                        print("Calle a cruzar22222")
                        pos = self.pos
                        self.crossing = True
                        if pos[0] > calleCruzar.pos[0]:
                            self.streetDir = "left"
                        elif pos[0] < calleCruzar.pos[0]:
                            self.streetDir = "right"
                        elif pos[1] > calleCruzar.pos[1]:
                            self.streetDir = "down"
                        elif pos[1] < calleCruzar.pos[1]:
                            self.streetDir = "up"
                        return

                if direccion == "der":
                    self.model.grid.move_agent(self, neighbors[3])
                elif direccion == "izq":
                    self.model.grid.move_agent(self, neighbors[0])
                elif direccion == "up":
                    self.model.grid.move_agent(self, neighbors[2])
                elif direccion == "down":
                    self.model.grid.move_agent(self, neighbors[1])
                
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

    def checarCalle(self, neighbors):
        """
        Método que checa si hay una calle en la dirección de la persona.

        Args:
            neighbors (list): lista de vecinos de la persona
        """
        possibleCross = []
        for n in neighbors:
            cell = self.model.grid.get_cell_list_contents([n])
            for c in cell:
                if isinstance(c, Street):
                    if c.walkable:
                        possibleCross.append(c)
        if len(possibleCross) > 0:
            return self.random.choice(possibleCross)
        return None

    def cruzarCalle(self):
        """
        Método que simula el cruce de la persona en la simulación.
        """
        print("Cruzando "+str(self.streetDir))
        cell = self.model.grid.get_cell_list_contents(self.pos)
        for c in cell:
            if isinstance(c, Street):
                if not c.walkable:
                    self.crossing = False
                    self.streetDir = None
                    self.onStreet = False
                    return
            if isinstance(c, Street):
                self.onStreet = True
            if self.onStreet:
                if isinstance(c, Building):
                    self.crossing = False
                    self.streetDir = None
                    self.onStreet = False
                    return
        print("Cruzando2222 "+str(self.streetDir))
        if self.streetDir == "up":
            print("Up")
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
        elif self.streetDir == "down":
            print("Down")
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
        elif self.streetDir == "left":
            print("Left")
            self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
        elif self.streetDir == "right":
            print("Right")
            self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
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

            if not self.crossing:
                self.caminar()
            else:
                self.cruzarCalle()

        #else:
            #self.subscribeToBus()
