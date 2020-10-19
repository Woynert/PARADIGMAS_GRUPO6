import pygame, sys, math, random
pygame.init()

#Crear ventana
screenhabSize = (528, 528)
roomhabSize = (176, 176)

screen = pygame.display.set_mode(screenhabSize, pygame.RESIZABLE)
drawSurface = pygame.Surface(roomhabSize)
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
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
listLevel.append(lvl)
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,1,1,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0]]
listLevel.append(lvl)
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,1,0,1,1,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,1,1,0,1,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
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
    for obj in lstWalls: 
        if type(obj) == id:
            lista.append(obj)
    for obj in fixLstMaster[Jsel][Isel]: 
        if type(obj) == id:
            lista.append(obj)
    for obj in lstDoors: 
        if type(obj) == id:
            lista.append(obj)
    return(lista)

def obj_collision(obj1, obj2, mx = 0, my = 0): #collision
    for objCol in obj_collect(obj2):
        if (obj1.x+mx + obj1.width > objCol.x) and (objCol.x + objCol.width > obj1.x+mx) and (obj1.y+my + obj1.height > objCol.y) and (objCol.y + objCol.height > obj1.y+my):
            return(True)
    return(False)

def level_create(_id):
    for i in range(0, 9):
        for j in range(0, 9):

            objId = listLevel[_id][i][j]

            if (objId == 1): #Wall
                Wall(x = j*16+16, y = i*16+16)
            elif (objId == 2): #Enemy
                Enemy(x = j*16+16, y = i*16+16)

def level_delete():
    listaMaster.clear()

def MasterCreate():
    global habSize

    #Rellenar la cuadricula con 0s
    for j in range(0, habSize*2 -1):
        lstMaster.append([])

        for i in range(0, habSize*2 -1):
            lstMaster[j].append(0)

    #Empezar generacion
    lstMaster[Jsel][Isel] = []  #COORDENADA PAR
    extractLevel(lstMaster[Jsel][Isel], random.randint(0, len(listLevel)-1))
    MasterCreateBranchC(Jsel, Isel)
    

def fixMasterList():
    global fixLstMaster, Jsel, Isel
    fixLstMaster = []

    _retStr = findEmptyMasterList(True)
    _retEnd = findEmptyMasterList(False)
    print(_retStr, _retEnd)
    #Cortar desde Comienzo hasta Final
    for j in range(_retStr[0], habSize*2-1 -_retEnd[0]):
        fixLstMaster.append([])

        for i in range(_retStr[1], habSize*2-1 -_retEnd[1]):
            print(j, i)
            _A = lstMaster[j][i]
            fixLstMaster[j-_retStr[0]].append(_A)

    Jsel -= _retStr[0]
    Isel -= _retStr[1]

    for n in fixLstMaster:
        print(n)

def findEmptyMasterList(start):
    global lstMaster
    _ret = []

    #DESDE EL COMIENZO
    if (start):
        #Horizontales
        for j in range(0, habSize*2 -1):

            for i in range(0, habSize*2 -1):
                _empty = True
                #print(lstMaster[j][i])
                if (lstMaster[j][i] != 0):
                    _empty = False
                    break

            if (_empty == True):
                pass#print("Fila Numero.", j, "Vacia")
            else:
                #print("Fila Vacias hasta:", j-1)
                _ret.append(j)
                break

        #Verticales
        for i in range(0, habSize*2 -1):

            for j in range(0, habSize*2 -1):
                _empty = True
                #print(lstMaster[j][i])
                if (lstMaster[j][i] != 0):
                    _empty = False
                    break

            if (_empty == True):
                pass#print("Columna Numero.", i, "Vacia")
            else:
                #print("Columnas Vacias hasta:", i-1)
                _ret.append(i)
                break

    else: #DESDE EL FINAL
        #Horizontales
        for j in range(1, habSize*2 -1):

            for i in range(1, habSize*2 -1):
                _empty = True
                #print(lstMaster[j][i])
                if (lstMaster[-j][-i] != 0):
                    _empty = False
                    break

            if (_empty == True):
                pass#print("Fila Numero.", j, "Vacia")
            else:
                #print("Fila Vacias hasta:", j-1)
                _ret.append(j-1)
                break
        #Verticales
        for i in range(1, habSize*2 -1):

            for j in range(1, habSize*2 -1):
                _empty = True
                #print(lstMaster[j][i])
                if (lstMaster[-j][-i] != 0):
                    _empty = False
                    break

            if (_empty == True):
                pass#print("Columna Numero.", i, "Vacia")
            else:
                #print("Columnas Vacias hasta:", i-1)
                _ret.append(i-1)
                break


    #Return    
    return(_ret)

