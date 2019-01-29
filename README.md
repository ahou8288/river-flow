### Determine where water will flow to based on height GIS data

# Method

1. Load data and convert it to a 2 dimensional list of height information
2. Convert each of the heights into a node
3. Connect each node to it's neighbours (above, below and to each size)
4. If two nodes of equal height are neighbours then merge them into one node
5. Store all the nodes in a sorted list
6. Flood low points;
    * Find all the points which are below all their neighbours. These points are called lakes.
    * For each of these lakes add all of the neighbours (the perimeter of the lake) to collection sorted by height
    * Starting from the lowest neighbour check if it is below the level of the lake. If it is then the flooding is complete.
    * Otherwise merge the point into the lake and raise the height of the lake to be equal to the point that was just merged into the lake. Add the neighbours of the point that is being merged into the sorted collection of lake neighbours.
7. Starting from the highest point send flow down to lower points.
8. Create images for each step as flow is sent down and compile into an animation.

# Data structure prep

list of list of heights
list of list of nodes
connect the nodes based on their location to the other nodes
add all the nodes into a list
return sort the list and return it

**Notes:**

* always merge towards the higher altitude node, then the position of the lake in the list will not need to change
* When finding an item look for it by original_location
* the list would probably work fast as a collections.deque

# Data

Landsat 8 data from USGS. 30m spaced grid of height data.

# Instructions for running

TODO

# Pictures

TODO - Will be generated by algorithm

# Tests

Run the tests with `python test.py`
