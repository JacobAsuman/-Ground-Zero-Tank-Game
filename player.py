import pygame

pygame.init()
window_width = 1280
window_height = 720
screen = pygame.display.set_mode((window_width, window_height))
red = (255, 0, 0)


class player:
    x: float
    y: float
    currentY = 0
    currentX = 350
    health = 100
    fuel = 100



