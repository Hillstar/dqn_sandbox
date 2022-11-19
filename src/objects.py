import pygame
import uuid
from enum import Enum

# object type
class Object_type(Enum):
    PLAYER = 1
    SCENE_OBJECT = 2
    CHECK_POINT = 3

class Object():
    def __init__(self, obj_type, center = (300, 300), color = (255, 255, 255), size = (45, 45)):
        self.id = uuid.uuid4()
        self.type = obj_type
        self.color = color
        left = center[0] - size[0] / 2
        top = center[1] - size[1] / 2
        self.rect = pygame.Rect((left, top), size)

class Scene_object(Object):
    def __init__(self, obj_type = Object_type.SCENE_OBJECT, center = (300, 300), color = (255, 255, 255), hit_color = (220, 220, 220), size = (45, 45)):
        self.hit = False
        self.default_color = color
        self.hit_color = hit_color
        super().__init__(obj_type, center, color, size)

    def get_color(self):
        if self.hit:
            return self.hit_color
        else:
            return self.default_color
    
    def rotate(self):
        # Just swap values to rotate to 90 degrees
        height = self.rect.height
        self.rect.height = self.rect.width
        self.rect.width = height

class Player(Object):
    def __init__(self, center = (75, 75), color = (100, 255, 100), size = (50, 50)):
        self.move_speed = 70
        super().__init__(Object_type.PLAYER, center, color, size)

    def reset_position(self):
        self.rect.center = (75, 75)
        self.color = (33, 255, 33)
