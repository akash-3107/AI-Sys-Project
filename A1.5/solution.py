import os

if __name__ == '__main__':
    currentDir = os.getcwd()
    python_str = 'python downward-main/fast-downward.py --alias lama-first --plan-file '
    map_pddl_dir = 'map-pddl'
    sol_pddl_dir = 'solution-pddl'
    sol_dir = 'solutions'
    map_pddl_path = os.path.join(currentDir,map_pddl_dir)
    soln_pddl_path = os.path.join(currentDir,sol_pddl_dir)
    soln_path = os.path.join(currentDir,sol_dir)
    domain_file = os.path.join(currentDir,'wumpus.pddl')
    dir=os.listdir(map_pddl_dir)
    dir.sort()

    # Generate soln.pddl files by running fast-downward
    
    for file in dir:
        filename = file+'.soln'
        path_file = os.path.join(soln_pddl_path,filename)
        map_file = os.path.join(map_pddl_path,file)
        python_cmd = python_str + path_file + ' ' + domain_file + ' ' + map_file
        os.system(python_cmd)
    
    
    # Generate final solution.txt from soln.pddl files
    #'''
    soln_pddldir=os.listdir(sol_pddl_dir)
    soln_pddldir.sort()
    for fName in soln_pddldir:
        filename = os.path.join(soln_pddl_path,fName)
        f = open(filename,'r')
        lines = f.readlines()
        solFile = os.path.join(soln_path,fName.split('.')[0]+'-solution.txt')
        f1 = open(solFile,'w')
        for l in lines:
            l = l.replace('(','')
            l = l.replace(')','')
            l = l.split(' ')[0]
            if l.startswith('push') or l.startswith('walk') or l.startswith('scare') or l.startswith('shoot'):
                action = l.split('-')
                f1.write(action[0] + ' ' + action[1] + '\n')
    #'''