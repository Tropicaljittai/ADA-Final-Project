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
            "tiang6" : Tiang(color = color.black, position = (13,0,-1), rotation = (0,180,0))
        }
        for key, value in kwargs.items():
            setattr(self, key, value)
