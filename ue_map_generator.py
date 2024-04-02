from BoxMap import BoxMap
import unreal

# Note: UE units are in cm
"""
Makes an Unreal Engine map by converting floor and wall assets into
boxes
"""
def ue_map_generator(map: BoxMap, scale_factor: int):

    ue_objects = []
    
    floors = map.get_floors()
    walls = map.get_walls()
    
    wall_height = 100
    floor_height = 1

    for floor in floors:
        boundaries = floor.get_boundaries()
        scaled_boundaries = tuple(x * scale_factor for x in boundaries)
        
        left_x, bottom_y, right_x, top_y = scaled_boundaries
        width = right_x - top_y
        length = top_y - bottom_y
        
        location = unreal.Vector(left_x, bottom_y, 0) # bottom left corner
        rotation = unreal.Rotator(0, 0, 0)  # rotate if needed
        scale = unreal.Vector(width, length, floor_height)

        # Create a box brush (for simplicity, might use Static Meshes for more complexity)
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Brush, location, rotation)
        actor.set_actor_scale3d(scale)
        ue_objects.append(actor)
    
    # same as floors
    for wall in walls:

        boundaries = wall.get_boundaries()
        scaled_boundaries = tuple(x * scale_factor for x in boundaries)
        
        left_x, bottom_y, right_x, top_y = scaled_boundaries
        width = right_x - top_y
        length = top_y - bottom_y

        location = unreal.Vector(left_x, bottom_y, 0)
        rotation = unreal.Rotator(0, 0, 0)
        scale = unreal.Vector(width, length, wall_height)

        # Create a box brush
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Brush, location, rotation)
        actor.set_actor_scale3d(scale)
        ue_objects.append(actor)
    
    return ue_objects