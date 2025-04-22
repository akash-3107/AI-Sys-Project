import os
import re
import itertools
from automathon import DFA
from pysat.solvers import MinisatGH
import numpy as np


# Create a symbol dictionary to maintain the corresponding cell values from the nonogram for encoding purpose
def create_symbol_dictionary(max_value,helpVariable,multicolor_flag):
    dictionary = {}
    maxHV=len(helpVariable)

    if multicolor_flag == False:
        for i in range(1,max_value+1):
            dictionary['C'+str(i)] = i
            dictionary['~C'+str(i)] = -i
        j=max_value+1
        count = 1
        for i in range(j,j+maxHV):
            dictionary['A'+str(count)] = i
            dictionary['~A'+str(count)] = -i
            count += 1
    
    elif multicolor_flag == True:
        for i in range(1,max_value+1):
            a=format(ord('a'), '08b')
            b=format(ord('b'), '08b')
            dictionary['aC'+str(i)] = int(str(a)+str(i))
            dictionary['~aC'+str(i)] = int('-'+str(a)+str(i))
            dictionary['bC'+str(i)] = int(str(b)+str(i))
            dictionary['~bC'+str(i)] = int('-'+str(b)+str(i))
        j=max_value+1
        count = 1    
        for i in range(1,maxHV+1):
            dictionary['A'+str(count)] = i
            dictionary['~A'+str(count)] = -i
            count += 1
    return dictionary


# Assign equivalent numbers according to encoding to generate input to the SAT solver
def cnf_str_to_list(cnf_expr_clause_list, symbol_dictionary):
    cnf_list = []
    temp_cnf_list = []
    for clause in cnf_expr_clause_list:
        and_clause_split = clause.split(' And ')
        for a in and_clause_split:
            a = a.replace('(','')
            a = a.replace(')','')
            a = a.replace('Not ', '~')
            a_split = a.split(' Or ')

            for a_s in a_split:
                temp_cnf_list.append(symbol_dictionary[a_s])
            cnf_list.append(temp_cnf_list)
            temp_cnf_list = []
    return cnf_list


# Read the puzzle data from the nonogram problem file
def read_puzzle(path_to_file):
    f = open(path_to_file)
    f_tmp = open(path_to_file)
    shape = f_tmp.readline()
    lines = f.read().splitlines()
    colors = []
    clues = []

    if 'rect' in shape or 'hex' in shape:
        for i in range(len(lines)):
            if i == 0:
                split_line = lines[i].split()
                if len(split_line) == 3:
                    type_of_grid = split_line[0]
                    num_rows = int(split_line[1])
                    num_cols = int(split_line[2])
                elif len(split_line) == 2:
                    type_of_grid = split_line[0]
                    hex_side = int(split_line[1])
            elif i == 1:
                colors.append(lines[i])
            else:
                clues.append(lines[i])

    f.close()
    f_tmp.close()
    if 'rect' in shape:
        return [type_of_grid,num_rows,num_cols,clues,colors]
    elif 'hex' in shape:
        return [type_of_grid,hex_side,clues,colors]

