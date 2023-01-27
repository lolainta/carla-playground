import carla
# client=carla.Client('localhost',2000)
# client.load_world('Town01')

client=carla.Client('localhost',2000)
client.load_world('Town03')
world=client.get_world()

spectator=world.get_spectator()
transform=spectator.get_transform()
print(transform)

spectator.set_transform(carla.Transform(carla.Location(x=4.672605, y=69.624626, z=29.992836), carla.Rotation(pitch=-90, yaw=-90, roll=0.000000)))
# spectator.set_transform(carla.Transform(carla.Location(80,-100,50),carla.Rotation(-90,90,0)))
# world=client.get_world()
# spectator=world.get_spectator()
# print(spectator.get_transform())

npc=list()

bp=world.get_blueprint_library().find('vehicle.audi.a2')
actor=world.try_spawn_actor(bp,carla.Transform(carla.Location(x=5.2, y=70, z=0), carla.Rotation(pitch=0, yaw=-90, roll=0.000000)))
# actor.set_simulate_physics(True)

npc.append(actor)

bp=world.get_blueprint_library().find('vehicle.bh.crossbike')
actor=world.try_spawn_actor(bp,carla.Transform(carla.Location(x=8.3, y=70, z=0), carla.Rotation(pitch=0, yaw=-90, roll=0.000000)))
# actor.set_simulate_physics(True)

npc.append(actor)
print(npc)