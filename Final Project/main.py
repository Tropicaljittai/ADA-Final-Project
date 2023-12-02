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

environment1 = environment()

#camera config
camera.fov = 60
camera.position = (5,5,-30)
camera.rotation = (0,0,0)
pos = 0

camera_button_pressed = False
#controlling the model
def update():
    #Change Camera Position
    global pos, camera_button_pressed
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
                follow = SmoothFollow(target=car1, speed=8, offset=[0,10,-4])
                camera.add_script(follow)
                pos = 0

            camera_button_pressed = True
    else:
        camera_button_pressed = False
    


app.run()
