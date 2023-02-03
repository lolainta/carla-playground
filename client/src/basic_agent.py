from sys import path as pythonPath
pythonPath.append('../PythonAPI/')

import carla

client=carla.Client('localhost',2000)
client.load_world('Town03')
world=client.get_world()
spectator=world.get_spectator()

vehicle_start_point=carla.Transform(carla.Location(x=5.2,y=70,z=0),carla.Rotation(pitch=0,yaw=-90,roll=0))

bp=world.get_blueprint_library().find('vehicle.audi.a2')
vehicle=world.try_spawn_actor(bp,vehicle_start_point)

print("NPC generated")

from agents.navigation.basic_agent import BasicAgent
from agents.navigation.global_route_planner import GlobalRoutePlanner

resolution=2
grp=GlobalRoutePlanner(world.get_map(),resolution)

import random
from RouteManger import RouteManager

routeManager=RouteManager(world)

def follow():
    camara=carla.Transform(vehicle.get_location()+carla.Location(z=20),carla.Rotation(-90))
    spectator.set_transform(camara)

while True:
    destination=random.choice(world.get_map().get_spawn_points())
    route=grp.trace_route(vehicle.get_location(),destination.location)
    routeManager.set_route(route)
    routeManager.draw_route()

    agent=BasicAgent(vehicle)
    agent.set_destination(destination.location)
    while not agent.done():
        vehicle.apply_control(agent.run_step())
        follow()
    print(f"Current route finished, starting next route.",flush=True)
