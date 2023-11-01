from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina()

# player = fpc()
#models
ground = Entity(model = 'asset/obj/ParkingLot.obj', collider = 'mesh', scale = 7, position  = (0,0,0))
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
car1.throttle = 0

#Brake
car1.braking = 0

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

    car1.throttle = car1.speed * time.dt * car1.forward
    car1.position += car1.throttle
    
    #Car movements
    if held_keys['w'] or held_keys['s']:

        if held_keys['w'] and held_keys['s']:
            car1.speed = 0
        if held_keys['w']:
            if(car1.speed > -3):
                car1.speed -= 1 * time.dt

        if held_keys['s']:
            if(car1.speed < 3):
                car1.speed += 1 * time.dt
                car1.rotation_directions[0,0,0]
                


        if (held_keys['w'] or held_keys['s']) and held_keys['a']:
            if car1.turning > 0:
                car1.turning = 0
            if car1.turning > -35:
                car1.turning -= 20 * time.dt
            car1.rotation_y += time.dt*car1.turning
        if (held_keys['w'] or held_keys['s']) and held_keys['d']:
            if car1.turning < 0:
                car1.turning = 0
            if car1.turning < 35:
                car1.turning += 20 * time.dt
            car1.rotation_y += time.dt*car1.turning
        
        if not held_keys['a'] and not held_keys['d']:

            if car1.turning < 0:
                car1.turning += 10 * time.dt
            if car1.turning > 0:
                car1.turning -= 10 * time.dt

    if not held_keys['w'] and not held_keys['s']:

        if(car1.speed > 0):
            car1.speed -= 1 * time.dt
        if(car1.speed < 0):
            car1.speed += 1 * time.dt
        


        if not held_keys['a'] and not held_keys['d']:

            if car1.turning < 0:
                car1.turning += 10 * time.dt
            if car1.turning > 0:
                car1.turning -= 10 * time.dt

    if held_keys['a'] or held_keys['d']:
        if held_keys['a'] and held_keys['d']:
            car1.turning = 0
        elif held_keys['a']:
            if int(car1.speed) != 0:
                if car1.turning > 0:
                    car1.turning = 0
                if car1.turning > -35:
                    car1.turning -= 10 * time.dt
                car1.rotation_y += time.dt*car1.turning
        elif held_keys['d']:
            if int(car1.speed) != 0:
                if car1.turning < 0:
                    car1.turning = 0
                if car1.turning < 35:
                    car1.turning += 10 * time.dt
                car1.rotation_y += time.dt*car1.turning

    if held_keys['space']:
        if car1.speed > 0:
            car1.speed -= 2 * time.dt
        if car1.speed < 0:
            car1.speed += 2 * time.dt

    print("Speed: ",car1.speed)

    



app.run()