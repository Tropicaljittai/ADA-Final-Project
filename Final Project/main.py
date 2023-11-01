from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

# player = fpc()
# models
ground = Entity(model='asset/obj/ParkingLot.obj', collider='mesh', scale=7, position=(0, 0, 0))
car1 = Entity(model="asset/gltf/car_sedan.gltf", position=(-1.3, 0.4, -0.6), scale=3.5, speed=0)
car1.rotation = (0, -90, 0)

car2 = Entity(model="asset/gltf/car_taxi.gltf", position=(9, 0.4, -3.7), scale=3.5, speed=8)
car2.rotation = (0, 90, 0)
smurfcat = Entity(model="asset/gltf/smurfs.gltf", position=(-5, 0, 5), scale=0.5)
# colliders
car1.collider = MeshCollider(car1, mesh=car1.model, center=Vec3(0, 0, 0))
car2.collider = MeshCollider(car2, mesh=car2.model, center=Vec3(0, 0, 0))

camera.position = (13, 14, -40)
camera.rotation = (18, -15, 0)

follow = SmoothFollow(target=car1, speed=8, offset=[0, 10, -4])
camera.add_script(follow)
car1.car1state = 0

# Steering
car1.turning = 0

# Throttle
car1.throttle = 0

# Brake
car1.braking = 0


# controlling the model
def update():
    # Car sensors
    r1 = raycast(car1.position, direction=(1, 0, 0), distance=7, debug=True)
    r2 = raycast(car1.position, direction=(-1, 0, 0), distance=7, debug=True)
    r3 = raycast(car1.position, direction=(1, 0, 100), distance=7, debug=True)
    r4 = raycast(car1.position, direction=(1, 0, -100), distance=7, debug=True)
    r5 = raycast(car1.position, direction=(1, 0, 1), distance=7, debug=True)
    r6 = raycast(car1.position, direction=(1, 0, -1), distance=7, debug=True)
    r7 = raycast(car1.position, direction=(-1, 0, -1), distance=7, debug=True)
    r8 = raycast(car1.position, direction=(-1, 0, 1), distance=7, debug=True)

    car1.throttle = car1.speed * time.dt * car1.forward
    car1.position += car1.throttle

    # Car movements
    car1.rotation_y+=((held_keys['d']-held_keys['a'])*time.dt*100)
    car1.position += (car1.forward * (held_keys['w'] - held_keys['s']) * time.dt * 5.0)




app.run()
