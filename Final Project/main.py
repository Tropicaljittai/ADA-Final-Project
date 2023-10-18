from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

player = fpc()
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

#controlling the model
def update():
    raycast(car1.position, direction=(1,0,0), distance=7, debug=True)
    raycast(car1.position, direction=(-1,0,0), distance=7, debug=True)
    raycast(car1.position, direction=(1,0,100), distance=7, debug=True)
    raycast(car1.position, direction=(1,0,-100), distance=7, debug=True)
    raycast(car1.position, direction=(1,0,1), distance=7, debug=True)
    raycast(car1.position, direction=(1,0,-1), distance=7, debug=True)
    raycast(car1.position, direction=(-1,0,-1), distance=7, debug=True)
    raycast(car1.position, direction=(-1,0,1), distance=7, debug=True)

    if (car1.intersects(car2).hit == False):
        car1.rotation_y += (held_keys['right arrow'] - held_keys['left arrow'])* time.dt*150
        car1.position += (held_keys['up arrow'] - held_keys['down arrow'])* car1.speed * time.dt * car1.forward
    else:
        car1.position -=  car1.speed * time.dt * car1.forward + Vec3(-1,0,0)
    if(car2.intersects(car1).hit == False):
        car2.rotation_y += (held_keys['j'] - held_keys['l'])* time.dt*100
        car2.position += (held_keys['i'] - held_keys['k'])* car1.speed * time.dt * car2.forward
    else:
        car2.position -=  car2.speed * time.dt * car2.forward + Vec3(-1,0,0)        

app.run()