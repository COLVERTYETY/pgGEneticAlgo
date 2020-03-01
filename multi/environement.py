import pygame as pg
import numpy as np
from part import *
import spatialhash
import ray
import psutil
import copy
from colorsys import hsv_to_rgb
import sys
import statistics
from math import sqrt
import selectingmenu
import drawings as dr
import plotter as plt


theARRY=[]
EVOLUTIONAVG=[]
EVOLUTIONMAX=[]
CELLSIZE = 20
GLOBALANTENNALENGTH=40
MAXFRAMECOUNT=100
startx = 95
starty = 440
MAX=35
dataarray = np.load(selectingmenu.getfile())
MAP = dataarray[6]
MAPGEO = dataarray[7]
(CELLSIZE,MAX,startx,starty,secondx,secondy)=(dataarray[0],dataarray[1],dataarray[2],dataarray[3],dataarray[4],dataarray[5])
dataarray=[]
being.initialvel=np.array([secondx/20,secondy/20])
amount=60
being.maxgridfit = MAX

pg.init() # pylint: disable=no-member
WIDTH=800
HEIGHT=700
screen = pg.display.set_mode((WIDTH,HEIGHT))
dr.init(screen)
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
done = False
BEST_W8 = np.zeros(((being.antenannumber*2)+2,2))
plotter = plt.plotter()


def evolve(listlist):
    global startx,starty,num_cpus , EVOLUTIONAVG , EVOLUTIONMAX,plotter,BEST_W8
    total_list=[]
    for i in listlist:
        total_list.extend(i)
    total_list.sort(key=lambda i : i.fitness,reverse = True)
    best_brain = total_list[0].weights
    np.savetxt("./brains/bestweights.txt",total_list[0].weights)
    avg=statistics.mean(map( lambda x: x.fitness,total_list))
    mmax=max(map( lambda x: x.fitness, total_list))
    EVOLUTIONAVG.append(avg)
    EVOLUTIONMAX.append(mmax)
    BEST_W8 =  plotter.update(EVOLUTIONMAX,EVOLUTIONAVG,best_brain,BEST_W8)
    new_dudes = []
    print("                    starting fuses            ")
    N = int(sqrt(2*len(total_list)+1/4)+1/2)
    for i in range(N):
        tmp = being(startx,starty)
        tmp.weights = total_list[i].weights
        new_dudes.append(tmp)
    tmp=[]
    for i,nd in enumerate(new_dudes):
        for _ in range(N-i,0,-1):
            dice = np.random.randint(0,len(new_dudes))
            ttmp = being(startx,starty)
            ttmp.weights = mutate(mutate2(fuser(nd.weights,new_dudes[dice].weights)))
            tmp.append(ttmp)
    new_dudes.extend(tmp)
    print("                    starting mutations       ")
    while len(new_dudes)<len(total_list):
        ttmp = being(startx,starty)
        dice = np.random.randint(0,len(new_dudes))
        ttmp.weights = mutate(mutate2(new_dudes[dice].weights))
        for i in range(100):
            ttmp.weights = mutate(mutate2(ttmp.weights))
        new_dudes.append(ttmp)
    if len(new_dudes)>len(total_list):
        new_dudes = new_dudes[0:len(total_list)]
    listofdudes = []
    print("                   starting division         ")
    for i in range(num_cpus):
        tmp = new_dudes[int(i*len(new_dudes)/num_cpus):int((i+1)*len(new_dudes)/num_cpus)]
        listofdudes.append(tmp)
    print("                    all done about to restart     ")
    return listofdudes

def fuser(first,second):
    out = np.copy(first)
    for i in range(len(first)):
        for j in range(len(first[i])):
            dice = np.random.randint(0,2)
            if dice == 1:
                out[i][j]=second[i][j]
    return out

def mutate(first):
    prob=0.5
    out = copy.copy(first)
    for i in range(len(first)):
        for j in range(len(first[i])):
            dice = np.random.rand()
            if dice<prob:
                dice = np.random.randint(0,2)
                mult = 1
                if dice ==1:
                    mult= -1
                out[i][j] = out[i][j] + mult*out[i][j]*(prob/100)
    return out

def mutate2(first):
    out = np.copy(first)
    out +=(np.random.rand((being.antenannumber*2)+2,2) - np.random.rand((being.antenannumber*2)+2,2))/1000
    return out

def splitter(length, i,n):
    (k,m) = divmod(length, n)
    low = i * k + min(i, m)
    high = (i + 1) * k + min(i + 1, m)
    return (low,high)

@ray.remote
def thetask(objarray,mapgrid,mapgeometry,ggrid,antennalength,sizeofcell):
    newtmp = copy.deepcopy(objarray)
    for i in newtmp:
        if i.alive:
            i.antennainput.fill(1)
            for j in spatialhash.getinreach(i,antennalength,ggrid):
                i.readantenna(j)
            i.apply()
            i.inmapgrid(mapgrid,sizeofcell)
    return newtmp


num_cpus = psutil.cpu_count(logical=True)-1
print("begin initializing the beings")
being.maxgridfit=MAX
for _i in range(num_cpus):
    tmp=[]
    print(_i)
    for _j in range(amount):
        ttmp=being(startx,starty)
        ttmp.weights = np.random.rand((being.antenannumber*2)+2,2) - np.random.rand((being.antenannumber*2)+2,2)
        tmp.append(ttmp)
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


dr.alldraw(MAP,MAX,MAPGEO,CELLSIZE)
frame_counter=0
while True:
    while not done:
            for event in pg.event.get():
                    if event.type == pg.QUIT:# pylint: disable=no-member
                            done = True
                            sys.exit()
            
            active = [thetask.remote(i,MAP_id,MAPGEO_ID,spacegrid_id,GLOBALANTENNALENGTH,CELLSIZE) for i in theARRY]
            screen.blit(dr.TEMPSURF,(0,0))
            for i in theARRY:
                for j in i:
                    #dr.drawantenna(j)
                    dr.drawpart(j,being.radius)
            fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
            screen.blit(fps, (50, 50))
            theARRY= ray.get(active)
            frame_counter+=1
            if frame_counter>MAXFRAMECOUNT:
                done=True
            frames = font.render(str(frame_counter), True, pg.Color('white'))
            screen.blit(frames, (50, 10))
            clock.tick()
            pg.display.flip()

    tmp = evolve(theARRY)
    theARRY = tmp
    print("num of workers:",len(theARRY))
    print("load per worker",len(theARRY[0]))
    done=False
    frame_counter=0