# Generate DNF encoding using Approach 1 
def generate_encoding_approach1_rect(rows,cols,clues,blocks):
    
    colLayout=[]
    gridLayout = np.ones((rows,cols),dtype=int)
    count=gridLayout[0][0]

    for i in range(gridLayout.shape[0]):
        
        for j in range(gridLayout.shape[1]):
            
            gridLayout[i][j] = count
            count=count+1
    colLayout = np.transpose(gridLayout)
    regExp=[]
    
    
    for i in range(len(clues)):
        exp='0*'
        clue=clues[i].split(' ')
        if clues[i]!='':
            if len(clue)>1:
                
                for j in range(len(clue)):
                    entity=clue[j][:-1]
                    if entity=='+':
                        exp=exp+'1+'
                    else:
                        exp=exp+'1{'+entity+'}'
                    exp=exp+'0+'
            else:
                entity=clue[0][:-1]
                if entity=='+':
                    exp=exp+'1+'
                else:
                    exp=exp+'1{'+entity+'}'
                exp=exp+'0+'     
        
        
        exp=exp[:-2]  
        exp=exp+'0*$'
        temp=[exp,clues[i]]
        regExp.append(temp)
    ListDNF=[]
    diffRC=False
    if cols!=rows:
        diffRC=True
        # Generate all possible combinations depending upon the number of colours
        # This is a bottleneck in cases where the grid size increases above 25 X 25
        TruthTable_R=list(itertools.product(['0', '1'], repeat=cols))
        TruthTable_C=list(itertools.product(['0', '1'], repeat=rows))
    else:
        TruthTable=list(itertools.product(['0', '1'], repeat=cols))
    
    colFlag=False
    for i in range(len(regExp)):
        if i==rows or colFlag:
            colFlag=True
            if diffRC:
                tt=TruthTable_C
            else:
                tt=TruthTable
            
            dnf = validateExpression(regExp[i][0],regExp[i][1],tt,cols,colLayout[abs(i-rows)])
        else:
            if diffRC:
                tt=TruthTable_R
            else:
                tt=TruthTable
            dnf = validateExpression(regExp[i][0],regExp[i][1],tt,cols,gridLayout[i])
        ListDNF.append(dnf)
    finalDNF = generateDNFString(ListDNF)    
    
    return ListDNF    

# This function is to generate encoding if two colours are present in the nonogram
def approach1EncodingMultiColor(rows,cols,clues,blocks):
    colLayout=[]
    gridLayout = np.ones((rows,cols),dtype=int)
    count=gridLayout[0][0]

    for i in range(gridLayout.shape[0]):
        for j in range(gridLayout.shape[1]):
            gridLayout[i][j] = count
            count=count+1
    colLayout = np.transpose(gridLayout)
    regExp=[]
    
    for i in range(len(clues)):
        exp='0*'
        clue=clues[i].split(' ')
        if clues[i]!='':
            if len(clue)>1:
                aFlag = False
                bFlag = False
                for j in range(len(clue)):
                    entity=clue[j][:-1]
                    value=clue[j][-1]
                    if value=='a':
                        bFlag = False
                        if aFlag:
                            exp = exp+'0+'
                            aFlag = False
                        
                        if entity=='+':
                            exp=exp+'1+'
                        else:
                            exp=exp+'1{'+entity+'}'
                        aFlag = True
                    elif value=='b':
                        aFlag = False
                        if bFlag:
                            exp = exp+'0+'
                            bFlag = False
                        
                        if entity=='+':
                            exp=exp+'2+'
                        else:
                            exp=exp+'2{'+entity+'}'
                        bFlag = True
                    exp=exp+'0*'
            else:
                entity=clue[0][:-1]
                value=clue[0][-1]
                if value=='a':
                    if entity=='+':
                        exp=exp+'1+'
                    else:
                        exp=exp+'1{'+entity+'}'  
                elif value=='b':
                    if entity=='+':
                        exp=exp+'2+'
                    else:
                        exp=exp+'2{'+entity+'}'     
                exp=exp+'0*'
        
        exp=exp[:-2]   
        exp=exp+'0*$'
        temp=[exp,clues[i]]
        regExp.append(temp)
    ListDNF=[]
    diffRC=False
    #truthTable elmnets depending on colors
    if len(blocks[0].split(' '))>2:
        elements = ['0','1','2']  
    else:
        elements = ['0','1']
    if cols!=rows:
        diffRC=True
        
        TruthTable_R=list(itertools.product(elements, repeat=cols))
        TruthTable_C=list(itertools.product(elements, repeat=rows))
    else:
        TruthTable=list(itertools.product(elements, repeat=cols))
    
    colFlag=False
    for i in range(len(regExp)):
        if i==rows or colFlag:
            colFlag=True
            if diffRC:
                tt=TruthTable_C
            else:
                tt=TruthTable
            
            dnf = validateExpression_Multicolor(regExp[i][0],tt,cols,colLayout[abs(i-rows)])
        else:
            if diffRC:
                tt=TruthTable_R
            else:
                tt=TruthTable
            dnf = validateExpression_Multicolor(regExp[i][0],tt,cols,gridLayout[i])
        ListDNF.append(dnf)
    return ListDNF

