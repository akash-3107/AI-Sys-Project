import pandas as pd
from datetime import datetime
import csv
import numpy as np
import heapq
import calendar

# Function to compute the problem attributes
def get_problem_attributes(file,index):
  problem_df=pd.read_csv(file)
  row=problem_df.loc[problem_df['ProblemNo'] == index]
  fromStation = row['FromStation'][index]
  toStation = row['ToStation'][index]
  schedule = row['Schedule'][index]
  costfn=row['CostFunction'][index]
  return[fromStation,toStation,schedule,costfn]

# Function for building the graph as per the cost function
def read_csv_get_edges(file,costfn):
  schedule_df=pd.read_csv(file,usecols=['Train No.','islno','station Code','Arrival time','Departure time','Distance'])
  schedule_df = schedule_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
  scheduleList = schedule_df.values.tolist()
  default_date=[1,1,1]
  atday = default_date[0]
  visitedStation=[]
  stationDetails = []
  graph_src = []
  graph_dest = []
  for i in range(len(scheduleList)-2):
    if (i%1000)==0:
      print(i)
    tempEdge_from=[]
    sc = scheduleList[i][2]
    trainNo = scheduleList[i][0].replace("'","")
    toTrain = scheduleList[i+1][0].replace("'","")
    sc_to = scheduleList[i+1][2]
    islno = scheduleList[i][1]
    toIslno = scheduleList[i+1][1]
    dt1 = scheduleList[i][5]
    dt2 = scheduleList[i+1][5]
    
    if sc in graph_src:
      index = graph_src.index(sc)
      tempEdge_from = graph_dest[index]
    if sc_to in graph_src:
      index = graph_src.index(sc_to)   

    
    stationD1 = toTrain+','+scheduleList[i+1][3]+','+str(toIslno)+','+str(dt2)
    atTrain1 = scheduleList[i][3].replace("'","")
    atTrain2 = scheduleList[i+1][3].replace("'","")
    t1_temp = atTrain1.split(':')
    t2_temp = atTrain2.split(':')
                    
    t1=[int(t1_temp[0]),int(t1_temp[1]),int(t1_temp[2])]
    t2=[int(t2_temp[0]),int(t2_temp[1]),int(t2_temp[2])]
    if int(t1[0])>int(t2[0]):
      t1datetime = datetime(default_date[2],default_date[1],atday,t1[0],t1[1],t1[2])
      atday=atday+1
      t2datetime = datetime(default_date[2],default_date[1],atday,t2[0],t2[1],t2[2]) 
    else:
      atday=atday
      t1datetime = datetime(default_date[2],default_date[1],atday,t1[0],t1[1],t1[2])
      t2datetime = datetime(default_date[2],default_date[1],atday,t2[0],t2[1],t2[2])
    
    
    
    if trainNo==toTrain:
          visitedStation.append(sc_to)
          stationDetails.append(stationD1)
          if costfn == 'stops':
            connection_from = [sc_to,[1,islno,toIslno,trainNo,toTrain]]
            
          elif costfn == 'distance':
            distance = dt2-dt1
            connection_from = [sc_to,[distance,islno,toIslno,trainNo,toTrain]]

          elif costfn == 'price':
            atTrain1 = scheduleList[i][3].replace("'","")
            atTrain2 = scheduleList[i+1][3].replace("'","")
            t1 = atTrain1.split(':')
            t2 = atTrain2.split(':')
            
            t1=[int(t1[0]),int(t1[1]),int(t1[2])]
            t2=[int(t2[0]),int(t2[1]),int(t2[2])]
            num_days = calendar.monthrange(default_date[0],default_date[1])[1]
            if atday >= num_days: 
                  default_date[1]+=1
                  atday=1
            if int(t1[0])>int(t2[0]):
              t1datetime = datetime(default_date[2],default_date[1],atday,t1[0],t1[1],t1[2])
              atday=atday+1
              t2datetime = datetime(default_date[2],default_date[1],atday,t2[0],t2[1],t2[2]) 
            else:
              t1datetime = datetime(default_date[2],default_date[1],atday,t1[0],t1[1],t1[2])
              t2datetime = datetime(default_date[2],default_date[1],atday,t2[0],t2[1],t2[2])
              
            dayt1=t1datetime.day
            dayt2=t2datetime.day
            
            wt = dayt2-dayt1
            
            connection_from = [sc_to,[wt,islno,toIslno,trainNo,toTrain,t1datetime,t2datetime]]
          
          elif costFunction == 'arrivaltime':
            depttimet1=scheduleList[i][4].replace("'","")
            depttimet2=scheduleList[i+1][4].replace("'","")            
            t2hh=t2datetime.hour
            t2min=t2datetime.minute
            t2sec=t2datetime.second
            tempDefault=datetime(1,1,1,0,0,0)
            tempArrivalt2 = datetime(1,1,1,t2hh,t2min,t2sec)
            timeSec = (tempArrivalt2-tempDefault)
            timeSec=timeSec.total_seconds()
            
            connection_from = [sc_to,[timeSec,islno,toIslno,trainNo,toTrain,t1datetime,t2datetime,depttimet1,depttimet2]]
          
          if tempEdge_from==[]:
            tempEdge_from.append(connection_from)
            graph_src.append(sc)
            graph_dest.append(tempEdge_from)
          else:
            tempEdge_from.append(connection_from)
            index = graph_src.index(sc)
            graph_dest[index] = tempEdge_from

    else:
      atday = default_date[0]
      default_date[1] = 1
      continue
    
    tempVS=np.array(visitedStation)
    index = np.where(tempVS==sc)
  
  return graph_src,graph_dest

