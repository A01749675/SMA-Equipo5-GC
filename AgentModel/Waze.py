type WeightedGraph = dict[int, set[tuple[int, int]]]
from GraphStructure import *

class Waze:
    def __init__(self):
        self.parkingGraph: WeightedGraph = {}
        self.graphDirections = {}
        self.knownParkings = set()

    def addDirection(self, direction, steps):
        if direction in self.graphDirections:
            if len(steps) < len(self.graphDirections[direction]):
                self.graphDirections[direction] = steps
        else:
            self.graphDirections[direction] = steps

    def addParkingNeighbors(self, parkingId, neighbor, steps):
        if parkingId in self.parkingGraph:
            self.parkingGraph[parkingId].add((neighbor, len(steps)))
        else:
            self.parkingGraph[parkingId] = {(neighbor, len(steps))}
        self.knownParkings.add(parkingId)

    def routeExists(self, start, end):
        path = str(start) + "-" + str(end)
        if path in self.graphDirections:
            return True
        return False

    def bestRouteToParking(self, start, end):
        
        cost, result = kruskal_mst(self.parkingGraph)
        best_path = []
        current_node = start
        print(f"start {start} end {end}")
        print(result)
        print("-----")
        print(self.knownParkings)
        print(self.graphDirections)
        
        if end not in self.knownParkings:
            return []


        while current_node != end:
            for children in result[current_node]:
                
                child = children[0]

                best_path += self.graphDirections[str(current_node) + "-" + str(child)]
                current_node = child
                if current_node == end: 
                    break

        print(f"Best path from {start} to {end} is {best_path}")
        return best_path