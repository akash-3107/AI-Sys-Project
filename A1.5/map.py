import string 
import os
import numpy as np

class Map():
    def __init__(self,col,row,fname,filepath):
        self.col = col
        self.row = row
        self.filename = fname
        self.filepath = filepath
        self.map = None

    def adjTiles(self):
        adjs = ''
        if self.col > 1 and self.row > 1:  # rectangle
            for y in range(0, self.row+1):
                for x in range(0, self.col+2):
                    adjs += '(adjSouth t-{0}-{1} t-{2}-{3}) (adjNorth t-{2}-{3} t-{0}-{1})\n   '. \
                        format(x, y, x, y + 1)
                    if x < (self.col+1):
                        adjs += '(adjEast t-{0}-{1} t-{2}-{3}) (adjWest t-{2}-{3} t-{0}-{1})\n   '. \
                            format(x, y, x + 1, y)
            
            for x in range(0,self.col+1):
                adjs += '(adjEast t-{0}-{1} t-{2}-{3}) (adjWest t-{2}-{3} t-{0}-{1})\n   '. \
                    format(x, (self.row+1), x + 1, (self.row+1))
                
            for x in range(0, self.col+1):  # connect bottom row
                adjs += '(adjEast t-{0}-{1} t-{2}-{3}) (adjWest t-{2}-{3} t-{0}-{1})\n   '. \
                    format(x, self.row, x + 1, self.row)

            for y in range(0, self.row+1):  # connect last row
                adjs += '(adjSouth t-{0}-{1} t-{2}-{3}) (adjNorth t-{2}-{3} t-{0}-{1})\n   '. \
                    format(self.col, y, self.col, y + 1)
            
        elif self.col == 1 and self.row > 1:  # 1 column
            for y in range(0, self.row+1):
                adjs += '(adjSouth t-{0}-{1} t-{2}-{3}) (adjNorth t-{2}-{3} t-{0}-{1})\n   '. \
                    format(1, y, 1, y + 1)
        elif self.col > 1 and self.row == 1:  # 1 row
            for x in range(0, self.col+1):
                adjs += '(adjEast t-{0}-{1} t-{2}-{3}) (adjWest t-{2}-{3} t-{0}-{1})\n   '. \
                    format(x, 1, x + 1, 1)
        return adjs

    def wallConstraints(self):
        f = open(self.filepath, 'r')
        lines = f.readlines()
        self.map=np.ones(shape=(self.row,self.col), dtype=np.str_)
        walls = ''
        for i in range(self.map.shape[0]):#row
            for j in range(self.map.shape[1]):#column
                self.map[i][j]=lines[i][j]
               
        for y in range(0, self.row):
                for x in range(0, self.col):
                    if self.map[y][x] == 'X':
                        walls += '(at X t-' + str(x+1) + '-' + str(y+1) + ')\n'
        return walls           

    def agentConstraints(self):
        if self.map is not None:
            start = np.where(self.map == 'S')
            return '(at S t-' + str(start[1][0]+1) + '-' + str(start[0][0]+1) + ')\n'

    def emptyConstraints(self):
        empty_str = ''
        if self.map is not None:
            for y in range(0, self.row):
                for x in range(0, self.col):
                    if self.map[y][x] == ' ':
                        empty_str += '(at E t-' + str(x+1) + '-' + str(y+1) + ')\n'
            
            for x in range(0,self.col+1):
                empty_str += '(at B t-' + str(x+1) + '-0' +')\n'
            
            for v in range(0,self.row+1):
                empty_str+= '(at B t-' + str(x+1) + '-' + str(v+1) + ')\n'
            
            for x in range(0, self.row+1):  # connect bottom row
                empty_str += '(at B t-0' + '-'+ str(x+1) +')\n'
                
            for z in range(0,self.col+1):
                empty_str += '(at B t-' + str(z+1) + '-' + str(x+1) + ')\n'
            return empty_str   
            
    def crateConstraints(self):
        crate_str = ''
        if self.map is not None:
            crate_list = np.where(self.map == 'C')
            c = crate_list[1]
            r = crate_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    crate_str += '(at C t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return crate_str
            else:
                return ''
        
    def halfCrateConstraints(self):
        half_crate_str = ''
        if self.map is not None:
            halfcrate_list = np.where(self.map == 'H')
            c = halfcrate_list[1]
            r = halfcrate_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    half_crate_str += '(at H t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return half_crate_str
            else:
                return ''

    def arrowConstraints(self):
        arrow_str = ''
        if self.map is not None:
            arrow_list = np.where(self.map == 'A')
            c = arrow_list[1]
            r = arrow_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    arrow_str += '(at A t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return arrow_str
            else:
                return ''
    
    def fireworksConstraints(self):
        fireworks_str = ''
        if self.map is not None:
            fireworks_list = np.where(self.map == 'F')
            c = fireworks_list[1]
            r = fireworks_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    fireworks_str += '(at F t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return fireworks_str
            else:
                return ''

    def wumpusConstraints(self):
        wumpus_str = ''
        if self.map is not None:
            wumpus_list = np.where(self.map == 'W')
            c = wumpus_list[1]
            r = wumpus_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    wumpus_str += '(at W t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return wumpus_str
            else:
                return ''
            
    def pitConstraints(self):
        pit_str = ''
        if self.map is not None:
            pit_list = np.where(self.map == 'P')
            c = pit_list[1]
            r = pit_list[0]
            if len(c)!=0 and len(r)!=0:
                for i in range(len(c)):
                    pit_str += '(at P t-'+str(c[i]+1)+'-'+str(r[i]+1)+')\n'
                return pit_str
            else:
                return ''

    def goalConstraints(self):
        goal_list = []
        goal_str = ''
        for y in range(0, self.row+2):
                for x in range(0, self.col+2):
                    if y==0 or y==9 or x==0 or x==13:
                        goal_list.append([x,y])
                        goal_str += '(at S t-'+str(x)+'-'+str(y)+')\n'
        return goal_str

    def generateMapPddl(self):
        values = {'problemName': 'problemName',
                  'problemDomain': 'problemDomain',
                  'tiles': 'tiles',
                  'adjTiles': 'adjTiles',
                  'walls' : 'walls',
                  'agents' : ' agents',
                  'empty' : 'empty',
                  'goal' : 'goal',
                  'crate' : 'crate',
                  'halfcrate' : 'halfcrate',
                  'arrow' : 'arrow',
                  'fireworks' : 'fireworks',
                  'wumpus' : 'wumpus',
                  'pit' : 'pit'
                  }
        
        pddl = string.Template(
            """(define (problem $problemName)
  (:domain $problemDomain)
  (:objects
   $tiles - tile
   S - agent
   X - wall
   C - crate
   H - halfcrate
   A - arrow
   F - fireworks
   W - wumpus
   P - pit
   E - empty
   B - boundary
   HP - halfpit
  )
  (:init
   $adjTiles
   $walls
   $empty
   $agents
   $crate
   $halfcrate
   $arrow
   $fireworks
   $wumpus
   $pit
  )
  (:goal (or $goal))
    )
""")
        values['problemName'] = self.filename
        values['problemDomain'] = 'wumpus_cave'
        values['adjTiles'] = self.adjTiles()
        values['tiles'] = " ".join(['t-{0}-{1}'.format(y,x) for y in range(0, self.col + 2) for x in range(0, self.row + 2)])

        values['walls'] = self.wallConstraints()
        values['empty'] = self.emptyConstraints()
        values['agents'] = self.agentConstraints()
        
        values['goal'] = self.goalConstraints()
        if self.crateConstraints()!='':
            values['crate'] = self.crateConstraints()
        if self.halfCrateConstraints()!='':
            values['halfcrate'] = self.halfCrateConstraints()
        if self.arrowConstraints()!='':
            values['arrow'] = self.arrowConstraints()
        if self.fireworksConstraints()!='':
            values['fireworks'] = self.fireworksConstraints()
        if self.wumpusConstraints()!='':
            values['wumpus'] = self.wumpusConstraints()
        if self.pitConstraints()!='':
            values['pit'] = self.pitConstraints()
        return pddl.substitute(values)
    
    def createPddlFile(self):
        fn = os.path.join('map-pddl',self.filename)
        pddlFile = open(fn +'.pddl','w')
        pddl = self.generateMapPddl()
        pddlFile.write(pddl)

if __name__ == '__main__':
    directory = 'example-maps'
    dir=os.listdir(directory)
    dir.sort()
    for file in dir:
        fname = os.path.join(directory,file)
        m = Map(12,8,file.split('.')[0],fname)
        m.createPddlFile()
