
import itertools
import json
import logging
import requests
import time
import numpy as np

# Returns the unaccessable locations on the board to create star pattern in 2D array
def getList():
    unaccessableList = []
    unaccessableList.append([0,0])
    for i in range(0,7):
            for j in range(0,7):
                if i<4 and j>3:
                    unaccessableList.append([i,j])
                if i>=4:
                    unaccessableList.append([i,j])
    
    unaccessableList.append([-2,6])
    unaccessableList.append([-4,0])
    
    for i in range(-6,0):
            for j in range(0,7):
                if i==-1 and j>4:
                    unaccessableList.append([i,j])
                if i==-4 and j>3:
                    unaccessableList.append([i,j])
                if i<=-5 and (j!=3 and j!=2):
                    unaccessableList.append([i,j])
                    
    unaccessableList.append([2,-6])
    unaccessableList.append([5,-1])
    unaccessableList.append([-6,2])
    
    for i in range(0,7):
            for j in range(-6,0):
                if i==0 and j<-3:
                    unaccessableList.append([i,j])
                if i==1 and j<-4:
                    unaccessableList.append([i,j])
                if i==4 and j<-3:
                    unaccessableList.append([i,j])
                if i==5 and j<-3:
                    unaccessableList.append([i,j])
                if i==6 and j!=-3:
                    unaccessableList.append([i,j])
    
    for i in range(-6,0):
            for j in range(-6,0):
                if i>-4 and j<-3:
                    unaccessableList.append([i,j])
                if i<-3:
                    unaccessableList.append([i,j])
                    
    return unaccessableList

# Create a board after receiving the request from the server with 2 players
def getBoard_2(a,b):
    # 2D array containing coordinate system value
    coordinate_arr = np.ones((13, 13), dtype=list) 
    # Map array containg current state of board corresponding to 2D array
    map_arr = np.ones((13, 13), dtype=np.unicode_) 
    coordinate_list = []
    dest_coordinate_list = []
    dest_a=[[-3,6], [-3,5], [-2,5], [-3,4], [-2,4], [-1,4]]
    x=np.linspace(-6,6,num=13,dtype=int)
    y=np.flip(np.linspace(-6,6,num=13,dtype=int))
    unaccessableList = getList()
    
    for i in range(13):
        for j in range(13):
            coordinate_arr[j,i]=[x[i],y[j]]
            if coordinate_arr[j,i] in unaccessableList:
                    map_arr[j,i] = '0'
    
    for k in range(len(a)):
        for i in range(13):
            for j in range(13):
                if(coordinate_arr[j,i] == a[k]):
                    coordinate_list.append([j,i])
                    map_arr[j,i] = 'A'
                if(coordinate_arr[j,i] == dest_a[k]):
                    dest_coordinate_list.append([j,i])
                
    for k in b:
        for i in range(13):
            for j in range(13):
                if(coordinate_arr[j,i] == k):
                    map_arr[j,i] = 'B'
    return map_arr,coordinate_arr,coordinate_list,dest_coordinate_list

# Create a board after receiving the request from the server for 3 players
def getBoard_3(a,b,c):
    coordinate_arr = np.ones((13, 13), dtype=list)
    map_arr = np.ones((13, 13), dtype=np.unicode_)
    coordinate_list = []
    dest_coordinate_list = []
    dest_a=[[-3,6], [-3,5], [-2,5], [-3,4], [-2,4], [-1,4]]
    x=np.linspace(-6,6,num=13,dtype=int)
    y=np.flip(np.linspace(-6,6,num=13,dtype=int))
    unaccessableList = getList()
    
    for i in range(13):
        for j in range(13):
            coordinate_arr[j,i]=[x[i],y[j]]
            if coordinate_arr[j,i] in unaccessableList:
                    map_arr[j,i] = '0'
    
    for k in range(len(a)):
        for i in range(13):
            for j in range(13):
                if(coordinate_arr[j,i] == a[k]):
                    coordinate_list.append([j,i])
                    map_arr[j,i] = 'A'
                if(coordinate_arr[j,i] == dest_a[k]):
                    dest_coordinate_list.append([j,i])
                
    for k in b:
        for i in range(13):
            for j in range(13):
                if(coordinate_arr[j,i] == k):
                    map_arr[j,i] = 'B'

    for k in c:
        for i in range(13):
            for j in range(13):
                if(coordinate_arr[j,i] == k):
                    map_arr[j,i] = 'C'
    return map_arr,coordinate_arr,coordinate_list,dest_coordinate_list

