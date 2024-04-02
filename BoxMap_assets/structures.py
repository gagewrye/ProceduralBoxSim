from BoxMap_assets.Tile import FloorTile, WallTile, Target
import random

"""
Rooms and Hallways
"""
class Room():
    """
    A room of variable size surrounded by walls.

    Contains a single floor tile and multiple surrounding walls
    """
    def __init__(self, vertex: tuple, max_room_size: int, other_rooms: list['Room'], target_offset):
        x, y = vertex
        
        top_Y = y + random.randint(1, max_room_size)
        right_X = x + random.randint(1,max_room_size)
        left_X = x - random.randint(1,max_room_size)
        bottom_Y = y - random.randint(1, max_room_size)

        self.boundaries = (left_X, bottom_Y, right_X, top_Y)
        self.floor = _build_floor(self.boundaries, target_offset)
        self.walls = _build_walls(self.floor, other_rooms)
        
        
    def get_tiles(self) -> list:
        return [self.floor] + self.walls
    def get_floor(self) -> FloorTile:
        return self.floor
    def get_walls(self) -> list[WallTile]:
        return self.walls
    def get_target(self) -> Target:
        return self.floor.get_target()
    def add_target(self, target: Target) -> None:
        curr_targ = self.get_target()
        curr_targ.add_target(target)
    
    def contains(self, x, y) -> bool:
        left_x, bottom_y, right_x, top_y = self.floor.get_boundaries()
        return ((left_x <= x < right_x) and (bottom_y <= y < top_y))
    
def _build_floor(boundaries: tuple, target_offset: float) -> FloorTile:
    left_x, bottom_y, right_x, top_y = boundaries
    return FloorTile(left_x, bottom_y, right_x, top_y, target_offset)

def _build_walls(floor: FloorTile, other_rooms: list[Room]) -> list:
    walls = []
    left_x, bottom_y, right_x, top_y = floor.get_boundaries()

    def _add_wall_segments(constant, range_start, range_end, vertical=False):
        start = None
        for pos in range(range_start, range_end + 1):
            is_blocked = any(room.contains(pos, constant) if vertical else room.contains(constant, pos) for room in other_rooms)

            if not is_blocked:
                if start is None:
                    start = pos
                # Add the segment if this is the last position in range and a start point was marked
                if pos == range_end:
                    if vertical:
                        walls.append(WallTile(constant, start, constant, pos))
                    else:
                        walls.append(WallTile(start, constant, pos, constant))
            else:
                if start is not None:
                    if vertical:
                        walls.append(WallTile(constant, start, constant, pos - 1))
                    else:
                        walls.append(WallTile(start, constant, pos - 1, constant))
                    start = None  # Reset start for the next segment
    
    # Left wall
    _add_wall_segments(left_x, bottom_y, top_y, vertical=True)
    # Top wall
    _add_wall_segments(top_y, left_x, right_x, vertical=False)
    # Right wall
    _add_wall_segments(right_x, bottom_y, top_y, vertical=True)
    # Bottom wall
    _add_wall_segments(bottom_y, left_x, right_x, vertical=False)

    return walls


class Hallway:
    """
    Builds floors along the path between two rooms.
   
    Walls should be built using build_walls after all hallways have been constructed.
    """
    def __init__(self, start: tuple, end: tuple, rooms: list, floor_locations: dict[tuple, FloorTile], target_offset):
        self.vertex1 = start
        self.vertex2 = end
        self.floors = _build_hallway(start, end, rooms, floor_locations, target_offset)
        self.walls = list[WallTile]
        
    def get_hallway(self):
        return self.walls + self.floors
    
    def get_floors(self):
        return self.floors
    
    def get_walls(self):
        return self.walls
    
    def build_walls(self, hallway_floors: list, rooms: list):
        walls_to_add = []
        # TODO: Add wall building logic

        return walls_to_add
    
def _build_hallway(start: tuple, end: tuple, rooms: list[Room],
                   other_floors: dict[tuple, FloorTile], target_offset) -> list[FloorTile]:
    hallway_floors = []

    # Initialize location and hallway direction
    current_x, current_y = start
    end_x, end_y = end
    
    # Adjust step based on direction
    x_step = 1 if end[0] >= start[0] else -1
    y_step = 1 if end[1] >= start[1] else -1

    
    start_room = is_in_any_room(current_x, current_y, rooms)
    start_target = start_room.get_target()

    # navigate to the end of the room
    while current_x <= end_x:
        current_x += x_step
        if not start_room.contains(current_x + x_step, current_y):
            break
            # You have exited the room
    if start_room.contains(current_x, current_y): # still in room
        while current_y != end_y:
            current_y += y_step
            if not start_room.contains(current_x, current_y):
                break
    # add the floor tile and link to the room
    _add_floor_and_targets(current_x, current_y, other_floors,
                            hallway_floors, target_offset, start_target)
    
    while current_x <= end_x:
        # Check room entry
        room = is_in_any_room(current_x, current_y, rooms)
        if room: # Entering room
            # link room to entering hallway
            room.add_target(hallway_floors[-1].get_target())
            hallway_floors[-1].add_target(room.get_target())
            room.add_target(hallway_floors[-1].get_target())
            # traverse through room
            start_target = room.get_target()
            while current_x != end_x:
                current_x += x_step
                if not room.contains(current_x, current_y): # Exiting room
                    break
        # In case you end in a room
        if current_x == end_x: 
            break
        _add_floor_and_targets(current_x, current_y, other_floors,
                                hallway_floors, target_offset, start_target)
        current_x += x_step

    while current_y <= end_y:
        room = is_in_any_room(current_x, current_y, rooms)
        if room:
            # link room to entering hallway
            room.add_target(hallway_floors[-1].get_target())
            hallway_floors[-1].add_target(room.get_target())
            # Traverse through room
            start_target = room.get_target()
            while current_y != end_y:
                current_y += y_step
                if not room.contains(current_x, current_y): # Exiting room
                    break
        if current_y == end_y:
            break
        _add_floor_and_targets(current_x, current_y, other_floors,
                                hallway_floors, target_offset, start_target)
        current_y += y_step

    end_room = is_in_any_room(end_x, end_y, rooms)
    if end_room:
        end_target = end_room.get_target()
        if hallway_floors:
            last_floor = hallway_floors[-1]
            last_floor.add_target(end_target)
            end_room.add_target(last_floor)

    return hallway_floors

def is_in_any_room(x, y, rooms) -> Room:
    for room in rooms:
        if room.contains(x, y):
            return room
    return None

def _add_floor_and_targets(x, y, other_floors: dict[tuple, FloorTile], hallway_floors: list[FloorTile],
                            target_offset, target:Target=None):
    proposed_location = other_floors.get((x,y))
    if proposed_location is None: # empty/no floor
        # build floor
        new_floor = FloorTile(x, y, x+1, y+1, target_offset)
        # link floor
        new_floor.add_target(target)
        target.add_target(new_floor)
        target = new_floor.get_target()
        # Add Floor
        other_floors[(x,y)] = new_floor
        hallway_floors.append(new_floor)
    else: # Already a floor here
        # link floor
        proposed_location.add_target(target)
        target.add_target(proposed_location)
        target = proposed_location.get_target()

def _check_surrounding_for_floors(x, y, all_tiles):
    surrounding_floors = []
    # Define offsets for all eight surrounding positions
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in offsets:
        adj_x, adj_y = x + dx, y + dy
        # Check if there's a floor at each surrounding position
        for tile in all_tiles:
            if isinstance(tile, FloorTile) and tile.x == adj_x and tile.y == adj_y:
                surrounding_floors.append(tile)

    return surrounding_floors