# This function is for creating all possible combinations of the encoding
def truthtable(n,element):
  if n < 1:
    return [[]]
  subtable = truthtable(n-1,element)
  return [ row + [v] for row in subtable for v in element ]

# Decide which encoding is acceptable according to the clue (For 2 colours)
def validateExpression_Multicolor(exp,Truthtable,cols,grid):
    accepted=[]
    for element in Truthtable:
        strElement=''
        strTemp='0'
        for i in range(len(element)):
            strElement = strElement+' '+element[i]
            strTemp = strTemp+element[i]
        strTemp = strTemp+'0'
        if bool(re.match(exp,strTemp)):
            accepted.append(strElement)
    dnf = generateDNF_multicolor(accepted,grid)
    return dnf         

# Decide which encoding is acceptable according to the clue (For 1 colour)
def validateExpression(exp,clues,Truthtable,cols,grid):
    accepted=[]
    for element in Truthtable:
        strElement=''
        strTemp='0'
        for i in range(len(element)):
            strElement = strElement+' '+element[i]
            strTemp = strTemp+element[i]
        strTemp = strTemp+'0'
        if bool(re.match(exp,strTemp)):
            accepted.append(strElement)
    dnf = generateDNF(accepted,grid)
    return dnf 

# Generate DNF for 2 colours
def generateDNF_multicolor(accepted,grid):
    DNF=''
    #clue=clues.split(' ')
    countE=0
    
    for i in range(len(accepted)):
        temp = accepted[i].split(' ')
        clause=''
        for j in range(1,len(temp)):
            countV=grid[j-1]
            
            if temp[j]=='0':
                tempFlag = True
                countE+=1
                clause = clause +' Not aC'+str(countV)+' And Not bC'+str(countV)+' And'
            elif temp[j]=='1':
                clause = clause +' aC'+str(countV)+' And Not bC'+str(countV)+' And'
            elif temp[j]=='2':
                clause = clause +' bC'+str(countV)+' And Not aC'+str(countV)+' And'

        accepted[i]=clause[:-3].strip()
    for cl in accepted:
      DNF='('+cl+') Or '+DNF
    return DNF[:-4] 

# Generate DNF for a single colour
def generateDNF(accepted,grid):
    DNF=''
    for i in range(len(accepted)):
        temp = accepted[i].split(' ')
        clause=''
        for j in range(1,len(temp)):
            countV=grid[j-1]
            if temp[j]=='0':
                clause = clause +' Not C'+str(countV)+' And'
            elif temp[j]=='1':
                clause = clause +' C'+str(countV)+' And'

        accepted[i]=clause[:-3].strip()
    for cl in accepted:
      DNF='('+cl+') Or '+DNF     
    return DNF[:-4]   


# To check whether the automata we create is valid or not
def validateAutomata(automata,TruthTable,cols,grid):
    DNF=''
    accepted=[]
    QList=[]
    for keys in automata:
        QList.append(keys)
    
    Q=set(QList)
    sigma = {'0', '1'}
    delta = automata
    initialState = 's'
    F = {'e'}
    # To generate an automata we are using the library Automathon
    automata1 = DFA(Q, sigma, delta, initialState, F)
    for element in TruthTable:
        strElement=''
        strTemp='0'
        for i in range(len(element)):
            strElement = strElement+' '+element[i]
            strTemp = strTemp+element[i]
        strTemp = strTemp+'0'
        if automata1.accept(strTemp):
            accepted.append(strElement)  
    #countV=0 
    dnf = generateDNF(accepted,grid)
    return dnf
 