# computes the valid move and make changes in board accordingly
def valid_move(map_arr, start, end,dest_coordinate_list):
    x1, y1 = start
    x_start, y_start = start
    x2, y2 = end
    moves = []
    simple_move = False
    hop = False
    swap_move = False
    # dictionary to store the direction of movement and moves made in that direction
    direction_dictionary={'NW':[],'W':[],'N':[],'E':[]}
    # check if start location and end location is not the same
    if x1 != x2 or y1 != y2:
        # append the initial location of peg
        moves.append(start)
        # heck if the peg is near destination and swap is possible
        if len(moves)==1:
            # swap move
            # to get the distance between initial position of peg and destination location
            initial_distance=getDistance([x1,y1],end)
            if (map_arr[x1-1,y1-1] not in ['0','1','A']) and ((x1-1)==x2) and ((y1-1)==y2):       #north west
                temp = map_arr[x1-1,y1-1]
                direction_dictionary['NW'].append([x1-1,y1-1])
                swap_move = True
            if (map_arr[x1, y1-1] not in ['0','1','A']) and (x1==x2) and ((y1-1)==y2):           #west
                temp = map_arr[x1, y1-1]
                direction_dictionary['W'].append([x1, y1-1])
                swap_move = True
            if (map_arr[x1-1,y1] not in ['0','1','A']) and ((x1-1)==x2) and (y1==y2):         #north
                temp = map_arr[x1-1,y1]
                direction_dictionary['N'].append([x1-1,y1])
                swap_move = True
            if (map_arr[x1, y1+1] not in ['0','1','A']) and (x1==x2) and ((y1+1)==y2):           #east
                temp = map_arr[x1, y1+1]
                direction_dictionary['E'].append([x1, y1+1])
                swap_move = True
        if swap_move == True and len(temp)!=0:
            final_moves=makeFinalMoves(direction_dictionary,end,initial_distance)
            if len(final_moves)!=0:
                moves.append(final_moves[0])
                direction_dictionary={'NW':[],'W':[],'N':[],'E':[]}
            else:
                final_moves=[]

        if swap_move==False:
            # loop to chcek if chain hop/simple hop possible from current location
            while True:
                # hop move
                initial_distance=getDistance([x1,y1],end)
                if (map_arr[x1-1,y1-1] not in ['0','1']): # north west
                    if map_arr[x1 - 2, y1 - 2] == '1':  
                        direction_dictionary['NW'].append(([x1 - 2, y1 - 2]))
                        hop = True
                    elif map_arr[x1 - 2, y1 - 2] in['B','C'] and [x1 - 2, y1 - 2] in dest_coordinate_list:
                        temp = map_arr[x1 - 2, y1 - 2]
                        direction_dictionary['NW'].append(([x1 - 2, y1 - 2]))
                        hop = True
                        swap_move = True

                if (map_arr[x1, y1-1] not in ['0','1']):# west
                    if map_arr[x1, y1-2] == '1':  
                        direction_dictionary['W'].append([x1, y1-2])
                        hop = True
                    elif map_arr[x1, y1-2] in['B','C'] and [x1, y1-2] in dest_coordinate_list:  
                        temp = map_arr[x1, y1-2]
                        direction_dictionary['W'].append([x1, y1-2])
                        hop = True
                        swap_move=True

                if (map_arr[x1-1, y1] not in ['0','1']):# north
                    if (map_arr[x1-2, y1] == '1'):  
                        direction_dictionary['N'].append([x1-2, y1])
                        hop = True
                    elif map_arr[x1-2, y1] in ['B','C'] and [x1-2, y1] in dest_coordinate_list:  
                        temp = map_arr[x1-2, y1]
                        direction_dictionary['N'].append([x1-2, y1])
                        hop = True
                        swap_move =True
                        

                if (map_arr[x1, y1+1] not in ['0','1']):#east
                    if (map_arr[x1, y1+2] == '1'):     
                        direction_dictionary['E'].append([x1, y1+2])
                        hop = True
                    elif map_arr[x1, y1+2] in ['B','C'] and [x1, y1+2] in dest_coordinate_list:  
                        temp = map_arr[x1, y1+2]
                        direction_dictionary['E'].append([x1, y1+2])
                        hop = True
                

                if hop == True:
                    final_moves=makeFinalMoves(direction_dictionary,end,initial_distance)
                    if len(final_moves)!=0:
                        x1,y1=final_moves[-1]
                        if [x1,y1] in moves:
                            break
                        moves.append(final_moves[0])
                        direction_dictionary={'NW':[],'W':[],'N':[],'E':[]}
                        hop=False
                    else:
                        final_moves=[]
                        break
                else:
                    break
            # check if simple move is possible from current location
            if len(moves)==1:
                initial_distance=getDistance([x1,y1],end)
                # simple move
                if (map_arr[x1 - 1, y1 - 1] == '1'):  # north west
                    direction_dictionary['NW'].append([x1 - 1, y1 - 1])
                    simple_move = True
                if (map_arr[x1, y1-1] == '1'):  # west
                    direction_dictionary['W'].append([x1, y1-1])
                    simple_move = True
                if (map_arr[x1-1, y1] == '1'):  # north
                    direction_dictionary['N'].append([x1-1, y1])
                    simple_move = True
                if (map_arr[x1, y1+1] == '1'):  # east
                    direction_dictionary['E'].append([x1, y1+1])
                    simple_move = True
            if simple_move == True:
                final_moves=makeFinalMoves(direction_dictionary,end,initial_distance)
                if len(final_moves)!=0:
                    moves.append(final_moves[0])
                else:
                    final_moves=[]
        # if no move possible from current location    
        if len(moves)==1:
            return []
        if swap_move ==True and len(temp)!=0:
            map_arr[x_start, y_start] = temp
        else:
            map_arr[x_start, y_start] = '1'
        # update the map values
        index=moves[-1]
        x,y=index
        map_arr[x,y] = 'A'
        return moves

