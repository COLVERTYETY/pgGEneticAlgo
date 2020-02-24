import numpy as np

GRID = []

def ingrid(x,y,ggrid):
    return (x>= 0 and x<len(ggrid[0]) and y>=0 and y<len(ggrid))

def init(width,height):
    global GRID
    GRID=[]
    for _y in range(height):
        tmp=[]
        for _x in range(width):
            tmp.append([])
        GRID.append(tmp)

def organise(arrayoflines,cellsize):
    global GRID
    for line in arrayoflines:
        x = int(line[0][0]/cellsize)
        y = int(line[0][1]/cellsize)
        if ingrid(x,y,GRID):
            GRID[y][x].append(line)

def getinreach(i,cellsize,ggrid):
    x = int(i.pos[0]/cellsize)
    y = int(i.pos[1]/cellsize)
    res=[]
    for i in range(-1,2):
        for j in range(-1,2):
            if ingrid(x+i,y+j,ggrid):
                res.extend(ggrid[y+j][x+i])
    return res
