import os
from pysat.solvers import MinisatGH
import numpy as np


# create dictionary containg numbers corresponsing to eachg variable.
# This is used to create CNF list later.
def create_symbol_dictionary_2(max_value,clues,helpVarCount,multicolor_flag,list_symbol_dictionary):
    dictionary = {}
    cnt = 1
    clue_list = []
    for c in clues:
        space_split = c.split(' ')
        if len(space_split) == 1:
            clue_list.append(space_split[0])
        else:
            for c1 in space_split:
                clue_list.append(c1)    
    clue_len = len(clue_list)

    # Generate dictionary containg varaibles for each clues and its integer
    for l in range(clue_len):
        for i in range(max_value):
            if cnt<clue_len:
                dictionary['a'+str(l+1)+'C'+str(i+1)] = (i+1)
                dictionary['~a'+str(l+1)+'C'+str(i+1)] = -(i+1)
    count = i+2

    # Add element in dictionary with unique integer for each helper variables as well
    for i in range(helpVarCount):
        dictionary['A'+ str(i)] = count
        dictionary['~A'+str(i)] = -count
        count += 1
    
    return dictionary

# Convert the CNF string to CNF list splitting on AND and OR.
# This list is passed to Mini SAT for processing
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

# Create grid structure deping on rectangle or hexagonal clues. 
# This grid is used to number the cell and generate CNF accordingly.
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

# Visualize solution generated from the MiniSAT
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

# Create .solution file
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

# Create DNF for each clause depening on the clues sent.
# The grid Layout is used to number the cells and generate unique variables for each cells.
def generateDNF_2(clue_dictionary,grid_layout):
    list_DNF = []
    list_xor = []
    # used to create implies realtion between alpha and beta cells.
    # eg: 1a 2a, where alpha=1a and beta=2a
    list_xor_duplicate=[]
    list_implies = {}
    list_dict_keys = list(clue_dictionary.keys())
    max_length_flag = False
    one_clue_flag = False
    min_length_flag = False
    valid_available_cells = 0
    
    for key in list_dict_keys:
        value=clue_dictionary[key].split('a')
        if value[0] != '':
            valid_available_cells = valid_available_cells+int(value[0])+1
        else:
            valid_available_cells = 0
    valid_available_cells-=1  
    
    # chcek how may clues for each clause is there and update the subsequent flags.
    if len(list_dict_keys)==1:
        value=clue_dictionary[list_dict_keys[0]]
        if len(value) == 0:
            min_length_flag = True
        else:
            value = value[:-1]
            if int(value)==len(grid_layout):
                max_length_flag = True
            elif int(value)>1:
                one_clue_flag = True
    
    # generate XOR list       
    for i in range(len(list_dict_keys)):
        temp = []
        temp_1=[]
        value = clue_dictionary[list_dict_keys[i]]
        
        for j in range(len(grid_layout)):
            element = ''
            
            t = list_dict_keys[i]+grid_layout[j]
            temp.append(t) 
            if len(value) != 0:
                value_int = int(value.split('a')[0])
                if j+value_int<=len(grid_layout):
                    for el in grid_layout[j:j+value_int]:
                        element = element+' And '+list_dict_keys[i]+el
                    list_xor.append(element[5:])
                    temp_1.append(element[5:])
        list_xor_duplicate.append(temp_1)            
        list_DNF.append(temp)
    
    # when only one clue for each clause is encountered.
    # Generate implies rtelation for diffrent cells.
    if one_clue_flag:
        for i in range(len(list_DNF[0])):
            value = int(clue_dictionary[list_DNF[0][i].split('C')[0]][:-1])
            implies1 = ''
            if i+value>=len(list_DNF[0]):
                start_index = len(list_DNF[0])
            else:
                start_index = i+value                
            for k in range(start_index,len(list_DNF[0])):
                implies1 = implies1+' And Not '+list_DNF[0][k]            
            temp_list=implies1[5:]
            if temp_list!='':
                list_implies[list_DNF[0][i]]=temp_list
    
    # when more clues for each clause.
    # Genrate implies relations, relating alpha clue to beta and so on..
    if len(list_DNF)>1:
        count = 0    
        for i in range(len(list_xor_duplicate)-1):
            value=int(clue_dictionary[list_dict_keys[i]][:-1])
            valid_available_cells = valid_available_cells-value
            if i>0:
                valid_available_cells-=1
            for k in range(len(list_xor_duplicate[i])):
                temp=''
                initial_index = len(list_xor_duplicate[i])
                if k+valid_available_cells >= initial_index: 
                    break
                else:
                    end_index = k+value+1
                for j in range(end_index):
                    if 'And' in list_xor_duplicate[i+1][j]:
                        temp = temp + ' And Not (' +list_xor_duplicate[i+1][j] + ')'
                    else:
                        temp = temp + ' And Not ' +list_xor_duplicate[i+1][j]    
                if temp!='':
                    list_implies[list_xor_duplicate[i][k]] = temp[5:]
    
    final_DNF = []
    temp = ''
    
    # In case of having only 1 colored cell in a calue or  all cell of clause is colored.
    # Generating CNF with AND/AND NOT without any implications.
    if max_length_flag or min_length_flag:
        for el in list_DNF:
            temp = ''
            for el1 in el:
                if max_length_flag:
                    temp = temp +' And '+el1
                elif min_length_flag:
                    temp = temp +' And Not '+el1
            final_DNF.append(temp[5:])        
    
    # Generate Xor string
    else:
        for key in list_dict_keys:
            t=''
            for el in list_xor:
                
                if len(list_dict_keys)==1:
                    if 'And' in el:
                        t = t +' Xor ('+el+')'
                    else:
                        t = t +' Xor '+el
                elif key in el:
                    if 'And' in el:
                        t = t +' Xor ('+el+')'
                    else:
                        t = t +' Xor '+el
            temp=temp+'('+t[5:]+') And '      
            
        final_DNF.append(temp[:-5])
    
    implies_final=''
    
    # Add additional conditions for each clause containing implications
    for el in list_implies:
        if ' And ' in el:
            value = list_implies[el].split(' And ')
        elif ') And' in list_implies[el]:
            value = list_implies[el].split(') And ')
            for v in range(len(value)):
                if not value[v].endswith(')'):
                    value[v] += ')'
        else:
            value = list_implies[el].split(' And ')       
        for eel in value:
            if eel!='':
                imp = el+ ' -> '+eel
                final_DNF.append(imp)        

    return list_DNF,final_DNF   