# Generate the encoding according to approach 4
def generate_encoding_approach4_rect(rows,cols,clues,blocks):
    colLayout=[]
    gridLayout = np.ones((rows,cols),dtype=int)
    count=gridLayout[0][0]
    for i in range(gridLayout.shape[0]):
        
        for j in range(gridLayout.shape[1]):
            
            gridLayout[i][j] = count
            count=count+1

    ListAutomata=[]
    colLayout=np.transpose(gridLayout)
    for i in range(len(clues)):
        clue = clues[i].split(' ')
        
        graph={}
        
        entityCount = 1
        count = 1
        iterator = entityCount
        if len(clue[0])==0:
            graph['s']={'0':'e'}
        else:
            graph['s']={'0':'s','1':'a1'}
            for i in range(len(clue)):
                if int(clue[i][0])>1:
                    for j in range(iterator,iterator+int(clue[i][0])):
                        #adding intermediate state
                        entityCount=j
                        if j == int(clue[i][0])+iterator-1:
                            graph['a'+str(entityCount)]={'0':'g'+str(i+1)}                        
                        #adding last block element
                        else:
                            graph['a'+str(entityCount)]={'1':'a'+str(entityCount+1)}
                #adding 2nd last   
                else:
                    graph['a'+str(entityCount)]={'0':'g'+str(i+1)}
                #adding gap
                if i+1<len(clue):
                    entityCount+=1
                    graph['g'+str(i+1)]={'0':'g'+str(i+1),'1':'a'+str(entityCount)}
                    iterator=entityCount
                    #count+=1
                if i+1==len(clue):
                    graph['a'+str(entityCount)]={'0':'e'}

        #adding termination state
        graph['e']={'0':'e'}
        ListAutomata.append(graph)
    ListDNF=[]
    finalDNF=''
    diffRC=False
    if cols!=rows:
        diffRC=True
        TruthTable_R=list(itertools.product(['0', '1'], repeat=cols))
        TruthTable_C=list(itertools.product(['0', '1'], repeat=rows))
    else:
        TruthTable=list(itertools.product(['0', '1'], repeat=cols))
    c=[0]*cols
    colFlag=False
    for i  in range(len(ListAutomata)):
        
        if i==rows or colFlag:
            colFlag=True
            if diffRC:
                dnf = validateAutomata(ListAutomata[i],TruthTable_C,cols,colLayout[abs(i-cols)])
            else:
                dnf = validateAutomata(ListAutomata[i],TruthTable,cols,colLayout[abs(i-cols)])
        else:
            if diffRC:
                dnf = validateAutomata(ListAutomata[i],TruthTable_R,cols,gridLayout[i])
            else:
                dnf = validateAutomata(ListAutomata[i],TruthTable,cols,gridLayout[i])
        ListDNF.append(dnf)
        
    finalDNF = generateDNFString(ListDNF)    
    
    return finalDNF

# Generate the DNF in a string format
def generateDNFString(ListDNF):
    finalDNF=''
    for i in range(len(ListDNF)):   
        finalDNF=finalDNF+'('+ListDNF[i]+') And '
    finalDNF='('+finalDNF[:-5]+')' 
    return finalDNF

# Generate a final solution for the nonogram (For 1 colour)
def generate_solution(sat_variable_list, rows, cols):
    solution = np.ones((rows,cols), dtype=np.unicode_)
    count = 0
    for i in range(solution.shape[0]):
        for j in range(solution.shape[1]):
            var = sat_variable_list[count]
            if var > 0:
                solution[i][j] = 'a'
            else:
                solution[i][j] = '-'
            count += 1
    return solution

# Generate a final solution for the nonogram (For 2 colours)
def generate_solution_color(sat_variable_list, rows, cols):
    solution = np.ones((rows,cols), dtype=np.unicode_)
    count = 0
    for i in range(solution.shape[0]): #rows
        for j in range(solution.shape[1]): #cols   
            a = int(str(format(ord('a'), '08b'))+str(count))
            b = int(str(format(ord('b'), '08b'))+str(count))
            if sat_variable_list[a]>0:
                solution[i][j] = 'a'
            elif sat_variable_list[b]>0:
                solution[i][j] = 'b'
            else:
                solution[i][j] = '-'
            count += 1
    return solution

