import csv
import math
import time

from ursina import *
import random
from car import Car
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
        }
        self.barrierList = {
            "bar1": Entity(model = "wireframe_cube", scale = 35, position = (-30,0,0), collider = "box", color = color.red, visible = False),
            "bar2": Entity(model = "wireframe_cube", scale = 35, position = (40,0,0), collider = "box", color = color.blue, visible = False),
            "bar3": Entity(model = "wireframe_cube", scale = 35, position = (4,0,-36), collider = "box", color = color.green, visible = False),
            "bar4": Entity(model = "wireframe_cube", scale = 35, position = (4,0, 33), collider = "box", visible = False),
        }
        for key, value in kwargs.items():
            setattr(self, key, value)

    def summonCar(self):
        destroy(self.modelList["car"])
        self.modelList["car"] = Car()

    def visibleBarrier(self, bool):
        self.barrierList["bar1"].visible = bool
        self.barrierList["bar2"].visible = bool
        self.barrierList["bar3"].visible = bool
        self.barrierList["bar4"].visible = bool

    def calculate_reward(self, car):
        reward = 0
        # Calculate positive rewards for proximity to the parking spot
        distance_to_parking_spot = self.modelList['car'].position
        reward += max(0, 1 - distance_to_parking_spot)

        # Additional reward for proper parking alignment
        alignment = ...  # Calculate alignment angle
        reward += max(0, 1 - abs(alignment))

        # Penalize for collisions or moving away
        if car.has_collided:
            reward -= 5  # Example penalty for collision

        return reward