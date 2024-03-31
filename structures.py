import Tile
import random
import partial

class Room():
    def __init__(self, vertex: tuple, max_room_size: int, other_rooms: list['Room'], target_offset, rand: random):
        x, y = vertex
        
        top_Y = y + rand.randint(0, max_room_size)
        right_X = x + rand.randint(0,max_room_size)
        left_X = x - rand.randint(0,max_room_size)
        bottom_Y = y - rand.randint(0, max_room_size)

        self.center = ((right_X - left_X) , (top_Y - bottom_Y))
        self.boundaries = (left_X, bottom_Y, right_X, top_Y)
        self.floor = _build_floor(self.boundaries, target_offset, rand)
        self.walls = _build_walls(self.floor, other_rooms)
        
        
    def get_tiles(self) -> list:
        tiles = []
        tiles.append(self.floor)
        tiles.extend(self.walls)
        return tiles
    def get_floor(self) -> Tile.FloorTile:
        return self.floor
    def get_walls(self) -> list[Tile.WallTile]:
        return self.walls
    def get_target(self) -> Tile.Target:
        return self.floor.get_target()
    def add_target(self, target: Tile.Target) -> None:
        self.floor.add_adjacent_target(target)
    
    def contains(self, x, y) -> bool:
        left_x, bottom_y, right_x, top_y = self.floor.get_boundaries()
        return ((left_x - 1 <= x < right_x) and (bottom_y - 1 <= y < top_y))
    
def _build_floor(boundaries: tuple, target_offset: float, rand: random) -> Tile.FloorTile:
    left_x, bottom_y, right_x, top_y = boundaries
    return Tile.FloorTile(left_x, bottom_y, right_x, top_y, target_offset, rand)

def _build_walls(floor: Tile.FloorTile, other_rooms) -> list:
    walls = []
    left_x, bottom_y, right_x, top_y = floor.get_boundaries()

    # add a wall, segmenting in case of interruptions
    def _add_wall_segments(constant, range_start, range_end, vertical=False):
        start = None
        for pos in range(range_start, range_end + 1):
            if vertical:
                is_blocked = any(room.contains(constant, pos) for room in other_rooms)
            else:
                is_blocked = any(room.contains(pos, constant) for room in other_rooms)
            
            if not is_blocked and start is None:
                start = pos
            elif is_blocked and start is not None:
                if vertical:
                    walls.append(Tile.FloorTile.WallTile(constant, start, constant, pos - 1))
                else:
                    walls.append(Tile.FloorTile.WallTile(start, constant, pos - 1, constant))
                start = None
            elif not is_blocked and pos == range_end:
                if vertical:
                    walls.append(Tile.FloorTile.WallTile(constant, start, constant, pos))
                else:
                    walls.append(Tile.FloorTile.WallTile(start, constant, pos, constant))
        
    # Add wall segments around the perimeter
    _add_wall_segments(left_x - 1, bottom_y, top_y, vertical=True)  # Left
    _add_wall_segments(top_y, left_x, right_x)  # Top
    _add_wall_segments(right_x, top_y, bottom_y, vertical=True)  # Right
    _add_wall_segments(bottom_y - 1, right_x, left_x)  # Bottom

    return walls

class Hallway:
    """
    Builds floors along the path between two rooms.
   
    Walls should be built using build_walls after all hallways have been constructed.
    """
    def __init__(self, start: tuple, end: tuple, rooms: list, other_floors: list):
        self.vertex1 = start
        self.vertex2 = end
        self.floors = _build_hallway(start, end, rooms, other_floors)
        self.walls = list[Tile.WallTile]
        
    def get_hallway(self):
        return self.walls + self.floors
    
    def get_floors(self):
        return self.floors
    
    def get_walls(self):
        return self.walls
    
    def build_walls(self, hallway_floors: list, rooms: list):
        walls_to_add = []
        # TODO: Add wall building logic

        self.walls += walls_to_add
    