# Function to compute the shortest path for a graph according to a cost function
def dijkstra(graph_src, graph_dest, start, end,costFunction,arrivalTime):
    # Initialize distances and visited set
    n = len(graph_src)
    start_index = graph_src.index(start)
    end_index = graph_src.index(end)
    distances = [float('infinity')] * n
    distances[start_index] = 0
    visited = []
    visited_sc=[]
    
    previous = [None] * n
    # Priority queue to keep track of the next vertex to explore
    priority_queue = [(0, start_index,[])]
    
    while priority_queue:
        # Get the vertex with the smallest distance
        current_distance, current_vertex, trainList = heapq.heappop(priority_queue)
 
        # Stop if the end vertex is reached
        if current_vertex == end_index:
            path = []
            connection = []
            shortest_path = []

            while current_vertex is not None:
                path.insert(0, current_vertex)
                if previous[current_vertex] is not None:
                  shortest_path.insert(0,previous[current_vertex][1][0][0])
                  connection.insert(0,previous[current_vertex][1][0])
                  current_vertex = previous[current_vertex][0]
                else:
                  current_vertex = previous[current_vertex]
                
            return distances[end_index], path ,connection, shortest_path
 
        # Skip if the vertex has already been visited
        if current_vertex in visited:
            continue
 
        # Update the distance for neighboring vertices
        a = graph_dest[current_vertex]
        
        if costFunction == 'arrivaltime' and current_vertex==start_index:
          tempList=[]
          tempData=[]
          arrivalTime=arrivalTime.split(':')
          
          arrivalTime = [int(arrivalTime[0]),int(arrivalTime[1]),int(arrivalTime[2])]
          
          arrivalTime=datetime(1,1,1,arrivalTime[0],arrivalTime[1],arrivalTime[2])
        
        for i in range(len(a)):
            wt=0
            waitTime=0
            neighbor = a[i][0]
            train1=a[i][1][3]
            train2=a[i][1][4]
            if costFunction in ['price','arrivaltime']:
              if current_vertex == start_index:
                  trainList= [a[i][1][4],a[i][1][6],a[i],a[i][1][5]]
              else:
                if a[i][0] in visited_sc:
                  continue
            
            if costFunction=='price':
              att1=a[i][1][5]
              att2=a[i][1][6]
              if train1 not in trainList and trainList[1].hour>att2.hour:
                wt=wt+1
              else:
                if train1 not in trainList:
                  wt=wt+1
                if trainList[1].hour>att2.hour:
                  wt=wt+1
              
              if att1.day!=att2.day:
                wt=wt+1
            
            if costFunction=='arrivaltime':
              att1=a[i][1][5]
              att2=a[i][1][6]
              dd=[1,1,1]
              tempatHH=trainList[1].hour
              tempatMM=trainList[1].minute
              tempatSS=trainList[1].second
              tempat=datetime(dd[0],dd[1],dd[2],tempatHH,tempatMM,tempatSS)
              arrivalT=a[i][1][7].split(':')
              arrivalTHH=int(arrivalT[0])
              arrivalTMM=int(arrivalT[1])
              arrivalTSS=int(arrivalT[2])
              arrivalT=datetime(dd[0],dd[1],dd[2],arrivalTHH,arrivalTMM,arrivalTSS)
              waitTime=(arrivalT-tempat).total_seconds()
              
              tempatt1=datetime(1,1,1,att1.hour,att1.minute,att1.second)
              tempatt2=datetime(1,1,1,att2.hour,att2.minute,att2.second)
              
              if current_vertex != start_index:
                wt=int(waitTime)
                if wt<600 and train1!=trainList[0]:
                  wt = wt+86400
                
                weight = a[i][1][0]-trainList[2][1][0]
              
              else:
                tD=(tempatt1-arrivalTime).total_seconds()
                
                if tD<0:
                  wt = 86400+tD

                weight = (tempatt2-tempatt1).total_seconds()

              if weight<0:
                weight=weight+86400
            
              weight = weight+wt
             
            if costFunction=='arrivaltime':
              distance = weight+current_distance
            
            else:
              weight = a[i][1][0]+wt
              distance = current_distance + weight
            
            if neighbor in graph_src:
              neighbor_index = graph_src.index(neighbor)
            else:
              continue
            
            # If a shorter path is found, update the distance
            if distance < distances[neighbor_index]:  
              distances[neighbor_index] = distance
              previous[neighbor_index] = [current_vertex,[a[i]]]
              if costFunction in ['price','arrivaltime']:
                heapq.heappush(priority_queue, (distance, neighbor_index,[train2,att2,a[i],att1]))
              else:
                heapq.heappush(priority_queue, (distance, neighbor_index,[]))
        # Mark the current vertex as visited
        visited.append(current_vertex)
        visited_sc.append(graph_src[current_vertex])

    # If the end vertex is not reached, return infinity
    return float('infinity')

