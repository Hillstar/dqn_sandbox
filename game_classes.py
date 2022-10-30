import pygame
import uuid
from enum import Enum

# object type
class Object_type(Enum):
    CAR = 1
    BOUNDARY = 2
    FINISH = 3

class Game_object():
    def __init__(self, obj_type, color = (255, 255, 255), center = (300, 300), size = (150, 20)):
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
    def __init__(self, center = (300, 300), size = (150, 20)):
        color = (255, 255, 255)
        super().__init__(Object_type.BOUNDARY, color, center, size)
    
class Car(Game_object):
    move_speed = 500

    def __init__(self, center = (300, 300), size = (50, 50)):
        color = (0, 255, 0)
        super().__init__(Object_type.CAR, color, center, size)

class Finish(Game_object):
    def __init__(self, center = (300, 300), size = (150, 20)):
        color = (0, 0, 255)
        super().__init__(Object_type.FINISH, color, center, size)