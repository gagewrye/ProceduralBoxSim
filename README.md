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
1. Something that simultaneously tracks the number of times every block has been traversed. Once all of the blocks traversed >= 1, then we will know that the environment has been fully explored. We could probably use an array that stores the references/pointers to every floor tile's traversion count and then return false if any are 0.
Done: tiles
Done: Minimum Spanning Tree



## Algorithms:

1. Hallway generator to connect a room to another room. It will build only in the x/-x and y/-y directions to simplify the process for now.
2. Room Generator - variables for minimum room size, maximum room size. Produces a single floor tile block surrounded by wall tiles
Done: Prim's
Done: Point placer and graph generator

## Main generation function:
Inputs: map size (X x Y), number of rooms, minimum room size, maximum room size, seed for random function (int)
Output: Map size, tile objects, traversal tracker



The result should be mostly compatible with boxnav, hopefully
