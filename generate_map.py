from argparse import ArgumentParser, Namespace
import random
import MinimumSpanningTree
import ConstructMap
import Tile

def parse_args() -> Namespace:
    arg_parser = ArgumentParser("Train command classification networks.")

    arg_parser.add_argument("num_rooms", help="Number of rooms on map")
    arg_parser.add_argument("--room_seed", default=47, help="Determines what the map looks like")
    arg_parser.add_argument("--map_size_x", default=1920, help="X-axis size")
    arg_parser.add_argument("--map_size_y", default=1080, help="Y-axis size")
    arg_parser.add_argument("--max_room_size", default=10, help="How large the rooms can be") 
    arg_parser.add_argument("--target_offset", default=0, help="Offsets the targets from the center."
                             "Higher numbers can be further away. Keep below floor size / 2") 
    
    arg_parser.add_argument("--num_cycles",
                            default=2,
                            help="cycles will add complexity and loops to the map, creating more challenging exploration")
    return arg_parser.parse_args()



def __main__():
    args = parse_args()
    rand = random.seed(args.room_seed)
    mst = MinimumSpanningTree.MST(args.num_rooms, args.map_size_x, args.map_size_y, args.max_room_size, args.room_seed, rand)
    mst.add_cycles(args.num_cycles)
    map = ConstructMap.BoxMap(mst, rand, args.target_offset) # Build Rooms and Hallways
    # TODO: Save map somewhere
    tiles = map.get_tiles()
    Tile.draw_map(tiles, args.map_size_x, args.map_size_y)

if __name__ == "__main__":
    main()