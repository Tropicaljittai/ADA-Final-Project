import csv
import math
import time

from ursina import *
import random
from car import Car
from carObj import CarObj
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

class environment(Entity):
    def __init__(self, **kwargs):
        self.ground = Entity(model = 'asset/obj/parkinglot.obj', collider = 'mesh', scale = 7, position  = (0,0,0)),
        self.modelList = {
            "car": Car(),
            "tiang1" : Tiang(color = color.red, position = (1,0,0)),
            "tiang2" : Tiang(color = color.blue, position = (0.75,0,-7)),
            "tiang3" : Tiang(color = color.green, position = (-5,0,-20)),
            "tiang4" : Tiang(color = color.yellow, position = (7.25,0,23), rotation = (0,180,0)),
            "tiang5" : Tiang(color = color.white, position = (7.25,0,16), rotation = (0,180,0)),
            "tiang6" : Tiang(color = color.black, position = (13,0,-1), rotation = (0,180,0)),
            "carObj1": CarObj(color = color.red, position = (-1,0,-0.5), rotation = (0,270,0)),
            "carObj2": CarObj(color = color.yellow, position = (-1,0,-3.75), rotation = (0,270,0)),
            "carObj3": CarObj(color = color.green, position = (-1,0,-10), rotation = (0,270,0)),
            "carObj4": CarObj(color = color.blue, position = (9,0,2.5), rotation = (0,90,0)),
            "carObj5": CarObj(color = color.brown, position = (9,0,-3.75), rotation = (0,90,0)),
            "carObj6": CarObj(color = color.gold, position = (9,0,-10), rotation = (0,90,0)),
           'rectangle_3d': Entity(model="cube", color=color.red, scale=(4, 4, 2.5), wireframe=True, position = (9,2,-7))
        }   
        self.barrierList = {
            "bar1": Entity(model = "wireframe_cube", scale = 35, position = (-30,0,0), collider = "box", color = color.red, visible = False),
            "bar2": Entity(model = "wireframe_cube", scale = 35, position = (40,0,0), collider = "box", color = color.blue, visible = False),
            "bar3": Entity(model = "wireframe_cube", scale = 35, position = (4,0,-36), collider = "box", color = color.green, visible = False),
            "bar4": Entity(model = "wireframe_cube", scale = 35, position = (4,0, 33), collider = "box", visible = False),
        }
        for key, value in kwargs.items():
            setattr(self, key, value)

    def summonCar(self, ai):
        destroy(self.modelList["car"])
        self.modelList["car"] = Car(is_driving = ai)

    def visibleBarrier(self, bool):
        self.barrierList["bar1"].visible = bool
        self.barrierList["bar2"].visible = bool
        self.barrierList["bar3"].visible = bool
        self.barrierList["bar4"].visible = bool
    
    def change_wireframe_color(self):
        self.modelList["rectangle_3d"].color = color.green

    def calculate_reward(self, car):
        reward = 0
        # Calculate positive rewards for proximity to the parking spot
        # distance_to_parking_spot = self.modelList['car'].position - target.position
        # reward += max(0, 1 - distance_to_parking_spot)

        # Additional reward for proper parking alignment
        # alignment = self.modelList['car'].rotation_y - 90 # Calculate alignment angle
        # reward += max(0, 1 - abs(alignment))

        # Penalize for collisions or moving away
        if car.has_collided:
            reward -= 5  # Example penalty for collision

        return reward
    
    def update(self):
        if self.modelList["car"].x < self.modelList["rectangle_3d"].x + self.modelList["rectangle_3d"].scale_x/2 and \
       self.modelList["car"].x > self.modelList["rectangle_3d"].x - self.modelList["rectangle_3d"].scale_x/2 and \
       self.modelList["car"].y < self.modelList["rectangle_3d"].y + self.modelList["rectangle_3d"].scale_y/2 and \
       self.modelList["car"].y > self.modelList["rectangle_3d"].y - self.modelList["rectangle_3d"].scale_y/2 and \
       self.modelList["car"].z < self.modelList["rectangle_3d"].z + self.modelList["rectangle_3d"].scale_z/2 and \
       self.modelList["car"].z > self.modelList["rectangle_3d"].z - self.modelList["rectangle_3d"].scale_z/2:
            self.change_wireframe_color()
            print("detected")