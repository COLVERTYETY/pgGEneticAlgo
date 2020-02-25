import pygame as pg
import numpy as np
from part import *
import spatialhash
import ray
import psutil
import copy
from colorsys import hsv_to_rgb
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
GLOBALANTENNALENGTH=40
startx = 100
starty = 450
MAX=1

def drawmap(mapgrid,mmax):
    global CELLSIZE
    for y in range(len(mapgrid)):
        for x in range(len(mapgrid[y])):
            if mapgrid[y][x]!=0:
                h = (mapgrid[y][x]/mmax)*359
                s=0.80
                v = 1
                colo = hsv_to_rgb(h,s,v)
                (e,r,t) = colo
                colo = (255*e,255*r,255*t)
                pg.draw.rect(screen,colo,pg.Rect(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))

def drawgeometry(linearr):
    for line in linearr:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(screen,(255,0,0),(x1,y1),(x2,y2),1)

def draw(part):
        pg.draw.circle(screen,(0,255,0),(int(part.pos[0]),int(part.pos[1])), being.radius)

def splitter(length, i,n):
    (k,m) = divmod(length, n)
    low = i * k + min(i, m)
    high = (i + 1) * k + min(i + 1, m)
    return (low,high)

@ray.remote
def thetask(objarray,mapgrid,mapgeometry,ggrid,antennalength,sizeofcell):
    newtmp = copy.deepcopy(objarray)
    for i in newtmp:
        i.apply()
        i.antennainput.fill(1)
        for j in spatialhash.getinreach(i,antennalength,ggrid):
            i.readantenna(j)
        if  not i.inmapgrid(mapgrid,sizeofcell):
            i.pos=np.array([100,450])
            i.vel = np.array([np.random.randint(0,4)-2,np.random.randint(0,4)-2])
    return newtmp

amount=100
num_cpus = psutil.cpu_count(logical=True)-1
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
print("hash size : n*n with n= ",len(spatialhash.GRID))
print("number of cores::",num_cpus)
print("starting ray::")
ray.init(num_cpus=num_cpus)
print("done")
print("moving data to shared memory::")
MAP_id = ray.put(MAP)
MAPGEO_ID = ray.put(MAPGEO)
spacegrid_id = ray.put(spatialhash.GRID)
print("done")

while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
        
        active = [thetask.remote(i,MAP_id,MAPGEO_ID,spacegrid_id,GLOBALANTENNALENGTH,CELLSIZE) for i in theARRY]
        screen.fill((0,0,0))
        drawmap(MAP,MAX)
        drawgeometry(MAPGEO)
        for i in theARRY:
            for j in i:
                draw(j)
        theARRY= ray.get(active)
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick(30)
        pg.display.flip()
    