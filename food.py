# food.py
import pygame
import random
from game_config import *

class Food:
    def __init__(self):
        self.position = [random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE),
                         random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)]

    def spawn(self):
        self.position = [random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE),
                         random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)]

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, (*self.position, BLOCK_SIZE, BLOCK_SIZE))
