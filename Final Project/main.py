import csv
import math
import time

from ursina import *
import random
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

# create a window
app = Ursina(
    title = "joseph",
    vsync = True,
    development_mode = True
)

#camera config
camera.fov = 60
camera.position = (5,5,-30)
camera.rotation = (0,0,0)

#models
ground = Entity(model = 'asset/obj/parkinglot.obj', collider = 'mesh', scale = 7, position  = (0,0,0))
car1 = Entity(model = "asset/gltf/car_sedan.gltf", position = (-1.3,0.1,-0.6), scale = 3.5, topspeed = -5, acceleration = 0.05, braking_strength = 5, friction = 0.6, camera_speed = 8, rigidbody = True)

#tiang/pole
tiang = Tiang(color = color.red, position = (1,0,0))
tiang2 = Tiang(color = color.blue, position = (0.75,0,-7))
tiang3 = Tiang(color = color.green, position = (-5,0,-20))
#rotated pole
tiang4 = Tiang(color = color.yellow, position = (7.25,0,23), rotation = (0,180,0))
tiang5 = Tiang(color = color.white, position = (7.25,0,16), rotation = (0,180,0))
tiang6 = Tiang(color = color.black, position = (13,0,-1), rotation = (0,180,0))

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

#driving data
driving_data = []
#recording
is_driving = False
#Sensors
rayCount = 10
rayLength = 10
raySpread = 360
ray_lines = []

line_shader = Shader(language=Shader.GLSL, vertex='''
#version 140
uniform mat4 modelview_projection;

in vec4 p3d_Vertex;

void main() {
    gl_Position = modelview_projection * p3d_Vertex;
}
''', fragment='''
#version 140

uniform vec4 color;
out vec4 fragColor;

void main() {
    fragColor = color;
}
''')



def save_to_csv():
    global driving_data
    # Open a CSV file for writing
    with open('driving_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=driving_data[0].keys())
        # Write the data to the CSV file
        writer.writeheader()
        for data in driving_data:
            writer.writerow(data)
    # Reset the driving_data list
    driving_data = []
#controlling the model
def update():
    global is_driving, driving_data
    for i in range(rayCount):
        rayAngle = i / (rayCount) * raySpread - raySpread / 2
        direction = Vec3(math.sin(math.radians(rayAngle)), 0, -math.cos(math.radians(rayAngle)))
        start_point = car1.position
        end_point = car1.position + direction * rayLength

        ray_line = Entity(model='cube', shader=line_shader, color=color.yellow, scale=(0.05, 0.05, rayLength))
        ray_line.position = (start_point + end_point)/2
        ray_line.look_at(end_point)
        ray_lines.append(ray_line)
    if car1.driving:
        is_driving = True
        data = {
            'speed': car1.speed,
            'steering_angle': math.degrees(car1.pivot.rotation_z),
            'position': car1.position,
            'rotation': car1.rotation,
            'rotation_speed': car1.rotation_speed

        }
        driving_data.append(data)
    else:
        is_driving = False

        if driving_data:
            save_to_csv()


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

    if car1.speed >= 0.7:
        if held_keys[car1.controls[1]] or held_keys["left arrow"]:
            car1.rotation_speed += car1.steering_amount * time.dt
            if car1.speed >= 1:
                car1.speed -= car1.turning_speed / 5 * time.dt
            elif car1.speed <= 0:
                car1.speed += car1.turning_speed / 5 * time.dt
        elif held_keys[car1.controls[3]] or held_keys["right arrow"]:
            car1.rotation_speed -= car1.steering_amount * time.dt
            if car1.speed >= 1:
                car1.speed -= car1.turning_speed /5 * time.dt
            elif car1.speed <= 0:
                car1.speed += car1.turning_speed / 5 * time.dt
        else:
            if car1.rotation_speed > 0:
                car1.rotation_speed -= 5 * time.dt
            elif car1.rotation_speed < 0:
                car1.rotation_speed += 5 * time.dt
    elif car1.speed <= -0.7:
        if held_keys[car1.controls[1]] or held_keys["left arrow"]:
            car1.rotation_speed -= car1.steering_amount * time.dt
            if car1.speed >= 1:
                car1.speed -= car1.turning_speed / 5 * time.dt
            elif car1.speed <= 0:
                car1.speed += car1.turning_speed / 5 * time.dt
        elif held_keys[car1.controls[3]] or held_keys["right arrow"]:
            car1.rotation_speed += car1.steering_amount * time.dt
            if car1.speed >= 1:
                car1.speed -= car1.turning_speed /5 * time.dt
            elif car1.speed <= 0:
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
    if car1.speed <= 0 or car1.speed >= 0:
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

    # Braking
    if held_keys[car1.controls[2] or held_keys["down arrow"]]:
        car1.speed += car1.acceleration * 50 * time.dt
        car1.speed += -car1.velocity_y * 4 * time.dt

        car1.driving = True

    if not (held_keys[car1.controls[0]] or held_keys["up arrow"]) and not (held_keys[car1.controls[2] or held_keys["down arrow"]]):
        car1.driving = False
        if car1.speed < -1:
            car1.speed += car1.friction * 5 * time.dt
        elif car1.speed > 1:
            car1.speed -= car1.friction * 5 * time.dt

        if str(car1.speed)[0:2] == '-0':
            car1.speed = 0
        elif str(car1.speed)[0] == '0':
            car1.speed = 0


    # Hand Braking
    if held_keys["space"]:
        if car1.speed < 0:
            if car1.rotation_speed < 0:
                car1.rotation_speed -= 3 * time.dt
            elif car1.rotation_speed > 0:
                car1.rotation_speed += 3 * time.dt
            car1.speed += 20 * time.dt
            car1.max_rotation_speed = 3.0
        if car1.speed > 0:
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
                car1.y = y_ray.world_point.y + 0.3
                car1.hitting_wall = False
            else:
                # Car is hitting a wall
                car1.hitting_wall = True

            if car1.copy_normals:
                car1.ground_normal = car1.position + y_ray.world_normal
            else:
                car1.ground_normal = car1.position + (0, 180, 0)
    

        else:
            car1.y += movementY * 50 * time.dt
            car1.velocity_y -= 50 * time.dt
            car1.rotation_parent.rotation = car1.rotation

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


app.run()