def extractLevel(lvlList, _id):
    for i in range(0, habSize-1):
        for j in range(0, habSize-1):

            _objId = listLevel[_id][i][j]
            _obj = 0

            if (_objId == 1): #Wall
                _obj = Wall(x = j*16+16, y = i*16+16)
            elif (_objId == 2): #Enemy
                _obj = Enemy(x = j*16+16, y = i*16+16)
            if (_obj != 0):
                lvlList.append(_obj)

def createDoors():
    global lstDoors, Jsel, Isel
    lstDoors = []


    _yHabSize = len(fixLstMaster)
    _xHabSize = len(fixLstMaster[0])

    #Derecha
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel+1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel +1] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 160, y = (16)*4+8, height = (16)*4+8, dir = 0))
    else:
        lstDoors.append(Wall(x = 160, y = (16)*4+8, height = (16)*4+8))

    #Izquierda
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel-1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel -1] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 0, y = (16)*4+8, height = (16)*4+8, dir = 2))
    else:
        lstDoors.append(Wall(x = 0, y = (16)*4+8, height = (16)*4+8))

    #Arriba
    _needDoor = False;
    if (0 <= Jsel-1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel -1][Isel] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = (16)*4+8, y = 0, width = (16)*4+8, dir = 3))
    else:
        lstDoors.append(Wall(x = (16)*4+8, y = 0, width = (16)*4+8))

    #Abajo
    _needDoor = False;
    if (0 <= Jsel+1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel +1][Isel] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = (16)*4+8, y = 160, width = (16)*4+8, dir = 1))
    else:
        lstDoors.append(Wall(x = (16)*4+8, y = 160, width = (16)*4+8))

def showMap():
    global fixLstMaster, Jsel, Isel

    _ls = []
    for j in fixLstMaster:
        _ls2 = []
        for i in j:
            if (i == fixLstMaster[Jsel][Isel]):
                _ls2.append(5)
            elif ((i != 0) and (i != 1)):
                _ls2.append(8)
            else:
                _ls2.append(i)

        _ls.append(_ls2)

    print("###")
    for o in _ls:
        print(o)




class MasterCreateBranchC():

    def __init__(self, y, x):
        guides.append(self)
        self.x = x
        self.y = y
        self.particiones = random.randint(1, 4)
        self.count = 0

    def step(self):
        global habMax

        if (self.particiones > 0 and habMax > 0):
            x = self.x
            y = self.y

            _lsDir = self.habExists()
            print(y,x, _lsDir)
            if not _lsDir: #No hay espacio
                pass#guides.remove(self) #AutoDelete
            else:
                #Create
                _dir = random.choice(_lsDir)
                print("SELECTED ",_dir)

                #crear habitación
                lstMaster[self.y +_dir[0]][self.x +_dir[1]] = [] 
                extractLevel(lstMaster[self.y +_dir[0]][self.x +_dir[1]], random.randint(0, len(listLevel)-1))

                lstMaster[self.y +int(_dir[0]/2)][self.x +int(_dir[1]/2)] = 1 #crear puerta
                MasterCreateBranchC(self.y +_dir[0], self.x +_dir[1]) #Crear Pointer
                print("Creando en: ",self.y +_dir[0], self.x +_dir[1])

                #Update
                habMax -= 1 #Disminuir habitaciones por crear
                self.particiones -= 1 #Disminuir particiones por crear




    def habExists(self):
        _lsDir = [] 
        _d = 2
        _pHabSize = habSize*2 -1
        if (0 <= self.y < _pHabSize) and (0 <= self.x+_d < _pHabSize):
            if (lstMaster[self.y][self.x+_d] == 0):
                _lsDir.append([0, _d])

        if (0 <= self.y+_d < _pHabSize) and (0 <= self.x < _pHabSize):
            if (lstMaster[self.y+_d][self.x] == 0):
                _lsDir.append([_d, 0])

        if (0 <= self.y < _pHabSize) and (0 <= self.x-_d < _pHabSize):
            if (lstMaster[self.y][self.x-_d] == 0):
                _lsDir.append([0, -_d])

        if (0 <= self.y-_d < _pHabSize) and (0 <= self.x < _pHabSize):
            if (lstMaster[self.y-_d][self.x] == 0):
                _lsDir.append([-_d, 0])

        return(_lsDir)

