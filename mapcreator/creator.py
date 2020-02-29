import pygame as pg
import numpy as np
import mapgenerator as mg
import os.path
from colorsys import hsv_to_rgb
import selectingmenu
WIDTH=800
HEIGHT=700
CELLSIZE=20
startx=-100
starty=-100
secondx=1
secondy=1
(w,h)=(int(WIDTH/CELLSIZE),int(HEIGHT/CELLSIZE))
NAME="map.npy"
MAX=1
CURRENTLAYER=1
print("welcome to map generator !!")
mmap = selectingmenu.getfile()
if mmap == "../maps/new_map":
    mg.initialize(w,h)
else:
    (NAME,CELLSIZE,MAX,startx,starty,secondx,secondy) = mg.megaload(mmap)
# mg.loadgeometry("mapGEO.npy")
pg.init() # pylint: disable=no-member
screen = pg.display.set_mode((WIDTH,HEIGHT))
tempsurf = pg.Surface((WIDTH,HEIGHT)) #pylint: disable=too-many-function-args
font = pg.font.Font(None, 20)
smallfont = pg.font.Font(None, 15)
clock = pg.time.Clock()
done = False
spaceisdown = False

def drawgeomtry():
    for line in mg.GEOMETRYARRAY:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(tempsurf,(255,0,0),(x1,y1),(x2,y2),1)

def gui():
    global MAX , CURRENTLAYER , screen ,clock
    fps = font.render("fps: "+str(int(clock.get_fps())), True, pg.Color('white'))
    layer = font.render("current layer: "+str(CURRENTLAYER),True, pg.Color('white'))
    mmax = font.render("max layer: "+str(MAX),True, pg.Color('white'))
    screen.blit(fps, (10, 10))
    screen.blit(mmax,(10,25))
    screen.blit(layer,(10,40))
    h = (CURRENTLAYER/MAX)*359
    s=0.80
    v = 1
    colo = hsv_to_rgb(h,s,v)
    (e,r,t) = colo
    colo = (255*e,255*r,255*t)
    pg.draw.rect(screen,colo,pg.Rect(layer.get_width()+15,40,30,layer.get_height()))

def startpos(spaceisdown):
    global startx,starty,secondx,secondy
    pg.draw.circle(screen,(255,255,255),(startx,starty),5)
    if spaceisdown:
        (secondx,secondy)  = pg.mouse.get_pos()
        secondx-=startx
        secondy-=starty
        angle = np.arctan2(secondy,secondx)
        secondx = 20*np.cos(angle)
        secondy = 20*np.sin(angle)
    pg.draw.line(screen,(255,255,255),(startx,starty),(int(startx+secondx),int(starty+secondy)),2)
    
    

def draw(ggrid,mmax):
    global CELLSIZE , smallfont
    for y in range(len(ggrid)):
        for x in range(len(ggrid[y])):
            if ggrid[y][x]!=0:
                h = (ggrid[y][x]/mmax)*359
                s=0.80
                v = 1
                colo = hsv_to_rgb(h,s,v)
                (e,r,t) = colo
                colo = (255*e,255*r,255*t)
                pg.draw.rect(tempsurf,colo,pg.Rect(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))
                txt = smallfont.render(str(int(ggrid[y][x])),True,pg.Color('white'))
                tempsurf.blit(txt,(int(((x+0.5)*CELLSIZE)-(txt.get_width()/2)),int(((y+0.5)*CELLSIZE)-(txt.get_height()/2))))

def alldraw():
    tempsurf.fill((0,0,0))
    draw(mg.GRID,MAX)
    drawgeomtry()
mouseisdown=False
state=1
alldraw()
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
                if event.type == pg.MOUSEBUTTONDOWN: # pylint: disable=no-member
                        mouseisdown=True
                        if event.button== 1:#LEFT
                            state=CURRENTLAYER
                        if event.button== 3:#RIGHT
                            state=0
                        (w,h) = pg.mouse.get_pos()
                        mpos=np.array([w,h])                 
                        if mg.toggle(mpos,CELLSIZE,state):
                            mg.fullgeometry(CELLSIZE)
                            alldraw()
                if event.type == pg.MOUSEBUTTONUP: # pylint: disable=no-member
                        mouseisdown=False
                if event.type == pg.MOUSEMOTION: # pylint: disable=no-member   
                    if mouseisdown:
                        (w,h) = pg.mouse.get_pos()
                        mpos=np.array([w,h])                 
                        if mg.toggle(mpos,CELLSIZE,state):
                            mg.fullgeometry(CELLSIZE)
                            alldraw()
                if event.type == pg.KEYDOWN:# pylint: disable=no-member
                    if event.key == pg.K_UP:# pylint: disable=no-member
                        CURRENTLAYER+=1
                        if CURRENTLAYER>MAX:
                            CURRENTLAYER=1
                    if event.key == pg.K_DOWN:# pylint: disable=no-member
                        CURRENTLAYER-=1
                        if CURRENTLAYER<1:
                            CURRENTLAYER=MAX
                    if event.key == pg.K_RETURN:# pylint: disable=no-member
                        MAX+=1
                        alldraw()
                    if event.key == pg.K_SPACE: # pylint: disable=no-member
                        (startx,starty) = pg.mouse.get_pos()
                        spaceisdown=True
                if event.type == pg.KEYUP:# pylint: disable=no-member
                    if event.key == pg.K_SPACE: # pylint: disable=no-member
                        spaceisdown=False

        screen.blit(tempsurf,(0,0))
        startpos(spaceisdown)
        gui()
        clock.tick()
        pg.display.flip()

mmax = 0
for i in  mg.GRID:
    for j in i:
        if j >mmax:
            mmax = j
MAX = mmax
megamap = np.array([CELLSIZE,MAX,startx,starty,secondx,secondy,mg.GRID,mg.GEOMETRYARRAY])
mg.megasave(megamap,NAME)
print("saved to "+ NAME)
print("MAX IS :::  ",MAX)
print("(startx,starty): ",startx,starty)