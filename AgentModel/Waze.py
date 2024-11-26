#Clase que define la estructura de un grafo ponderado en el que se guarda la información de los estacionamientos y las direcciones entre ellos.
#Guarda, asimismo, los pasos a seguir para llegar de un estacionamiento a otro.
#Author :Carlos Iker Fuentes Reyes A01749675
#Fecha de creación: 13/11/2024



from GraphStructure import *
from collections import deque


#type WeightedGraph = dict[int, set[tuple[int, int]]]


class Waze:
    """
    Clase que define la estructura de un grafo ponderado en el que se guarda la información de los estacionamientos y las direcciones entre ellos.
    Guarda, asimismo, los pasos a seguir para llegar de un estaconamiento a otro.
    """
    def __init__(self):
        self.parkingGraph = {}
        self.graphDirections = {}
        self.knownParkings = set()

    def addDirection(self, direction, steps):
        """Añaade una dirección al grafo de direcciones. En caso de que ya exista, actualiza los pasos a seguir si son menores a los actuales.

        Args:
            direction (str): define como llegar de un estaconamiento a otro
            steps (list[tuple[int,int]]): pasos a seguir para llegar de un estacionamiento a otro
        """
        split = direction.split("-")
        if split[0] == split[1]:
            return
        if direction in self.graphDirections:
            if len(steps) < len(self.graphDirections[direction]):
                print(f"Updating direction {direction} with {steps}")
                self.graphDirections[direction] = steps
        else:
            self.graphDirections[direction] = steps

    def addParkingNeighbors(self, parkingId, neighbor, steps):
        """Añaade un vecino a un estacionamiento en el grafo ponderado.

        Args:
            parkingId (int): id del estacionamiento
            neighbor (int): id del vecino
            steps (list[tuple[int,int]]): pasos a seguir para llegar de un estacionamiento a otro
        """
        if parkingId in self.parkingGraph and parkingId != neighbor:
            self.parkingGraph[parkingId].add((neighbor, len(steps)))
        elif parkingId != neighbor and parkingId not in self.parkingGraph:
            self.parkingGraph[parkingId] = {(neighbor, len(steps))}
        self.knownParkings.add(parkingId)

    def routeExists(self, start, end):
        """
        Código que verifica si existe una ruta entre dos estacionamientos.

        Args:
            start (int): id del estacionamiento de inicio
            end (int): id del estacionamiento de destino

        Returns:
            bool: depende de si existe una ruta entre los estacionamientos
        """
        if start == end:
            return False
        if start not in self.knownParkings or end not in self.knownParkings:
            return False
        if start not in self.parkingGraph or end not in self.parkingGraph:
            return False
        if self.shortestPath(start, end):
            return True
        # if self.bestRouteToParking(start, end):
        #     return True
        return False

    def bestRouteToParking(self, start, end):
        """
        Código que genera la mejor ruta entre dos estacionamientos, primero creando el arbol de expansion minima y luego buscando el camino más corto.
        Se añden estos valores  a un queue que se regresa al final.
        Como el grafo se va construyendo con el tiempo, puede que se encuentre incompleto en las primeras llamadas a la función, por lo que se implementó un 
        manejo de errore sy un contador para evitar que se quede en un ciclo infinito.

        Args:
            start (int): estaconamiento de inicio
            end (int): estacionamiento de destino

        Returns:
            deque: pasos a seguir para llegar de un estacionamiento a otro
        """
        try: 
            queue = deque()
            direction = str(start) + "-" + str(end)
            if direction in self.graphDirections:
                for elem in self.graphDirections[direction]:
                    queue.append(elem)
                return queue
            
            
            cost, result = kruskal_mst(self.parkingGraph)
            best_path = []
            current_node = start
            
            if end not in self.knownParkings:
                return []
        
            seen = set()
            seen.add(current_node)
            max_cycle = len(self.knownParkings)
            while current_node != end and max_cycle > 0:
                for children in result[current_node]:
                    if children[0] in seen:
                        if children[0] == end:
                            break
                        continue
                    child = children[0]

                    best_path += self.graphDirections[str(current_node) + "-" + str(child)]
                    current_node = child
                    seen.add(current_node)
                    if current_node == end: 
                        break
                max_cycle -= 1

           # print(f"Best path from {start} to {end} is {best_path}")
            
            if best_path:
                for path in best_path:
                    queue.append(path)
        except Exception as e:
            print
            print(f"Error: {e}")
            return deque()
        print(F"result: {result}")
        return queue
    
    def shortestPath(self,start,end):
        """
        This algorithm uses djiksra's algorithm to find the shortest path between two nodes in a graph. 
        It generates the graph using the known parkings and the directions between them, and measures the distances having the starting graph. 

        Args:
            start (int): id del estacionamiento de inicio
            end (int): id del estacionamiento de destino

        Returns:
            deque: pasos a seguir para llegar de un estacionamiento a otro
        """
        try: 
            queue = deque()
            direction = str(start) + "-" + str(end)
            if direction in self.graphDirections:
                for elem in self.graphDirections[direction]:
                    queue.append(elem)
                return queue
            
            
            result = dijkstra_spt(start,self.parkingGraph)
            best_path = []
            current_node = start
            
            if end not in self.knownParkings:
                return []
        
            seen = set()
            seen.add(current_node)
            max_cycle = len(self.knownParkings)
            while current_node != end and max_cycle > 0:
                for children in result[current_node]:
                    if children[0] in seen:
                        if children[0] == end:
                            break
                        continue
                    child = children[0]

                    best_path += self.graphDirections[str(current_node) + "-" + str(child)]
                    current_node = child
                    seen.add(current_node)
                    if current_node == end: 
                        break
                max_cycle -= 1

            #print(f"Best path from {start} to {end} is {best_path}")
            
            if best_path:
                for path in best_path:
                    queue.append(path)
        except Exception as e:
           #print(f"Error: {e}")
            return deque()
        #print(F"result: {result}")
        return queue