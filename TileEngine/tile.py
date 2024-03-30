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

class WallTile(Tile):
    def __init__(self, X, Y, neg_X, neg_Y):
        super().__init__(X, Y, neg_X, neg_Y)
        self.tile_type = "wall"

class FloorTile(Tile):
    def __init__(self, target_X, target_Y, X_boundary, Y_boundary, neg_X_boundary, neg_Y_boundary):
        super().__init__(X_boundary, Y_boundary, neg_X_boundary, neg_Y_boundary)
        self.target_X = target_X
        self.target_Y = target_Y
        self.adjacent_targets = set()
        self.tile_type = "floor"
        self.times_traversed = 0
    
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