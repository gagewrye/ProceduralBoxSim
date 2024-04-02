# ProceduralBoxSim


## TODO:


- The map generates the rooms well, some rooms are built inside of other rooms though. Possible fixes:
1. Generate walls after building the room and hallway floors. This would give the hallways and entrance to the rooms too, getting two birds stoned at once. Remove the _build_hallways() method from Room Class and place it outside as a separate callable method.
2. Check if the center of every room is inside another room and delete that room. We could probably do this in addition to #1


- The hallways usually work, but they get confused by the nested rooms. Hallway wall building function needs to be made too.


- Find a way to integrate into BoxNav

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

Output: BoxMap pkl, TargetHandler pkl, map visualization image - These are saved in a folder title with the seed number
