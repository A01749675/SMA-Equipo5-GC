#CLase que implementa el algoritmo de Kruskal para encontrar el arbol de expansion minima de un grafo.
#Author: Carlos Iker Fuentes Reyes A01749675 con inspiración de la clase del profesor Ariel Ortiz. El código fue adaptado para el presente problema
#pero los méritos del desarrollo en su mayoría son del profesor Ariel Ortiz, 

from heapq import heapify, heappop
from typing import NamedTuple
from pprint import pprint
type WeightedGraph = dict[int, set[tuple[int,int]]]

class Edge(NamedTuple):
    """Clase que hereda de NamedTuple y define una arista en un grafo ponderado.

    Args:
        NamedTuple Super clase

    
    """
    weight : int
    u : int #starting vertex
    v : int # ending vertex
    
    def __eq__(self, other :object)->bool:
        """ 
        Método que compara si dos aristas son iguales.
        """
        if not isinstance(other,Edge):
            return False
        
        return (self.weight == other.weight
                and ((self.u == other.u and self.v == other.v)
                    or (self.u == other.v and self.v == other.u)))
        
    def __hash__(self)->int:
        """Genera un hash para la arista.

        Returns:
            int: hash de la arista
        """
        return hash(self.weight)+hash(self.u)+hash(self.v)
                

def kruskal_mst(graph : WeightedGraph)-> tuple[int,WeightedGraph]:
    """Genera el arbol de expansion minima de un grafo ponderado.

    Args:
        graph (WeightedGraph): grafo ponderado para los estacinamientos

    Returns:
        tuple[int,WeightedGraph]: grafo que establece las direcciones
    """
    if not graph:
        return (0,{})
    queue : list[Edge] = make_heap(graph)
    result: WeightedGraph = {k : set() for k in graph}
    remaining_edges : int = len(graph) - 1
    total_cost : int = 0
    visited: set[str] = set()
    while remaining_edges:
        edge: Edge = heappop(queue)
        add_edge(result,edge)
        if (edge.u in visited and edge.v in visited and has_cycle(edge.u, result)):
            remove_edge(result,edge)
        else:
            visited.add(edge.u)
            visited.add(edge.v)
            total_cost += edge.weight
            remaining_edges -= 1
    return (total_cost,result)

def make_heap(graph: WeightedGraph)->list[Edge]:
    """Código que genera un heap a partir de los elementos del grafo

    Args:
        graph (WeightedGraph): _description_

    Returns:
        list[Edge]: _description_
    """
    result : set[Edge] = set()
    u: str 
    neighbors: set[tuple[str,int]]
    for u,neighbors in graph.items():
        v: str
        weight: int
        for v,weight in neighbors:
            result.add(Edge(weight,u,v))
    queue : list[Edge] = list(result)
    heapify(queue)
    return queue

def add_edge(graph: WeightedGraph, edge: Edge)->None:
    """Función para agregar una arista al grafo.

    Args:
        graph (WeightedGraph): grafo construido de los estacionamientos
        edge (Edge): arista a agregar entre estacionamientos 
    """
    weight,u,v = edge
    graph[u].add((v,weight))
    graph[v].add((u,weight))
    
def remove_edge(graph: WeightedGraph, edge: Edge)->None:
    """Eliminar una arista del grafo.

    Args:
        graph (WeightedGraph): : grafo construido de los estacionamientos
        edge (Edge): arista a agregar entre estacionamientos 
    """
    weight,u,v = edge
    graph[u].remove((v,weight))
    graph[v].remove((u,weight))
    
def has_cycle(initial: str,
              graph: WeightedGraph,
              visited : set[str] | None = None,
              parent:str | None = None,
              path :list[str] | None=None)->bool:
    """Función que determina si un grafo tiene ciclo"""
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(initial)
    path.append(initial)
    vertex: str
    for vertex, _ in graph[initial]:
        if vertex in visited:
            if vertex != parent:
                return True
        elif has_cycle(vertex,graph,visited,initial):
            return True
    return False
    
    
    

    