import pygame
import uuid

class boundary:
    def __init__(self, center = (300, 300), size = (150, 20)):
        self.id = uuid.uuid4()
        self.rect = pygame.Rect(center, size)
    
    def rotate(self):
        # Just swap values to rotate to 90 degrees
        height = self.rect.height
        self.rect.height = self.rect.width
        self.rect.width = height
