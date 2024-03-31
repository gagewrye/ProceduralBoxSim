import random
import MinimumSpanningTree
import structures
import Tile

class BoxMap():
    """
    Creates a map of rooms and hallways using a graph.
    The building is represented using floor tiles and wall tiles.
    Targets can be extracted from the floor tiles. (See FloorTile class in Tile.py)
    """
    def __init__(self, mst: MinimumSpanningTree.MST, rand: random, target_offset=0) -> None:
        self.seed = mst.get_seed()
        self.map = mst
        self.floors, self.walls = _build(mst, target_offset, rand)
        self.targets = {}
    
    def get_tiles(self) -> list[Tile.Tile]:
        return self.floors + self.walls
    def get_floors(self) -> list[Tile.FloorTile]:
        return self.floors
    def get_walls(self) -> list[Tile.WallTile]:
        return self.walls

def _hallway_blueprint(mst: MinimumSpanningTree.MST) -> list:
    # save the hallway as a list of point pairs
    hallways = []
    vertices = mst.get_vertices()
    n = len(vertices)

    for i in range(n):
        vertex1 = vertices[i]
        for j in range(i+1,n):
            vertex2 = vertices[j]
            if MinimumSpanningTree.directly_connected(mst, vertex1, vertex2):
                room1 = vertex1[0]
                room2 = vertex2[0]
                # build hallway between those points
                hallways.append((room1, room2))
    return hallways

def _construct_rooms(rooms: list, max_size: int, target_offset, rand: random) -> list[structures.Room]:
    # list of rooms, passed into Room class to avoid collisions and overwriting
    rooms = list[structures.Room]
    for room in rooms:
        addition = structures.Room(room, max_size, rooms, target_offset, rand)
        rooms.append(addition)
    return rooms

def _construct_hallways(planned_hallways: list[tuple], rooms, target_offset, rand) -> list[structures.Hallway]:
    other_floors = list[Tile.FloorTile]
    walls = list[Tile.WallTile]
    hallways = list[structures.Hallway]
    # Build Hallway floors
    for start, end in planned_hallways:
        hallway = structures.Hallway(start, end, rooms, other_floors, target_offset, rand)
        other_floors += hallway.get_floors()
        hallways.append(hallway)
    # Build hallway walls
    for hallway in hallways:
        hallway.build_walls(hallways, rooms) # TODO: finish function
        walls.append(hallway.get_walls())
    return other_floors, walls

def _build(mst: MinimumSpanningTree.MST, target_offset, rand: random) -> tuple:
    """
    Returns: a list of rooms and hallways
    """
    floors = list[Tile.FloorTile]
    walls = list[Tile.WallTile]
    # Create blueprint
    planned_rooms = mst.get_vertices
    planned_hallways = _hallway_blueprint(mst)

    # place rooms
    rooms = _construct_rooms(planned_rooms, mst.get_max_room_size(), target_offset, rand)
    # connect rooms
    hallway_floors, hallway_walls = _construct_hallways(planned_hallways, rooms, target_offset, rand)

    # separate floors and walls
    for room in rooms:
        floors.append(room.get_floor())
        walls += room.get_walls()
    floors += hallway_floors
    walls += hallway_walls
    
    return floors, walls