# Create the final solution file
def create_solution_file(solution_array,file):
    
    r, c = solution_array.shape
    
    fname = file.split('.')[0] + '.solution'
    
    f = open(fname,'w')
    for i in range(r):
        for j in range(c):
            f.write(solution_array[i][j])
        if i < r-1:
            f.write('\n')
    f.close()


# Check if any expression is already in the form of a CNF
def AlredayCNF(clause):
    element = clause.split('And')
    count = 0
    for e in element:
        
        if e.count('C')>1:
            if e.strip().startswith('(') and e.strip().endswith('('):
                pass
            else:
                count+=1
        
    if count>0:
        flagCNF = False
    else:
        flagCNF = True
        
    return flagCNF

# Intermediate function to convert implications to CNF form
def create_cnf_and_implies(str, hVar):
    conj = ''
    conjn = []
    final_conjn = []
    str_split = str.split(' And ')
    for s in str_split:
        s = s.replace('(','')
        s = s.replace(')','')
        conjn.append(hVar + ' -> ' + s)
   
    for c in conjn:
        c_split = c.split(' -> ')
        final_conjn.append('(Not ' + c_split[0] + ' Or ' + c_split[1]+')')
 
    for c1 in final_conjn:
        conj += c1 + ' And '
   
    conj = conj[:-5]
    return conj

# Generate CNF in a string format
def create_cnf(clause,index):
    clause_split = clause.split(' Or ')
    helper_variables=[]
    cnf = ''       
    for c in range(len(clause_split)):
        helper_variables.append('A'+str(c+index))

    cnf += '('
    for h in helper_variables:
        cnf += h + ' Or '
    cnf = cnf[:-4]
    cnf += ') And '
 
    for c in range(len(clause_split)):
        cnf += create_cnf_and_implies(clause_split[c],helper_variables[c]) + ' And '
    cnf = cnf[:-5]
    return cnf,helper_variables


if __name__ == '__main__':
    filename = 'arrow-1.clues'
    foldername = 'clues'
    
    files = os.listdir(foldername)
    multiColorFlag = False
    
    path_to_clue_file = os.path.join(foldername,filename)
    
    f1 = open(path_to_clue_file)
    shape = f1.readline()
    f1.close()
    
    if 'rect' in shape:
        grid_type, rows, cols, clues, blocks = read_puzzle(path_to_clue_file)
        for c in clues:
            if 'a' in c and 'b' in c:
                multiColorFlag = True
                break
            else:
                multiColorFlag = False

        if multiColorFlag == True:
            input_dnf_str1_rect = approach1EncodingMultiColor(rows,cols,clues,blocks)
        elif multiColorFlag == False:
            input_dnf_str1_rect = generate_encoding_approach1_rect(rows,cols,clues,blocks)

    temp=[]
    helpV=[]
    for clause in input_dnf_str1_rect:
        flagCNF = AlredayCNF(clause)
        if flagCNF:
            temp.append(clause)
        else:
            if len(helpV)!=0:
                hV = helpV[-1][-1]
                index=int(hV.split('A')[1])
            else:
                index=0
            new_clause,helpVar = create_cnf(clause,index+1)
            helpV.append(helpVar)
            temp.append(new_clause)
            
    finalCNF = generateDNFString(temp)
    
    helpVariable = [x 
                 for xs in helpV 
                 for x in xs ]
    
    input_dnf_str = finalCNF
    
    symbol_dictionary = create_symbol_dictionary(rows*cols, helpVariable, multiColorFlag)

    input_dnf_str = input_dnf_str.replace('And', '&')
    input_dnf_str = input_dnf_str.replace('Not ', '~')
    input_dnf_str = input_dnf_str.replace('Or', '|')
    
    cnf_list = cnf_str_to_list(temp, symbol_dictionary)
    
    solver = MinisatGH(bootstrap_with=cnf_list)
    
    result = solver.solve()
    if result:
        model = solver.get_model()
        if multiColorFlag == True:
            solution = generate_solution_color(model, rows, cols)
        elif multiColorFlag == False:
            solution = generate_solution(model, rows, cols)
        create_solution_file(solution,filename)
    