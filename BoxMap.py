from BoxMap_assets import Hallway, Room, MST, MinimumSpanningTree, FloorTile, WallTile
import matplotlib.pyplot as plt
import matplotlib.patches as patches



class BoxMap():
    """
    Creates a map of rooms and hallways using a graph.
    The building is represented using floor tiles and wall tiles.
    
    The self.floors variable is a dictionary with coordinates mapped to floor tiles.
    Targets can be extracted from the floor tiles. (See FloorTile class in Tile.py)
    """
    def __init__(self, mst: MST, target_offset=0) -> None:
        self.map = mst
        self.floors, self.walls = _build(mst, target_offset)
        
        
    def get_floors(self) -> list[FloorTile]:
        return self.floors
    def get_walls(self) -> list[WallTile]:
        return self.walls
    def get_seed(self) -> int:
        return self.map.get_seed()
    
    def draw_map(self, show: bool = False):
        """
        Draws a matplotlib graph of the tiles to visualize the tile map.
        """
        _, ax = plt.subplots()

        x, y = self.map.map_size
        ax.set_xlim(0, x)
        ax.set_ylim(0, y)

        color_map = {
            "floor": 'grey',
            "wall": 'green',
            "target": 'red',
            "traversed_target": 'green',
            "connection": 'purple'
        }

        # Plot floor tiles
        for tile in self.get_floors():  # Assuming get_floors() returns iterable of floor tiles
            left_x, bottom_y, right_x, top_y = tile.get_boundaries()

            width = right_x - left_x
            height = top_y - bottom_y

            # Corrected to use bottom-left corner for Rectangle
            rect = patches.Rectangle((left_x, bottom_y), width, height, linewidth=0.2, edgecolor='none', facecolor=color_map["floor"])
            ax.add_patch(rect)

            # Add target
            target = tile.get_target()
            target_X, target_Y = target.get_coordinates()
            target_color = "target" if target.get_times_traversed() == 0 else 'traversed_target'
            target_patch = patches.Circle((target_X, target_Y), 0.1, color=color_map[target_color])
            ax.add_patch(target_patch)
            
            # Draw connections to other targets
            for connected_target in target.get_adjacent_targets():
                x, y = connected_target.get_coordinates()
                plt.plot([target_X, x], [target_Y, y], color=color_map["connection"], linewidth=0.5)


        # Plot wall tiles
        for tile in self.get_walls():
            left_x, bottom_y, right_x, top_y = tile.get_boundaries()

            width = right_x - left_x
            height = top_y - bottom_y

            # Corrected to use bottom-left corner for Rectangle
            rect = patches.Rectangle((left_x, bottom_y), width, height, linewidth=1, edgecolor='black', facecolor=color_map["wall"])
            ax.add_patch(rect)

        if show:
            plt.show()

def _hallway_blueprint(mst: MST) -> list:
    # save the hallway as a list of point pairs
    hallways = []
    # Get Room Centers
    vertices = mst.get_vertices()
    n = len(vertices)

    for i in range(n):
        vertex1 = vertices[i]
        for j in range(i+1,n):
            vertex2 = vertices[j]
            if MinimumSpanningTree.directly_connected(mst, vertex1, vertex2):
                room1 = vertex1
                room2 = vertex2
                # build hallway between those points
                hallways.append((room1, room2))
    return hallways

def _construct_rooms(planned_rooms: list, max_size: int, target_offset) -> list[Room]:
    # list of rooms, passed into Room class to avoid collisions and overwriting
    rooms = []
    for room in planned_rooms:
        addition = Room(room, max_size, rooms, target_offset)
        rooms.append(addition)
    return rooms

def _construct_hallways(planned_hallways: list[tuple], rooms, target_offset) -> tuple:
    walls = []
    hallways = []
    floors = []
    floor_locations: dict[tuple, FloorTile] = {}
    wall_locations: dict[tuple, WallTile] = {}
    # Build Hallway floors
    for start, end in planned_hallways:
        hallway = Hallway(start, end, rooms, floor_locations, wall_locations, target_offset)
        hallways.append(hallway)
        floors.extend(hallway.get_floors())
        walls.extend(hallway.get_walls())
    # Build hallway walls
    for hallway in hallways:
        hallway.build_walls(hallways, rooms, floors) # TODO: finish function
        # walls.append(hallway.get_walls())
    return floors, walls

def _build(mst: MST, target_offset) -> tuple:
    """
    Returns: a list of rooms and hallways
    """
    floors = []
    walls = []
    
    # Create blueprint
    planned_rooms = mst.get_vertices()
    planned_hallways = _hallway_blueprint(mst)

    # place rooms
    rooms = _construct_rooms(planned_rooms, mst.get_max_room_size(), target_offset)
    # connect rooms
    hallway_floors, hallway_walls = _construct_hallways(planned_hallways, rooms, target_offset)

    # separate floors and walls
    for room in rooms:
        floors.append(room.get_floor())
        walls += room.get_walls()
    floors += hallway_floors
    walls += hallway_walls
    
    return floors, walls