# Generate encodings following 2nd approach
def generate_encoding_approach2_rect(row, col, clues):
    clue_dictionary = {}
    list_clue_dictionary = []
    count = 1
    final_dnf = ''
    
    # iterating over each clause
    for c in clues:        
        c = c.split(' ')
        len_c = len(c)
        for l in range(len_c):
            clue_dictionary['a'+str(count)] = c[l]
            count += 1
        list_clue_dictionary.append(clue_dictionary)
        clue_dictionary = {}
        
    colLayout=[]
    gridLayout = np.ones((rows,cols),dtype=int)
    count_grid=gridLayout[0][0]

    for i in range(gridLayout.shape[0]):
        for j in range(gridLayout.shape[1]):
            gridLayout[i][j] = count_grid
            count_grid=count_grid+1
    colLayout = np.transpose(gridLayout)
    count_clue_dict = 0
    row_list = []
    dnf = []
    create_symbol_list=[]
    t_temp2 = ''
    
    # creating encoding for each row clues and passing sepecify grid layout numbering.
    for r in range(row):
        for r1 in gridLayout[r]:
            row_list.append('C'+str(r1))
        clue_dict = list_clue_dictionary[count_clue_dict]
        temp1,temp2=generateDNF_2(clue_dict, row_list)
        create_symbol_list.append(temp1[0])
        for t2 in temp2:
            dnf.append(t2)
        temp2 = ''
        t_temp2 = ''
        count_clue_dict += 1
        row_list = []

    col_list = []
    
    # creating encoding for each column clues and passing sepecify grid layout numbering.
    for c in range(col):
        for c1 in colLayout[c]:
            col_list.append('C'+str(c1))
        clue_dict = list_clue_dictionary[count_clue_dict]
        temp1,temp2=generateDNF_2(clue_dict, col_list)
        create_symbol_list.append(temp1[0])
        for t2 in temp2:
            dnf.append(t2)
        temp2 = ''
        t_temp2 = ''
        count_clue_dict += 1
        col_list = []

    return dnf,create_symbol_list

# Convert implies expression to CNF
def convert_implication_to_cnf(clause):
    clause = clause.replace('(','')
    clause = clause.replace(')','')
    clause_split = clause.split(' -> ')
    cnf = ''
    if len(clause_split) == 2:
        cnf = 'Not ' + clause_split[0] + ' Or ' + clause_split[1]

    return cnf

# Convert AND and implies expression to CNF
def convert_and_implication_cnf(clause,help_count):
    imply_split = clause.split(' -> ')
    dict={}
    converted1 = []
    for i in imply_split:
        dict[i] = 'A' + str(help_count)
        help_count += 1
    temp = ''
    for i in dict:
        temp += dict[i] + ' -> '
    temp = temp[:-4]
    converted1.append(temp)
    for i in imply_split:
        if 'And' in i:
            And_split = i.split(' And ')
            for i1 in And_split:
                converted1.append('Not ' + dict[i] + ' Or ' + i1)    
    return converted1,help_count

