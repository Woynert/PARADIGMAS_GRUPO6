import pygame, sys, math, random
pygame.init()

#Crear ventana
screenhabSize = (816, 528)
roomhabSize = (816, 528) #roomhabSize = (176, 176)

screen = pygame.display.set_mode(screenhabSize, pygame.RESIZABLE)
drawSurface = pygame.Surface(roomhabSize)
clock = pygame.time.Clock()

#Definir colores
BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
GRAY   = (  30,  30,  30)
GREEN  = (   0, 255,   0)
RED    = ( 255,   0,   0)
BLUE   = (   0,   0, 255)
YELLOW = ( 252, 186,   3)
sign = lambda x: int(math.copysign(1, x))

#Fonts
font1 = pygame.font.Font(None, 30)
myText = font1.render("TEXTO DE PRUEBA", 0, WHITE)

"""
Elements
0 -> Aire
1 -> Pared
2 -> Enemigo Perseguidor
"""

#LEVELS
lvlSel = 0
listLevel = []
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,2,0,0,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
listLevel.append(lvl)
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,1,1,1,0,1,1,1,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,1,1,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0]]
listLevel.append(lvl)
lvl  = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,1,1,0,1,1,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,0,2,0,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,1,1,0,1,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
listLevel.append(lvl)
    

#FUNCIONES
def draw_grid():
    #Vertical
    for i in range(0, 10):
        pygame.draw.line(drawSurface, GRAY, (i*16*3, 0), (i*16*3, 160*3))
    #Horizontal
    for i in range(0, 10):
        pygame.draw.line(drawSurface, GRAY, (0, i*16*3), (160*3, i*16*3))

def obj_collect(id): #object collecion
    lista = []

    #juntar todos los objetos en una lista
    for obj in lstWalls: 
        if type(obj) == id:
            lista.append(obj)
    for obj in fixLstMaster[Jsel][Isel][0]: 
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
            lstMaster[j].append([0, 0, 0])

    #Empezar generacion
    lstMaster[Jsel][Isel] = []  #COORDENADA PAR
    lstMaster[Jsel][Isel].append(extractLevel(random.randint(0, len(listLevel)-1)))
    lstMaster[Jsel][Isel].append(0) #id
    lstMaster[Jsel][Isel].append(1) #vistado
    #unlockNearbyDoors(Jsel, Isel, lstMaster)
    #extractLevel(lstMaster[Jsel][Isel], random.randint(0, len(listLevel)-1))
    MasterCreateBranchC(Jsel, Isel)
    

def fixMasterList():
    global fixLstMaster, Jsel, Isel
    fixLstMaster = []

    _retStr = findEmptyMasterList(True)
    _retEnd = findEmptyMasterList(False)
    #print(_retStr, _retEnd)
    #Cortar desde Comienzo hasta Final
    for j in range(_retStr[0], habSize*2-1 -_retEnd[0]):
        fixLstMaster.append([])

        for i in range(_retStr[1], habSize*2-1 -_retEnd[1]):
            #print(j, i)
            _A = lstMaster[j][i]
            fixLstMaster[j-_retStr[0]].append(_A)

    Jsel -= _retStr[0]
    Isel -= _retStr[1]

    #print("fixLstMaster")
    for n in fixLstMaster:
        #print(n)
        pass

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
                if (lstMaster[j][i][0] != 0):
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
                if (lstMaster[j][i][0] != 0):
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
                if (lstMaster[-j][-i][0] != 0):
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
                if (lstMaster[-j][-i][0] != 0):
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

def extractLevel(_id):
    _lsEx = []
    for i in range(0, habSize-1):
        for j in range(0, habSize-1):

            _objId = listLevel[_id][i][j]
            _obj = 0

            if (_objId == 1): #Wall
                _obj = Wall(x = j*16+16, y = i*16+16)
            elif (_objId == 2): #Enemy
                _obj = Enemy(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2)
            if (_obj != 0):
                _lsEx.append(_obj)
    return(_lsEx)

