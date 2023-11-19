from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

class Tiang(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = "asset/obj/tiang.obj"
        self.scale = 6.5
        self.collider = 'box'
        self.collision = True
        self.rigidbody = True

        for key, value in kwargs.items():
            setattr(self, key, value)

