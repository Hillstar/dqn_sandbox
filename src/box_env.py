from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np
import time

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

from scene import Scene
from scene import Move_type

HITS_TO_WIN = 3

class Box_env(py_environment.PyEnvironment):

    def __init__(self):
        self.scene = Scene()
        self.start_time = time.time()
        self.step_rew = 0

        width, height = self.scene.get_screen_size()

        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')

        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(width, height, 3), dtype=np.uint8, 
            minimum=0, maximum=255, name='observation')
        
        self.scene.load_scene()
        self.check_point_hits = 0

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self.scene.restart_scene()
        self.start_time = time.time()
        self.check_point_hits = 0
        pixels = self.scene.get_screen_pixels()
        return ts.restart(pixels)

    def _step(self, action):
        self.scene.move_player(action = Move_type(action.item()))
        self.scene.render_scene()

        pixels = self.scene.get_screen_pixels()

        if time.time() - self.start_time > 15: # TIMEOUT
            self.scene.restart_scene()
            self.start_time = time.time()
            self.check_point_hits = 0
            reward = -10
            print("TMT")
            return ts.termination(pixels, reward)

        if self.scene.boundary_hit: # BOUNDARY
            self.scene.restart_scene()
            self.start_time = time.time()
            self.check_point_hits = 0
            reward = -10
            print("BNDR")
            return ts.termination(pixels, reward)

        elif self.scene.get_collisions():
            self.check_point_hits += 1
            if self.check_point_hits >= HITS_TO_WIN:
                self.scene.restart_scene()
                self.check_point_hits = 0
                self.start_time = time.time()
                reward = 20
                print("WIN")
                return ts.termination(pixels, reward)
            else:
                self.start_time = time.time()
                reward = 15
                print("CHECK POINT")
                return ts.transition(pixels, reward=reward, discount=1.0)
        
        else:
            return ts.transition(pixels, reward=0, discount=1.0)