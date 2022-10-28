import pygame
import uuid

class car:

    move_speed = 300
    v_cdt = 100
    h_cdt= 100

    def __init__(self):
        self.id = uuid.uuid4()
        self.rect = pygame.Rect(300, 300, 75, 75)
