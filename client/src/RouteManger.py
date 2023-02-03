import carla

class RouteManager():
    def __init__(self,world):
        self.world=world
        pass
    
    def set_route(self,route):
        self.route=route

    def draw_route(self,col=carla.Color(255,0,0)):
        wid=0
        for w in self.route:
            wid+=1
            self.world.debug.draw_string(w[0].transform.location,str(wid),color=col,life_time=120)
            print(wid,w[0].transform.location)