def createDoors():
    global lstDoors, Jsel, Isel
    lstDoors = []


    _yHabSize = len(fixLstMaster)
    _xHabSize = len(fixLstMaster[0])

    #Derecha
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel+1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel +1][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 160, y = (16)*4+8, height = (16)*4+8, dir = 0))
    else:
        lstDoors.append(Wall(x = 160, y = (16)*4+8, height = (16)*4+8))

    #Izquierda
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel-1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel -1][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 0, y = (16)*4+8, height = (16)*4+8, dir = 2))
    else:
        lstDoors.append(Wall(x = 0, y = (16)*4+8, height = (16)*4+8))

    #Arriba
    _needDoor = False;
    if (0 <= Jsel-1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel -1][Isel][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = (16)*4+8, y = 0, width = (16)*4+8, dir = 3))
    else:
        lstDoors.append(Wall(x = (16)*4+8, y = 0, width = (16)*4+8))

    #Abajo
    _needDoor = False;
    if (0 <= Jsel+1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel +1][Isel][0] == 1):
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
            #print("ShowMapTest")
            #print(i, fixLstMaster[Jsel][Isel])
            if (i == fixLstMaster[Jsel][Isel]): #Current
                _ls2.append([9, 1])
            elif (i[1] == 1): #Jefe
                _ls2.append([11, i[2]])
            elif ((i[0] != 0) and (i[0] != 1)): 
                _ls2.append([10, i[2]])
            else:
                _ls2.append([i[0], i[2]])

        _ls.append(_ls2)

    #print("showMap")
    for o in _ls:
        #print(o)
        pass

    return(_ls)

def unlockNearbyDoors(_y, _x, _lsMasterCase):
    
    _lsDir = [] 
    _d = 1
    _yHabSize = len(_lsMasterCase)
    _xHabSize = len(_lsMasterCase[0])
    if (0 <= _y < _yHabSize) and (0 <= _x+_d < _xHabSize):
        #if (_lsMasterCase[_y][_x+_d][0] == 1):
        _lsDir.append([0, _d])

    if (0 <= _y+_d < _yHabSize) and (0 <= _x < _xHabSize):
        #if (_lsMasterCase[_y+_d][_x][0] == 1):
        _lsDir.append([_d, 0])

    if (0 <= _y < _yHabSize) and (0 <= _x-_d < _xHabSize):
        #if (_lsMasterCase[_y][_x-_d][0] == 1):
        _lsDir.append([0, -_d])

    if (0 <= _y-_d < _yHabSize) and (0 <= _x < _xHabSize):
        #if (_lsMasterCase[_y-_d][_x][0] == 1):
        _lsDir.append([-_d, 0])

    print("Preuba _lsMasterCase")
    for b in _lsDir:
        _lsMasterCase[_y+b[0]][_x+b[1]][2] = 1




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
            #print(y,x, _lsDir)
            if not _lsDir: #No hay espacio
                pass#guides.remove(self) #AutoDelete
            else:
                #Create
                _dir = random.choice(_lsDir)
                #print("SELECTED ",_dir)

                #crear habitación
                lstMaster[self.y +_dir[0]][self.x +_dir[1]] = [] 
                lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(extractLevel(random.randint(0, len(listLevel)-1))) #objetos extraidos

                if (habMax == 1): #Habitación del jefe
                    print("OOOEEEAAA") 
                    lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(1) #id
                    
                else: #Habitación normal
                    print("OOOEEEAAA2222222222")
                    lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #id


                lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #visitado

                
                
                #extractLevel(lstMaster[self.y +_dir[0]][self.x +_dir[1]], random.randint(0, len(listLevel)-1))

                lstMaster[self.y +int(_dir[0]/2)][self.x +int(_dir[1]/2)][0] = 1 #crear puerta
                #lstMaster[self.y +int(_dir[0]/2)][self.x +int(_dir[1]/2)][2] = 0 #crear puerta
                MasterCreateBranchC(self.y +_dir[0], self.x +_dir[1]) #Crear Pointer
                #print("Creando en: ",self.y +_dir[0], self.x +_dir[1])



                #Update
                habMax -= 1 #Disminuir habitaciones por crear
                self.particiones -= 1 #Disminuir particiones por crear




    def habExists(self):
        _lsDir = [] 
        _d = 2
        _pHabSize = habSize*2 -1
        if (0 <= self.y < _pHabSize) and (0 <= self.x+_d < _pHabSize):
            if (lstMaster[self.y][self.x+_d][0] == 0):
                _lsDir.append([0, _d])

        if (0 <= self.y+_d < _pHabSize) and (0 <= self.x < _pHabSize):
            if (lstMaster[self.y+_d][self.x][0] == 0):
                _lsDir.append([_d, 0])

        if (0 <= self.y < _pHabSize) and (0 <= self.x-_d < _pHabSize):
            if (lstMaster[self.y][self.x-_d][0] == 0):
                _lsDir.append([0, -_d])

        if (0 <= self.y-_d < _pHabSize) and (0 <= self.x < _pHabSize):
            if (lstMaster[self.y-_d][self.x][0] == 0):
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
                player.y = 16*5 +16/2 -player.height/2
            elif (self.dir == 1): #abajo
                Jsel += 2
                player.x = 16*5 +16/2 -player.width/2
                player.y = 16
            elif (self.dir == 2): #izquierda
                Isel -= 2
                player.x = 160-16
                player.y = 16*5 +16/2 -player.height/2
            elif (self.dir == 3): #arriba
                Jsel -= 2
                player.x = 16*5 +16/2 -player.width/2
                player.y = 160-16
            fixLstMaster[Jsel][Isel][2] = 1
            unlockNearbyDoors(Jsel, Isel, fixLstMaster)
            
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

        self.spdH = 0
        self.spdV = 0
        self.acc = 0.3

        self.vida = 10
        self.vidaMax = 10

        self.scoty = False


    def applyMovement(self, spdH, spdV):
        if spdH != 0:
            if obj_collision(self, Wall, spdH, 0):
                for i in range(1, abs(int(spdH))):
                    if not obj_collision(self, Wall, sign (spdH), 0):
                        self.x += sign(spdH)
                    else:
                        spdH = 0
                        break
            else:
                self.x += spdH
            
        if spdV != 0:
            if obj_collision(self, Wall, 0, spdV):
                for i in range(1, abs(int(spdV))):
                    if not obj_collision(self, Wall, 0, sign(spdV)):
                        self.y += sign(spdV)
                    else:
                        spdV = 0
                        break
            else:
                self.y += spdV

    def movimiento(self):

        #Controles
        keys = pygame.key.get_pressed()
        keyH = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        keyV = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        #if (abs(self.spdH) < ) 
        #self.spdH += keyH * self.spdMax * self.acc
        #self.spdV += keyV * self.spdMax * self.acc

        #Aplicar 
        a = keyH
        b = keyV
        hip = math.sqrt(pow(a, 2) +pow(b, 2))
        sen = 0;
        cos = 0;
        if (hip != 0):
            sen += a/hip *sign(keyH)
            cos += b/hip *sign(keyV)

        if (keyH != 0 or keyV != 0):
            if (abs(self.spdH) < abs(sen * self.spdMax)):
                self.spdH += sen * self.spdMax * keyH * self.acc
            if (abs(self.spdV) < abs(cos * self.spdMax)):
                self.spdV += cos * self.spdMax * keyV * self.acc

        #Inercia
        if (abs(self.spdH) > 0):
            if (abs(self.spdH) < 0.05):
                self.spdH = 0
            self.spdH *= 0.7
        if (abs(self.spdV) > 0):
            if (abs(self.spdV) < 0.05):
                self.spdV = 0
            self.spdV *= 0.7

        self.applyMovement(self.spdH, self.spdV)
        



