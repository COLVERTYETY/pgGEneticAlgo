import pygame as pg
import numpy as np
from part import *
import spatialhash
import ray
import psutil
import copy
from colorsys import hsv_to_rgb
import sys
import matplotlib.pyplot as plt
plt.ion() # make matplotlib interactif
pg.init() # pylint: disable=no-member
WIDTH=800
HEIGHT=700
screen = pg.display.set_mode((WIDTH,HEIGHT))
font = pg.font.Font(None, 30)
clock = pg.time.Clock()
done = False

theARRY=[]
being.SURFACE=screen
EVOLUTIONAVG=[]
EVOLUTIONMAX=[]
MAPGEO = np.load("./map-layeredGEO.npy")
MAP = np.load("./map-layered.npy")
CELLSIZE = 20
GLOBALANTENNALENGTH=40
MAXFRAMECOUNT=400
startx = 100
starty = 450
MAX=11

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

def evolve(listlist):
    global startx,starty,num_cpus , EVOLUTIONAVG , EVOLUTIONMAX
    total_list=[]
    for i in listlist:
        total_list.extend(i)
    total_list.sort(key=lambda i : i.fitness,reverse = True)
    avg=0
    mmax=0
    for i in total_list:
        k=i.fitness
        avg+=k
        if k > mmax:
            mmax=k
        print(i)
    avg/=len(total_list)
    EVOLUTIONAVG.append(avg)
    EVOLUTIONMAX.append(mmax)
    new_dudes = []
    print("                    starting fuses            ")
    for i in range(50):
        tmp = being(startx,starty)
        tmp.weights = mutate(total_list[i].weights)
        new_dudes.append(tmp)
    tmp=[]
    for i in new_dudes:
        for _ in range(len(total_list)//len(new_dudes)):
            dice = np.random.randint(0,len(new_dudes))
            ttmp = being(startx,starty)
            ttmp.weights = mutate(fuser(i.weights,new_dudes[dice].weights))
            tmp.append(ttmp)
    new_dudes.extend(tmp)
    print("                    starting mutations       ")
    while len(new_dudes)<len(total_list):
        ttmp = being(startx,starty)
        dice = np.random.randint(0,len(new_dudes))
        ttmp.weights = mutate(new_dudes[dice].weights)
        for i in range(100):
            ttmp.weights = mutate(ttmp.weights)
        new_dudes.append(ttmp)
    if len(new_dudes)>len(total_list):
        new_dudes = new_dudes[0:len(total_list)-1]
    listofdudes = []
    print("                   starting division         ")
    for i in range(num_cpus):
        tmp = new_dudes[int(i*len(new_dudes)/num_cpus):int((i+1)*len(new_dudes)/num_cpus)]
        listofdudes.append(tmp)
    print("                    all done about to restart     ")
    return listofdudes

def fuser(first,second):
    out = copy.copy(first)
    for i in range(len(first)):
        for j in range(len(first[i])):
            dice = np.random.randint(0,2)
            if dice == 1:
                out[i][j]=second[i][j]
    return out

def mutate(first):
    prob=0.05
    out = copy.copy(first)
    for i in range(len(first)):
        for j in range(len(first[i])):
            dice = np.random.randint(0,101)
            if dice<=(2*prob*100):
                dice = np.random.randint(0,2)
                mult = 1
                if dice ==1:
                    mult= -1
                out[i][j] = out[i][j] + mult*out[i][j]*(prob/10)
    return out

def drawgeometry(linearr):
    for line in linearr:
        x1 = int(line[0][0])
        y1 = int(line[0][1])
        x2 = int(line[1][0])
        y2 = int(line[1][1])
        pg.draw.line(screen,(255,0,0),(x1,y1),(x2,y2),1)

def draw(part):
    colora = (255,255,255)
    if not part.alive:
        colora=(150,150,150)
    pg.draw.circle(screen,colora,(int(part.pos[0]),int(part.pos[1])), being.radius)
    pg.draw.circle(screen,(0,0,0),(int(part.pos[0]),int(part.pos[1])), being.radius+1,1)

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

amount=100
num_cpus = psutil.cpu_count(logical=True)-1
print("begin initializing the beings")
for _i in range(num_cpus):
    tmp=[]
    print(_i)
    for _j in range(amount):
        ttmp=being(startx,starty)
        ttmp.weights = np.random.rand((being.antenannumber*2)+3,2) - np.random.rand((being.antenannumber*2)+3,2)
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

frame_counter=0
while True:
    while not done:
            for event in pg.event.get():
                    if event.type == pg.QUIT:# pylint: disable=no-member
                            done = True
                            sys.exit()
            
            active = [thetask.remote(i,MAP_id,MAPGEO_ID,spacegrid_id,GLOBALANTENNALENGTH,CELLSIZE) for i in theARRY]
            screen.fill((0,0,0))
            drawmap(MAP,MAX)
            drawgeometry(MAPGEO)
            for i in theARRY:
                for j in i:
                    draw(j)
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
    print(len(theARRY[0]))
    plt.plot(EVOLUTIONAVG)
    plt.plot(EVOLUTIONMAX)
    plt.draw()
    plt.pause(0.1)
    done=False
    frame_counter=0