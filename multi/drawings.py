import pygame as pg
import numpy as np
from colorsys import hsv_to_rgb
pg.font.init()
SCREEN=pg.Surface((100,100)) #pylint: disable=too-many-function-args
TEMPSURF = pg.Surface((100,100)) #pylint: disable=too-many-function-args
smallfont = pg.font.SysFont('arial', 15)

def init(screensurf):
    global SCREEN , TEMPSURF
    (w,h) = screensurf.get_size()
    SCREEN = screensurf
    TEMPSURF = pg.Surface((w,h))#pylint: disable=too-many-function-args

def drawantenna(ob):
    global SCREEN
    for i in ob.betterconstructantenna():
        pg.draw.line(SCREEN,(255,255,255),(int(ob.pos[0]),int(ob.pos[1])),(int(ob.pos[0]+i[0]),int(ob.pos[1]+i[1])),1)

def drawpart(part,rad):
    global SCREEN
    colora = (255,255,255)
    if not part.alive:
        colora=(150,150,150)
    pg.draw.circle(SCREEN,colora,(int(part.pos[0]),int(part.pos[1])), rad)
    pg.draw.circle(SCREEN,(0,0,0),(int(part.pos[0]),int(part.pos[1])), rad+1,1)


def draw(ggrid,mmax,CELLSIZE):
    global smallfont , TEMPSURF
    for y in range(len(ggrid)):
        for x in range(len(ggrid[y])):
            if ggrid[y][x]!=0:
                h = (ggrid[y][x]/mmax)*359
                s=0.80
                v = 1
                colo = hsv_to_rgb(h,s,v)
                (e,r,t) = colo
                colo = (255*e,255*r,255*t)
                pg.draw.rect(TEMPSURF,colo,pg.Rect(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))
                txt = smallfont.render(str(int(ggrid[y][x])),True,pg.Color('white'))
                TEMPSURF.blit(txt,(int(((x+0.5)*CELLSIZE)-(txt.get_width()/2)),int(((y+0.5)*CELLSIZE)-(txt.get_height()/2))))

def startpos(spaceisdown,startx,starty,secondx,secondy):
    global  TEMPSURF
    pg.draw.circle(TEMPSURF,(255,255,255),(startx,starty),5)
    if spaceisdown:
        (secondx,secondy)  = pg.mouse.get_pos()
        secondx-=startx
        secondy-=starty
        angle = np.arctan2(secondy,secondx)
        secondx = 20*np.cos(angle)
        secondy = 20*np.sin(angle)
    pg.draw.line(TEMPSURF,(255,255,255),(startx,starty),(int(startx+secondx),int(starty+secondy)),2)
 
def drawgeomtry(geoarray):
    global TEMPSURF
    for line in geoarray:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(TEMPSURF,(255,0,0),(x1,y1),(x2,y2),1)

def alldraw(gridd,mmax,geoarray,cellsize):
    global TEMPSURF
    TEMPSURF.fill((0,0,0))
    draw(gridd,mmax,cellsize)
    drawgeomtry(geoarray)