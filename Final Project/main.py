from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

player = fpc()
#models
ground = Entity(model = 'asset/obj/ParkingLot.obj', collider = 'mesh', scale = 5, position  = (0,0,0))
car1 = Entity(model = "asset/gltf/car_sedan.gltf", position = (5,0.4,5), scale = 5, speed = 8)
car2 = Entity(model = "asset/gltf/car_taxi.gltf", position = (10,0.4,5), scale = 5, speed = 8)
smurfcat = Entity(model = "asset/gltf/smurfs.gltf", position = (-5,0,5), scale = 0.5)
#colliders
car1.collider = BoxCollider(car1, center=Vec3(0,0,0), size=Vec3(0.75,0.75,0.75))
car2.collider = BoxCollider(car2, center=Vec3(0,0,0), size=Vec3(0.75,0.75,0.75))

#controlling the model
def update():
    if (car1.intersects(car2).hit == False):
        car1.rotation_y += (held_keys['right arrow'] - held_keys['left arrow'])* time.dt*100
        car1.position += (held_keys['up arrow'] - held_keys['down arrow'])* car1.speed * time.dt * car1.forward
    else:
        car1.position -=  car1.speed * time.dt * car1.forward + Vec3(-1,0,0)
    if(car2.intersects(car1).hit == False):
        car2.rotation_y += (held_keys['j'] - held_keys['l'])* time.dt*100
        car2.position += (held_keys['i'] - held_keys['k'])* car1.speed * time.dt * car2.forward
    else:
        car2.position -=  car2.speed * time.dt * car2.forward + Vec3(-1,0,0)        

app.run()