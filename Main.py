import pygame, sys, math
pygame.init()

#Crear ventana
screenSize = (528, 528)
roomSize = (176, 176)

screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
drawSurface = pygame.Surface(roomSize)
clock = pygame.time.Clock()

#Definir colores
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
GRAY  = (  30,  30,  30)
GREEN = (   0, 255,   0)
RED   = ( 255,   0,   0)
BLUE  = (   0,   0, 255)
sign = lambda x: int(math.copysign(1, x))


#LEVELS
lvlSel = 0
listLevel = []
lvl  = [[1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,1,1,1,0,0,0],
        [1,0,0,0,0,0,0,0,1]]
    
listLevel.append(lvl)
    

#FUNCIONES
def draw_grid():
    #Vertical
    for i in range(0, 10):
        pygame.draw.line(drawSurface, GRAY, (i*16, 0), (i*16, 160))
    #Horizontal
    for i in range(0, 10):
        pygame.draw.line(drawSurface, GRAY, (0, i*16), (160, i*16))

def obj_collect(id): #object collecion
    lista = []

    #juntar todos los objetos en una lista
    for obj in listaMaster: 
        if type(obj) == id:
            lista.append(obj)
    return(lista)

def obj_collision(obj1, obj2, mx = 0, my = 0): #collision
    for objCol in obj_collect(obj2):
        if (obj1.x+mx + obj1.width > objCol.x) and (objCol.x + objCol.width > obj1.x+mx) and (obj1.y+my + obj1.height > objCol.y) and (objCol.y + objCol.height > obj1.y+my):
            return(True)
    return(False)

def level_create():
    for i in range(0, 9):
        for j in range(0, 9):

            objId = listLevel[0][i][j]

            if (objId == 1): #Wall
                Wall(x = j*16+16, y = i*16+16)
            elif (objId == 2): #Enemy
                Enemy(x = j*16+16, y = i*16+16)






#CLASES 
class Object:
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        listaMaster.append(self)

class Wall(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Pared"
        self.color = BLUE

class Player(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Jugador"
        self.color = RED
        self.spdMax = 2

    def movimiento(self):

        #Controles
        keys = pygame.key.get_pressed()
        keyH = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        keyV = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        spdH = keyH * self.spdMax
        spdV = keyV * self.spdMax

        #Aplicar 
        if spdH != 0:
            if obj_collision(player, Wall, spdH, 0):
                for i in range(1, abs(spdH)):
                    if not obj_collision(player, Wall, sign (spdH), 0):
                        self.x += sign(spdH)
                    else:
                        spdH = 0
                        break
            else:
                self.x += spdH
            
        if spdV != 0:
            if obj_collision(player, Wall, 0, spdV):
                for i in range(1, abs(spdV)):
                    if not obj_collision(player, Wall, 0, sign(spdV)):
                        self.y += sign(spdV)
                    else:
                        spdV = 0
                        break
            else:
                self.y += spdV

class Enemy(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Enemigo"
        self.color = GREEN
        self.spdMax = 1

    def movimiento(self):
        if not obj_collision(self, Wall, self.spdMax):
            self.x += self.spdMax
        else:
            self.spdMax *= -1

#START
listaMaster = []

#crear objetos
Wall(x = 0, y = 0, height = 176)
Wall(x = 0, y = 0, width = 176)
Wall(x = 160, y = 0, height = 176)
Wall(x = 0, y = 160, width = 176)
player = Player(64, 64)
enemy = Enemy(32, 32)

#imprimir el nombre de todos los objetos
for obj in listaMaster:
    print(obj.name)


#Debug
level_create()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #movimiento
    player.movimiento()
    #enemy.movimiento()

    if (obj_collision(player, Enemy)):
        print("enemigo")

    #fondo
    drawSurface.fill(BLACK)
    
    #cuadricula
    draw_grid()

    #dibujar objetos
    for obj in listaMaster:
        pygame.draw.rect(drawSurface, obj.color, [obj.x, obj.y, obj.width, obj.height])
        

    #actualizar
    pygame.transform.scale(drawSurface, screenSize, screen)
    pygame.display.flip()
    clock.tick(60)

