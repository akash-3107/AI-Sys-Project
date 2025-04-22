import os
import numpy as np
import random

# Get the neighbouring element indices    
def get_neighbours(x, y):
    return {'down':[x+1,y], 'up':[x-1,y], 'left':[x,y-1], 'right':[x,y+1]}

# Get the current co-ordinates
def currentCoordinates(maparr):
    start = np.where(maparr == 'S')
    down = np.where(maparr == 'v')
    up = np.where(maparr == '^')
    left = np.where(maparr == '<')
    right = np.where(maparr == '>')

    c = [0,0]
    o = 'B'

    if len(start[0]) != 0 and len(start[1]) != 0:
        o = 'S'
        c = [start[0][0], start[1][0]]

    if len(up[0]) != 0 and len(up[1]) != 0:
        o = '^'
        c = [up[0][0], up[1][0]]

    elif len(right[0]) != 0 and len(right[1]) != 0:
        o = '>'
        c = [right[0][0], right[1][0]]

    elif len(down[0]) != 0 and len(down[1]) != 0:
        o = 'v'
        c = [down[0][0], down[1][0]]

    elif len(left[0]) != 0 and len(left[1]) != 0:
        o = '<'
        c = [left[0][0], left[1][0]]
    
    return [c,o]

#Perform action L (Turn left)
def actionL(orient,co_ord,maparr):
    if orient == '^':
        maparr[(co_ord[0], co_ord[1])] = '<'
    elif orient == '>':
        maparr[(co_ord[0], co_ord[1])] = '^'
    elif orient == 'v':
        maparr[(co_ord[0], co_ord[1])] = '>'
    elif orient == '<':
        maparr[(co_ord[0], co_ord[1])] = 'v'
    return maparr

# Perform action R (Turn Right)
def actionR(orient,co_ord,maparr):
    if orient == '^':
        maparr[(co_ord[0], co_ord[1])] = '>'
    elif orient == '>':
        maparr[(co_ord[0], co_ord[1])] = 'v'
    elif orient == 'v':
        maparr[(co_ord[0], co_ord[1])] = '<'
    elif orient == '<':
        maparr[(co_ord[0], co_ord[1])] = '^'
    return maparr

# Perform action M (Move one step ahead in the direction of the robot)
def actionM(orient,co_ord,maparr,visited):
    neighbours = get_neighbours(co_ord[0],co_ord[1])
    for dir in neighbours:
        n = neighbours[dir]
        if maparr[n[0],n[1]] != 'X':
            if dir=='down' and orient=='v':
                maparr[n[0],n[1]] = 'v'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
            elif dir=='up' and orient=='^':
                maparr[n[0],n[1]] = '^'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
            elif dir=='left' and orient=='<':
                maparr[n[0],n[1]] = '<'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
            elif dir=='right' and orient=='>':
                maparr[n[0],n[1]] = '>'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
    return visited


# apply the plan on specific map with a specific plan
def applyPlan(map_arr,pl):
    v = []
    for p in pl:
        coord, orien = currentCoordinates(map_arr)
        if p == 'L':
            actionL(orien,coord,map_arr)
        elif p == 'R':
            actionR(orien,coord,map_arr)
        elif p == 'M':
            v = actionM(orien,coord,map_arr,v)
    return v

# Perform action M (for find plan)
def actionM_1(orient,co_ord,maparr,visited):
    neighbours = get_neighbours(co_ord[0],co_ord[1])
    new_coords = []
    for dir in neighbours:
        n = neighbours[dir]
        #print(maparr)
        #print('X')
        if maparr[n[0],n[1]] != 'X':
            if dir=='down' and orient=='v':
                maparr[n[0],n[1]] = 'v'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
                new_coords = n
            elif dir=='up' and orient=='^':
                maparr[n[0],n[1]] = '^'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
                new_coords = n
            elif dir=='left' and orient=='<':
                maparr[n[0],n[1]] = '<'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
                new_coords = n
            elif dir=='right' and orient=='>':
                maparr[n[0],n[1]] = '>'
                maparr[(co_ord[0], co_ord[1])] = ' '
                if n not in visited:
                    visited.append(n)
                new_coords = n
    return maparr,visited,new_coords

