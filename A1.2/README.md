# Repository for ss23.1.2/team503
This is the repository for you solution. You can modify this README file any way you see fit.
[Members: Akash Tambe, Prashansa Priyadarshini]
**Topic:** SS23 Assignment 1.2: Play FAUhalma

We implemented search algorithms in this assignment and created an agent for a variant of ChineseCheckers i.e. FAUHalma.

Following are the functions we defined as a part of this assignment in client_simple.py file:

Filename: client_simple.py
1. getList() : Returns the unaccessable locations on the board to create star pattern in 2D array
2. getBoard_2(a,b) : Create a board after receiving the request from the server for 2 players
3. getBoard_3(a,b,c) : Create a board after receiving the request from the server for 3 players
4. valid_move(map_arr, start, end,dest_coordinate_list) : computes the valid move and make changes in board accordingly
5. makeFinalMoves(direction_dictionary,end,initial_distance) : Evaluate the distances between the new location to move the peg and destination location
6. fetch_MinDistance(a_currentLoc,a_destinationLoc) : Returns list containing min distnace between destination and peg and 2D distance array 
7. getDistance(peg1,peg2) : Calculation of the eucledien distance between two peg locations(coordinates)
8. updatePegs(a_current,a_destination) : Updates list of pegs if destination has already been reached
9. get_Moves(coordinate_array,valid_moves) : Convert moves made in 2D array to coordinate system 
10. move(dict) : Accepts the dictionary from server and return the next moves made by the peg back to the server

Approach:
1. As player A, we move the pegs of player A
2. We select the closest end destination location where A should be and move the peg that reduces the distance between them 
3. Our aim is to move all the pegs in the destination location before any other player, which results in us winning the game

To run:
1. Go to the directory which has client_simple.py file.
2. Run the file passing a config file as an argument.
Ex: python client_simple.py config_easy_star.json

Modules used while solving the assignment :
1. itertools
2. json
3. logging
4. requests
5. time
6. numpy as np

Environment: 
1. Two player star environment easy[config_easy_star.json]
2. Three player star environment easy[config_easy_3_star.json]