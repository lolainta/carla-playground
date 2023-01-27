import carla
import time

client=carla.Client('localhost',2000)
world=client.get_world()

# config.get_time

actor_list=world.get_actors()
# actor_list[0].id)
id=actor_list[0].id
actor=actor_list.find(id)
print(actor)
print(actor.get_location())
while True:
    config=world.get_snapshot()
    frame=config.frame

    loc=actor.get_location()
    print(frame,loc)
    world.get_spectator().set_transform(carla.Transform(loc+carla.Location(z=80),carla.Rotation(-90,0,0)))
    time.sleep(0.05)