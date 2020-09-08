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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    #fondo
    drawSurface.fill(BLACK)
    
    #dibujar objetos
    pygame.draw.rect(drawSurface, RED, [0, 0, 16, 16])
    
    #actualizar
    pygame.transform.scale(drawSurface, screenSize, screen)
    pygame.display.flip()
    clock.tick(60)