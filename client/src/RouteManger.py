from __future__ import annotations
import carla
import math
from agents.tools.misc import compute_distance

class RouteManager():
    def __init__(self,world):
        self.world=world
        pass
    
    def set_route(self,route):
        self.waypoints=[w[0] for w in route]
        self._build()
    
    def draw_route(self,sz=0.1,col=carla.Color(255,0,0)):
        for w in self.waypoints:
            self.world.debug.draw_point(w.transform.location,size=sz,color=col,life_time=len(self.waypoints))

    def draw_points(self,sz=0.1,col=carla.Color(255,0,0)):
        for pts in self.points:
            self.world.debug.draw_point(pts,size=sz,color=col,life_time=len(self.waypoints))

    def perturb(self,func):
        n=len(self.waypoints)
        ret=list()
        for i in range(n+1):
            ret.append(self._query(func(i/n)*self.total_length))
        # self.waypoints=ret
        self.points=ret

    def distance(self,wpt1,wpt2):
        return compute_distance(wpt1.transform.location,wpt2.transform.location)

    def _bs(self,l:int,r:int,x:float) -> tuple[int,int]:
        assert x>=0, f"Query cannot be negtive! found {x}"
        assert x<=self.total_length, f"Query out of range! {x}>{self.total_length}"
        assert l<=r, f"Internal error, l>=r"
        if r-l==1:
            return l,r
        mid=(l+r)//2
        if x>self._prefix[mid]:
            return self._bs(mid,r,x)
        else:
            return self._bs(l,mid,x)
    
    def _interpolate(self,wpt1,wpt2,alpha):
        loc1=wpt1.transform.location
        loc2=wpt2.transform.location
        return loc1*alpha+loc2*(1-alpha)
    
    def _build(self):
        self._prefix=[0]
        cur=0
        for i in range(len(self.waypoints)-1):
            cur+=self.distance(self.waypoints[i],self.waypoints[i+1])
            self._prefix.append(cur)
        assert len(self._prefix)==len(self.waypoints)
        self.total_length=cur

    def _query(self,x):
        p,q=self._bs(0,len(self._prefix),x)
        dp=x-self._prefix[p]
        dq=self._prefix[q]-x
        # print(x,p,q,dq/(dp+dq))
        return self._interpolate(self.waypoints[p],self.waypoints[q],dq/(dp+dq))
