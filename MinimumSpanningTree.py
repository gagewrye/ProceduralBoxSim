import random
import heapq

class MST():
    def __init__(self, num_points: int, map_size_x: int, map_size_y: int, max_room_size: int, rand: random) -> None:
        self.map_size = (map_size_x, map_size_y)
        self.num_points = num_points
        self.max_room_size = max_room_size
        self.vertices = create_points(num_points, map_size_x, map_size_y, rand, max_room_size)
        self.graph = generate_graph(self.vertices)
        self.mst = prims_algorithm(self.graph, next(iter(self.graph)))
    
    # Adds additional connections between rooms to create loops and complexity
    def add_cycles(self, num_cycles: int) -> None:
        possible_connections = []

        for vertex1 in self.vertices:
            for vertex2 in self.vertices:
                if vertex1 != vertex2 and not directly_connected(self.mst, vertex1, vertex2):
                    distance = manhattan_distance(vertex1, vertex2)
                    # Use a heap to maintain the smallest distances at the top
                    heapq.heappush(possible_connections, (distance, vertex1, vertex2))
        
        for _ in range(num_cycles):
            if possible_connections:
                distance, room1, room2 = heapq.heappop(possible_connections)
                
                self.mst[room1].append((room2, distance))
            else:
                break  # No more connections to add - you have turned it back into a fully connected graph!


def create_points(num_points: int, x: int, y: int, rand: random, max_room_size: int) -> list:
    points = []
    buffer = max_room_size
    for _ in range(num_points):
        points.append((rand.randint(0+buffer,x-buffer), rand.randint(0+buffer,y-buffer)))
    return points

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Generate a fully connected graph from a list of points
def generate_graph(points):
    graph = {}
    for point1 in points:
        for point2 in points:
            if point1 != point2:
                distance = manhattan_distance(point1, point2)
                graph[point1].append((point2, distance))
    return graph

# Prim's Algorithm to find the MST - chatGPT
def prims_algorithm(graph, starting_vertex):
    mst = {}
    visited = set([starting_vertex])
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex]]
    
    while edges:
        cost, frm, to = sorted(edges)[0]
        edges = [edge for edge in edges if edge[2] != to]
        
        if to not in visited:
            visited.add(to)
            mst[frm].append((to, cost))
            for next_to, cost in graph[to]:
                if next_to not in visited:
                    edges.append((cost, to, next_to))
    
    return mst

def directly_connected(mst, room1, room2):
    for dest, _ in mst.get(room1):
        if dest == room2:
            return True
    for dest, _ in mst.get(room2):
        if dest == room1:
            return True
    return False


# Example
rand = random.Random(47)
mst = MST(5, 100, 100, rand)
mst.add_cycles(5)