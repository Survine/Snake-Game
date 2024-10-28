import pygame
from pygame.locals import *
import time
import random

# Constants
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
INITIAL_SPEED = 0.25  # Initial speed for level 1

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.move()  # Initialize at random position

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

class PowerUp:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/power_up.png").convert()
        self.x, self.y = -SIZE, -SIZE  # Start off-screen

    def activate(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

    def deactivate(self):
        self.x, self.y = -SIZE, -SIZE  # Hide off-screen

    def draw(self):
        if self.x >= 0 and self.y >= 0:
            self.parent_screen.blit(self.image, (self.x, self.y))
            pygame.display.flip()

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def move_left(self): self.direction = 'left'
    def move_right(self): self.direction = 'right'
    def move_up(self): self.direction = 'up'
    def move_down(self): self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i], self.y[i] = self.x[i-1], self.y[i-1]

        if self.direction == 'left': self.x[0] -= SIZE
        if self.direction == 'right': self.x[0] += SIZE
        if self.direction == 'up': self.y[0] -= SIZE
        if self.direction == 'down': self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Enhanced Snake Game")
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.power_up = PowerUp(self.surface)
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED
        self.power_up_active = False
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + SIZE and y1 >= y2 and y1 < y2 + SIZE

    def check_boundaries(self):
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or self.snake.y[0] < 0 or self.snake.y[0] >= 800:
            return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.score}  Level: {self.level}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def increase_level(self):
        if self.score > 0 and self.score % 5 == 0:
            self.level += 1
            self.speed = max(self.speed - 0.02, 0.1)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.power_up.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.score += 1
            self.snake.increase_length()
            self.apple.move()
            self.increase_level()
            if random.randint(1, 5) == 1:  # 20% chance of power-up
                self.power_up.activate()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.power_up.x, self.power_up.y):
            self.power_up_active = True
            self.power_up.deactivate()
            # Temporarily boost snake speed for the power-up
            original_speed = self.speed
            self.speed = 0.1
            pygame.time.set_timer(USEREVENT+1, 5000)  # Power-up effect for 5 seconds

        if self.check_boundaries():
            self.show_game_over()
            raise "Game Over"

    def show_game_over(self):
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is {self.score}.", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again, press Enter. To exit, press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running, paused = True, False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: running = False
                    elif event.key == K_RETURN: paused = False; pygame.mixer.music.unpause()
                    if not paused:
                        if event.key == K_LEFT: self.snake.move_left()
                        elif event.key == K_RIGHT: self.snake.move_right()
                        elif event.key == K_UP: self.snake.move_up()
                        elif event.key == K_DOWN: self.snake.move_down()
                elif event.type == QUIT: running = False
                elif event.type == USEREVENT+1:  # End power-up effect
                    self.speed = original_speed
                    self.power_up_active = False
            try:
                if not paused: self.play()
            except Exception as e:
                self.show_game_over()
                paused = True
                self.reset()
            time.sleep(self.speed)

if __name__ == '__main__':
    game = Game()
    game.run()