class Enemy(Object):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Enemigo"
        self.color = GREEN
        self.spdMax = 0.5

        self.spdH = 0
        self.spdV = 0
        self.damage = 1

    def applyMovement(self, spdH, spdV):
        if spdH != 0:
            if obj_collision(self, Wall, spdH, 0):
                """for i in range(1, abs(int(spdH))):
                    if not obj_collision(player, Wall, sign (spdH), 0):
                        self.x += sign(spdH)
                    else:
                        spdH = 0
                        break"""
                pass
            else:
                self.x += spdH
            
        if spdV != 0:
            if obj_collision(self, Wall, 0, spdV):
                """for i in range(1, abs(int(spdV))):
                    if not obj_collision(player, Wall, 0, sign(spdV)):
                        self.y += sign(spdV)
                    else:
                        spdV = 0
                        break"""
                pass
            else:
                self.y += spdV

    def movimiento(self):
        global Alarm1, player
        """if not obj_collision(self, Wall, self.spdMax):
            self.x += self.spdMax
        else:
            self.spdMax *= -1"""
        #math.sin()
        a = self.x -player.x
        b = self.y -player.y
        hip = math.sqrt(pow(a, 2) +pow(b, 2))

        cos = -a/hip
        sen = -b/hip

        if (hip != 0):
            self.spdH = cos * self.spdMax
            self.spdV = sen * self.spdMax

        

        #Personaje
        if (obj_collision(self, Player, self.spdMax)):
            if (player.scoty == False):
                pygame.time.set_timer(Alarm1, 1000)
                player.vida -= self.damage
                player.scoty = True
                #print(player.vida)
            player.spdH += cos * self.spdMax*10
            player.spdV += sen * self.spdMax*10
        else:
            self.applyMovement(self.spdH, self.spdV)


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

