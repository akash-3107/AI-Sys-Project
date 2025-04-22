# Repository for ws2324.1.1/team479

**Topic:** WS2324 Assignment 1.1: Find Train Connections

[Members: Akash Tambe, Prashansa Priyadarshini]

We implemented a solution to fetch shortest path between 2 station connections depending on variable cost function using dijkstra algorithm.


Filename : main.py

1. get_problem_attributes(file,index) : Function to compute the problem attributes
2. read_csv_get_edges(file,costfn) : Function for building the graph as per the cost function
3. dijkstra(graph_src, graph_dest, start, end,costFunction,arrivalTime) : Function to compute the shortest path for a graph according to a cost function
4. create_solution_file(filename,solution_list) : Function to create the solution file 
5. createConnection(pathConnection) : Function to create the connection from the shortest path
6. cost_function(connection,costFunction,arrivalTime) : Function to compute the cost of the connection depending on the cost function


Approach :

1. We created different graph depending on cost funstions:
  1.a) cost function as stops: created graph with station codes as nodes and assigned 0 as weight to edge data
  1.b) cost function as distance: created graph with station codes as nodes and assigned distance between 2 station codes as weight to edge data
  1.c) cost function as price: created graph with station codes as nodes and assigned number of day change between station code depending on there arrival time on the sattion as weight to edge data
  1.d) cost function as arrival time: created graph with station codes as nodes and assigned arrival time to the destination station as weight to edge data
2. Once the graph is created, we used dijkstra algorithm to fetch the shortest path depending on the weight. For arrival time cost function we pick whichever train is closest to the arrival time provided in problem file and then continue with checking for shortest path.
3. After getting the shortest path, we make the connection string containing islno and train number. We also calculate the cost of connection from the shortest path, depending on the cost function.
4. Post that we create a solution file for all the problems.

More points regarding the approach : (Pros and Cons)
1. Creation of algorithm and debugging was easier with smaller data set.
2. Dataset was very elaborate to create good connected graph.
3. It was easier to calculate shortest paths for cost functions of stops and distance.
4. Considering the price cost function, the complexity for computing the shortest path increased. In some problems, the shortest path based on price cost function was not optimal. This was due to selection of an incorrect connection. Our algorithm was considering the connection which had the departure time of the next train to be catched before(lesser) than the arrival time of the current train hence adding a day to the overall cost. Which increased the overall cost by 1(in most cases).
5. The arrivaltime cost function was the hardest to implement. We faced a lot of difficulties designing a graph in a way where we could identify the connections considering the difference between departure times and arrival times. There was one example where there are two trains travelling in opposite directions of each other. This data was hard to maintain programatically as we were using dictionary to maintain graph data. As the station codes were duplicated, the values were being overwritten. This also caused non-optimal cost computations in this particular cost function of arrival time.
6. In general, graph making from the train data available taking into consideration what value to assign as the weight to the edges and what would be the graph nodes was a crucial point in solving this assignment.
7. Modifying dijkstra to calculate shortest path for different cost functions was also challenging as the weight assigned to each nodes had to be updtaed differently for each functions. For price and arrival time, the calculation of shortest path was with considering the day and train change as well as the 10 min. minimum switch time between the train.

To run:

1. Go to the directory which has main.py file.
2. Make sure that all the required schedule and problem files are present in the same location as that of main.py
3. Run the file.

Modules used while solving the assignment :

1. pandas
2. datetime
3. time
4. csv
5. numpy
6. heapq
7. calendar






