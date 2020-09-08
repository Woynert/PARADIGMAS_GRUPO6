import pygame, sys, math
pygame.init()

#Crear ventana
screenSize = (480, 480)
roomSize = (160, 160)

screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
drawSurface = pygame.Surface(roomSize)
clock = pygame.time.Clock()

#Definir colores
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
GREEN = (   0, 255,   0)
RED   = ( 255,   0,   0)
BLUE  = (   0,   0, 255)

