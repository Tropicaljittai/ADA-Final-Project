from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

# player = fpc()
#models
ground = Entity(model = 'asset/obj/parking_lot.obj', collider = 'mesh', scale = 7, position  = (0,0,0))
car1 = Entity(model = "asset/gltf/car_sedan.gltf", position = (-1.3,0.4,-0.6), scale = 3.5, speed = 0)
car1.rotation = (0,-90,0)

car2 = Entity(model = "asset/gltf/car_taxi.gltf", position = (9,0.4,-3.7), scale = 3.5, speed = 0)
car2.rotation = (0,90,0)
smurfcat = Entity(model = "asset/gltf/smurfs.gltf", position = (-5,0,5), scale = 0.5)
#colliders
car1.collider = MeshCollider(car1, mesh=car1.model, center=Vec3(0,0,0))
car2.collider = MeshCollider(car2, mesh=car2.model, center=Vec3(0,0,0))

camera.position = (13,14,-40)
camera.rotation = (18,-15,0)

follow = SmoothFollow(target=car1, speed=8, offset=[0,10,-4])
camera.add_script(follow)
car1.car1state = 0

# Steering
car1.turning = 0

#Throttle
car1.speed = 0
car1.throttle = 0

#Brake
car1.braking = 0

ai_throttle = 0
ai_braking = 0
ai_turning = 0


#controlling the model
def update():
        
    ai_throttle = random.uniform(-1, 1.0)
    ai_braking = random.uniform(-1, 1.0)
    ai_turning = random.uniform(-1, 1.0)

    print(ai_throttle)
    # ai_turning = random.uniform(0.0, 1.0)
    #Car sensors
    r1 = raycast(car1.position, direction=(1,0,0), distance=7, debug=True)
    r2 = raycast(car1.position, direction=(-1,0,0), distance=7, debug=True)
    r3 = raycast(car1.position, direction=(1,0,100), distance=7, debug=True)
    r4 = raycast(car1.position, direction=(1,0,-100), distance=7, debug=True)
    r5 = raycast(car1.position, direction=(1,0,1), distance=7, debug=True)
    r6 = raycast(car1.position, direction=(1,0,-1), distance=7, debug=True)
    r7 = raycast(car1.position, direction=(-1,0,-1), distance=7, debug=True)
    r8 = raycast(car1.position, direction=(-1,0,1), distance=7, debug=True)


    car1.throttle = (car1.speed * time.dt) * car1.forward
    car1.position += car1.throttle
    
    # #Car movements manual
    # if held_keys['w']:
    #     if car1.speed > -5:
    #         car1.speed -= 2 * time.dt
    #     car1.speed += car1.braking * time.dt
    #     car1.rotation_y += time.dt*car1.turning
    #     if held_keys['a']:
    #         if car1.turning >  -20:
    #             car1.turning = -20
    #         if car1.turning > -100:
    #             car1.turning -= 15 * time.dt
        
    #     if held_keys['d']:
    #         if car1.turning < 20:
    #             car1.turning = 20
    #         if car1.turning < 100:
    #             car1.turning += 15 * time.dt

    # if held_keys['s']:
    #     if car1.speed < 5:
    #         car1.speed += 2 * time.dt
    #     car1.speed += car1.braking * time.dt
    #     car1.rotation_y += time.dt*car1.turning
    #     if held_keys['a']:
    #         if car1.turning >  -20:
    #             car1.turning = -20
    #         if car1.turning > -100:
    #             car1.turning -= 15 * time.dt
        
    #     if held_keys['d']:
    #         if car1.turning < 20:
    #             car1.turning = 20
    #         if car1.turning < 100:
    #             car1.turning += 15 * time.dt

    # if held_keys['space']:
    #     if car1.speed <= 0.03 and car1.speed >= -0.03:
    #         car1.speed = 0
    #         car1.braking = 0
    #     else:
    #         if car1.speed < 0:
    #             car1.braking += 2 * time.dt
    #         if car1.speed > 0:
    #             car1.braking -= 2 * time.dt


    # if not held_keys['a'] and not held_keys['d']:
    #     if car1.turning < 0:
    #         car1.turning += 100 * time.dt
    #     if car1.turning > 0:
    #         car1.turning -= 100 * time.dt

    # if not held_keys['space']:
    #     car1.braking = 0

    # if not held_keys['w'] and not held_keys['s']:
    #     if held_keys['a']:
    #         if car1.turning >  -20:
    #             car1.turning = -20
    #         if car1.turning > -100:
    #             car1.turning -= 15 * time.dt
        
    #     if held_keys['d']:
    #         if car1.turning < 20:
    #             car1.turning = 20
    #         if car1.turning < 100:
    #             car1.turning += 15 * time.dt
    #     if car1.speed < 0:
    #         car1.speed += 3 * time.dt
    #         car1.rotation_y += time.dt*car1.turning
    #     if car1.speed > 0:
    #         car1.speed -= 3  * time.dt
    #         car1.rotation_y += time.dt*car1.turning
    #     if car1.speed <= 0.01 and car1.speed >= -0.09:
    #         car1.speed = 0

    #Car movements for ai

    car1.braking = ai_braking * 5
    car1.speed = ai_throttle * 5
    car1.speed += car1.braking * time.dt 
    car1.rotation_y += ai_turning * 100

    car1.throttle = (car1.speed * time.dt) * car1.forward
    car1.position += car1.throttle

app.run()