# Convert Xor expression for clues containing a single colored cells.
def convert_xor_1a(expr):
    cnf = ''
    xor_split = expr.split(' Xor ')
    temp_cnf = ''
    cnf_list = []
    for x in xor_split:
        temp_cnf += x + ' Or '
    temp_cnf = temp_cnf[:-4]
    cnf_list.append(temp_cnf)

    for x in range(0,len(xor_split)):
        temp = xor_split[(x+1):]
        if x == len(xor_split)-1:
            continue
        for y in temp:
            temp_cnf = 'Not ' + xor_split[x] + ' Or Not ' + y
            cnf_list.append(temp_cnf)     
    return cnf_list


# Convert Xor expression for clues containing a multiple colored cells in accordance with another clues.
def convert_xor_na_multiple(clause,helper_variable_count):
    temp=clause
    cnf_list = []
    xor_split = temp.split(' Xor ')
    temp = temp.replace('Xor','Or')
    cnf_list.append(temp)
    dict = {}
    temp_implies = []
    helper_var = []
    cnt = helper_variable_count
    final_cnf_list = []
    for x in range(len(xor_split)):
        dict[xor_split[x]] = 'A' + str(cnt)
        cnt += 1
    and_split = []
      
    for c in cnf_list:
        if '->' in c:
            implies_split = c.split(' -> ')
            t = ''
            for i in implies_split:
                i = i.replace('Not ', '')
                t += dict[i] + ' -> Not '
                i1 = i.replace('(','')
                i1 = i1.replace(')','')
                i1 = i1.replace('Not ', '')
                and_split = i1.split(' And ')
                for a in and_split:
                    temp_implies.append(dict[i] + ' -> ' + a)
            temp_implies.append(t[:-8])
        elif 'Or' in c:
            or_split = c.split(' Or ')
            t = ''
            for o in or_split:
                t += dict[o] + ' Or '
                i1 = o.replace('(','')
                i1 = i1.replace(')','')
                i1 = i1.replace('Not ', '')
                and_split = i1.split(' And ')
                for a in and_split:
                    temp_implies.append(dict[o] + ' -> ' + a)
            temp_implies.append(t[:-4])
    
    temp_implies = list(dict.fromkeys(temp_implies))
    for t in temp_implies:
        if 'Or' not in t:
            final_cnf_list.append(convert_implication_to_cnf(t))
        else:
            final_cnf_list.append(t)

    return final_cnf_list,helper_variable_count

# Convert Xor expression for clues containing a multiple colored cells.
def convert_xor_na(clause,helper_variable_count):
    temp=clause
    cnf_list = []
    xor_split = temp.split(' Xor ')
    temp = temp.replace('Xor','Or')
    cnf_list.append(temp)
    dict = {}
    temp_implies = []
    helper_var = []
    cnt = helper_variable_count
    final_cnf_list = []
    for x in range(len(xor_split)-1):
        cnf_list.append(xor_split[x] + ' -> Not ' + xor_split[x+1])        
    for x in range(len(xor_split)):
        dict[xor_split[x]] = 'A' + str(cnt)
        cnt += 1
    and_split = []
    for c in cnf_list:
        if '->' in c:
            implies_split = c.split(' -> ')
            t = ''
            for i in implies_split:
                i = i.replace('Not ', '')
                t += dict[i] + ' -> Not '
                i1 = i.replace('(','')
                i1 = i1.replace(')','')
                i1 = i1.replace('Not ', '')
                and_split = i1.split(' And ')
                for a in and_split:
                    temp_implies.append(dict[i] + ' -> ' + a)
            temp_implies.append(t[:-8])
        elif 'Or' in c:
            or_split = c.split(' Or ')
            t = ''
            for o in or_split:
                t += dict[o] + ' Or '
                i1 = o.replace('(','')
                i1 = i1.replace(')','')
                i1 = i1.replace('Not ', '')
                and_split = i1.split(' And ')
                for a in and_split:
                    temp_implies.append(dict[o] + ' -> ' + a)
            temp_implies.append(t[:-4])
    temp_implies = list(dict.fromkeys(temp_implies))
    for t in temp_implies:
        if 'Or' not in t:
            final_cnf_list.append(convert_implication_to_cnf(t))
        else:
            final_cnf_list.append(t)
    return final_cnf_list,cnt

