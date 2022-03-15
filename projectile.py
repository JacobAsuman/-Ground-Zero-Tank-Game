import pygame

pygame.init()
window_width = 1280
window_height = 720
screen = pygame.display.set_mode((window_width, window_height))
red = (255, 0, 0)


class projectile:
    x: float
    y: float
    xSpeed: float
    ySpeed: float
    angle: float
    magnitude: float
