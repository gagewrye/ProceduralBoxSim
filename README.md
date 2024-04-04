# ProceduralBoxSim

This project is intended to randomly generate maps of varying size and complexity for training an agent to explore a simulated environment. The intended path of travel can be set to create a 'wandering' effect by increasing the target offset - this will place the targets away from the center of the floor tiles.

Running generate_map.py will create a map visual with floors, walls, target, and target connections. It will also create a map object and a target handler interface that allows you to traverse the map and track where you have traversed.

## TODO:


- The map generates the rooms well, some rooms are built inside of other rooms though. Possible fixes:
1. Generate walls after building the room and hallway floors. This would give the hallways an entrance to the rooms too, getting two birds stoned at once. Remove the _build_hallways() method from Room Class and place it outside as a separate callable method.
2. Check if the center of every room is inside another room and delete that room. We could probably do this in addition to #1

- The hallways usually work, but they sometimes build walls blocking other hallways. The also dont fully connect with the rooms. Maybe setting the room contains check to a smaller area will fix it.

- Find a way to integrate into BoxNav

- Test ue_map_generator
  
## Overview:
1. Define the size of the 2d plane
2. Place random points on the plane
3. Connect every point to every other point to create a fully connected graph. Calculate the manhattan distance between each room to use for the weights edges
4. Use Prim's Algorithm to find the minimum spanning tree. This tree will be what we base the map on
5. At each point in our tree, create a randomly sized room.
6. For every edge, build a hallway that connects a room to the room at the other end.
7. Convert this map to unreal engine environment


## generate_map.py:
Inputs: map size (X x Y), number of rooms, minimum room size, maximum room size, seed for random function (int)

Output: BoxMap pkl, TargetHandler pkl, map image and Unreal Engine map - These are saved in a folder titled with the seed number
