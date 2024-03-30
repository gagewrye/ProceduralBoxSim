import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Tile():
    def __init__(self, X, Y, neg_X, neg_Y):
        self.X_boundary = X
        self.Y_boundary = Y
        self.neg_X_boundary = neg_X
        self.neg_Y_boundary = neg_Y
        self.tile_type = "tile"
    
    def get_boundaries(self):
        return self.X_boundary, self.Y_boundary, self.neg_X_boundary, self.neg_Y_boundary

    def get_type(self):
        return self.tile_type
    
    def collides(self, tile: 'Tile') -> bool:
        other_x, other_y, other_neg_x, other_neg_y = tile.get_boundaries()
        this_x, this_y, this_neg_x, this_neg_y = self.get_boundaries()

        # Check if one rectangle is to the left of the other
        if this_x >= other_neg_x or other_x >= this_neg_x:
            return False

        # Check if one rectangle is above the other
        if this_y <= other_neg_y or other_y <= this_neg_y:
            return False

        # If neither of the above, the rectangles are colliding
        return True

class WallTile(Tile):
    def __init__(self, X, Y, neg_X, neg_Y):
        super().__init__(X, Y, neg_X, neg_Y)
        self.tile_type = "wall"

class FloorTile(Tile):
    def __init__(self, X_boundary, Y_boundary, neg_X_boundary, neg_Y_boundary):
        super().__init__(X_boundary, Y_boundary, neg_X_boundary, neg_Y_boundary)
        # default target is in the center
        self.target_X = X_boundary - ((X_boundary - neg_X_boundary)/2)
        self.target_Y = Y_boundary - ((Y_boundary - neg_Y_boundary)/2)
        
        self.adjacent_targets = set()
        self.tile_type = "floor"
        self.times_traversed = 0
    
    def set_target(self, target_x, target_y):
        self.target_X = target_x
        self.target_Y = target_y
    def get_target(self):
        return self.target_X, self.target_Y
    def get_adjacent_targets(self):
        return self.adjacent_targets
    def get_times_traversed(self):
        return self.times_traversed
    def add_adjacent_target(self,target):
        self.adjacent_targets.add(target)
    def remove_adjacent_target(self,target):
        self.adjacent_targets.remove(target)
    def traverse(self):
        self.times_traversed += 1

def draw_map(tiles, x, y):
    _ , ax = plt.subplots()

    ax.set_xlim(0, x)
    ax.set_ylim(0, y)

    color_map = {"floor" : 'green',
                "wall" : 'blue'}

    for tile in tiles:
        x , y, neg_x, neg_y = tile.get_boundaries()
        tile_type = tile.get_type()

        width = x - neg_x
        height = y - neg_y

        x = x - (width / 2)
        y = y - (height / 2)
        # Create a rectangle patch for each tile
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor=color_map.get(tile_type, "grey"))
        
        if tile_type == "floor": # add target
            target_X, target_Y = tile.get_target()
            target_color = 'red' if tile.get_times_traversed() == 0 else 'green'
            target = patches.Circle((target_X,target_Y), 0.1, color=target_color)
            ax.add_patch(target)
        
        ax.add_patch(rect)

    # hide axis
    plt.axis('off')
    plt.show()