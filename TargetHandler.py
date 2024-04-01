import Tile

class TargetHandler():
    """
    This is the interface for interacting with the map using target coordinates.
    
    Maps coordinates to corresponding Target objects
    """
    def __init__(self) -> None:
        self.targets : dict[tuple, Tile.Target] = {}
    
    
    def find_new_target(self, current_coordinates: tuple) -> tuple:
        """
        Gets the coordinates of the target that has been traversed the least.

        TODO: Maybe randomize which target is picked if multiple are 0?
        """
        current_target = self.targets.get(current_coordinates)
        lowest = 100
        next_target = None
        for adjacent_target in current_target.get_adjacent_targets():
            times_traversed = adjacent_target.get_times_traversed()
            if times_traversed <= lowest:
                next_target = adjacent_target
                lowest = times_traversed
        return next_target.get_coordinates()
    
    def get_starting_coordinate(self) -> tuple:
        """
        Get a coordinate from the targets to begin navigation
        """
        coordinate, target = next(iter(self.targets.items()))
        return coordinate
    
    def get_current_target(self, current_coordinates: tuple) -> Tile.Target:
        return self.targets.get(current_coordinates)

    def get_adjacent_targets(self, coordinates: tuple) -> set[Tile.Target]:
        """
        Returns a list of Target Objects that can be traveled to from this target
        """
        target = self.targets.get(coordinates)
        return target.get_adjacent_targets()
    
    def add_targets_from_tiles(self, tiles: list[Tile.FloorTile]) -> None:
        for tile in tiles:
            target = tile.get_target()
            self.targets[target.get_coordinates()] = target

    def _add_target(self, target: Tile.Target) -> None:
        """
        Adds a single target
        """
        self.targets[target.get_coordinates()] = target
    
    def traverse_target(self, target_coordinates: tuple) -> None:
        """
        Adds 1 to time_traversed
        """
        self.targets.get(target_coordinates).traverse()

    def reset_targets(self):
        """
        Set times traversed to 0 for all targets
        """
        for _ , target in self.targets.items():
            target.reset()
    
    def is_fully_traveresed(self) -> bool:
        """
        Check if all targets have been traversed
        """
        for _, target in self.targets.items():
            if target.get_times_traversed() == 0:
                return False
        return True
    