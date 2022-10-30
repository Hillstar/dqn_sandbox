import pygame
import uuid

class car:
    move_speed = 500

    def __init__(self, center = (300, 300), size = (50, 50)):
        self.id = uuid.uuid4()
        self.rect = pygame.Rect(center, size)
