# snake.py
import pygame
from game_config import *

class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = RIGHT
        self.growing = False

    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != DOWN:
            self.direction = UP
        elif key == pygame.K_DOWN and self.direction != UP:
            self.direction = DOWN
        elif key == pygame.K_LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif key == pygame.K_RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        head = self.body[0][:]
        if self.direction == UP:
            head[1] -= BLOCK_SIZE
        elif self.direction == DOWN:
            head[1] += BLOCK_SIZE
        elif self.direction == LEFT:
            head[0] -= BLOCK_SIZE
        elif self.direction == RIGHT:
            head[0] += BLOCK_SIZE

        self.body.insert(0, head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def eat_food(self, food_position):
        return self.body[0] == food_position

    def check_collision_with_boundaries(self):
        x, y = self.body[0]
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT

    def check_collision_with_self(self):
        return self.body[0] in self.body[1:]

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, (*segment, BLOCK_SIZE, BLOCK_SIZE))
