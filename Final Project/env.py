import csv
import math
import time
import numpy as np
from ursina import *
import random
from car import Car
from carObj import CarObj
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from gym import spaces
class environment(Entity):
    def __init__(self, **kwargs):
        self.ground = Entity(model = 'asset/obj/parkinglot.obj', collider = 'mesh', scale = 7, position  = (0,0,0)),
        self.target_pos = Vec3(9,2,-7)
        self.action_space = spaces.Discrete(4)
        min_x, max_x = -7, 7  # Spanning 14 meters in x-direction
        min_y, max_y = -21, 21  # Spanning 42 meters in y-direction
        min_yaw, max_yaw = 0,360
        self.observation_space = spaces.Box(low=np.array([min_x, min_y, min_yaw]),
                                            high=np.array([max_x, max_y, max_yaw]),
                                            dtype=np.float32)
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

    def cal_distance(self,pos1, pos2):
        return math.sqrt((pos1.x-pos2.x)**2 + (pos1.x-pos2.y)**2 + (pos1.z-pos2.z)**2)
    def get_state(self):
        car = self.modelList['car']
        pos = car.position
        rot = car.rotation
        speed = car.speed
        distance_to_target = self.cal_distance(car, self.target_pos)

        # Flatten the state into a single array
        # Assuming pos and rot are simple x, y, z coordinates
        state = np.array([pos.x, pos.y, pos.z, rot.x, rot.y, rot.z, speed, distance_to_target])

        return state

    def change_wireframe_color(self):
        self.modelList["rectangle_3d"].color = color.green
    def calculate_reward(self, car):
        reward = 0

        # Calculate the distance to the target
        distance_to_target = self.cal_distance(self.modelList['car'].position, self.target_pos)

        # Add reward based on proximity to the target
        # The closer the car is to the target, the higher the reward
        # You can adjust the scale factor to suit the specific scale of your environment
        proximity_reward = max(0, 10 - distance_to_target)  # Example: Reward decreases with distance
        reward += proximity_reward

        # Penalize for collisions
        if car.hitting_wall:
            reward -= 5

        # Cap the minimum reward
        reward = max(reward, -20)

        return reward

    def isDone(self):
        done = False
        if self.isParked():
            done = True
        if self.modelList['car'].hitting_wall:
            done = True

    def isParked(self):
        distance_to_target = self.cal_distance(self.modelList['car'], self.target_pos)
        parking_threshold = self.modelList['car'].length / 2  # Half the car's length as a threshold

        return distance_to_target <= parking_threshold

    def reset(self):
        # reset_car = self.summonCar(True)
        get_state = self.get_state()
        return get_state

    def step(self,action):
        reward = self.calculate_reward(self.modelList['car'])

        isDone = self.isDone()
        reset = self.reset()

        return self.get_state(), reward, isDone, reset
    
    def update(self):
        if self.modelList["car"].x < self.modelList["rectangle_3d"].x + self.modelList["rectangle_3d"].scale_x/2 and \
       self.modelList["car"].x > self.modelList["rectangle_3d"].x - self.modelList["rectangle_3d"].scale_x/2 and \
       self.modelList["car"].y < self.modelList["rectangle_3d"].y + self.modelList["rectangle_3d"].scale_y/2 and \
       self.modelList["car"].y > self.modelList["rectangle_3d"].y - self.modelList["rectangle_3d"].scale_y/2 and \
       self.modelList["car"].z < self.modelList["rectangle_3d"].z + self.modelList["rectangle_3d"].scale_z/2 and \
       self.modelList["car"].z > self.modelList["rectangle_3d"].z - self.modelList["rectangle_3d"].scale_z/2:
            self.change_wireframe_color()
            print("detected")