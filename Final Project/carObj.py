import csv
from ursina import *
import time
import random
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

class CarObj(Entity):
    def __init__(self, **kwargs):
        super().__init__(
        model = 'asset/gltf/car_sedan.gltf',
        position = (-1.3,0.1,-0.6),
        scale = 3.5,
        is_driving = False
        )
        # Physics
        self.gravity = (0, -9.8, 0)
        self.collider = 'mesh'
        # Car Statistics
        self.engine_force = 1
        self.braking_force = 0
        self.steering_force = -1
        self.topspeed = -5
        self.acceleration = 0.05
        self.braking_strength = 5
        self.friction = 0.6
        self.camera_speed = 8
        self.rigidbody = True
        self.rotation_parent = Entity()

        # Car's values
        self.copy_normals = False
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.steering_amount = 8
        self.turning_speed = 5
        self.pivot_rotation_distance = 1

        # Bools
        self.driving = False
        self.braking = False

        self.ai = False
        self.ai_list = []

        # Pivot for drifting
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        pass