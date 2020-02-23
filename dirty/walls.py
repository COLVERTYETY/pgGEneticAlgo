import pygame as pg
import numpy as np

CSURFACE  = pg.Surface((100,100)) # pylint: disable=too-many-function-args

class capsule(object):
    def __init__(self,circlea=0,circleb=0):
        self.a=circlea
        self.b = circleb
        self.color = (90,90,90)
    def __repr__(self):
        return str(self.a)+" "+ str(self.b)
    def downclick(self,mpos):
        self.a.ifselected(mpos)
        self.b.ifselected(mpos)
    def dragclick(self,mpos):
        self.a.adjustforselected(mpos)
        self.b.adjustforselected(mpos)
    def upclick(self,mpos):
        self.a.unselect()
        self.b.unselect()
    def initilialize(self,x1,y1,x2,y2,radius):
        self.a=circle(x1,y1,radius)
        self.b=circle(x2,y2,radius)

    def draw(self):
        global CSURFACE
        self.a.draw()
        self.b.draw()
        vnorm = np.array([0,0])
        vnorm[0]= (-1*(self.b.pos[1]-self.a.pos[1]))
        vnorm[1]=(self.b.pos[0]-self.a.pos[0])
        nn = np.linalg.norm(vnorm)
        vnorm*=self.a.radius
        vnorm=vnorm/nn
        pg.draw.line(CSURFACE,self.color,(int(self.a.pos[0]+vnorm[0]),int(self.a.pos[1]+vnorm[1])),(int(self.b.pos[0]+vnorm[0]),int(self.b.pos[1]+vnorm[1])),1)
        pg.draw.line(CSURFACE,self.color,(int(self.a.pos[0]-vnorm[0]),int(self.a.pos[1]-vnorm[1])),(int(self.b.pos[0]-vnorm[0]),int(self.b.pos[1]-vnorm[1])),1)
    
    @staticmethod
    def continuous(arrofpos,radius):
        res=[]
        tmp = arrofpos[0]
        tmp = circle(tmp[0],tmp[0],radius)
        for i in range(1,len(arrofpos)):
            n= circle(arrofpos[i][0],arrofpos[i][1],radius)
            line = capsule(tmp,n)
            tmp = n
            res.append(line)
        n= circle(arrofpos[0][0],arrofpos[0][1],radius)
        line = capsule(tmp,n)
        res.append(line)
        return res



class circle(object):
    def __init__(self,x,y,radius):
        self.pos=np.array([x,y])
        self.radius=radius
        self.color=(100,100,100)
        self.selected=False
        self.offset=np.array([0,0])
    def __repr__(self):
        return str(self.pos)+' '+str(self.radius)
    def draw(self):
        global CSURFACE
        width=1
        if self.selected==True:
            width=0
        pg.draw.circle(CSURFACE,self.color,tuple(self.pos.astype(int)),self.radius,width)
    def ifselected(self,mpos):
        if self.radius>np.linalg.norm(mpos-self.pos):
            self.offset=self.pos-mpos
            self.selected=True
    def unselect(self):
        self.selected=False
    def adjustforselected(self,mpos):
        if self.selected==True:
            self.pos=mpos+self.offset
