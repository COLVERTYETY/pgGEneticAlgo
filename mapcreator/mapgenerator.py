
import numpy as np

GRID=np.zeros([10,10])
GEOMETRYGRID = []
GEOMETRYARRAY =[]
def initialize(width,height):
    global GRID
    GRID = np.zeros([height,width])

def toggle(mpos,cellsize,state):
    global GRID
    res = False
    x=mpos[0]//cellsize
    y=mpos[1]//cellsize
    if ingrid(x,y):
        if  GRID[y][x]!=state:
            GRID[y][x]=state
            res = True
    return res
def fullgeometry(cellsize):
    global GRID, GEOMETRYGRID , GEOMETRYARRAY
    #shape of line x1,y1 x2,y2
    #[[x1,y1],[x2,y2]]
    GEOMETRYGRID = GRID.copy().tolist()
    GEOMETRYARRAY=[]
    for y in range(len(GRID)):
        for x in range(len(GRID[0])):
            GEOMETRYGRID[y][x]=tile(GRID[y][x]) 
    for y in range(len(GEOMETRYGRID)):
        for x in range(len(GEOMETRYGRID[0])):
            if GEOMETRYGRID[y][x].state!=0: 
                if ingrid(x,y-1):#check north
                    if GEOMETRYGRID[y-1][x].state==0:#if no northern neighbour
                        GEOMETRYGRID[y][x].northernborder=[[x*cellsize,y*cellsize],[(x+1)*cellsize,(y)*cellsize]]#no west border so we create the border
                        GEOMETRYARRAY.append(GEOMETRYGRID[y][x].northernborder)# add the new border to the border list
                if ingrid(x,y+1):#check south
                    if GEOMETRYGRID[y+1][x].state==0:#if no southern neighbour
                        GEOMETRYGRID[y][x].southernborder=[[x*cellsize,(y+1)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                        GEOMETRYARRAY.append(GEOMETRYGRID[y][x].southernborder)# add the new border to the border list
                if ingrid(x-1,y):#check west
                    if GEOMETRYGRID[y][x-1].state==0:#if no western neighbour
                        GEOMETRYGRID[y][x].westernborder=[[(x)*cellsize,(y)*cellsize],[(x)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                        GEOMETRYARRAY.append(GEOMETRYGRID[y][x].westernborder)# add the new border to the border list
                if ingrid(x+1,y):#check east
                    if GEOMETRYGRID[y][x+1].state==0:#if no western neighbour
                        GEOMETRYGRID[y][x].easternborder=[[(x+1)*cellsize,(y)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                        GEOMETRYARRAY.append(GEOMETRYGRID[y][x].easternborder)# add the new border to the border list
def generategeometry(cellsize):
    global GRID, GEOMETRYGRID , GEOMETRYARRAY
    #shape of line x1,y1 x2,y2
    #[[x1,y1],[x2,y2]]
    GEOMETRYGRID = GRID.copy().tolist()
    GEOMETRYARRAY=[]
    for y in range(len(GRID)):
        for x in range(len(GRID[0])):
            GEOMETRYGRID[y][x]=tile(GRID[y][x])
    for y in range(len(GEOMETRYGRID)):
        for x in range(len(GEOMETRYGRID[0])):
            if GEOMETRYGRID[y][x].state==1: 
                if ingrid(x,y-1):#check north
                    if GEOMETRYGRID[y-1][x].state!=1:#if no northern neighbour
                        if ingrid(x-1,y):#check west
                            if GEOMETRYGRID[y][x-1].state==1:#if there is a western neighbour
                                if not isinstance(GEOMETRYGRID[y][x-1].northernborder,int):#if our nighbour has a northernborder
                                    GEOMETRYGRID[y][x].northernborder=GEOMETRYGRID[y][x-1].northernborder# his border is my border 
                                    GEOMETRYGRID[y][x].northernborder[1][0]+=cellsize # stretch the border
                                else:
                                    GEOMETRYGRID[y][x].northernborder=[[x*cellsize,y*cellsize],[(x+1)*cellsize,(y)*cellsize]]#no west border so we create the border
                                    GEOMETRYARRAY.append(GEOMETRYGRID[y][x].northernborder)# add the new border to the border list
                            else:
                                GEOMETRYGRID[y][x].northernborder=[[x*cellsize,y*cellsize],[(x+1)*cellsize,(y)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].northernborder)# add the new border to the border list
                        else:
                                GEOMETRYGRID[y][x].northernborder=[[x*cellsize,y*cellsize],[(x+1)*cellsize,(y)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].northernborder)# add the new border to the border list
                if ingrid(x,y+1):#check south
                    if GEOMETRYGRID[y+1][x].state!=1:#if no southern neighbour
                        if ingrid(x-1,y):#check west
                            if GEOMETRYGRID[y][x-1].state==1:#if there is a western neighbour
                                if not isinstance(GEOMETRYGRID[y][x-1].southernborder,int):#if our nighbour has a southern
                                    GEOMETRYGRID[y][x].southernborder=GEOMETRYGRID[y][x-1].southernborder# his border is my border 
                                    GEOMETRYGRID[y][x].southernborder[1][0]+=cellsize # stretch the border
                                else:
                                    GEOMETRYGRID[y][x].southernborder=[[x*cellsize,(y+1)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                    GEOMETRYARRAY.append(GEOMETRYGRID[y][x].southernborder)# add the new border to the border list
                            else:
                                GEOMETRYGRID[y][x].southernborder=[[x*cellsize,(y+1)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].southernborder)# add the new border to the border list
                        else:
                                GEOMETRYGRID[y][x].southernborder=[[x*cellsize,(y+1)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].southernborder)# add the new border to the border list
                if ingrid(x-1,y):#check west
                    if GEOMETRYGRID[y][x-1].state!=1:#if no western neighbour
                        if ingrid(x,y-1):#check north
                            if GEOMETRYGRID[y-1][x].state==1:#if there is a northern neighbour
                                if not isinstance(GEOMETRYGRID[y-1][x].westernborder,int):#if our nighbour has a west
                                    GEOMETRYGRID[y][x].westernborder=GEOMETRYGRID[y-1][x].westernborder# his border is my border 
                                    GEOMETRYGRID[y][x].westernborder[1][1]+=cellsize # stretch the border
                                else:
                                    GEOMETRYGRID[y][x].westernborder=[[(x)*cellsize,(y)*cellsize],[(x)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                    GEOMETRYARRAY.append(GEOMETRYGRID[y][x].westernborder)# add the new border to the border list
                            else:
                                GEOMETRYGRID[y][x].westernborder=[[(x)*cellsize,(y)*cellsize],[(x)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].westernborder)# add the new border to the border list
                        else:
                                GEOMETRYGRID[y][x].westernborder=[[(x)*cellsize,(y)*cellsize],[(x)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].westernborder)# add the new border to the border list
                if ingrid(x+1,y):#check east
                    if GEOMETRYGRID[y][x+1].state!=1:#if no western neighbour
                        if ingrid(x,y-1):#check north
                            if GEOMETRYGRID[y-1][x].state==1:#if there is a northern neighbour
                                if not isinstance(GEOMETRYGRID[y-1][x].easternborder,int):#if our nighbour has a west
                                    GEOMETRYGRID[y][x].easternborder=GEOMETRYGRID[y-1][x].easternborder# his border is my border 
                                    GEOMETRYGRID[y][x].easternborder[1][1]+=cellsize # stretch the border
                                else:
                                    GEOMETRYGRID[y][x].easternborder=[[(x+1)*cellsize,(y)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                    GEOMETRYARRAY.append(GEOMETRYGRID[y][x].easternborder)# add the new border to the border list
                            else:
                                GEOMETRYGRID[y][x].easternborder=[[(x+1)*cellsize,(y)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].easternborder)# add the new border to the border list
                        else:
                                GEOMETRYGRID[y][x].easternborder=[[(x+1)*cellsize,(y)*cellsize],[(x+1)*cellsize,(y+1)*cellsize]]#no west border so we create the border
                                GEOMETRYARRAY.append(GEOMETRYGRID[y][x].easternborder)# add the new border to the border list

    GEOMETRYGRID=[]

    
def ingrid(x,y):
    global GRID
    if x >=0 and x <len(GRID[0]) and y>=0 and y<len(GRID):
        return True
    else:
        return False

def savemaparray(name):
    global GRID
    np.save(name,GRID.astype(int))

def megasave(dataarray,name):
    np.save("../maps/"+name,dataarray)
    

def savegeometry(name):
    global GEOMETRYARRAY
    tmp = name.find(".npy")
    tmp = name[:tmp]
    tmp+="GEO.npy"
    np.save(tmp,np.asarray(GEOMETRYARRAY))

def loadgeometry(name):
    global GEOMETRYARRAY
    GEOMETRYARRAY = np.load(name)

def megaload(name):
    global GRID , GEOMETRYARRAY
    dataarray = np.load(name,allow_pickle = True)
    GRID = dataarray[6]
    GEOMETRYARRAY = dataarray[7]
    # 0 is cellsize
    # 1 is max
    # 2 is startx
    # 3 is starty
    # 4 is startvectx
    # 5 is startvecty
    # 6 is GRID
    # 7 is GRID GEO
    return (name,dataarray[0],dataarray[1],dataarray[2],dataarray[3],dataarray[4],dataarray[5])

def loadmaparray(name):
    global GRID
    GRID = np.load(name)


class tile(object):
    def __init__(self,state):
        self.state=state
        self.northernborder=0
        self.southernborder=0
        self.westernborder=0
        self.easternborder=0
        #shape of line x1,y1 x2,y2
        #[[x1,y1],[x2,y2]]