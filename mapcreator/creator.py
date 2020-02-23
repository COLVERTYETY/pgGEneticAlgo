import pygame as pg
import numpy as np
import mapgenerator as mg
import os.path


WIDTH=800
HEIGHT=700
CELLSIZE=20
(w,h)=(int(WIDTH/CELLSIZE),int(HEIGHT/CELLSIZE))
NAME="map.npy"

print("welcome to map generator !!")
print("enter a name to load a file, if no file is found a file will be created !!")
res = input()
if len(res)>1:
    NAME=res
    if os.path.exists('./'+res):
        mg.loadmaparray(res)
        
        print("a map has been found and loaded")
    else:
        mg.initialize(w,h)
        print("no map has been found and an empty map has been created")
else:
    print("empty name, clearing and editing "+NAME)
    mg.initialize(w,h)
# mg.loadgeometry("mapGEO.npy")

pg.init() # pylint: disable=no-member
screen = pg.display.set_mode((WIDTH,HEIGHT))
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
done = False


def drawgeomtry():
    for line in mg.GEOMETRYARRAY:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(screen,(255,0,0),(x1,y1),(x2,y2),1)

def draw(ggrid):
    global CELLSIZE
    for y in range(len(ggrid)):
        for x in range(len(ggrid[y])):
            if ggrid[y][x]==1:
                pg.draw.rect(screen,(0,0,255),pg.Rect(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))
mouseisdown=False
state=1
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
                if event.type == pg.MOUSEBUTTONDOWN: # pylint: disable=no-member
                        mouseisdown=True
                        if event.button== 1:#LEFT
                            state=1
                        if event.button== 3:#RIGHT
                            state=0
                        (w,h) = pg.mouse.get_pos()
                        mpos=np.array([w,h])                 
                        mg.toggle(mpos,CELLSIZE,state)
                        mg.generategeometry(CELLSIZE)
                if event.type == pg.MOUSEBUTTONUP: # pylint: disable=no-member
                        mouseisdown=False
                if event.type == pg.MOUSEMOTION: # pylint: disable=no-member
                    if mouseisdown:
                        (w,h) = pg.mouse.get_pos()
                        mpos=np.array([w,h])                 
                        mg.toggle(mpos,CELLSIZE,state)
                        mg.generategeometry(CELLSIZE)
        
       
        screen.fill((0,0,0))
        draw(mg.GRID)
        drawgeomtry()
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick()
        pg.display.flip()

mg.savemaparray(NAME)
mg.savegeometry(NAME)
print("saved to "+ NAME)