#CLASES 
class Object:
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        #listaMaster.append(self)

class Wall(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Pared"
        self.color = BLUE

class Door(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0, dir = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Puerta"
        self.color = GREEN
        self.dir = dir

    def colPlayer(self):
        global Jsel, Isel

        #Cambiar de escenario
        if (obj_collision(self, Player)):
            if (self.dir == 0): #derecha
                Isel += 2
                player.x = 16
                player.y = 16*5
            elif (self.dir == 1): #abajo
                Jsel += 2
                player.x = 16*5
                player.y = 16
            elif (self.dir == 2): #izquierda
                Isel -= 2
                player.x = 160-16
                player.y = 16*5
            elif (self.dir == 3): #arriba
                Jsel -= 2
                player.x = 16*5
                player.y = 160-16
            
            createDoors()
            showMap()

            


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
lstWalls = []


#crear objetos

#Pared Izquierda
lstWalls.append(Wall(x = 0, y = 0, height = (16)*4+8))
lstWalls.append(Wall(x = 0, y = (16)*6+8, height = 16*4 *8))

#Pared Arriba
lstWalls.append(Wall(x = 0, y = 0, width = (16)*4+8))
lstWalls.append(Wall(x = (16)*6+8, y = 0, width = (16)*4+8))

#Pared Derecha
lstWalls.append(Wall(x = 160, y = 0, height = (16)*4+8))
lstWalls.append(Wall(x = 160, y = (16)*6+8, height = 16*4 *8))

#Pared Abajo
lstWalls.append(Wall(x = 0, y = 160, width = (16)*4+8))
lstWalls.append(Wall(x = (16)*6+8, y = 160, width = (16)*4+8))

player = Player(64, 64)
lstWalls.append(player)
#enemy = Enemy(32, 32)

#imprimir el nombre de todos los objetos
for obj in lstWalls:
    print(obj.name)


#START
Jsel = 6
Isel = 6

#Debug
#level_create(1)

lstMaster = []
fixLstMaster = []

habMax = 10 -1
habSize = 10
guides = [] #
MasterCreate()



for n in lstMaster:
    print(n)

#Crear Habitaciones
while (habMax > 0):
    for guide in guides:
        
        guide.count+=1
        print(guide.y, guide.x, guide.particiones)

        if (guide.count > 1):
            guide.step()

    print("Done")
    print("Count: ", len(guides))

#elif (habMax == 0): #Recortar
fixMasterList()
    #habMax = -1

#PUERTAS
lstDoors = []
createDoors()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                pass
                

            elif event.key == pygame.K_UP:
                showMap()
                #print("")
                #for n in lstMaster:
                #    print(n)

            elif event.key == pygame.K_DOWN:
                pass

    



    #movimiento
    player.movimiento()
    #enemy.movimiento()


    #print(player.x)

    #if (obj_collision(player, Enemy)):
    #    level_delete()
    #    print("enemigo")

    #print(habMax)


    

    #fondo
    drawSurface.fill(BLACK)
    
    #cuadricula
    draw_grid()

    #dibujar objetos
    
    #Puertas
    for obj in lstDoors:
        if type(obj) == Door:
            obj.colPlayer()

        pygame.draw.rect(drawSurface, obj.color, [obj.x, obj.y, obj.width, obj.height])

    #Paredes Limites y player
    for obj in lstWalls:
        pygame.draw.rect(drawSurface, obj.color, [obj.x, obj.y, obj.width, obj.height])

    #Objetos del nivel
    #print(Jsel, Isel)
    for obj in fixLstMaster[Jsel][Isel]:
        pygame.draw.rect(drawSurface, obj.color, [obj.x, obj.y, obj.width, obj.height])
        

    #actualizar
    pygame.transform.scale(drawSurface, screenhabSize, screen)
    pygame.display.flip()
    clock.tick(60)

