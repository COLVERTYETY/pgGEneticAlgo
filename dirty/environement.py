import pygame as pg
import numpy as np
from part import *
import walls
pg.init() # pylint: disable=no-member
WIDTH=800
HEIGHT=700
screen = pg.display.set_mode((WIDTH,HEIGHT))
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
done = False

theARRY=[]
wallarray=[]
walls.CSURFACE=screen
being.SURFACE=screen

wallborder = [
    [0,0],
    [WIDTH,0],
    [WIDTH,HEIGHT],
    [0,HEIGHT]
]

# for _ in range(3):
#     tmp=walls.capsule()
#     tmp.initilialize(np.random.randint(0,WIDTH),np.random.randint(0,HEIGHT),np.random.randint(0,WIDTH),np.random.randint(0,HEIGHT),10)
#     wallarray.append(tmp)

wallarray.extend(walls.capsule.continuous(wallborder,10))

for _ in range(300):
    theARRY.append(being(np.random.randint(0,WIDTH),np.random.randint(0,HEIGHT)))

while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:# pylint: disable=no-member
                        done = True
                if event.type == pg.MOUSEBUTTONDOWN: # pylint: disable=no-member
                        (mx,my)=pg.mouse.get_pos()
                        mpos=np.array([mx,my])
                        if event.button== 1:#LEFT
                                for i in wallarray:
                                    i.downclick(mpos)
                if event.type == pg.MOUSEBUTTONUP: # pylint: disable=no-member
                        (mx,my)=pg.mouse.get_pos()
                        mpos=np.array([mx,my])
                        if event.button==1:
                            for i in wallarray:
                                i.upclick(mpos)
                if event.type == pg.MOUSEMOTION: # pylint: disable=no-member
                        (mx,my)=pg.mouse.get_pos()
                        mpos = np.array([mx,my])
                        for i in wallarray:
                            i.dragclick(mpos)
        
        # being.rebuildgrid()
        # for i in theARRY:
        #     i.localise()
        screen.fill((0,0,0))
        for i in theARRY:
            i.apply()
            i.draw()
            i.drawantenna()
            for j in wallarray:
                i.collidecapsule(j)
            # tmp=i.getneighbours()
            # for j in tmp:
            #     i.colidecircle(j)
            # for j in theARRY:
            #     i.colidecircle(j)
        for i in wallarray:
            i.draw()
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick()
        pg.display.flip()
    