# Convert Xor expression for clues containing a single colored cell which is in accordance with another clues
def convert_xor_1a_multiple(expr):
    cnf = ''
    xor_split = expr.split(' Xor ')
    temp_cnf = ''
    cnf_list = []
    for x in xor_split:
        temp_cnf += x + ' Or '
    temp_cnf = temp_cnf[:-4]
    cnf_list.append(temp_cnf)
    return cnf_list

# main function
if __name__ == '__main__':
    # load clues file
    filename = 'stripes-004.clues'
    foldername = 'generated'
    files = os.listdir(foldername)
    multiColorFlag = False
    path_to_clue_file = os.path.join(foldername,filename)
    f1 = open(path_to_clue_file)
    shape = f1.readline()
    f1.close()
    clue_keys = []
    
    # Trigger shape specefic functions
    if 'rect' in shape:
        grid_type, rows, cols, clues, blocks = read_puzzle(path_to_clue_file)
        for c in clues:
            if 'a' in c and 'b' in c:
                multiColorFlag = True
                break
            else:
                multiColorFlag = False
        if multiColorFlag == True:
            pass
        elif multiColorFlag == False:
            input_dnf_str1_rect,list_symbol_dictionary = generate_encoding_approach2_rect(rows,cols,clues)
            temp_dnf = []
            final_and = []
            final_implies = []
            final_xor_1a = []
            final_xor_na = []
            final_and_implies = []
            final = []
            tmp = ''
            helper_variable_count = 0
            temp_converted = []
            temp_converted_1a = []
            
            # iterate over generated DNF for each clause and convert them into CNF
            for i in input_dnf_str1_rect:
                if '))' in i and 'Xor' in i:   
                    and_split_1 = i.split(')) And (')
                    if len(and_split_1) == 1:
                        converted_xor_na,helper_variable_count = convert_xor_na(i,helper_variable_count)
                    else:
                        for x1 in and_split_1:
                            if x1.startswith('(('):
                                x1 += '))'
                            elif x1.endswith(')'):
                                x1 = '(' + x1
                            if 'And' in x1 and 'Xor' in x1:
                                converted, helper_variable_count = convert_xor_na_multiple(x1,helper_variable_count)
                            else:
                                x1 = x1.replace('(','')
                                x1 = x1.replace(')','')
                                converted = convert_xor_1a_multiple(x1)
                            temp_converted.append(converted)
                        converted_xor_na = [
                                        x
                                            for xs in temp_converted
                                            for x in xs
                                        ]
                        temp_converted = []
                    for c1 in converted_xor_na:
                        final_xor_na.append(c1)              
                elif ') And (' in i:
                    xor_n1a_split = i.split(') And (')
                    for x2 in xor_n1a_split:
                        x2 = x2.replace('(','')
                        x2 = x2.replace(')','')
                        converted_xor_1a = convert_xor_1a_multiple(x2)
                        temp_converted_1a.append(converted_xor_1a)
                    converted_xor_1a = [
                                        x
                                            for xs in temp_converted_1a
                                            for x in xs
                                        ]
                    temp_converted_1a = []
                    for c2 in converted_xor_1a:
                        final_xor_1a.append(c2)
                else:    
                    and_split = i.split(') And (')
                    for a in and_split:
                        if 'Xor' in a:
                            xor_expr = a.replace('(','')
                            xor_expr = xor_expr.replace(')','')
                            converted_xor = convert_xor_1a(xor_expr)
                            for c in converted_xor:
                                final_xor_1a.append(c)
                        elif 'And' in a and '->' in a:
                            converted_list, helper_variable_count = convert_and_implication_cnf(a,helper_variable_count)
                            for c1 in converted_list:
                                final_and_implies.append(c1)
                        elif 'And' in a:
                            and_expr = a.replace('(','')
                            and_expr = and_expr.replace(')','')
                            final_and.append(and_expr)
                        elif '->' in a:
                            converted_implies = convert_implication_to_cnf(a)
                            if converted_implies != '':
                                final_implies.append(converted_implies)
            
            # Generate final CNF string for complete clues
            final = final_xor_na + final_xor_1a + final_and + final_implies + final_and_implies
            symbol_dictionary = create_symbol_dictionary_2(rows*cols,clues,helper_variable_count,False,list_symbol_dictionary)
            cnf_list = cnf_str_to_list(final,symbol_dictionary)
    
    # trigger MiniSAT for created CNF list
    solver = MinisatGH(bootstrap_with=cnf_list)
    result = solver.solve()
    
    # Visualize the result from mode, if result is TRUE
    if result:
        model = solver.get_model()
        if multiColorFlag == True:
            pass
        elif multiColorFlag == False:
            solution = generate_solution(model, rows, cols)
        create_solution_file(solution,filename)
    