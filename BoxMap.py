from structures import Hallway, Room
from MinimumSpanningTree import MST
from Tile import FloorTile, WallTile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import MinimumSpanningTree
import random


class BoxMap():
    """
    Creates a map of rooms and hallways using a graph.
    The building is represented using floor tiles and wall tiles.
    Targets can be extracted from the floor tiles. (See FloorTile class in Tile.py)
    """
    def __init__(self, mst: MST, rand: random, target_offset=0) -> None:
        self.map = mst
        self.floors, self.walls = _build(mst, target_offset, rand)
        self.targets = {}
    
    def get_tiles(self) -> list:
        return self.floors + self.walls
    def get_floors(self) -> list[FloorTile]:
        return self.floors
    def get_walls(self) -> list[WallTile]:
        return self.walls
    def get_seed(self) -> int:
        return self.map.get_seed()
    
    def draw_map(self):
        """
        Draws a matplot graph of the tiles to visualize the tile map
        """
        _ , ax = plt.subplots()

        x,y =self.map.map_size
        ax.set_xlim(0, x)
        ax.set_ylim(0, y)

        color_map = {"floor" : 'grey',
                    "wall" : 'blue',
                    "target": 'red',
                    "traversed_target": 'green'}

        for tile in self.get_tiles():
            left_x , bottom_y, right_x, top_y = tile.get_boundaries()
            tile_type = tile.get_type()

            width = right_x - left_x
            height = top_y - bottom_y

            # Create a rectangle patch for each tile
            center = (right_x - (width/2), top_y - (height/2))
            rect = patches.Rectangle(center, width, height, linewidth=1, edgecolor='black', facecolor=color_map.get(tile_type, "grey"))
            
            if tile_type == "floor": # add target
                target_X, target_Y = tile.get_target()
                target_color = "target" if tile.get_times_traversed() == 0 else 'traversed_target'
                target = patches.Circle((target_X,target_Y), 0.1, color=color_map.get(target_color))
                ax.add_patch(target)
            
            ax.add_patch(rect)

    plt.show()

def _hallway_blueprint(mst: MST) -> list:
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

def _construct_rooms(rooms: list, max_size: int, target_offset, rand: random) -> list[Room]:
    # list of rooms, passed into Room class to avoid collisions and overwriting
    rooms = list[Room]
    for room in rooms:
        addition = Room(room, max_size, rooms, target_offset, rand)
        rooms.append(addition)
    return rooms

def _construct_hallways(planned_hallways: list[tuple], rooms, target_offset, rand) -> list[Hallway]:
    other_floors = list[FloorTile]
    walls = list[WallTile]
    hallways = list[Hallway]
    # Build Hallway floors
    for start, end in planned_hallways:
        hallway = Hallway(start, end, rooms, other_floors, target_offset, rand)
        other_floors += hallway.get_floors()
        hallways.append(hallway)
    # Build hallway walls
    for hallway in hallways:
        hallway.build_walls(hallways, rooms) # TODO: finish function
        walls.append(hallway.get_walls())
    return other_floors, walls

def _build(mst: MST, target_offset, rand: random) -> tuple:
    """
    Returns: a list of rooms and hallways
    """
    floors = list[FloorTile]
    walls = list[WallTile]
    
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