player = Player(x = 64, y = 64, width = 10, height = 10)
lstWalls.append(player)
#enemy = Enemy(32, 32)

#imprimir el nombre de todos los objetos
print("Object Names lstWalls")
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

#Alarms
Alarm1 = pygame.USEREVENT +1
pygame.time.set_timer(Alarm1, 0)
Alarm2 = Alarm1 +1
pygame.time.set_timer(Alarm2, 0)

print("lstMaster")
for n in lstMaster:
    #print(n)
    pass

#Crear Habitaciones
while (habMax > 0):
    for guide in guides:
        
        guide.count+=1
        #print(guide.y, guide.x, guide.particiones)

        if (guide.count > 1):
            guide.step()

    #print("Done")
    #print("Count: ", len(guides))

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
        if event.type == Alarm1:
            player.scoty = False
            pygame.time.set_timer(Alarm1, 0)
            #print("AAAAA")


    



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

        pygame.draw.rect(drawSurface, obj.color, [obj.x*3, obj.y*3, obj.width*3, obj.height*3])

    #Paredes Limites y player
    for obj in lstWalls:
        pygame.draw.rect(drawSurface, obj.color, [obj.x*3, obj.y*3, obj.width*3, obj.height*3])

    #Objetos del nivel
    #print(Jsel, Isel)
    for obj in fixLstMaster[Jsel][Isel][0]:

        if type(obj) == Enemy: #Movimiento Enemigo
            obj.movimiento()
        pygame.draw.rect(drawSurface, obj.color, [obj.x*3, obj.y*3, obj.width*3, obj.height*3])

    #UI
    _width = 12
    for i in range(0, 5):
        pygame.draw.rect(drawSurface, WHITE, [(160+16+8+17*i)*3, 20*3, _width*3, _width*3])
        for j in range(0, 2):
            if (player.vida >= (i*2)+j+1):
                    pygame.draw.rect(drawSurface, RED, [(160+16+8+17*i +_width/2*j +1 -j)*3, (20+1)*3, (_width/2 -1)*3 , (_width-2)*3])


    #Mapa
    _ls = showMap()
    _g  = int((816-528-20)/((len(_ls[0])+1)/2)) +1


    #for o in _ls:
        #print(o)

    if (_g*((len(_ls)+1)/2) > 528-60*3):
        _gh = (528-60*4) / ((len(_ls)+1)/2)
    else:
        _gh = _g

    _g2 = _g/2
    _gh2 = _gh/2
    for j in range(0, int((len(_ls)+1)/2)):
        for i in range(0, int((len(_ls[0])+1)/2)): #184 176
            _color = WHITE

            

            #Puertas
            #Horizontales

            if ((j*2 < len(_ls)) and i*2+1 < len(_ls[0])):
                _color = GREEN
                if (_ls[j*2][i*2+1][1] == 1):
                    #print("Prueba _ls", _ls[j*2][i*2+1][0])
                    if (_ls[j*2][i*2+1][0] == 1) :
                        _color = WHITE
                        pygame.draw.rect(drawSurface, _color, [(528 +_g*(i+1) +12 -_g2/2), 60*3 +_gh*j +_gh2/2, _g2, _gh2])

            #Verticales
            if ((j*2+1 < len(_ls)) and i*2 < len(_ls[0])):
                _color = GREEN
                if (_ls[j*2+1][i*2][1] == 1):
                    if (_ls[j*2+1][i*2][0] == 1) :
                        _color = WHITE
                        pygame.draw.rect(drawSurface, _color, [(528 +_g*i +_g/2 +12 -_g2/2), 60*3 +_gh*(j+1) -_gh2/2, _g2, _gh2])

                #Habitacion
            if (_ls[j*2][i*2][1] == 1): #Visto
                _color = BLUE
                if (_ls[j*2][i*2][0] == 9): #Current Room
                    _color = YELLOW
                elif (_ls[j*2][i*2][0] == 11): #Boss Room
                    _color = RED
                if (_ls[j*2][i*2][0] != 0):
                    pygame.draw.rect(drawSurface, _color, [(528 +_g*i +12), (60*3 +_gh*j), (_g-5), (_gh-5)])
            

        
    #actualizar
    pygame.transform.scale(drawSurface, screenhabSize, screen)
    
    #Texto
    screen.blit(font1.render("HEALTH", 0, WHITE), ((160+16+8)*3, 10*3))
    screen.blit(font1.render("MAP", 0, WHITE), ((160+16+8)*3, 50*3))



    pygame.display.flip()
    clock.tick(60)

