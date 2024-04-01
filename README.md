# ProceduralBoxSim

## Overview:

1. Define the size of the 2d plane
2. Place random points on the plane
3. Connect every point to every other point to create a fully connected graph. Calculate the manhattan distance between each room to use for the weights edges
4. Use Prim's Algorithm to find the minimum spanning tree. This tree will be what we base the map on
5. At each point in our tree, create a randomly sized room.
6. For every edge, build a hallway that connects a room to the room at the other end.
7. Convert this map to unreal engine environment

## Data Structures:
Done: Map interface

Done: tiles

Done: Minimum Spanning Tree

Done: Rooms and Hallways



## Algorithms:

1. Hallway generator to connect a room to another room. It builds only in the x/-x and y/-y directions to simplify the process. build_walls, a function to build walls around a hallway, needs to be finished. We should probable edit the build_hallway method to include more complex construction, since it just builds in the horizontal direction and then in the vertical direction.

Done: Room generator, input a point and build a randomly sized room around it using a floor tile and wall tiles.

Done: Prim's

Done: Point placer and graph generator

## Main generation function:
Inputs: map size (X x Y), number of rooms, minimum room size, maximum room size, seed for random function (int)

Output: Map size, tile objects, TargetHandler




The result should be mostly compatible with boxnav, hopefully
