# ProceduralBoxSim

Overview:

1. Define the size of the 2d plane
2. Place random points on the plane
3. Connect every point to every other point to create a fully connected graph
4. Use Prim's Algorithm to find the minimum spanning tree. This tree will be what we base the map on
5. At each point in our tree, create a randomly sized room.
6. For every edge, build a hallway that connects a room to the room at the other end.
7. Convert this map to unreal engine environment

Data Structures:
1. MinHeap to store the edges for Prim's
2. Floor tile: stores an integer to count how many times it has been traversed, target - (X x Y), boundaries (X, Y, -X, -Y), and adjacent targets (list of connecting tile blocks)
3. Wall tile: boundaries (X, Y, -X, -Y)
4. Something that simultaneously tracks the number of times every block has been traversed. Once all of the blocks traversed >= 1, then we will know that the environment has been fully explored. We could probably use an array that stores the references/pointers to every floor tile's traversion count and then return false if any are false.


Algorithms:
1. Point placer - variable for how many points/rooms
2. Prim's
3. Hallway algorithm to connect a room to another room. It will build only in the x/-x and y/-y directions to simplify the process for now.
4. Room Generator - variables for minimum room size, maximum room size. Produces a single floor tile block surrounded by wall tiles

Main generation function:
Inputs: map size (X x Y), number of rooms, minimum room size, maximum room size, seed for random function (int)
Output: Map size, tile objects



The result should be mostly compatible with boxnav, hopefully
