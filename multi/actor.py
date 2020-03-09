import ray 
import copy
import spatialhash


@ray.remote
class A_worker(object):
    def __init__(self,mapgrid,mapgeometry,ggrid,antennalength,sizeofcell):
        self.objarray = []
        self.mapgrid = mapgrid
        self. mapgeometry = mapgeometry
        self.ggrid = ggrid
        self.antennalength = antennalength
        self.sizeofcell = sizeofcell
        self.n_alive=0

    def restock(self,objarray):
        self.objarray = copy.deepcopy(objarray)
        self.n_alive = len(self.objarray)

    def thetask(self):
        self.n_alive=len(self.objarray)
        for i in self.objarray:
            if i.alive:
                i.antennainput.fill(1)
                for j in spatialhash.getinreach(i,self.antennalength,self.ggrid):
                    i.readantenna(j)
                i.apply()
                i.inmapgrid(self.mapgrid,self.sizeofcell)
            else:
                self.n_alive-=1
        return self.objarray

    def status(self):
        return self.n_alive