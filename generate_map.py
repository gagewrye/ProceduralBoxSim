from ue_map_generator import ue_map_generator
from argparse import ArgumentParser, Namespace
from TargetHandler import TargetHandler
from BoxMap import BoxMap
from BoxMap_assets import MST
import matplotlib.pyplot as plt
import random
import pickle
import os


def parse_args() -> Namespace:
    arg_parser = ArgumentParser(description="Train command classification networks.")

    arg_parser.add_argument("--num_rooms", type=int, default=4, help="Number of rooms on map")
    arg_parser.add_argument("--room_seed", type=int, default=47, help="Determines what the map looks like")
    arg_parser.add_argument("--map_size_x", type=int, default=100, help="X-axis size")
    arg_parser.add_argument("--map_size_y", type=int, default=100, help="Y-axis size")
    arg_parser.add_argument("--max_room_size", type=int, default=10, help="How large the rooms can be")
    arg_parser.add_argument("--target_offset", type=int, default=0, help="Offsets the targets from the center. Higher numbers can be further away. Keep below floor size / 2")
    arg_parser.add_argument("--num_cycles", type=int, default=2, help="Cycles will add complexity and loops to the map, creating more challenging exploration")
    arg_parser.add_argument("--ue_scaling_factor", type=int, default=100, help="Scales the tiles up for Unreal Engine map")
    
    return arg_parser.parse_args()



def main():
    args = parse_args()
    random.seed(args.room_seed)

    # Create Minimum Spanning Tree and add cycles to it
    mst = MST(args.num_rooms, args.map_size_x, args.map_size_y, args.max_room_size, args.room_seed)
    mst.add_cycles(args.num_cycles)
    
    # Build Rooms and Hallways
    map = BoxMap(mst, args.target_offset)
    floors = map.get_floors()
    
    # Create Interface
    target_handler = TargetHandler()
    target_handler.add_targets_from_tiles(floors)
    
    # build unreal engine map
    ue_map = ue_map_generator(map, args.ue_scaling_factor)

    # Create a directory named after the seed
    directory_name = f"./{args.room_seed}"
    os.makedirs(directory_name, exist_ok=True)

    # visualize and save image
    map.draw_map(show=False)
    plt.savefig(os.path.join(directory_name, "map_visualization.png"))
    plt.close()  

    # Save BoxNav map, target handler, and Unreal Engine map as pickle files
    print("Saving to {directory_name}")
    with open(os.path.join(directory_name, "BoxNav_map.pkl"), 'wb') as map_file:
        pickle.dump(map, map_file)
    with open(os.path.join(directory_name, "target_handler.pkl"), 'wb') as target_file:
        pickle.dump(target_handler, target_file)
    with open(os.path.join(directory_name, "ue_map.pkl"), 'wb') as ue_map_file:
        pickle.dump(ue_map, ue_map_file)


if __name__ == '__main__':
    main()