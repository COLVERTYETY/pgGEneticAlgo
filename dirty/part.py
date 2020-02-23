import pygame as pg
import numpy as np
import walls


class being(object):
    GRID = np.zeros([10, 10])
    SURFACE = pg.Surface((100,100)) # pylint: disable=too-many-function-args
    MAXSPEED=10
    CELLSIZE=10
    def __init__(self,x,y):
        self.pos=np.array([x,y])
        self.vel=np.array([np.random.randint(0,4)-2,np.random.randint(0,4)-2])
        self.acc=np.array([0,0])
        self.antenannumber=3
        self.antennaangle=np.pi/8
        self.antennalength=40
        self.radius=5
        self.color=(0,255,0)
        self.antennacolor=(100,255,100)
    
    def __repr__(self):
        return ("("+str(self.pos)+" "+str(self.vel)+" "+str(self.acc)+")")

    def localise(self):
        (w,h) = being.SURFACE.get_size()
        width = w//being.CELLSIZE
        height = h//being.CELLSIZE
        x=self.pos[0]//being.CELLSIZE
        y=self.pos[1]//being.CELLSIZE
        if x>=0 and x<width and y>=0 and y<height:
            being.GRID[y][x].append(self) 

    def readantennas(self,allthewalls):
        res=[]
        for i in self.constructanennas():
            # base=self.pos
            # end=self.pos+i
            #if intersection
                #get coord
                #convert distance to percent
                #append percent to res
                #calculate color according to percent
                #draw antenna to avoid redundence
            pass
        return res

    def getneighbours(self):
        neighbours=[]
        (w,h) = being.SURFACE.get_size()
        width = w//being.CELLSIZE
        height = h//being.CELLSIZE
        x=self.pos[0]//being.CELLSIZE
        y=self.pos[1]//being.CELLSIZE
        for i in range(-1,2):
            for j in range(-1,2):
                if (x+i)>=0 and (x+i)<width and (j+y)>=0 and (y+j)<height:
                    neighbours.extend(being.GRID[y+j][x+i])
        return neighbours
                

    def apply(self):
        self.vel+=self.acc
        self.acc=np.array([0,0])
        norm = np.linalg.norm(self.vel)
        if norm>being.MAXSPEED:
            self.vel[0]/=norm/being.MAXSPEED
            self.vel[1]/=norm/being.MAXSPEED
        self.pos+=self.vel

    def constructanennas(self):
        angle = np.arctan2(self.vel[1],self.vel[0])
        x=self.antennalength*np.cos(angle)
        y = self.antennalength*np.sin(angle)
        yield np.array([x,y])
        for _ in range(self.antenannumber):
            angle+= self.antennaangle
            x=self.antennalength*np.cos(angle)
            y = self.antennalength*np.sin(angle)
            yield np.array([x,y])
        angle = np.arctan2(self.vel[1],self.vel[0])
        for _ in range(self.antenannumber):
            angle-= self.antennaangle
            x=self.antennalength*np.cos(angle)
            y = self.antennalength*np.sin(angle)
            yield np.array([x,y])
        
    def collidecapsule(self,other):
        vline = other.b.pos - other.a.pos #vect of the capsule
        vpline = self.pos - other.a.pos # vect of particule to line
        lvline = vline[0]*vline[0] + vline[1]*vline[1] #norm squarded of capsule
        dot  = vline[0]*vpline[0]+vline[1]*vpline[1]
        #t = np.dot(vpline,vline) #dot product of particule on line     #? shadow of the particule on the capsule
        t = max(0,min(lvline,dot))/(lvline)
        closespos=np.array([0,0]) #initempty vect for closest point
        closespos = (t*vline) + other.a.pos #calculate closespos
        tmp = walls.circle(closespos[0],closespos[1],other.a.radius)#create a temp circle at that pos
        self.colidecircle(tmp)# resolv colision as if with a circle

    def colidecircle(self,other):
        dist=np.linalg.norm(self.pos-other.pos)
        if dist < (self.radius+other.radius):
            if dist<0.0001:
                dist=0.0001
            overlap = 0.5*(dist-other.radius-self.radius)
            other.pos[0]-=overlap*(other.pos[0]-self.pos[0])/dist
            self.pos[0]-=overlap*(self.pos[0]-other.pos[0])/dist
            other.pos[1]-=overlap*(other.pos[1]-self.pos[1])/dist
            self.pos[1]-=overlap*(self.pos[1]-other.pos[1])/dist


    def drawantenna(self):
        for i in self.constructanennas():
            pg.draw.line(being.SURFACE,self.antennacolor,(int(self.pos[0]),int(self.pos[1])),(int(self.pos[0]+i[0]),int(self.pos[1]+i[1])),1)

    def draw(self):
        pg.draw.circle(being.SURFACE,self.color,(int(self.pos[0]),int(self.pos[1])), self.radius)

    @staticmethod
    def rebuildgrid():
        (w,h) = being.SURFACE.get_size()
        width = w//being.CELLSIZE
        height = h//being.CELLSIZE
        being.GRID= [[[] for j in range(width)] for i in range(height)]
    
        