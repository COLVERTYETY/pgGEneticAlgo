import pygame as pg
import numpy as np


class being(object):
    GRID = np.zeros([10, 10])
    SURFACE = pg.Surface((100,100)) # pylint: disable=too-many-function-args
    MAXSPEED=10
    CELLSIZE=10
    def __init__(self,x,y):
        self.pos=np.array([x,y])
        self.vel=np.array([np.random.randint(0,4)-2,np.random.randint(0,4)-2])
        self.acc=np.array([0,0])
        self.antenannumber=2
        self.antennainput=np.zeros(((self.antenannumber*2)+1))
        self.antennaangle=np.pi/6
        self.antennalength=80
        self.radius=5
        self.color=(0,255,0)
        self.antennacolor=(100,255,100)
    
    def __repr__(self):
        return ("("+str(self.pos)+" "+str(self.vel)+" "+str(self.acc)+")")

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
        
    def drawantenna(self):
        for i in self.constructanennas():
            pg.draw.line(being.SURFACE,self.antennacolor,(int(self.pos[0]),int(self.pos[1])),(int(self.pos[0]+i[0]),int(self.pos[1]+i[1])),1)

    def inmapgrid(self,mapgrid,CELLSIZE):
        gridpos= self.pos//CELLSIZE
        if gridpos[0]>=0 and gridpos[1]>=0 and gridpos[0]<len(mapgrid[0]) and gridpos[1]<len(mapgrid):
            return mapgrid[int(gridpos[1])][int(gridpos[0])]==1


    def readantenna(self,line):
        cc=-1
        if line[0][0]==line[1][0]:#line is vertical
            for i in self.constructanennas():
                cc+=1
                antenna = [[],[]]
                antenna[0] = self.pos
                antenna[1] = self.pos+i
                if ((line[0][0] <= max(antenna[0][0],antenna[1][0])) and (line[0][0] >= min(antenna[0][0],antenna[1][0]))) and antenna[0][0]!=antenna[1][0]:
                    #colision is possible because x are compatible, checking y still necessary, we ignore if both parallel cause lazy
                    A1 = (antenna[0][1]-antenna[1][1])/(antenna[0][0]-antenna[1][0])# divide by 0 is impossible because we ignore paralel case
                    B1 = antenna[0][1] - (A1*antenna[0][0])
                    Ya = A1*line[0][0] + B1
                    intersectpos=np.array([line[0][0],Ya])
                    if Ya <= max(line[0][1],line[1][1]) and Ya>= min(line[1][1],line[0][1]):# if the point is on the line, the y is compatible
                        dist = np.linalg.norm(intersectpos-self.pos)
                        res = dist/self.antennalength#make it to %
                        if self.antennainput[cc] >=res:
                            self.antennainput[cc]=res
        elif line[0][1]==line[1][1]:#if line is horisontal
            for i in self.constructanennas():
                cc+=1
                antenna = [[],[]]
                antenna[0] = self.pos
                antenna[1] = self.pos+i
                if ((line[0][1] <= max(antenna[0][1],antenna[1][1])) and (line[0][1] >= min(antenna[0][1],antenna[1][1]))) and antenna[0][1]!=antenna[1][1]:
                    #colision is possible because y are compatible, checking x still necessary , we ignore paralel cause lazy
                    A1 = (antenna[0][0]-antenna[1][0])/(antenna[0][1]-antenna[1][1])# divide by 0 is impossible because we ignore paralel case
                    B1 = antenna[0][0] - (A1*antenna[0][1])#so we did the calculations by seraching x = A1*y+B1
                    Xa = A1*line[0][1] + B1
                    intersectpos=np.array([Xa,line[0][1]])
                    if Xa <= max(line[0][0],line[1][0]) and Xa>= min(line[1][0],line[0][0]):# if the point is on the line, the y is compatible
                        dist = np.linalg.norm(intersectpos-self.pos)
                        res = dist/self.antennalength#make it to %
                        if res<=self.antennainput[cc]:
                            self.antennainput[cc]=res
                         


    def circlepointsegment(self,line):
        vline = line[1]-line[0]
        vpline = self.pos-line[0]
        lvline = vline[0]*vline[0]+vline[1]*vline[1]
        dot = vline[0]*vpline[0]+vline[1]*vpline[1]
        t = max(0,min(lvline,dot))/(lvline)
        closespos=np.array([0,0])
        closespos = (t*vline) + line[0]
        dist = np.linalg.norm(self.pos-closespos)
        if dist < (self.radius):
            if dist<0.0001:
                dist=0.0001
            overlap = (dist-self.radius)
            self.pos[0]-=overlap*(self.pos[0]-closespos[0])/dist
            self.pos[1]-=overlap*(self.pos[1]-closespos[1])/dist


    def draw(self):
        pg.draw.circle(being.SURFACE,self.color,(int(self.pos[0]),int(self.pos[1])), self.radius)

    
        