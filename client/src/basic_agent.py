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

import math
import time

def func(t):
    return abs(math.sin(t/5))*30+10
while True:
    destination=random.choice(world.get_map().get_spawn_points())
    route=grp.trace_route(vehicle.get_location(),destination.location)
    routeManager.set_route(route)
    routeManager.draw_route(sz=0.2,col=carla.Color(255,0,0))
    print(f"{time.strftime('[%F %a %H:%M:%S] ')}There are {len(route)} waypoints with length {routeManager.total_length} in the current route.")

    agent=BasicAgent(vehicle)
    agent.set_destination(destination.location)
    agent.follow_speed_limits(False)
    agent.ignore_traffic_lights()
    agent.ignore_stop_signs()
    agent.ignore_vehicles()
    while not agent.done():
        agent.set_target_speed(func(time.time()))
        vehicle.apply_control(agent.run_step())
        follow()
    print(f"{time.strftime('[%F %a %H:%M:%S] ')}Current route finished, starting next route.",flush=True)
