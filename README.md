# Labyrinth Solver

This repository contains a Python program designed to analyze and display features of labyrinths. The labyrinth is represented by a specific encoding of its elements, stored in a text file, and processed to extract various features.

## Features

The program is able to:

1. Verify the correctness of the labyrinth input.
2. Display a visual representation of the labyrinth.
3. Calculate and display the following features:
   - Number of gates (entry points).
   - Number of sets of connected walls.
   - Number of inaccessible inner points.
   - Number of accessible areas.
   - Number of accessible cul-de-sacs.
   - Number of entry-exit paths without intersections leading to cul-de-sacs.

## Input

The input consists of a text file that encodes the labyrinth using the digits 0, 1, 2, and 3. The digits represent the following:

- **0**: Point connected to neither right nor below neighbors.
- **1**: Point connected to the right neighbor but not below.
- **2**: Point connected to the below neighbor but not to the right.
- **3**: Point connected to both right and below neighbors.

The program reads the file, validates the input, and extracts the labyrinth structure.

### Example Input

1 0 2 2 1 2 3 0 
3 2 2 1 2 0 2 2 
3 0 1 1 3 1 0 0 
2 0 3 0 0 1 2 0 
3 2 2 0 1 2 3 2 
1 0 0 1 1 0 0 0



## Output

The program outputs the following features of the labyrinth:

- The number of gates.
- The number of connected wall sets.
- The number of inaccessible inner points.
- The number of accessible areas.
- The number of accessible cul-de-sacs.
- The number of entry-exit paths.

### Example Output

The labyrinth has 2 gates. 
The labyrinth has 3 sets of walls. 
The labyrinth has 4 inaccessible inner points. 
The labyrinth has 2 accessible areas. The labyrinth has 1 accessible cul-de-sac. 
The labyrinth has 2 entry-exit paths with no intersections leading to cul-de-sacs.

Requirements
Python 3.x