# Function to create the solution file 
def create_solution_file(filename,solution_list):
  s = open(filename,'w',newline='')
  writer = csv.writer(s)
  count = 0
  for sol in solution_list:
    if count == 0:
      header = ['ProblemNo','Connection','Cost']
      writer.writerow(header)
    writer.writerow(sol)
    count += 1
  s.close()


# Function to create the connection from the shortest path
def createConnection(pathConnection):
  conn = ''
  src_islno = str(pathConnection[0][1][1])
  src_tno = pathConnection[0][1][3]
  conn += src_tno + ' : ' + src_islno + ' -> '
  old_src_tno = src_tno
  old_dest_islno = ''
  for i in pathConnection:
    new_src_tno = i[1][3]
    new_dest_islno = i[1][2]
    if new_src_tno == old_src_tno:
      old_src_tno = new_src_tno
      old_dest_islno = new_dest_islno
      continue
    else:
      if old_dest_islno != '':
        conn += str(old_dest_islno) + ' ; '
      conn += new_src_tno + ' : ' + str(i[1][1]) + ' -> '
      old_src_tno = new_src_tno
      old_dest_islno = new_dest_islno
  conn += str(i[1][2])
  return conn

# Function to compute the cost of the connection depending on the cost function
def cost_function(connection,costFunction,arrivalTime):
  if costFunction == 'price':
    cost = 1
    for i in range(len(connection)):
      if i<len(connection)-1:
        if connection[i][1][3]!=connection[i+1][1][3]:
          cost=cost+1
        elif connection[i][1][3]==connection[i+1][1][3] and connection[i][1][5].day != connection[i][1][6].day:
          cost=cost+1
      else:
        if connection[i][1][5].day!=connection[i][1][6].day:
          cost = cost + 1
  
  elif costFunction == 'arrivaltime':
    arrivalTime = arrivalTime.split(':')
    hourAT = int(arrivalTime[0])
    minuteAT = int(arrivalTime[1])
    tmp = connection[0][1][5]
    hourConnection = tmp.hour
    minuteConnection = tmp.minute
    if hourAT<hourConnection or (hourAT==hourConnection and minuteAT<minuteConnection):
      count = 0
    else:
      count = 1
      
    for i in range(len(connection)):
      
      if (i+1) < len(connection):
        if connection[i][1][6].hour > connection[i+1][1][6].hour:
          count += 1
        if connection[i][1][3] != connection[i+1][1][3] and connection[i][1][5].hour > connection[i][1][6].hour:
          count += 1

    count = str(count)
    arrivaltime = connection[i][1][6]
    arrivalHoursInt = arrivaltime.hour
    arrivalMinInt = arrivaltime.minute
    arrivalMins = str(arrivaltime.minute)
    arrivalHours = str(arrivaltime.hour)
    if arrivalHoursInt < 10:
      arrivalHours = '0' + arrivalHours
 
    if arrivalMinInt < 10:
      arrivalMins = '0' + arrivalMins
    arrivaltime = arrivaltime.day
    cost = '0' + count + ':' + arrivalHours + ':' + arrivalMins + ':00'
  
  else:
    cost = 0
    for elemnet in connection:
      cost = cost+elemnet[1][0]
  return cost


if __name__ == '__main__':
  
  problem_file = 'problems.csv'
  solution_file = 'solutions.csv'
  results = pd.read_csv(problem_file) 
  solutions = []
  create_graph = True
  count = 0
  for problem_index in range(len(results)):
    print(problem_index)
    
    if problem_file == 'problems.csv' and problem_index in [5,44,67]:
      continue

    if problem_file == 'example-problems.csv' and problem_index in [64,66]:
      continue

    fromStation, toStation, schedule, costFunction = get_problem_attributes(problem_file,problem_index)
    
    if 'arrivaltime' in costFunction:
      temp = costFunction.split(' ')[0]
      arrivalTime = costFunction.split(' ')[1]
      costFunction=temp
    else:
      arrivalTime = ''

    if create_graph == True:
      graph_src,graph_dest = read_csv_get_edges(schedule,costFunction)
      create_graph = False

    distance,path,conn,sp = dijkstra(graph_src,graph_dest, fromStation, toStation,costFunction,arrivalTime)
    cost = cost_function(conn,costFunction,arrivalTime)
    connection = createConnection(conn)
    solutions.append([problem_index,connection,cost])
    if problem_index in [9,19,29,39,49,59,69]:
      create_graph = True

  create_solution_file(solution_file,solutions)