# Evaluate the distances between the new location to move the peg and destination location
def makeFinalMoves(direction_dictionary,end,initial_distance):
    distance=[]
    distanceDic={}
    for element in direction_dictionary:
        if(len(direction_dictionary[element])>0):
            end_loc=direction_dictionary[element][-1]
            distance.append(getDistance(end_loc,end))
            distanceDic[element]=getDistance(end_loc,end)
    min_distance=np.min(distance)
    # compare the new distnace and initial distance
    if min_distance<initial_distance:
        for element in distanceDic:
            if distanceDic[element]==min_distance:
                final_moves=direction_dictionary[element]
    else:
        final_moves=[]
    return final_moves

# Returns list containing min distnace between destination and peg and 2D distance array 
def fetch_MinDistance(a_currentLoc,a_destinationLoc):
    min_distancePeg=[]
    distanceToPeg=[]
    temp=[]    
    for i in range(len(a_destinationLoc)):
        peg_d=[]
        x1,y1=a_destinationLoc[i]
        for j in range(len(a_currentLoc)):
            x2,y2 = a_currentLoc[j]
            d_temp = np.power((x2-x1),2)+np.power((y2-y1),2)
            d = np.sqrt(d_temp)
            peg_d.append(d)# one distance to all pegs d1-p1,p2..p6
        distanceToPeg.append(peg_d)# list of list of distance dn-pn
        min_d=np.min(peg_d)
        min_distancePeg.append(min_d)# list of min distance between dn-pn 
    return min_distancePeg,distanceToPeg

# Calculation of the euclidean distance between two peg locations(coordinates)
def getDistance(peg1,peg2):
    x1,y1 = peg1
    x2,y2 = peg2
    d_temp = np.power((x2-x1),2)+np.power((y2-y1),2)
    distance = np.sqrt(d_temp)
    return distance

# Updates list of pegs if destination has already been reached
def updatePegs(a_current,a_destination):
    for elemnet in a_current[:]:
        if(elemnet in a_destination):
            a_current.remove(elemnet)
            a_destination.remove(elemnet)            
    return a_current,a_destination

# Convert moves made in 2D array to coordinate system 
def get_Moves(coordinate_array,valid_moves):
    moves=[]
    for eachMove in valid_moves:
        x,y=eachMove        
        value=coordinate_array[x,y]
        value[0] = int(value[0])
        value[1] = int(value[1])
        moves.append(value)
    return moves

