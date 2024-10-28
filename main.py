import pygame
from pygame.locals import *
if __name__ == '__main__':
    pygame.init()
    
    # Set up the display
    surface = pygame.display.set_mode((711, 400))
    surface.fill((0,0,0))
    
    block = pygame.image.load("block.png")
    pygame.display.flip()
    
    #eventloop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                pass
            elif event.type == QUIT:
                running = False