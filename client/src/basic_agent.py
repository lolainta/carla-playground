from sys import path as pythonPath
pythonPath.append('../PythonAPI/')

import carla

client=carla.Client('localhost',2000)
client.load_world('Town03')
world=client.get_world()
spectator=world.get_spectator()
spectator.set_transform(carla.Transform(carla.Location(x=5,y=60,z=40), carla.Rotation(pitch=-90)))

vehicle_start_point=carla.Transform(carla.Location(x=5.2,y=70,z=0),carla.Rotation(pitch=0,yaw=-90,roll=0))
bike_start_point=carla.Transform(carla.Location(x=2.2,y=70,z=0),carla.Rotation(pitch=0,yaw=-90,roll=0))

bp=world.get_blueprint_library().find('vehicle.audi.a2')
vehicle=world.try_spawn_actor(bp,vehicle_start_point)
bp=world.get_blueprint_library().find('vehicle.audi.a2')
# actor=world.try_spawn_actor(bp,bike_start_point)

print("NPC generated")

from agents.navigation.basic_agent import BasicAgent
from agents.navigation.behavior_agent import BehaviorAgent

from agents.navigation.global_route_planner import GlobalRoutePlanner

end_waypoint=carla.Location(x=4.672605,y=39.624626,z=0)

resolution=2
grp=GlobalRoutePlanner(world.get_map(),resolution)

import random
destination=random.choice(world.get_map().get_spawn_points())
vRoute=grp.trace_route(vehicle_start_point.location,destination.location)
bRoute=grp.trace_route(bike_start_point.location,end_waypoint)

vAgent=BasicAgent(vehicle)
vAgent.set_destination(destination.location)

def draw_route(route,col):
    for w in route:
        world.debug.draw_string(w[0].transform.location,'O',draw_shadow=False,color=col,life_time=120.0,persistent_lines=True)

# draw_route(vRoute,carla.Color(255,0,0))
draw_route(vRoute,carla.Color(0,255,0))
# vAgent=BehaviorAgent(vehicle,behavior='cautious')
# vAgent.set_destination(end_waypoint)
# rt=vAgent.get_global_planner().trace_route(carla.Location(x=5.2,y=70,z=0),end_waypoint)
# print(type(rt[0]),rt[0][0],rt[0][1])

# bAgent=BehaviorAgent(actor,behavior='cautious')
# bAgent.set_destination(end_waypoint)

# for i in range(1500):
#     vehicle.apply_control(vAgent.run_step())

while True:
    if not vAgent.done():
        vehicle.apply_control(vAgent.run_step())
#     if not bAgent.done():
#         actor.apply_control(bAgent.run_step())
#     if vAgent.done() and bAgent.done():
#         print("The target has been reached, stopping the simulation")
#         break
        