def _build_hallway(start: tuple, end: tuple, rooms: list[Room],
                   other_floors: list[Tile.FloorTile], target_offset,
                    rand) -> list[Tile.FloorTile]:
    _add_floor = partial(_add_floor_and_targets, target_offset=target_offset, rand=rand)
    hallway_floors = []
    start_x, start_y = start
    end_x, end_y = end
    x_step, y_step = 1
    if end_x < start_x:
        x_step = -1
    if end_y < start_y:
        y_step = -1

    current_x, current_y = start_x, start_y
    start_room = is_in_any_room(current_x, current_y, rooms)
    start_target = start_room.get_target()

    # navigate to the end of the room
    while current_x != end_x:
        current_x += x_step
        if not room.contains(current_x, current_y):
            break
            # You have exited the room
    if room.contains(current_x, current_y): # still in room
        while current_y != end_y:
            current_y += y_step
            if not room.contains(current_x, current_y):
                break
                
    # Horizontal placement
    while current_x != end_x:
        # Check room entry
        room = is_in_any_room(current_x, current_y, rooms)
        if room: # Entering room
            # link room to entering hallway
            room.add_target(hallway_floors[-1].get_target())
            hallway_floors[-1].add_adjacent_target(room.get_target())
            # traverse through room
            start_target = room.get_target()
            while current_x != end_x:
                current_x += x_step
                if not room.contains(current_x, current_y): # Exiting room
                    break
        _add_floor(current_x, current_y, other_floors, hallway_floors, start_target)
        start_target = None  # Only link the first tile after exiting a room
        current_x += x_step

    # Reset for vertical placement
    start_target = room.get_target() if is_in_any_room(current_x, current_y, rooms) else None

    while current_y != end_y:
        room = is_in_any_room(current_x, current_y, rooms)
        if room:
            # link room to entering hallway
            room.add_target(hallway_floors[-1].get_target())
            hallway_floors[-1].add_adjacent_target(room.get_target())
            # Traverse through room
            start_target = room.get_target()
            while current_y != end_y:
                current_y += y_step
                if not room.contains(current_x, current_y): # Exiting room
                    break
        _add_floor(current_x, current_y, other_floors, hallway_floors, start_target)
        start_target = None  # Reset after linking
        current_y += y_step

    end_room = is_in_any_room(end_x, end_y, rooms)
    if end_room:
        end_target = end_room.get_target()
        if hallway_floors:
            last_floor = hallway_floors[-1]
            last_floor.add_adjacent_target(end_target)
            end_room.add_adjacent_target(last_floor)
    
    def is_in_any_room(x, y, rooms) -> Room:
        for room in rooms:
            if room.contains(x, y):
                return room
        return None

    def _add_floor_and_targets(x, y, other_floors: list[Tile.FloorTile], hallway_floors, target_offset, rand, target=None):
        if not any(floor.X_boundary == x and floor.Y_boundary == y for floor in other_floors):
            new_floor = Tile.FloorTile(x, y, x+1, y+1, target_offset, rand)
            if target:
                # Link the floor tile with the room's target
                new_floor.add_adjacent_target(target)
                # Assuming the room has a method to add targets as well, you might need to adjust this
                target.add_adjacent_target(new_floor)
            for floor in _check_surrounding_for_floors(x, y, other_floors):
                new_floor.add_adjacent_target(floor)
                floor.add_adjacent_target(new_floor)
            hallway_floors.append(new_floor)

    return hallway_floors

def _check_surrounding_for_floors(x, y, all_tiles):
    surrounding_floors = []
    # Define offsets for all eight surrounding positions
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in offsets:
        adj_x, adj_y = x + dx, y + dy
        # Check if there's a floor at each surrounding position
        for tile in all_tiles:
            if isinstance(tile, Tile.FloorTile) and tile.x == adj_x and tile.y == adj_y:
                surrounding_floors.append(tile)

    return surrounding_floors