# Accepts the dictionary from server and return the next moves made by the peg back to the server
def move(dict,num_players):
    
    moves=[]
    # Split dictionary to diffrent pegs
    if num_players == 2:
        a = dict['A']
        b = dict['B']
        # get the current board layout
        map_arr,coordinate_arr,coordinate_list,dest_coordinate_list=getBoard_2(a,b)
    elif num_players == 3:
        a = dict['A']
        b = dict['B']
        c = dict['C']
        # get the current board layout
        map_arr,coordinate_arr,coordinate_list,dest_coordinate_list=getBoard_3(a,b,c)

    # if the 2nd row at destination gets filled before the the 1st row, 
    # make swap move
    if map_arr[0,3] in ['B','C','1']:
        temp = map_arr[0,3]
        if (map_arr[1,3]=='A' and map_arr[1,4]=='A') or map_arr[1,4]=='A':
            moves.append([1,4])
            map_arr[1,4]=temp
            moves.append([0,3])
            map_arr[0,3]='A'
                    
        elif map_arr[1,3]=='A':
            moves.append([1,3])
            map_arr[1,3]=temp
            moves.append([0,3])
            map_arr[0,3]='A'
        if len(moves)!=0:
            updatedMoves=get_Moves(coordinate_arr,moves)
            return updatedMoves

    coordinate_list,dest_coordinate_list=updatePegs(coordinate_list,dest_coordinate_list)
    distanceList,indexList=fetch_MinDistance(coordinate_list,dest_coordinate_list)
    # get min distance destination location
    min_dist_loccation=np.min(distanceList) #min dn-pn
    peg_index=np.where(distanceList==min_dist_loccation)[0][0]
    dest_loc=dest_coordinate_list[peg_index]#dn location
    # get list of distance
    destination_index=indexList[peg_index]#list of dn
    distanceList_sorted=np.sort(destination_index)
    # traverse the list to get which peg to move
    for distance in distanceList_sorted:
        dist_index=np.where(destination_index==distance)[0][0]
        start_loc=coordinate_list[dist_index]
        validMoves=valid_move(map_arr,start_loc,dest_loc,dest_coordinate_list)
        # if moves possible for any peg, break
        if len(validMoves)!=0:
            break
    # if no moves possible for any peg, swap values in 2nd row of destination 
    # location to break any deadlock situation. We expect this condition to happen rarely.
    if len(validMoves)==0:
        if map_arr[1,3]=='A' and map_arr[1,4]=='1':
            moves.append([1,3])
            map_arr[1,3]='1'
            moves.append([1,4])
            map_arr[1,4]='A'
        elif map_arr[1,4]=='A' and map_arr[1,3]=='1':
            moves.append([1,4])
            map_arr[1,4]='1'
            moves.append([1,3])
            map_arr[1,3]='A'
        if len(moves)!=0:
            updatedMoves=get_Moves(coordinate_arr,moves)
            return updatedMoves
    
    updatedMoves=get_Moves(coordinate_arr,validMoves)
    return updatedMoves
    
def agent_function(request_dict):
    print('I got the following request:')
    print(request_dict)
    num_players = len(request_dict)
    updated_dict = move(request_dict, num_players)
    return updated_dict


def run(config_file, action_function, single_request=False):
    logger = logging.getLogger(__name__)

    with open(config_file, 'r') as fp:
        config = json.load(fp)
    
    logger.info(f'Running agent {config["agent"]} on environment {config["env"]}')
    logger.info(f'Hint: You can see how your agent performs at {config["url"]}agent/{config["env"]}/{config["agent"]}')

    actions = []
    for request_number in itertools.count():
        logger.debug(f'Iteration {request_number} (sending {len(actions)} actions)')
        # send request
        response = requests.put(f'{config["url"]}/act/{config["env"]}', json={
            'agent': config['agent'],
            'pwd': config['pwd'],
            'actions': actions,
            'single_request': single_request,
        })
        if response.status_code == 200:
            response_json = response.json()
            for error in response_json['errors']:
                logger.error(f'Error message from server: {error}')
            for message in response_json['messages']:
                logger.info(f'Message from server: {message}')

            action_requests = response_json['action-requests']
            if not action_requests:
                logger.info('The server has no new action requests - waiting for 1 second.')
                time.sleep(1)  # wait a moment to avoid overloading the server and then try again
            # get actions for next request
            actions = []
            for action_request in action_requests:
                actions.append({'run': action_request['run'], 'action': action_function(action_request['percept'])})
        elif response.status_code == 503:
            logger.warning('Server is busy - retrying in 3 seconds')
            time.sleep(3)  # server is busy - wait a moment and then try again
        else:
            # other errors (e.g. authentication problems) do not benefit from a retry
            logger.error(f'Status code {response.status_code}. Stopping.')
            break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import sys
    run(sys.argv[1], agent_function, single_request=False)
