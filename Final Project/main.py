import csv
import math
import time

from env import environment

from car import Car

# from env import environment
from ursina import *
import random
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

# create a window
app = Ursina(
    title = "joseph",
    development_mode = True
)
EditorCamera()
Sky()

environment1 = environment()


# def create_barrier(position, scale):
#     return Entity(model='cube', color=color.green, scale=scale, position=position)
    
# barrier_left = create_barrier(position=(environment1.ground - environment1.ground.scale_x / 2, 0, 0), scale=(0.1, 1, environment1.ground.scale_z))
# barrier_right = create_barrier(position=(environment1.ground.x + environment1.ground.scale_x / 2, 0, 0), scale=(0.1, 1, environment1.ground.scale_z))
# barrier_front = create_barrier(position=(0, 0, environment1.ground.z - environment1.ground.scale_z / 2), scale=(environment1.ground.scale_x, 1, 0.1))
# barrier_back = create_barrier(position=(0, 0, environment1.ground.z + environment1.ground.scale_z / 2), scale=(environment1.ground.scale_x, 1, 0.1))

#camera config
camera.fov = 60
camera.position = (-4, 35, -30)
camera.rotation = (53, 10, 0)
pos = 0

# camera.parent = environment1.modelList["car"]
# camera.z = -40
# camera.x = -10
# camera.y = 50
respawn_pressed = False
barrier_visible_pressed = False
barrier_visible_active = False
driving_mode_pressed = False

#controlling the model
def update():
    #Change Camera Position
    global pos, camera_button_pressed, respawn_pressed, barrier_visible_pressed, barrier_visible_active
    if held_keys["c"]:
        if not camera_button_pressed:
            if pos == 0:
                camera.position = (13,14,-40)
                camera.rotation = (18,-15,0)
                pos += 1
            elif pos == 1:
                camera.position = (5,5,-30)
                camera.rotation = (0,0,0)
                pos += 1
            elif pos == 2:
                pos = 0
            camera_button_pressed = True
    else:
        camera_button_pressed = False
    
    if held_keys["p"]:
        if not respawn_pressed:
            environment1.summonCar(True)

    if held_keys["l"]:
        if not respawn_pressed:
            environment1.summonCar(False)

    if held_keys["v"]:
        if not barrier_visible_pressed:
            environment1.visibleBarrier(barrier_visible_active)
            barrier_visible_active = False if barrier_visible_active else True
        
app.run()
