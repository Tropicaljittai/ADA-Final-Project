from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

class Tiang(Entity):
    cooldown_timer = 0.0
    cooldown_update = 1.0
    def __init__(self, **kwargs):
        super().__init__()
        self.name = ""
        self.model = "asset/obj/tiang.obj"
        self.scale = 6.5
        self.collider = 'mesh'
        self.collision = True
        self.rigidbody = True

        # Physics
        self.gravity = Vec3(0, -9.8, 0)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        pass
    #    self.y += self.gravity.y * time.dt