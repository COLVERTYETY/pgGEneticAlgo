import pygame as pg
import numpy as np
from part import *
import spatialhash

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

#pg.draw.circle(screen,(255,255,0),(100,450),10)
for _ in range(10):
    theARRY.append(being(startx,starty))

spatialhash.init(int(WIDTH/GLOBALANTENNALENGTH),int(HEIGHT/GLOBALANTENNALENGTH))
spatialhash.organise(MAPGEO,GLOBALANTENNALENGTH)

while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
                
        screen.fill((0,0,0))
        drawmap(MAP)
        drawgeometry(MAPGEO)
        for i in theARRY:
            i.apply()
            i.antennainput.fill(1)
            for j in spatialhash.getinreach(i,GLOBALANTENNALENGTH):
                i.readantenna(j)
            if i.inmapgrid(MAP,CELLSIZE):
                i.color=(255,0,0)
            else:
                i.color=(0,255,0)
                i.pos=np.array([startx,starty])
                i.vel=np.array([np.random.randint(0,4)-2,np.random.randint(0,4)-2])
            i.draw()
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick()
        pg.display.flip()
    