# Function to find a plan depending on the orientation, co-ordinates and the map array
def findPlan(blank_sq, vis, map_array,orientation,co_ordinates,orig_co_ordinates):
    plan = ''
    while True:  
        if len(blank_sq) == len(vis):
            break
        map_array_orig = np.copy(map_array)
        map_array_bkp = np.copy(map_array)
        
        maparr_new_m,vis,new_co_ordinates = actionM_1(orientation,co_ordinates,map_array_orig,vis)
        
        if np.array_equal(maparr_new_m,map_array_bkp) is False:
            plan += 'M'
            map_array = np.copy(maparr_new_m)
            co_ordinates = new_co_ordinates
            if orig_co_ordinates in vis:
                vis.remove(co_ordinates)
            continue
        
        if random.choice([True,False]):
            maparr_new_l = actionL(orientation,co_ordinates,map_array_orig)
            if np.array_equal(maparr_new_l,map_array_bkp) is False:
                plan += 'L'
                map_array = np.copy(maparr_new_l)
                if orientation == '^':
                    orientation = '<'
                elif orientation == '>':
                    orientation = '^'
                elif orientation == 'v':
                    orientation = '>'
                elif orientation == '<':
                    orientation = 'v'

        else:
            maparr_new_r = actionR(orientation,co_ordinates,map_array_orig)
            if np.array_equal(maparr_new_r,map_array_bkp) is False:
                plan += 'R'
                map_array = np.copy(maparr_new_r)
                if orientation == '^':
                    orientation = '>'
                elif orientation == '>':
                    orientation = 'v'
                elif orientation == 'v':
                    orientation = '<'
                elif orientation == '<':
                    orientation = '^'
    return plan

# Get the minimum length of the plan
def get_min_plan(list_plan):
    length = []
    for l in list_plan:
        length.append(len(l))
    min_len = min(length)
    ind = length.index(min_len)
    return list_plan[ind]


