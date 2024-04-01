import random

# Note: tiles are built using the vertex as the bottom left corner
class Tile():
    """
    Base tile Class
    """
    def __init__(self, left_X, bottom_Y, right_X, top_Y):
        self._right_X_boundary = right_X
        self._top_Y_boundary = top_Y
        self._left_X_boundary = left_X
        self._bottom_Y_boundary = bottom_Y
        self._tile_type = "tile"
    
    def get_boundaries(self) -> tuple:
        return self._left_X_boundary, self._bottom_Y_boundary, self._right_X_boundary, self._top_Y_boundary

    def get_type(self) -> str:
        return self._tile_type
    def set_type(self, type: str):
        self._tile_type = type

class WallTile(Tile):
    """
    It's a wall...
    """
    def __init__(self, X, Y, neg_X, neg_Y):
        super().__init__(X, Y, neg_X, neg_Y)
        self._tile_type = "wall"

class FloorTile(Tile):
    """
    Floor with a target somewhere around the center, depending on how high target_offset is.
    """
    def __init__(self, left_X_boundary, bottom_Y_boundary, right_X_boundary, top_Y_boundary, target_offset=0, rand:random=None):
        super().__init__(left_X_boundary, bottom_Y_boundary, right_X_boundary, top_Y_boundary)
        # default target is in the center
        target_X = right_X_boundary - ((right_X_boundary - left_X_boundary)/2)
        target_Y = top_Y_boundary - ((top_Y_boundary - bottom_Y_boundary)/2)

        if target_offset != 0:
            target_X += rand.random(-target_offset, target_offset)
            target_Y += rand.random(-target_offset, target_offset)
        
        self.target = Target(target_X, target_Y)
        self._tile_type = "floor"
    
    def get_target(self) -> 'Target':
        return self.target

class Target():
    """
    Target object for navigating. 

    It stores the coordinates of the target, nearby Target objects, and the number of times the target has been traversed.
    """
    def __init__(self, x, y):
        self._coordinates = (x,y)
        self._times_traversed = 0
        self._adjacent_targets = set()
    
    def get_times_traversed(self) -> int:
        return self._times_traversed
    def get_coordinates(self) -> tuple:
        return self._coordinates
    def get_adjacent_targets(self) -> set['Target']:
        """
        Returns a list of targets that can be traveled to from this target
        """
        return self._adjacent_targets
    def add_target(self, target: 'Target'):
        """
        Add a target to this targets's list of adjacent targets
        """
        self._adjacent_targets.add(target)
    def remove_target(self, target: 'Target'):
        """
        Remove a target from this target's list of adjacent targets
        """
        self._adjacent_targets.remove(target)
    def traverse(self):
        self._times_traversed += 1
    def reset(self):
        """
        Sets times_traveresed back to 0
        """
        self._times_traversed = 0

