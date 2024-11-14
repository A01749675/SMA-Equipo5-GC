type WeightedGraph = dict[int, set[tuple[int, int]]]
from GraphStructure import *
from collections import deque
class Waze:
    def __init__(self):
        self.parkingGraph: WeightedGraph = {}
        self.graphDirections = {}
        self.knownParkings = set()

    def addDirection(self, direction, steps):
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
        if parkingId in self.parkingGraph and parkingId != neighbor:
            self.parkingGraph[parkingId].add((neighbor, len(steps)))
        elif parkingId != neighbor and parkingId not in self.parkingGraph:
            self.parkingGraph[parkingId] = {(neighbor, len(steps))}
        self.knownParkings.add(parkingId)

    def routeExists(self, start, end):
        if start == end:
            return False
        if start not in self.knownParkings or end not in self.knownParkings:
            return False
        if start not in self.parkingGraph or end not in self.parkingGraph:
            return False
        if self.bestRouteToParking(start, end):
            return True
        return False

    def bestRouteToParking(self, start, end):
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

            print(f"Best path from {start} to {end} is {best_path}")
            
            if best_path:
                for path in best_path:
                    queue.append(path)
        except Exception as e:
            print
            print(f"Error: {e}")
            return deque()
        print(F"result: {result}")
        return queue