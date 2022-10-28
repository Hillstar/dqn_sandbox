import pygame
import uuid

class boundary:
    def __init__(self):
        self.id = uuid.uuid4()
        self.rect = pygame.Rect(300, 300, 150, 20)
    
    def rotate(self):
        # Just swap values to rotate to 90 degrees
        height = self.rect.height
        self.rect.height = self.rect.width
        self.rect.width = height
