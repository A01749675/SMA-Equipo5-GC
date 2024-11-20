import mesa

class AgentPerson(mesa.Agent):
    """Clase que define los agentes que representan a las personas en el modelo de la simulación.

    Args:
        uniqueId (int): id que identifica al agente
        model (mesa.Model): modelo en el que se encuentra el agente
    """
    def __init__(self,uniqueId,model):
        super().__init__(uniqueId,model)

    def caminar(self):
        """
        Método que simula el movimiento de la persona en la simulación.
        """
        pass

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