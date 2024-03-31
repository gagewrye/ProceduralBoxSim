import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# Note: tiles are built using the vertex as the bottom left corner
class Tile():
    """
    Base tile Class
    """
    def __init__(self, left_X, bottom_Y, right_X, top_Y):
        self.right_X_boundary = right_X
        self.top_Y_boundary = top_Y
        self.left_X_boundary = left_X
        self.bottom_Y_boundary = bottom_Y
        self.tile_type = "tile"
    
    def get_boundaries(self):
        # X > neg_X, Y > neg_Y
        return self.left_X_boundary, self.bottom_Y_boundary, self.right_X_boundary, self.top_Y_boundary

    def get_type(self):
        return self.tile_type

class WallTile(Tile):
    """
    It's a wall...
    """
    def __init__(self, X, Y, neg_X, neg_Y):
        super().__init__(X, Y, neg_X, neg_Y)
        self.tile_type = "wall"

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
        self.tile_type = "floor"
    
    def get_target(self) -> 'Target':
        return self.target
    def get_adjacent_targets(self) -> set[tuple]:
        return self.target.get_adjacent_targets()
    def get_times_traversed(self) -> int:
        return self.target.times_traversed()
    def add_adjacent_target(self,target):
        self.target.add_target(target)
    def remove_adjacent_target(self,target):
        self.target.remove_target(target)
    def traverse(self):
        self.target.traverse()

class Target():
    """
    Target object for navigating. 

    It stores the coordinates of the target, nearby Target objects, and the number of times the target has been traversed.
    """
    def __init__(self, x, y):
        self.coordinates = (x,y)
        self.times_traversed = 0
        self.adjacent_targets = set()
    
    def get_adjacent_targets(self) -> set['Target']:
        return self.adjacent_targets
    def add_target(self, target: 'Target'):
        self.adjacent_targets.add(target)
    def remove_target(self, target: 'Target'):
        self.adjacent_targets.remove(target)
    def traverse(self):
        self.times_traversed += 1
    def times_traversed(self) -> int:
        return self.times_traversed
    def reset(self):
        self.times_traversed = 0

def draw_map(tiles, x, y):
    _ , ax = plt.subplots()

    ax.set_xlim(0, x)
    ax.set_ylim(0, y)

    color_map = {"floor" : 'grey',
                "wall" : 'blue',
                "target": 'red',
                "traversed_target": 'green'}

    for tile in tiles:
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

    # hide axis
    plt.axis('off')
    plt.show()