if __name__ == '__main__':

    blank_sq = []
    missed = []
    map_array=np.ones(shape=(12,18), dtype=np.str_)
    directory = 'example-problems'
    solution_dir = 'solutions'
    dir=os.listdir(directory)
    dir.sort()
    
    # iterate over files
    for file in dir:
        fname = os.path.join(directory,file)
        f = open(fname,'r')
        fileContent = f.readlines()
        find_check_plan = fileContent[0]
        
        # Split the execution depending upon the flag (CHECK/FIND) plan
        if find_check_plan == 'CHECK PLAN\n':
            plan = fileContent[1]
            count = 0
            # read and store the plan into a numpy array
            for i in range(2,len(fileContent)):
                line = fileContent[i]
                for j in range(0,len(line)-1):
                    map_array[count][j] = line[j]
                count += 1
            map_array[count-1][j+1] ='X'
            
            # compute blank squares
            blank = np.where(map_array==' ')
            for i in range(len(blank[0])):
                blank_sq.append([blank[0][i], blank[1][i]])

            co_ordinates, orientation = currentCoordinates(map_array)

            # according to orientation and start position constraints, split the execution
            if orientation == 'S':
                map_array_bkp = np.copy(map_array)
                map_array[(co_ordinates[0], co_ordinates[1])] = '^'
                v1 = applyPlan(map_array,plan)
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = 'v'
                v2 = applyPlan(map_array,plan)
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = '<'
                v3 = applyPlan(map_array,plan)
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = '>'
                v4 = applyPlan(map_array,plan)
                common_elements = set(map(tuple, v1)).intersection(map(tuple, v2)).intersection(map(tuple, v3)).intersection(map(tuple, v4))
                visited = [list(elem) for elem in common_elements]

            elif orientation == '^' or orientation == 'v' or orientation == '<' or orientation == '>':
                visited = applyPlan(map_array,plan)
            
            else:
                map_array_bkp = np.copy(map_array)
                final_v = []
                for b in range(len(blank_sq)):
                    co_ordinates = blank_sq[b]
                    map_array[(co_ordinates[0], co_ordinates[1])] = '^'
                    v1 = applyPlan(map_array,plan)
                    if co_ordinates not in v1:
                        v1.append(co_ordinates)
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = 'v'
                    v2 = applyPlan(map_array,plan)
                    if co_ordinates not in v2:
                        v2.append(co_ordinates)
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = '<'
                    v3 = applyPlan(map_array,plan)
                    if co_ordinates not in v3:
                        v3.append(co_ordinates)
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = '>'
                    v4 = applyPlan(map_array,plan)
                    if co_ordinates not in v4:
                        v4.append(co_ordinates)
                    map_array = np.copy(map_array_bkp)
                    common_elements = set(map(tuple, v1)).intersection(map(tuple, v2)).intersection(map(tuple, v3)).intersection(map(tuple, v4))
                    vis = [list(elem) for elem in common_elements]
                    final_v.append(common_elements)
                common = set.intersection(*final_v)
                visited = [list(elem) for elem in common]


            for i in blank_sq:
                if i not in visited:
                    missed.append(i)
            
            # create the solution file
            file_split = file.split('_')
            sol_file_name = 'solution_'+file_split[1]+'_'+file_split[2]
            sol_file = os.path.join(solution_dir,sol_file_name)
            f_soln = open(sol_file,'w')

            if len(missed)==0:
                f_soln.write('GOOD PLAN\n')
            else:
                f_soln.write('BAD PLAN\n')
                for m in missed:
                    f_soln.write(str(m[1]) + ', ' + str(m[0]) + '\n')
                f_soln.close()
            f.close()
            visited.clear()
            blank_sq.clear()
            missed.clear()
        
        # Section for FINDING the plan
        else:
            count = 0
            for i in range(1,len(fileContent)):
                line = fileContent[i]
                for j in range(0,len(line)-1):
                    map_array[count][j] = line[j]
                count += 1
            map_array[count-1][j+1] ='X'
            vis = []
            co_ordinates, orientation = currentCoordinates(map_array)
            orig_co_ordinates = co_ordinates
            blank = np.where(map_array==' ')
            
            for i in range(len(blank[0])):
                blank_sq.append([blank[0][i], blank[1][i]])

            if orientation == 'S':
                len_p = []
                map_array_bkp = np.copy(map_array)
                map_array[(co_ordinates[0], co_ordinates[1])] = '^'
                orientation = '^'
                p1 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                vis.clear()
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = 'v'
                orientation = 'v'
                p2 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                vis.clear()
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = '<'
                orientation = '<'
                p3 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                vis.clear()
                map_array = np.copy(map_array_bkp)
                map_array[(co_ordinates[0], co_ordinates[1])] = '>'
                orientation = '>'
                p4 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                vis.clear()
                orientation = 'S'
                len_p1 = len(p1)
                len_p.append(len_p1)
                len_p2 = len(p2)
                len_p.append(len_p2)
                len_p3 = len(p3)
                len_p.append(len_p3)
                len_p4 = len(p4)
                len_p.append(len_p4)
                min_len = min(len_p)
                ind = len_p.index(min_len)
                if ind == 0:
                    p = p1
                elif ind == 1:
                    p = p2
                elif ind == 2:
                    p = p3
                elif ind == 3:
                    p = p4
                else:
                    p = ''
                
            elif orientation == '^' or orientation == 'v' or orientation == '<' or orientation == '>':
                p = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                vis.clear()

            else:
                len_p = []
                final_len_p = []
                
                map_array_bkp = np.copy(map_array)
                for b in range(len(blank_sq)):
                    pl = ''
                    co_ordinates = blank_sq[b]
                    map_array[(co_ordinates[0], co_ordinates[1])] = '^'
                    orientation = '^'
                    p1 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                    vis.clear()
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = 'v'
                    orientation = 'v'
                    p2 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                    vis.clear()
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = '<'
                    orientation = '<'
                    p3 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                    vis.clear()
                    map_array = np.copy(map_array_bkp)
                    map_array[(co_ordinates[0], co_ordinates[1])] = '>'
                    orientation = '>'
                    p4 = findPlan(blank_sq,vis,map_array,orientation,co_ordinates,orig_co_ordinates)
                    vis.clear()
                    map_array = np.copy(map_array_bkp)
                    len_p1 = len(p1)
                    len_p.append(len_p1)
                    len_p2 = len(p2)
                    len_p.append(len_p2)
                    len_p3 = len(p3)
                    len_p.append(len_p3)
                    len_p4 = len(p4)
                    len_p.append(len_p4)
                    min_len = min(len_p)
                    ind = len_p.index(min_len)
                    if ind == 0:
                        pl = p1
                    elif ind == 1:
                        pl = p2
                    elif ind == 2:
                        pl = p3
                    elif ind == 3:
                        pl = p4
                    else:
                        pl = ''
                    len_p.clear()
                    final_len_p.append(pl)
                p = get_min_plan(final_len_p)
            file_split = file.split('_')
            sol_file_name = 'solution_'+file_split[1]+'_'+file_split[2]
            sol_file = os.path.join(solution_dir,sol_file_name)
            f_soln = open(sol_file,'w')
            f_soln.write(p)
            f_soln.close()
            f.close()