from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

# player = fpc()
#models
ground = Entity(model = 'asset/obj/ParkingLot.obj', collider = 'mesh', scale = 7, position  = (0,0,0))
car1 = Entity(model = "asset/gltf/car_sedan.gltf", position = (-1.3,0.4,-0.6), scale = 3.5, speed = 4)
car1.rotation = (0,-90,0)

car2 = Entity(model = "asset/gltf/car_taxi.gltf", position = (9,0.4,-3.7), scale = 3.5, speed = 4)
car2.rotation = (0,90,0)
smurfcat = Entity(model = "asset/gltf/smurfs.gltf", position = (-5,0,5), scale = 0.5)
#colliders
car1.collider = BoxCollider(car1, center=Vec3(0,0,0), size=Vec3(0.75,0.75,0.75))
car2.collider = BoxCollider(car2, center=Vec3(0,0,0), size=Vec3(0.75,0.75,0.75))

camera.position = (13,14,-40)
camera.rotation = (18,-15,0)

follow = SmoothFollow(target=car1, speed=8, offset=[0,10,-4])
camera.add_script(follow)


#controlling the model
def update():

    #Car sensors
    r1 = raycast(car1.position, direction=(1,0,0), distance=7, debug=True)
    r2 = raycast(car1.position, direction=(-1,0,0), distance=7, debug=True)
    r3 = raycast(car1.position, direction=(1,0,100), distance=7, debug=True)
    r4 = raycast(car1.position, direction=(1,0,-100), distance=7, debug=True)
    r5 = raycast(car1.position, direction=(1,0,1), distance=7, debug=True)
    r6 = raycast(car1.position, direction=(1,0,-1), distance=7, debug=True)
    r7 = raycast(car1.position, direction=(-1,0,-1), distance=7, debug=True)
    r8 = raycast(car1.position, direction=(-1,0,1), distance=7, debug=True)


    # Car movements
    if (car1.intersects(car2).hit == False):
        car1.position += (held_keys['s'] - held_keys['w'])* car1.speed * time.dt * car1.forward
        if held_keys['w']:
            car1.rotation_y += (held_keys['d'] - held_keys['a'])* time.dt*200
        if held_keys['s']:
            car1.rotation_y += (held_keys['d'] - held_keys['a'])* time.dt*200
          

app.run()