from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

# create a window
app = Ursina()

#models
ground = Entity(model = 'asset/obj/ParkingLot.obj', collider = 'mesh', scale = 7, position  = (0,0,0))

car1 = Entity(model = "asset/gltf/car_sedan.gltf", position = (-1.3,0.1,-0.6), scale = 3.5, topspeed = -5, acceleration = 0.05, braking_strength = 5, friction = 0.6, camera_speed = 8   )

car1.rotation_parent = Entity()

# Controls
car1.controls = "wasd"

# Car's values
car1.copy_normals = False
car1.speed = 0
car1.velocity_y = 0
car1.rotation_speed = 0
car1.max_rotation_speed = 2.6
car1.steering_amount = 8
car1.turning_speed = 5
car1.pivot_rotation_distance = 1


# Bools
car1.driving = False
car1.braking = False

car1.ai = False
car1.ai_list = []

# Pivot for drifting
car1.pivot = Entity()
car1.pivot.position = car1.position
car1.pivot.rotation = car1.rotation

camera.position = (13,14,-40)
camera.rotation = (18,-15,0)

follow = SmoothFollow(target=car1, speed=8, offset=[0,10,-4])
camera.add_script(follow)


#controlling the model
def update():
    y_ray = raycast(origin = car1.world_position, direction = (0, -1, 0), ignore = [car1, ])

        # The y rotation distance between the car and the pivot
    car1.pivot_rotation_distance = (car1.rotation_y - car1.pivot.rotation_y)

    # Gravity
    movementY = car1.velocity_y / 50
    direction = (0, sign(movementY), 0)

    car1.rotation_y += car1.rotation_speed * 50 * time.dt

    if car1.rotation_speed > 0:
        car1.rotation_speed -= car1.speed / 6 * time.dt
    elif car1.rotation_speed < 0:
        car1.rotation_speed += car1.speed / 6 * time.dt

    if car1.speed > 1 or car1.speed < -1:
        if held_keys[car1.controls[1]] or held_keys["left arrow"]:
            car1.rotation_speed -= car1.steering_amount * time.dt
            if car1.speed > 1:
                car1.speed -= car1.turning_speed * time.dt
            elif car1.speed < 0:
                car1.speed += car1.turning_speed / 5 * time.dt
        elif held_keys[car1.controls[3]] or held_keys["right arrow"]:
            car1.rotation_speed += car1.steering_amount * time.dt
            if car1.speed > 1:
                car1.speed -= car1.turning_speed * time.dt
            elif car1.speed < 0:
                car1.speed += car1.turning_speed / 5 * time.dt
        else:
            if car1.rotation_speed > 0:
                car1.rotation_speed -= 5 * time.dt
            elif car1.rotation_speed < 0:
                car1.rotation_speed += 5 * time.dt
    else:
        car1.rotation_speed = 0

    # Cap the speed
    if car1.speed <= car1.topspeed:
        car1.speed = car1.topspeed
    if car1.speed >= 7:
        car1.speed = 7
    if car1.speed <= 0:
        car1.pivot.rotation_y = car1.rotation_y


    # Cap the steering
    if car1.rotation_speed >= car1.max_rotation_speed:
        car1.rotation_speed = car1.max_rotation_speed
    if car1.rotation_speed <= -car1.max_rotation_speed:
        car1.rotation_speed = -car1.max_rotation_speed
    

    if held_keys[car1.controls[0]] or held_keys["up arrow"]:
        car1.speed -= car1.acceleration * 50 * time.dt
        car1.speed -= -car1.velocity_y * 4 * time.dt

        car1.driving = True
    else:
        car1.driving = False
        if car1.speed < -1:
            car1.speed += car1.friction * 5 * time.dt
        elif car1.speed > 1:
            car1.speed -= car1.friction * 5 * time.dt

    # Braking
    if held_keys[car1.controls[2] or held_keys["down arrow"]]:
        car1.speed += car1.braking_strength * time.dt
        car1.braking = True
    else:
        car1.braking = False

    # Hand Braking
    if held_keys["space"]:
        if car1.rotation_speed < 0:
            car1.rotation_speed -= 3 * time.dt
        elif car1.rotation_speed > 0:
            car1.rotation_speed += 3 * time.dt
        car1.speed -= 20 * time.dt
        car1.max_rotation_speed = 3.0

    if car1.visible:
        if y_ray.distance <= car1.scale_y * 1.7 + abs(movementY):
            car1.velocity_y = 0
            # Check if hitting a wall or steep slope
            if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - car1.world_y < 0.5:
                # Set the y value to the ground's y value
                car1.y = y_ray.world_point.y + 1.4
                car1.hitting_wall = False
            else:
                # Car is hitting a wall
                car1.hitting_wall = True

            if car1.copy_normals:
                car1.ground_normal = car1.position + y_ray.world_normal
            else:
                car1.ground_normal = car1.position + (0, 180, 0)

            # Rotates the car according to the grounds normals
            if not car1.hitting_wall:
                car1.rotation_parent.look_at(car1.ground_normal, axis = "up")
                car1.rotation_parent.rotate((0, car1.rotation_y + 180, 0))
            else:
                car1.rotation_parent.rotation = car1.rotation

        else:
            car1.y += movementY * 50 * time.dt
            car1.velocity_y -= 50 * time.dt
            car1.rotation_parent.rotation = car1.rotation
            car1.start_fall = True

     # Movement
    movementX = car1.pivot.forward[0] * car1.speed * time.dt
    movementZ = car1.pivot.forward[2] * car1.speed * time.dt

    # Collision Detection
    if movementX != 0:
        direction = (sign(movementX), 0, 0)
        x_ray = raycast(origin = car1.world_position, direction = direction, ignore = [car1, ])

        if x_ray.distance > car1.scale_x / 2 + abs(movementX):
            car1.x += movementX

    if movementZ != 0:
        direction = (0, 0, sign(movementZ))
        z_ray = raycast(origin = car1.world_position, direction = direction, ignore = [car1, ])

        if z_ray.distance > car1.scale_z / 2 + abs(movementZ):
            car1.z += movementZ

    print(car1.speed)

   

app.run()