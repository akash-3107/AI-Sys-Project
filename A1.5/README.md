# Repository for ss23.1.5/team381
This is the repository for you solution. You can modify this README file any way you see fit.

**Topic:** SS23 Assignment 1.5: Escape Wumpus Cave

[Members: Akash Tambe, Prashansa Priyadarshini]

In this assignment, we learnt about planning and the PDDL format. Also, we understood how to encode a problem as a planning problem and create a solution for the problem using a planner.

We used "fast-downward" planner to generate the solution files.

Folder structure:
1. example-maps : contains all the example-maps from the assignment repository
2. maps : contains all the problem-maps from the assignment repository
3. map-pddl : contains all the mapXXX.pddl files which we generate using file "map.py"
4. solution-pddl : contains all the mapXXX.pddl.soln files which we generate by running the planner. This is done using file "solution.py"
5. solutions : contains all the final mapXXX-solution.txt which we generate from mapXXX.pddl.soln files. This is also done using the file "solution.py"
6. wumpus.pddl : This contains all the actions for the agent to move. This is a domain file

Approach :
1. In the problem file mapXXX.pddl, we created the initial position and defined it using adjacency matrix. We also mentioned the direction(i.e. North, South, East and West) while defining the same so as to easily identify where the agent is actually moving. Rest of the elements such as wumpus,fireworks,arrows,pit,crate and halfcrate were also defined. 
2. In the domain file wumpus.pddl, we defined corresponding actions with their pre-conditions and the effects which included walk,push,scare and shoot. All the scenarios mentioned in the assignment were taken into consideration. While writing the wumpus.pddl, we also mentioned the pre-conditions that need to be checked before applying the actions and post that we define the actions which need to be performed if the pre-conditions were satisfied.
3. The map file and the wumpus domain file were then passed on to the planner which generated a 'mapXXX.pddl.soln' file.
4. The post processing of the planner output was also automated to generate the final solution files in the required format.

What worked well and what didn't?
1. Realization of the environment of the map in a form of a planning problem was a bit difficult. For this we needed to get an idea regarding the format of the files which are expected by the planner.
2. Once we got an idea to represent the environment in a the planning format, we wrote python code to automate generation of the corresponding planning problem format for an equivalent problem which we wanted to solve. This helped us in generating the planning environment from the problem faster.
3. Once we achieved this, mostly the changes went in in the wumpus.pddl file wherein we specify the actions which need to be taken by the agent.
4. Initially, in the action file, we did not specify seperate actions for the agent to follow based on the direction. For eg, we only defined the action WALK which was confusing for the agent. Later on, we split the WALK action into WALK NORTH, WALK SOUTH,WALK WEST and WALK EAST which helped the agent as well as us to debug the code and visualize the path the agent actually followed.
5. This approach when replicated to rest of the actions of FIRE,etc worked in our favour.
6. Post that, we were able to generate all the final solutions required in a specific format in an automated way which helped us generate solutions faster.
7. We found it much easier to modify the PUSH/WALK action with multiple preconditions to check for cell properties(C,W,H,HC,etc.) and perform the effect accordingly rather than splitting them into multiple diffrent actions. 

Python modules used are as follows:
1. string
2. os
3. numpy

To run : 
1. Go to the directory where all the python files are present. (In this case, team381)
2. Execute map.py to generate the corresponding map.pddl files. (Pre-requisite : a folder containing all the maps should be present at the same location. Also, modify the folder name from where it refers the maps in map.py, if required)
3. Once the pddl files are generated successfully, run the solution.py file present at the same location. (PS: Change the folder/directory names if required)
4. At the end, check whether the .pddl.soln files are generated in solution-pddl folder and solution.txt files are generated in solutions folder.

