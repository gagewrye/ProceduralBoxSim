import random
import heapq

class MST():
    """
    This class creates a minimum spanning tree using a dictionary with (X,Y) vertices as
    the keys and a value of a list of vertices that the key is connected to.
    """
    def __init__(self, num_points: int, map_size_x: int, map_size_y: int, max_room_size: int, seed: int) -> None:
        self.seed = seed
        self.map_size = (map_size_x, map_size_y)
        self.max_room_size = max_room_size
        self.vertices = _create_points(num_points, map_size_x, map_size_y, max_room_size)
        graph = _generate_graph(self.vertices)
        self.mst = _prims_algorithm(graph, next(iter(graph)))
    
    def get_mst(self) -> dict:
        return self.mst
    def get_vertices(self) -> list[tuple]:
        return self.vertices
    def get_map_size(self) -> tuple:
        return self.map_size
    def get_seed(self) -> int:
        return self.seed
    def get_num_rooms(self) -> int:
        return len(self.vertices)
    def get_max_room_size(self) -> int:
        return self.max_room_size
    
    # Adds additional connections between rooms to create loops and complexity
    def add_cycles(self, num_cycles: int) -> None:
        possible_connections = []
        vertices = self.vertices

        for i in range(len(vertices)):
            vertex1 = vertices[i]
            for j in range(i+1,len(vertices)):
                vertex2 = vertices[j]
                if not directly_connected(self, vertex1, vertex2):
                    distance = manhattan_distance(vertex1, vertex2)
                    # Use a heap to maintain the smallest distances at the top
                    heapq.heappush(possible_connections, (distance, vertex1, vertex2))
        
        for _ in range(num_cycles):
            if possible_connections:
                distance, room1, room2 = heapq.heappop(possible_connections)
                self.mst[room1].append((room2, distance))
            else:
                break  # No more connections to add - you have turned it back into a fully connected graph!


def _create_points(num_points: int, x: int, y: int, max_room_size: int) -> list:
    points = []
    buffer = max_room_size
    for _ in range(num_points):
        points.append((random.randint(0+buffer,x-buffer), random.randint(0+buffer,y-buffer)))
    return points

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Generate a fully connected graph from a list of points
def _generate_graph(points: list) -> dict:
    graph = {}
    for point1 in points:
        graph[point1] = []  # Initialize every point with an empty list
        for point2 in points:
            if point1 != point2:
                distance = manhattan_distance(point1, point2)
                graph[point1].append((point2, distance))
    return graph


# Prim's Algorithm to find the MST - chatGPT
def _prims_algorithm(graph: dict, starting_vertex: tuple) -> dict:
    mst = {starting_vertex: []}  # Initialize the starting vertex with an empty list
    visited = set([starting_vertex])
    edges = [(cost, starting_vertex, to) for to, cost in graph[starting_vertex]]
    
    heapq.heapify(edges)  # Heapify the edges for efficient minimum extraction
    
    while edges:
        cost, frm, to = heapq.heappop(edges)  # Use heapq for efficient minimum edge extraction
        
        if to not in visited:
            visited.add(to)
            if to not in mst:
                mst[to] = []  # Ensure each new vertex is initialized in the MST
            mst[frm].append((to, cost))
            
            for next_to, cost in graph[to]:
                if next_to not in visited:
                    heapq.heappush(edges, (cost, to, next_to))
    
    return mst


def directly_connected(mst: MST, room1: tuple, room2: tuple) -> bool:
    for dest, _ in mst.get_mst()[room1]:
        if dest == room2:
            return True
    for dest, _ in mst.get_mst()[room2]:
        if dest == room1:
            return True
    return False