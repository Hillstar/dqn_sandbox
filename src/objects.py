import pygame
import uuid
from enum import Enum

# object type
class Object_type(Enum):
    PLAYER = 1
    BOUNDARY = 2
    FINISH = 3

class Game_object():
    def __init__(self, obj_type, center = (300, 300), color = (255, 255, 255), size = (150, 20)):
        self.id = uuid.uuid4()
        self.type = obj_type
        self.color = color
        self.rect = pygame.Rect(center, size)

    def rotate(self):
        # Just swap values to rotate to 90 degrees
        height = self.rect.height
        self.rect.height = self.rect.width
        self.rect.width = height

class Boundary(Game_object):
    def __init__(self, obj_type = Object_type.BOUNDARY, center = (300, 300), color = (255, 255, 255), size = (100, 20)):
        self.hit = False
        self.default_color = color
        self.hit_color = (255, 0, 0)
        super().__init__(obj_type, center, color, size)

    def get_color(self):
        if self.hit:
            return self.hit_color
        else:
            return self.default_color

class Finish(Boundary):
    def __init__(self, center = (300, 300), size = (100, 100)):
        color = (0, 0, 255)
        super().__init__(Object_type.FINISH, center, color, size)

class Player(Game_object):
    def __init__(self, center = (50, 50), size = (50, 50)):
        self.move_speed = 70
        color = (0, 255, 0)
        super().__init__(Object_type.PLAYER, center, color, size)

    def reset_position(self):
        self.rect.center = (50, 50)
        self.color = (33, 255, 33)
