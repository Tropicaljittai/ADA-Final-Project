import csv
import math
import time
import numpy as np
from env import environment
import gym
from car import Car
from ppo_agent import Agent
from env import environment
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
env = gym.make('CartPole-v0')
environment1 = environment()
N = 20
batch_size = 5
n_epochs = 4
alpha = 0.0003
agent = Agent(n_actions=environment1.action_space.n, batch_size=batch_size,
                    alpha=alpha, n_epochs=n_epochs,
                    input_dims=environment1.observation_space.shape)


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
    n_games = 300
    best_score = -100
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = environment1.reset()
        done = False
        score = 0
        while not done:
            print(observation)
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = environment1.step(action)
            n_steps += 1
            score += reward
            agent.remember(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
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
