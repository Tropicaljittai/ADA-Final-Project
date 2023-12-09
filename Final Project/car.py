import csv
from ursina import *
import time
import random
from tiang import Tiang
from ursina.prefabs.first_person_controller import FirstPersonController as fpc

class Car(Entity):
    rayCount = 10
    rayLength = 10
    raySpread = 360
    ray_lines = []

    driving_data = []
    is_driving = False
    sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

    cooldown_update = 1.0
    cooldown_timer = 0.0
    
    def __init__(self, **kwargs):
        super().__init__(
        model = 'asset/gltf/car_sedan.gltf',
        position = (-1.3,0.1,-0.6),
        scale = 3.5,
        is_driving = False
        )
        # Physics
        self.gravity = (0, -9.8, 0)

        # Car Statistics
        self.engine_force = 0
        self.braking_force = 0
        self.steering_force = 0
        self.topspeed = -5
        self.acceleration = 0.05
        self.braking_strength = 5
        self.friction = 0.6
        self.camera_speed = 8
        self.rigidbody = True
        self.rotation_parent = Entity()

        # Controls
        self.controls = "wasd"

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

    # def save_to_csv(self):
    #     # Open a CSV file for writing
    #     with open('driving_data.csv', 'w', newline='') as file:
    #         writer = csv.DictWriter(file, fieldnames=Car.driving_data[0].keys())
    #         # Write the data to the CSV file
    #         writer.writeheader()
    #         for data in Car.driving_data:
    #             writer.writerow(data)
    #     # Reset the Car.driving_data list
    #     Car.driving_data = []
    #
    def rotate_vector_y(vector, angle_degrees):
            angle_radians = math.radians(angle_degrees)
            x = vector.x * math.cos(angle_radians) - vector.z * math.sin(angle_radians)
            z = vector.x * math.sin(angle_radians) + vector.z * math.cos(angle_radians)
            return Vec3(x, vector.y, z)
    
    def printCollsion(self,r1,r2,r3,r4,r5,r6,r7,r8):
        print(f'''
        R1 - Red = {r1.hit}
        R2 - Orange = {r2.hit}
        R3 - Yellow = {r3.hit}
        R4 - Green = {r4.hit}
        R5 - Blue = {r5.hit}
        R6 - Magenta = {r6.hit}
        R7 - Pink = {r7.hit}
        R8 - White = {r8.hit}
              ''')

    def cast_and_color_ray(self, direction, initial_color):
        ray = raycast(self.position, direction=direction, distance=7, debug=True, color=initial_color)
        if ray.hit:  # If the raycast hits something, change the color to black
            raycast(self.position, direction=direction, distance=7, debug=True, color=color.black)
        return ray

    def update(self):
        self.rotation_y = 90
        print(self.rotation_y)
        left_45_direction = Car.rotate_vector_y(self.forward, -45)
        left_90_direction = Car.rotate_vector_y(self.forward, -90)
        right_45_direction = Car.rotate_vector_y(self.forward, 45)

        #back sensor
        r1 = self.cast_and_color_ray(self.forward, color.red)
        #front sensor
        r2 = self.cast_and_color_ray(-self.forward, color.orange)
        #south west sensor
        r3 = self.cast_and_color_ray(left_45_direction, color.yellow)
        #north east sensor
        r4 = self.cast_and_color_ray(-left_45_direction, color.green)
        #right sensor
        r5 = self.cast_and_color_ray(-left_90_direction, color.blue)
        #left sensor
        r6 = self.cast_and_color_ray(left_90_direction, color.magenta)
        #south east sensor
        r7 = self.cast_and_color_ray(right_45_direction, color.pink)
        #north west sensor
        r8 = self.cast_and_color_ray(-right_45_direction, color.white)


        if Car.cooldown_timer == 0.0:
            self.printCollsion(r1,r2,r3,r4,r5,r6,r7,r8)

        Car.cooldown_timer += time.dt

        if (Car.cooldown_timer >= Car.cooldown_update):
            Car.cooldown_timer = 0.0

        # if self.driving:
        #     Car.is_driving = True
        #     data = {
        #         'speed': self.speed,
        #         'steering_angle': math.degrees(self.pivot.rotation_z),
        #         'position': self.position,
        #         'rotation': self.rotation,
        #         'rotation_speed': self.rotation_speed
        #     }
        #     Car.driving_data.append(data)
        # else:
        #     Car.is_driving = False
        #
        #     if Car.driving_data:
        #         self.save_to_csv()


        y_ray = raycast(origin = self.world_position, direction = (0, -1, 0), ignore = [self, ])

        # The y rotation distance between the Car and the pivot
        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        # Gravity
        movementY = self.velocity_y / 50
        direction = (0, Car.sign(movementY), 0)

        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed / 6 * time.dt

        if self.speed >= 0.7:
            if self.steering_force > 0 or self.steering_force < 0:
                self.rotation_speed += self.steering_force * self.steering_amount * time.dt
                if self.speed >= 1:
                    self.speed -= self.turning_speed / 5 * time.dt
                elif self.speed <= 0:
                    self.speed += self.turning_speed / 5 * time.dt
            else:
                if self.rotation_speed > 0:
                    self.rotation_speed -= 5 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed += 5 * time.dt
        else:
            self.rotation_speed = 0

        # Cap the speed
        if self.speed <= self.topspeed:
            self.speed = self.topspeed
        if self.speed >= 7:
            self.speed = 7
        if self.speed <= 0 or self.speed >= 0:
            self.pivot.rotation_y = self.rotation_y


        # Cap the steering
        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed
        

        self.speed -= self.engine_force  * self.acceleration * 50 * time.dt
        self.speed -= self.engine_force  * -self.velocity_y * 4 * time.dt

        self.driving = True

        if self.engine_force == 0:
            self.driving = False
            if self.speed < -1:
                self.speed += self.friction * 5 * time.dt
            elif self.speed > 1:
                self.speed -= self.friction * 5 * time.dt

            if str(self.speed)[0:2] == '-0':
                self.speed = 0
            elif str(self.speed)[0] == '0':
                self.speed = 0


        # Hand Braking
        if self.speed < 0:
            if self.rotation_speed < 0:
                self.rotation_speed -= 3 * time.dt
            elif self.rotation_speed > 0:
                self.rotation_speed += 3 * time.dt
            self.speed += self.braking_force  * 20 * time.dt
            self.max_rotation_speed = 3.0
        if self.speed > 0:
            if self.rotation_speed < 0:
                self.rotation_speed -= 3 * time.dt
            elif self.rotation_speed > 0:
                self.rotation_speed += 3 * time.dt
            self.speed -= self.braking_force  * 20 * time.dt
            self.max_rotation_speed = 3.0

        if self.visible:
            if y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
                self.velocity_y = 0
                # Check if hitting a wall or steep slope
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                    # Set the y value to the ground's y value
                    self.y = y_ray.world_point.y + 0.3
                    self.hitting_wall = False
                else:
                    # Car is hitting a wall
                    self.hitting_wall = True

                if self.copy_normals:
                    self.ground_normal = self.position + y_ray.world_normal
                else:
                    self.ground_normal = self.position + (0, 180, 0)
        

            else:
                self.y += movementY * 50 * time.dt
                self.velocity_y -= 50 * time.dt
                self.rotation_parent.rotation = self.rotation

        # Movement
        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt
                
        # Collision Detection
        if movementX != 0:
            direction = (Car.sign(movementX), 0, 0)
            x_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if x_ray.distance > self.scale_x / 2 + abs(movementX):
                self.x += movementX

        if movementZ != 0:
            direction = (0, 0, Car.sign(movementZ))
            z_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if z_ray.distance > self.scale_z / 2 + abs(movementZ):
                self.z += movementZ