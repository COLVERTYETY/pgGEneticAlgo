import pygame as pg
import numpy as np
from part import *
import spatialhash
import ray
import psutil
pg.init() # pylint: disable=no-member
WIDTH=800
HEIGHT=700
screen = pg.display.set_mode((WIDTH,HEIGHT))
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
done = False

theARRY=[]
being.SURFACE=screen

MAPGEO = np.load("./mapGEO.npy")
MAP = np.load("./map.npy")
CELLSIZE = 20
GLOBALANTENNALENGTH=80
startx = 100
starty = 450


def drawmap(mapgrid):
    global CELLSIZE
    for y in range(len(mapgrid)):
        for x in range(len(mapgrid[y])):
            if mapgrid[y][x]==1:
                pg.draw.rect(screen,(0,0,255),pg.Rect(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))

def drawgeometry(linearr):
    for line in linearr:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(screen,(255,0,0),(x1,y1),(x2,y2),1)

def splitter(length, i,n):
    (k,m) = divmod(length, n)
    low = i * k + min(i, m)
    high = (i + 1) * k + min(i + 1, m)
    return (low,high)

@ray.remote
def thetask(objarray,mapgrid,mapgeometry,antennalength,sizeofcell):
    for i in objarray:
        i.apply()
        i.antennainput.fill(1)
        for j in spatialhash.getinreach(i,antennalength):
            i.readantenna(j)
        if  not i.inmapgrid(mapgrid,sizeofcell):
            i.pos=np.array([100,450])
            i.vel = np.array([np.random.randint(0,4)-2,np.random.randint(0,4)-2])
    return len(objarray)

amount=50
num_cpus = psutil.cpu_count(logical=False)
for _i in range(num_cpus):
    tmp=[]
    for _j in range(amount):
        tmp.append(being(startx,starty))
    theARRY.append(tmp)

print("total amount  = ",amount*num_cpus)
print("calculating spatial hash::")
spatialhash.init(int(WIDTH/GLOBALANTENNALENGTH),int(HEIGHT/GLOBALANTENNALENGTH))
spatialhash.organise(MAPGEO,GLOBALANTENNALENGTH)
print("done")
print("number of cores::",num_cpus)
print("starting ray::")
ray.init(num_cpus=num_cpus)
print("done")
print("moving data to shared memory::")
theARRY_id = []
for i in theARRY:
    theARRY_id.append(ray.put(i))
MAP_id = ray.put(MAP)
MAPGEO_ID = ray.put(MAPGEO)
print("done")

while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
        
        active = [thetask.remote(i,MAP_id,MAPGEO_ID,GLOBALANTENNALENGTH,CELLSIZE) for i in theARRY_id]
        screen.fill((0,0,0))
        drawmap(MAP)
        drawgeometry(MAPGEO)
        for i in theARRY:
            for j in i:
                j.draw()
        result= ray.get(active)
        print(result)
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick(30)
        pg.display.flip()
    