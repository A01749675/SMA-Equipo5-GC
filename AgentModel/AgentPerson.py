import mesa

from AgentStoplights import Stoplight
from AgentStreet import Street
from AgentBuilding import Building
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

        self.waiting = False
        self.waitingTime = 20

        self.inBus = inBus
        self.Bus = None
        self.justExited = False
        self.justGotIn = False

        self.crossing = False
        self.streetDir = None
        self.onStreet = False
        self.justCrossed = False

        self.waitingLightOrCar = False
        
    def is_agent_bus(self, obj, neighbors):
        from AgentBus import AgentBus  # Lazy import here
        return isinstance(obj, AgentBus)
    
    def getOutBus(self):
        """
        Método que simula la salida de la persona del bus en la simulación.
        """
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        cell = self.model.grid.get_cell_list_contents(neighbors[0]) + self.model.grid.get_cell_list_contents(neighbors[1]) + self.model.grid.get_cell_list_contents(neighbors[2]) + self.model.grid.get_cell_list_contents(neighbors[3])
        for c in cell:
            if isinstance(c, Building):
                if c.walkable:
                    self.model.grid.move_agent(self, c.pos)
                    break
        self.inBus = False
        self.Bus.people.remove(self)
        self.Bus = None
        self.justGotIn = False
        self.waiting = False
        self.waitingTime = 20
        self.justExited = True
    
    def caminar(self):
        """
        Método que simula el movimiento de la persona en la simulación.
        """

        if not self.waiting:
            current_cell = self.model.grid.get_cell_list_contents(self.pos)
            print("Caminandoooo")

            for c in current_cell:
                if isinstance(c,BusStop):
                    self.waiting = True
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

            if calleCruzar != None and not self.waitingLightOrCar:
                #print("Calle a cruzar")
                coin = self.random.choice([1, 2])
                if coin == 1 and not self.justCrossed:
                    #print("Calle a cruzar22222")
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

                    if self.checarSemaforo(neighbors) or self.checarCarro(neighbors):
                        self.waitingLightOrCar = True
                        return

                    return

            if direccion == "der":
                self.model.grid.move_agent(self, neighbors[3])
            elif direccion == "izq":
                self.model.grid.move_agent(self, neighbors[0])
            elif direccion == "up":
                self.model.grid.move_agent(self, neighbors[2])
            elif direccion == "down":
                self.model.grid.move_agent(self, neighbors[1])

            self.justExited = False

        else:
            print("Esperando")
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
            cell = self.model.grid.get_cell_list_contents(neighbors[0]) + self.model.grid.get_cell_list_contents(neighbors[1]) + self.model.grid.get_cell_list_contents(neighbors[2]) + self.model.grid.get_cell_list_contents(neighbors[3])
            for c in cell:
                if self.is_agent_bus(c, neighbors) and not self.justExited:
                    print("Busssss Busssss Busssss")
                    self.waiting = False
                    self.waitingTime = 20

                    self.inBus = True
                    self.Bus = c
                    c.people.append(self)
                    self.justGotIn = True

            self.waitingTime -= 1
            if self.waitingTime == 0 and self.waiting:
                self.waiting = False
                self.justExited = True
                self.waitingTime = 20


    def subscribedToBus(self):
        """
        Método que simula la suscripción de la persona al bus en la simulación.
        """
        self.model.grid.move_agent(self,self.Bus.pos)

    def checarSemaforo(self, neighbors):
        """
        Método que checa si hay un semáforo en la dirección de la persona.

        Args:
            neighbors (list): lista de vecinos de la persona
        """
        if self.streetDir == "up":
            cell = self.model.grid.get_cell_list_contents([neighbors[2]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c.state == "Green":
                        return True
                    else:
                        return False
        elif self.streetDir == "down":
            cell = self.model.grid.get_cell_list_contents([neighbors[1]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c.state == "Green":
                        return True
                    else:
                        return False
        elif self.streetDir == "left":
            cell = self.model.grid.get_cell_list_contents([neighbors[0]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c.state == "Green":
                        return True
                    else:
                        return False
        elif self.streetDir == "right":
            cell = self.model.grid.get_cell_list_contents([neighbors[3]])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c.state == "Green":
                        return True
                    else:
                        return False

        for n in neighbors:
            cell = self.model.grid.get_cell_list_contents([n])
            for c in cell:
                if isinstance(c, Stoplight):
                    if c.state == "Green":
                        return True
        return None

    def checarCarro(self, neighbors):
        """
        Método que checa si hay un carro en la dirección de la persona.

        Args:
            neighbors (list): lista de vecinos de la persona
        """
        from SmartAgentCar import SmartCar #lazy import
        from AgentBus import AgentBus #lazy import

        if self.streetDir == "up":
            cell = self.model.grid.get_cell_list_contents([neighbors[2]]) + self.model.grid.get_cell_list_contents([neighbors[2][0]+1,neighbors[2][1]]) + self.model.grid.get_cell_list_contents([neighbors[2][0]-1,neighbors[2][1]])
            #print(cell)
            for c in cell:
                if isinstance(c, SmartCar) or isinstance(c, AgentBus):
                    #print("car up")
                    return True
            #print("no car up")
            return False
        elif self.streetDir == "down":
            cell = self.model.grid.get_cell_list_contents([neighbors[1]]) + self.model.grid.get_cell_list_contents([neighbors[1][0]+1,neighbors[1][1]]) + self.model.grid.get_cell_list_contents([neighbors[1][0]-1,neighbors[1][1]])
            #print(cell)
            for c in cell:
                if isinstance(c, SmartCar) or isinstance(c, AgentBus):
                    #print("car down")
                    return True
            #print("no car down")
            return False
        elif self.streetDir == "left":
            cell = self.model.grid.get_cell_list_contents([neighbors[0]]) + self.model.grid.get_cell_list_contents([neighbors[0][0],neighbors[0][1]+1]) + self.model.grid.get_cell_list_contents([neighbors[0][0],neighbors[0][1]-1])
            #print(cell)
            for c in cell:
                if isinstance(c, SmartCar) or isinstance(c, AgentBus):
                    #print("car left")
                    return True
            #print("no car left")
            return False
        elif self.streetDir == "right":
            cell = self.model.grid.get_cell_list_contents([neighbors[3]]) + self.model.grid.get_cell_list_contents([neighbors[3][0],neighbors[3][1]+1]) + self.model.grid.get_cell_list_contents([neighbors[3][0],neighbors[3][1]-1])
            #print(cell)
            for c in cell:
                if isinstance(c, SmartCar) or isinstance(c, AgentBus):
                   # print("car right")
                    return True
            #print("no car right")
            return False

        for n in neighbors:
            cell = self.model.grid.get_cell_list_contents([n])
            for c in cell:
                if isinstance(c, SmartCar) or isinstance(c, AgentBus):
                    #print("carrrr")
                    return True
        #print("no carrrrr")
        return False

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
        #print("Cruzando "+str(self.streetDir))
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
        #print("Cruzando2222 "+str(self.streetDir))
        if self.streetDir == "up":
            #print("Up")
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
        elif self.streetDir == "down":
            #print("Down")
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
        elif self.streetDir == "left":
            #print("Left")
            self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
        elif self.streetDir == "right":
            #print("Right")
            self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
        pass

    def step(self):
        """
        Método que simula el paso de la persona en la simulación.
        """
        if not self.inBus:

            if not self.crossing or self.justExited:
                self.justExited = False
                self.caminar()
                self.justCrossed = False
            else:
                neigborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
                if self.checarCarro(neigborhood) and not self.waitingLightOrCar and not self.justCrossed:
                    self.waitingLightOrCar = True
                    #print("esperando carro")
                if not self.waitingLightOrCar:
                    #print("Cruzandooooooooo")
                    self.cruzarCalle()
                    self.justCrossed = True

                if not self.checarSemaforo(neigborhood) and not self.checarCarro(neigborhood) and self.waitingLightOrCar:
                    self.waitingLightOrCar = False
                    #print("fin de la esperaaaa")

                #print("me trabeeeeeee o estoy cruzando bien")
                #print(self.waitingLightOrCar)
                #print(self.streetDir)

        else:
            if not self.justExited:
                print("Subscrito al bus")
                print(self.Bus)
                print(self.inBus)
                self.subscribedToBus()
