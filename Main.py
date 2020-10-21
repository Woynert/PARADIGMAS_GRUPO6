import pygame, sys, math, random, numpy
pygame.init()

GlobalScale = 4;

#Crear ventana
screenhabSize = (16*17*GlobalScale, 16*11*GlobalScale)
roomhabSize = (16*17*GlobalScale, 16*11*GlobalScale) #roomhabSize = (176, 176)

screen = pygame.display.set_mode(screenhabSize, pygame.RESIZABLE)
drawSurface = pygame.Surface(roomhabSize)
clock = pygame.time.Clock()

#Definir colores
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
WHITE2  = ( 80, 80, 80)
GRAY    = (  30,  30,  30)
GRAY2   = (  45,  45,  45)
GRAY3   = (  70,  70,  70)
GREEN   = (   0, 255,   0)
RED     = ( 255,   0,   0)
BLUE    = (   0,   0, 255)
YELLOW  = ( 252, 186,   3)
YELLOW2 = ( 255, 255,   0)
ORANGE  = ( 255, 128,   0)
PURPLE  = ( 178,   0, 255)
FLOOR   = (  28,  41,  43)
sign = lambda x: int(math.copysign(1, x))

#Fonts
font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 80)

#Images
imgWeapon = []
#imgWeapon.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon0.png"), 0, 3))
imgWeapon.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon0.png"), 0, GlobalScale*0.9))
imgWeapon.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon1.png"), 0, GlobalScale*0.9))
imgWeapon.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon2.png"), 0, GlobalScale*0.9))

imgWeaponItem = []
imgWeaponItem.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon0.png"), 0, 1.1))
imgWeaponItem.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon1.png"), 0, 1.1))
imgWeaponItem.append(pygame.transform.rotozoom(pygame.image.load("resources/images/weapon2.png"), 0, 1.1))

imgItem = []
imgItem.append(pygame.transform.rotozoom(pygame.image.load("resources/images/item0.png"), 0, 1.1))
imgItem.append(pygame.transform.rotozoom(pygame.image.load("resources/images/item1.png"), 0, 1.1))

imgMap = []
imgMap.append(pygame.transform.rotozoom(pygame.image.load("resources/images/iconMap0.png"), 0, 1.1))

imgWall = pygame.transform.rotozoom(pygame.image.load("resources/images/background.png"), 0, 1)

#puerta
imgDoor0 = []
imgDoor0.append(pygame.transform.rotozoom(pygame.image.load("resources/images/door0.png"), 0, GlobalScale))
imgDoor0.append(pygame.transform.rotozoom(pygame.image.load("resources/images/door0.png"), -90, GlobalScale))
imgDoor0.append(pygame.transform.rotozoom(pygame.image.load("resources/images/door0.png"), 180, GlobalScale))
imgDoor0.append(pygame.transform.rotozoom(pygame.image.load("resources/images/door0.png"), 90, GlobalScale))

#Sonido
sndShoot = pygame.mixer.Sound("resources/sound/shoot.wav")
sndPick = pygame.mixer.Sound("resources/sound/win.wav")
sndHurt = pygame.mixer.Sound("resources/sound/hurt.wav")
sndWin = pygame.mixer.Sound("resources/sound/win2.wav")
sndEnter = pygame.mixer.Sound("resources/sound/enter2.wav")
sndDead = pygame.mixer.Sound("resources/sound/dead.wav")
sndLose = pygame.mixer.Sound("resources/sound/lose.wav")



"""
Elements
0 -> Aire
1 -> Pared
2 -> Enemigo Perseguidor
"""

#WEAPONS
weaponAmmo = []   #ammoMax
weaponAmmo.append([  0, 0.6])   #0 pistola
weaponAmmo.append([120, 0.5]) #1 uzi
weaponAmmo.append([ 23, 1.5])  #2 shotgun


#LEVELS
lvlSel = 0
listLevel = []
emptyLevel = [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]

bossLevel = [[0,0,0,0,0,0,0,0,0],
            [0,0,3,0,0,0,3,0,0],
            [0,3,0,0,2,0,0,3,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0,0],
            [0,3,0,0,0,0,0,3,0],
            [0,0,3,0,0,0,3,0,0],
            [0,0,0,0,0,0,0,0,0]]

bossLevel = [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,3,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]


    

#FUNCIONES
def niveles():
    global habSize

    _ll = []

    _ll0 = []
    #0 Cuatro entradas
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,1,1,1,0,1,1,1,0],
            [0,1,0,0,0,0,0,1,0],
            [1,1,0,0,0,0,0,1,1],
            [0,0,0,0,2,0,0,0,0],
            [1,1,0,0,0,0,0,1,1],
            [0,1,0,0,0,0,0,1,0],
            [0,1,1,1,0,1,1,1,0],
            [0,0,0,1,0,1,0,0,0]]
    _ll0.append(lvl)
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,1,1,0,1,1,0,0],
            [1,1,1,0,0,0,1,1,1],
            [0,0,0,0,2,0,0,0,0],
            [1,1,1,0,0,0,1,1,1],
            [0,0,1,1,0,1,1,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0]]
    _ll0.append(lvl)
    _ll.append(_ll0)


    _ll1 = []
    #1 Tres entradas Arriba
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,1,0,0,0,1,0,0],
            [1,1,0,0,0,0,0,1,1],
            [0,0,0,0,2,0,0,0,0],
            [1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll1.append(lvl)
    lvl  = [[0,0,1,0,0,0,1,0,0],
            [0,0,1,0,0,0,1,0,0],
            [1,1,1,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll1.append(lvl)
    _ll.append(_ll1)

    #2 Tres entradas Derecha #Girar nivel
    _ll2 = []
    for nivel in _ll1:
        _ll2.append(nivelRotate90(nivel)) 
    _ll.append(_ll2)

    #3 Tres entradas Abajo #Girar nivel
    _ll3 = []
    for nivel in _ll2:
        _ll3.append(nivelRotate90(nivel)) 
    _ll.append(_ll3)

    #4 Tres entradas Izquierda #Girar nivel
    _ll4 = []
    for nivel in _ll3:
        _ll4.append(nivelRotate90(nivel)) 
    _ll.append(_ll4)

    _ll5 = []
    #5 Dos entradas Paralelo Arriba
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,2,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0]]
    _ll5.append(lvl)
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,0,1,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,0,0,1],
            [1,0,0,0,2,0,0,0,1],
            [1,0,0,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,1,0],
            [0,0,1,0,0,0,1,0,0],
            [0,0,0,1,0,1,0,0,0]]
    _ll5.append(lvl)
    _ll.append(_ll5)

    #6 Dos entradas Paralelo Derecha #Girar nivel
    _ll6 = []
    for nivel in _ll5:
        _ll6.append(nivelRotate90(nivel)) 
    _ll.append(_ll6)

    _ll7 = []
    #7 Una entrada Arriba
    lvl  = [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [1,0,0,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll7.append(lvl)
    lvl  = [[1,1,1,1,0,1,1,1,1],
            [1,1,1,1,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,0,1,1,0,1,1,0,0],
            [1,1,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,1,1]]
    _ll7.append(lvl)
    lvl  = [[0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll7.append(lvl)
    _ll.append(_ll7)

    #8 Una entrada Derecha #Girar nivel
    _ll8 = []
    for nivel in _ll7:
        _ll8.append(nivelRotate90(nivel)) 
    _ll.append(_ll8)

    #9 Una entrada Abajo #Girar nivel
    _ll9 = []
    for nivel in _ll8:
        _ll9.append(nivelRotate90(nivel)) 
    _ll.append(_ll9)

    #10 Una entrada Izquierda #Girar nivel
    _ll10 = []
    for nivel in _ll9:
        _ll10.append(nivelRotate90(nivel)) 
    _ll.append(_ll10)

    _ll11 = []
    #11 Ezquina Arriba
    lvl  = [[0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,0,0,1,0,1,1,1,1],
            [0,0,0,1,2,0,0,0,0],
            [0,0,0,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll11.append(lvl)
    lvl  = [[0,0,1,0,0,0,1,0,0],
            [0,0,1,0,0,0,1,0,0],
            [0,0,1,0,0,0,1,1,1],
            [0,0,1,0,0,0,0,0,0],
            [0,0,1,0,2,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]
    _ll11.append(lvl)
    _ll.append(_ll11)

    #12 Ezquina Derecha #Girar nivel
    _ll12 = []
    for nivel in _ll11:
        _ll12.append(nivelRotate90(nivel)) 
    _ll.append(_ll12)

    #12 Ezquina Abajo #Girar nivel
    _ll13 = []
    for nivel in _ll12:
        _ll13.append(nivelRotate90(nivel)) 
    _ll.append(_ll13)

    #12 Ezquina Izquierda #Girar nivel
    _ll14 = []
    for nivel in _ll13:
        _ll14.append(nivelRotate90(nivel)) 
    _ll.append(_ll14)

    return(_ll)

def setStructureLevel(_ls):

    derecha   = False
    izquierda = False
    arriba    = False
    abajo     = False

    print(_ls)

    _d = 1
    for _a in _ls:
        if (_a == [0, _d]):
            derecha = True
        if (_a == [_d, 0]):
            abajo = True
        if (_a == [0, -_d]):
            izquierda = True
        if (_a == [-_d, 0]):
            arriba = True

    """print("Der", derecha)
    print("Izq", izquierda)
    print("Arr", arriba)
    print("Aba", abajo)"""

    if (derecha and izquierda and arriba and abajo):
        return(0)

    #3
    elif (derecha and izquierda and arriba and not abajo):
        return(1)
    elif (derecha and not izquierda and arriba and abajo):
        return(2)
    elif (derecha and izquierda and not arriba and abajo):
        return(3)
    elif (not derecha and izquierda and arriba and abajo):
        return(4)

    #2 Paralelo
    elif (not derecha and not izquierda and arriba and abajo):
        return(5)
    elif (derecha and izquierda and not arriba and not abajo):
        return(6)

    #1
    elif (not derecha and not izquierda and arriba and not abajo):
        return(7)
    elif (derecha and not izquierda and not arriba and not abajo):
        return(8)
    elif (not derecha and not izquierda and not arriba and abajo):
        return(9)
    elif (not derecha and izquierda and not arriba and not abajo):
        return(10)


    #2 Esquinas
    elif (derecha and not izquierda and arriba and not abajo):
        return(11)
    elif (derecha and not izquierda and not arriba and abajo):
        return(12)
    elif (not derecha and izquierda and not arriba and abajo):
        return(13)
    elif (not derecha and izquierda and arriba and not abajo):
        return(14)

    print("NONE")
    
def checkLevelsAround(_y, _x, _lsMasterCase):
    _lsDir = [] 
    _d = 1
    _yHabSize = len(_lsMasterCase)
    _xHabSize = len(_lsMasterCase[0])
    if (0 <= _y < _yHabSize) and (0 <= _x+_d < _xHabSize):
        if (_lsMasterCase[_y][_x+_d][0] == 1):
            _lsDir.append([0, _d])

    if (0 <= _y+_d < _yHabSize) and (0 <= _x < _xHabSize):
        if (_lsMasterCase[_y+_d][_x][0] == 1):
            _lsDir.append([_d, 0])

    if (0 <= _y < _yHabSize) and (0 <= _x-_d < _xHabSize):
        if (_lsMasterCase[_y][_x-_d][0] == 1):
            _lsDir.append([0, -_d])

    if (0 <= _y-_d < _yHabSize) and (0 <= _x < _xHabSize):
        if (_lsMasterCase[_y-_d][_x][0] == 1):
            _lsDir.append([-_d, 0])

    return(_lsDir)

def nivelRotate90(_lSource):
    _ret = []
    for i in range(0, habSize-1):
        _ls = []
        for j in range(1, habSize):
            #print(j)
            _ls.append(_lSource[-j][i])
        _ret.append(_ls)
    return(_ret)

def draw_grid():
    _color = WHITE2
    #Vertical
    for i in range(0, 10):
        pygame.draw.line(drawSurface, _color, (i*16*GlobalScale, 0), (i*16*GlobalScale, 160*GlobalScale))
    #Horizontal
    for i in range(0, 10):
        pygame.draw.line(drawSurface, _color, (0, i*16*GlobalScale), (160*GlobalScale, i*16*GlobalScale))

def obj_collect(id): #object collecion
    lista = []

    #juntar todos los objetos en una lista

    for obj in lstWalls: 
        if type(obj) == id:
            lista.append(obj)
    for obj in fixLstMaster[Jsel][Isel][0]: 
        if type(obj) == id:
            lista.append(obj)
    if (fixLstMaster[Jsel][Isel][3] == 1):        
        for obj in lstDoors: 
            if type(obj) == id:
                lista.append(obj)
    else:
        for obj in lstClosedDoors: 
            if type(obj) == id:
                lista.append(obj)
    return(lista)

def obj_collision(obj1, obj2, mx = 0, my = 0): #collision
    for objCol in obj_collect(obj2):
        if (obj1.x+mx + obj1.width > objCol.x) and (objCol.x + objCol.width > obj1.x+mx) and (obj1.y+my + obj1.height > objCol.y) and (objCol.y + objCol.height > obj1.y+my):
            return([True, objCol])
    return([False, None])

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
            lstMaster[j].append([0, 0, 0, 1])

    #Empezar generacion
    lstMaster[Jsel][Isel] = []  #COORDENADA PAR

    _lev = random.choice(listLevel[0])
    lstMaster[Jsel][Isel].append(extractLevel(emptyLevel))
    lstMaster[Jsel][Isel].append(0) #id
    lstMaster[Jsel][Isel].append(1) #vistado
    lstMaster[Jsel][Isel].append(0) #terminado
    unlockNearbyDoors(Jsel, Isel, lstMaster)
    #extractLevel(lstMaster[Jsel][Isel], random.randint(0, len(listLevel)-1))
    MasterCreateBranchC(Jsel, Isel)
    if (not anyEnemyRoom(lstMaster[Jsel][Isel])):
        lstMaster[Jsel][Isel][3] = 1

def fixMasterList():
    global fixLstMaster, lstMaster, Jsel, Isel, Jboss, Iboss
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

    Jboss -= _retStr[0]
    Iboss -= _retStr[1]

    #print("fixLstMaster")
    setRoomClear()
    fixLstMaster[Jsel][Isel][2] = 1

    #Create boss room
    fixLstMaster[Jboss][Iboss][0] = extractLevel(bossLevel)
    for n in fixLstMaster:
        #print(n[])
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

def extractLevel(_lvl):
    global Jsel, Isel, Jboss, Iboss

    _lsEx = []
    for i in range(0, habSize-1):
        for j in range(0, habSize-1):

            _objId = _lvl[i][j]
            _obj = 0

            if (_objId == 1): #Wall
                _obj = Wall(x = j*16+16, y = i*16+16)
            elif (_objId == 2): #EnemyDumb
                if (random.choice([0, 1]) == 1):
                    _obj = Enemy0Dumb(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2)
                else:
                    _obj = Enemy1Hunter(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2)

                if (Jboss == Jsel) and (Iboss == Isel):
                    _obj.width = _obj.width*2
                    _obj.height = _obj.height*2

            elif (_objId == 3): #EnemyHunter
                _obj = Enemy1Hunter(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2)

                if (Jboss == Jsel) and (Iboss == Isel):
                    _obj.width = _obj.width*2
                    _obj.height = _obj.height*2

            elif (_objId == 100): #Item -> Botiquin
                _obj = Item(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2, id = 0)
            elif (_objId == 101): #Item -> Municion
                _obj = Item(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2, id = 1)
            elif (_objId == 102): #Item -> Arma
                _obj = Item(x = j*16+16 +16/2 -10/2, y = i*16+16 +16/2 -10/2, id = 2)
            if (_obj != 0):
                _lsEx.append(_obj)
    _lsEx.append(Wall(x = -16 -random.randint(16, 160000), y = 0))
    return(_lsEx)

def createDoors():
    global lstDoors, lstClosedDoors, Jsel, Isel
    lstDoors = []
    lstClosedDoors = []


    _yHabSize = len(fixLstMaster)
    _xHabSize = len(fixLstMaster[0])

    #Derecha
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel+1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel +1][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 160, y = (16)*4+16, height = 16, dir = 0))
    else:
        lstDoors.append(Wall(x = 160, y = (16)*4+8, height = 16*2))
    lstClosedDoors.append(Wall(x = 160, y = (16)*4+8, height = 16*2))

    #Izquierda
    _needDoor = False;
    if (0 <= Jsel < _yHabSize) and (0 <= Isel-1 < _xHabSize):
        if (fixLstMaster[Jsel][Isel -1][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = 0, y = (16)*4+16, height = 16, dir = 2))
    else:
        lstDoors.append(Wall(x = 0, y = (16)*4+8, height = 16*2))
    lstClosedDoors.append(Wall(x = 0, y = (16)*4+8, height = 16*2))

    #Arriba
    _needDoor = False;
    if (0 <= Jsel-1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel -1][Isel][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = (16)*4+16, y = 0, width = 16, dir = 3))
    else:
        lstDoors.append(Wall(x = (16)*4+8, y = 0, width = 16*2))
    lstClosedDoors.append(Wall(x = (16)*4+8, y = 0, width = 16*2))

    #Abajo
    _needDoor = False;
    if (0 <= Jsel+1 < _yHabSize) and (0 <= Isel < _xHabSize):
        if (fixLstMaster[Jsel +1][Isel][0] == 1):
            _needDoor = True 

    if (_needDoor):
        lstDoors.append(Door(x = (16)*4+16, y = 160, width = 16, dir = 1))
    else:
        lstDoors.append(Wall(x = (16)*4+8, y = 160, width = 16*2))
    lstClosedDoors.append(Wall(x = (16)*4+8, y = 160, width = 16*2))

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

    #print("Preuba _lsMasterCase")
    for b in _lsDir:
        _lsMasterCase[_y+b[0]][_x+b[1]][2] = 1
        pass

def anyEnemyRoom(_lsMasterCase):
    for _sub in Enemy.__subclasses__():
        for _obj in _lsMasterCase:
            if (type(_obj) == _sub):
                #print(_obj.name)
                
                return(True)
    
    return(False)


def setRoomClear():
    #print(anyEnemyRoom(fixLstMaster[Jsel][Isel][0]))
    if (not anyEnemyRoom(fixLstMaster[Jsel][Isel][0])):
        fixLstMaster[Jsel][Isel][3] = 1
        sndWin.play() 

        #Crear escalera (Se pasó el juego)
        if (Jsel == Jboss) and (Isel == Iboss):
            fixLstMaster[Jsel][Isel][0].append(Stair())

        elif (random.randint(0, 8) == 1): #Recompensa por nivel
            fixLstMaster[Jsel][Isel][0].append(Item(x = 83, y = 83, id = random.choice([0, 1, 2])))



class MasterCreateBranchC():

    def __init__(self, y, x, count = 0):
        guides.append(self)
        self.x = x
        self.y = y
        self.particiones = random.randint(1, 4)
        self.count = count

        global Jboss, Iboss, countBoss
        if (self.count > countBoss):
            Jboss = self.y
            Iboss = self.x
            countBoss = self.count

    def step(self):
        global habMax

        if (self.particiones > 0 and habMax > 0):
            x = self.x
            y = self.y

            _lsDir = self.habExists(y, x)

            #print(y,x, _lsDir)
            if not _lsDir: #No hay espacio
                pass#guides.remove(self) #AutoDelete
            else:
                #Create
                _dir = random.choice(_lsDir)
                #print("SELECTED ",_dir)

                #crear habitación
                lstMaster[self.y +_dir[0]][self.x +_dir[1]] = [] 

                #Seleccionar un nivel
                """
                _indice = setStructureLevel(self.habExists(self.y +_dir[0], self.x +_dir[1]))
                if (_indice != None):
                    _lev = random.choice(listLevel[_indice])
                    lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(extractLevel(_lev)) #objetos extraidos"""

                lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(extractLevel(emptyLevel))
                if (habMax == 1): #Habitación del jefe
                    lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(1) #id
                    
                else: #Habitación normal
                    lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #id


                lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #visitado
                lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #completado
                #lstMaster[self.y +_dir[0]][self.x +_dir[1]].append(0) #completado

                
                
                #extractLevel(lstMaster[self.y +_dir[0]][self.x +_dir[1]], random.randint(0, len(listLevel)-1))

                lstMaster[self.y +int(_dir[0]/2)][self.x +int(_dir[1]/2)][0] = 1 #crear puerta
                #lstMaster[self.y +int(_dir[0]/2)][self.x +int(_dir[1]/2)][2] = 0 #crear puerta
                MasterCreateBranchC(self.y +_dir[0], self.x +_dir[1], self.count+1) #Crear Pointer
                #print("Creando en: ",self.y +_dir[0], self.x +_dir[1])


                #Update
                habMax -= 1 #Disminuir habitaciones por crear
                self.particiones -= 1 #Disminuir particiones por crear




    def habExists(self, _x, _y):
        _lsDir = [] 
        _d = 2
        _pHabSize = len(lstMaster)-1#habSize*2 -1
        if (0 <= _y < _pHabSize) and (0 <= _x+_d < _pHabSize): #Derecha
            if (lstMaster[_y][_x+_d][0] == 0):
                _lsDir.append([0, _d])

        if (0 <= _y+_d < _pHabSize) and (0 <= _x < _pHabSize): #Abajo
            if (lstMaster[_y+_d][_x][0] == 0):
                _lsDir.append([_d, 0])

        if (0 <= _y < _pHabSize) and (0 <= _x-_d < _pHabSize): #Izquierda
            if (lstMaster[_y][_x-_d][0] == 0):
                _lsDir.append([0, -_d])

        if (0 <= _y-_d < _pHabSize) and (0 <= _x < _pHabSize): #Arriba
            if (lstMaster[_y-_d][_x][0] == 0):
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
        if (obj_collision(self, Player)[0]):
            sndEnter.play()
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

            fixLstMaster[Jsel][Isel][2] = 1 #No terminado
            if (not anyEnemyRoom(fixLstMaster[Jsel][Isel][0])):
                fixLstMaster[Jsel][Isel][3] = 1 #Level

            unlockNearbyDoors(Jsel, Isel, fixLstMaster)
            
            createDoors()
            showMap()
  
class Stair(Object):
    def __init__(self, x = 0, y = 0, width = 18, height = 16, depth = 0, dir = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.x = 176/2 -self.width/2
        self.y = 176/2 -self.height/2
        self.name = "Puerta"
        self.color = YELLOW
        self.dir = dir
        self.toque = False

    def colPlayer(self):
        global Jsel, Isel, lstMaster
        print("HEY")
        if (obj_collision(self, Player)[0]):
            print("COLISION")
            if (self.toque == True):
                #GANAR
                player.piso += 1
                lstMaster = []
                GAMESTART()

        else:
            self.toque = True


 

class Bullet(Object):
    def __init__(self, x = 0, y = 0, width = 4, height = 4, depth = 0, id = 0, angle = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Bala"
        self.color1 = YELLOW2
        self.color2 = YELLOW
        self.color = self.color1

        self.x = self.x - width/2
        self.y = self.y - height/2

        self.sx = self.x
        self.sy = self.y

        self.spdH = 0 
        self.spdV = 0
        self.spdMax = 10
        self.damage = 0

        if (id == 0):   #Pistol
            self.damage = weaponAmmo[id][1] #0.6 
            self.spdMax = 4
        elif (id == 1): #Uzi
            self.damage = weaponAmmo[id][1] #0.5
            self.spdMax = 4
        elif (id == 2): #Shotgun
            self.damage = weaponAmmo[id][1] #1.5
            self.spdMax = 3

        #if (hip != 0):
        #print(angle )
        #print("cos",numpy.cos(angle ))
        self.spdH = numpy.cos(angle) * self.spdMax
        self.spdV = numpy.sin(angle) * self.spdMax
        #else:
            #fixLstMaster[Jsel][Isel][0].remove(self)
        sndShoot.play() #Shoot


    def movimiento(self):
        _alreadyCol = False

        #Enemigo
        for _sub in Enemy.__subclasses__():
            _enemyCol = obj_collision(self, _sub, 0, 0)
            if (_enemyCol[0]):
                _enemyCol[1].color = WHITE
                _enemyCol[1].vida -= self.damage
                if (_enemyCol[1].vida <= 0):
                    _enemyCol[1].morir()
                if (self in fixLstMaster[Jsel][Isel][0]):
                    fixLstMaster[Jsel][Isel][0].remove(self)
                _alreadyCol = True

        #Pared
        if (_alreadyCol == False):
            if obj_collision(self, Wall, 0, 0)[0]:
                if (self in fixLstMaster[Jsel][Isel][0]):
                    fixLstMaster[Jsel][Isel][0].remove(self)
            else:

                if obj_collision(self, Wall, 0, 0)[0]:
                    
                    if (self in fixLstMaster[Jsel][Isel][0]):
                        fixLstMaster[Jsel][Isel][0].remove(self)
                else:
                    self.y += self.spdV
                    self.x += self.spdH

class Player(Object):
    def __init__(self, x = 0, y = 0, width = 16, height = 16, depth = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Jugador"
        self.color1 = RED
        self.color = self.color1 
        self.spdMax = 2

        self.spdH = 0
        self.spdV = 0
        self.acc = 0.3

        self.vida = 10
        self.vidaMax = 10

        self.weapon = 2 #pistola
        self.ammo = 22 #pistola
        self.scoty = False
        self.ableToShoot = True

        self.piso = 1
        self.vivo = True


    def applyMovement(self, spdH, spdV):
        if (self.vivo):
            if spdH != 0:
                if obj_collision(self, Wall, spdH, 0)[0]:
                    for i in range(1, abs(int(spdH))):
                        if not obj_collision(self, Wall, sign (spdH), 0)[0]:
                            self.x += sign(spdH)
                        else:
                            spdH = 0
                            break
                else:
                    self.x += spdH
                
            if spdV != 0:
                if obj_collision(self, Wall, 0, spdV)[0]:
                    for i in range(1, abs(int(spdV))):
                        if not obj_collision(self, Wall, 0, sign(spdV))[0]:
                            self.y += sign(spdV)
                        else:
                            spdV = 0
                            break
                else:
                    self.y += spdV

    def shoot(self):
        if (self.vivo):
            if (self.ableToShoot) and ((self.weapon == 0) or (self.ammo > 0)):
                self.ableToShoot = False
                self.ammo -= 1
                mx, my = pygame.mouse.get_pos()
                _bul = None
                if (self.weapon == 0): #Pistola

                    _x = self.x +self.width/2 
                    _y = self.y +self.height/2 
                    _rd = 0

                    if ((_x-(mx/GlobalScale)) != 0):
                        _rd = numpy.arctan((_y-(my/GlobalScale))/(_x-(mx/GlobalScale)))

                        if (_x > (mx/GlobalScale)):
                            _rd += numpy.pi

                    pygame.time.set_timer(Alarm4, 500)
                    fixLstMaster[Jsel][Isel][0].append(Bullet(x = _x, y = _y, id = 0, angle = _rd))
                    
                elif (self.weapon == 1): #Uzi
                    _x = self.x +self.width/2 
                    _y = self.y +self.height/2 
                    _rd = 0

                    if ((_x-(mx/GlobalScale)) != 0):
                        _rd = numpy.arctan((_y-(my/GlobalScale))/(_x-(mx/GlobalScale)))

                        if (_x > (mx/GlobalScale)):
                            _rd += numpy.pi

                    pygame.time.set_timer(Alarm4, 150)
                    fixLstMaster[Jsel][Isel][0].append(Bullet(x = _x, y = _y, id = 1, angle = _rd))

                elif (self.weapon == 2): #Escopeta
                    _x = self.x +self.width/2 
                    _y = self.y +self.height/2 
                    _rd = 0
                    
                    if ((_x-(mx/GlobalScale)) != 0):
                        _rd = numpy.arctan((_y-(my/GlobalScale))/(_x-(mx/GlobalScale)))

                        if (_x > (mx/GlobalScale)):
                            _rd += numpy.pi

                    pygame.time.set_timer(Alarm4, 1000)

                    fixLstMaster[Jsel][Isel][0].append(Bullet(x = _x, y = _y, id = 2, angle = _rd -numpy.pi/12 +random.randint(-8, 8)*numpy.pi/180))
                    fixLstMaster[Jsel][Isel][0].append(Bullet(x = _x, y = _y, id = 2, angle = _rd +random.randint(-8, 8)*numpy.pi/180))
                    fixLstMaster[Jsel][Isel][0].append(Bullet(x = _x, y = _y, id = 2, angle = _rd +numpy.pi/12 +random.randint(-8, 8)*numpy.pi/180))

                #No ammo restore to pistol
                if (self.ammo < 1):
                    self.weapon = 0
            
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

        #Animación scooty
        if (self.scoty == False):
            self.color = self.color1
    
    def checkVida(self):
        if (self.vida <= 0) and (self.vida > -10000):
            pygame.time.set_timer(Alarm7, 4000)
            self.vida = -10000
            self.vivo = False
            sndLose.play()
            self.color = WHITE

class Enemy(Object):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, depth = 0):


        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Enemigo"
        self.color = GREEN
        self.spdMax = 0.4
        self.vida = 1

        self.spdH = 0
        self.spdV = 0
        self.damage = 1

    def applyMovement(self, spdH, spdV, Hunter):
        #print(spdH, spdV)
        if spdH != 0:
            _obCol = obj_collision(self, Wall, spdH, 0)
            if _obCol[0]:
                if (Hunter):
                    a = self.x -_obCol[1].x
                    b = self.y -_obCol[1].y
                    hip = math.sqrt(pow(a, 2) +pow(b, 2))

                    if (hip != 0):
                        cos = -a/hip *-1
                        sen = -b/hip *-1
                        #print("A", self.spdH, self.spdV)

                        if (abs(self.spdH) < abs(cos * self.spdMax *4)):
                            self.spdH += cos * self.spdMax *random.randint(1,4) 
                        if (abs(self.spdV) < abs(sen * self.spdMax *4)):
                            self.spdV += sen * self.spdMax *random.randint(1,4) 
                        #print("B", self.spdH, self.spdV)
                        #self.applyMovement(self.spdH, self.spdV)
                pass
            else:
                self.x += spdH
            
        if spdV != 0:
            _obCol = obj_collision(self, Wall, 0, spdV)
            if _obCol[0]:
                if (Hunter):
                    a = self.x -_obCol[1].x
                    b = self.y -_obCol[1].y
                    hip = math.sqrt(pow(a, 2) +pow(b, 2))

                    if (hip != 0):
                        cos = -a/hip *-1
                        sen = -b/hip *-1
                        #print("A", self.spdH, self.spdV)
                        if (abs(self.spdH) < abs(cos * self.spdMax *4)):
                            self.spdH += cos * self.spdMax *random.randint(1,4) 
                        if (abs(self.spdV) < abs(sen * self.spdMax *4)):
                            self.spdV += sen * self.spdMax *random.randint(1,4) 
                        #print("B", self.spdH, self.spdV)
                        #self.applyMovement(self.spdH, self.spdV)
                pass
            else:
                self.y += spdV

    def Repeler(self):

        for _sub in Enemy.__subclasses__():
            _obCol = obj_collision(self, _sub, 0, 0)
            #print(_obCol)
            if _obCol[0]:
                #print("Preuba Enemy Repeler")

                a = self.x -_obCol[1].x
                b = self.y -_obCol[1].y
                hip = math.sqrt(pow(a, 2) +pow(b, 2))

                if (hip != 0):
                    cos = -a/hip *-1
                    sen = -b/hip *-1

                    #self.spdH = cos * self.spdMax
                    #self.spdV = sen * self.spdMax
                    self.applyMovement(cos * self.spdMax, sen * self.spdMax, False)
                    return(True)
        return(False)

    def morir(self):
        sndDead.play()
        fixLstMaster[Jsel][Isel][0].remove(self)
        setRoomClear()
        self.x = -16
        self.y = -16

class Enemy0Dumb(Enemy):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, depth = 0):


        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Enemigo"

        self.color1 = GREEN
        self.color = self.color1
        self.spdMax = 0.4

        self.vida = 5

        self.spdH = 0
        self.spdV = 0
        self.damage = 1

        self.distance = 0



    def movimiento(self):
        if (self.distance > 0):
            self.applyMovement(self.spdH, self.spdV, False)
            self.distance -= abs(self.spdH) + abs(self.spdV)

        self.Repeler()

        global Alarm1, player

        a = self.x -player.x
        b = self.y -player.y
        hip = math.sqrt(pow(a, 2) +pow(b, 2))
        cos = 0
        sen = 0

        if (hip != 0):
            cos = -a/hip
            sen = -b/hip
        if (obj_collision(self, Player, self.spdMax)[0]):
            if (player.scoty == False):
                pygame.time.set_timer(Alarm1, 1000)
                player.vida -= self.damage
                sndHurt.play()
                player.scoty = True
                    #print(player.vida)
                player.spdH += cos * self.spdMax*10
                player.spdV += sen * self.spdMax*10
                player.checkVida()


    def randomMovement(self):

        self.distance = random.randint(10, 70)

        a = random.choice([-1, 0, 1])
        b = random.choice([-1, 0, 1])
        hip = math.sqrt(pow(a, 2) +pow(b, 2))
        
        if (hip != 0):
            cos = -a/hip
            sen = -b/hip

            self.spdH = cos * self.spdMax
            self.spdV = sen * self.spdMax

class Enemy1Hunter(Enemy):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, depth = 0):


        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Enemigo"
        self.color1 = GREEN
        self.color = self.color1
        self.spdMax = 0.4

        self.vida = 5

        self.spdH = 0
        self.spdV = 0
        self.acc = 0.1
        self.damage = 1

    def movimiento(self):
        global Alarm1, player

        a = self.x -player.x
        b = self.y -player.y
        hip = math.sqrt(pow(a, 2) +pow(b, 2))
        cos = 0
        sen = 0

        if (hip != 0):
            cos = -a/hip
            sen = -b/hip

        if (not self.Repeler()):
            if (hip != 0):
                if (abs(self.spdH)  < abs(cos * self.spdMax)):
                    self.spdH += cos * self.spdMax * self.acc
                else:
                    self.spdH -= self.spdH*self.acc

                if (abs(self.spdV)  < abs(sen * self.spdMax)):
                    self.spdV += sen * self.spdMax * self.acc
                else:
                    self.spdV -= self.spdV*self.acc


        #Personaje Empujar
        #if (player.scoty == False):
        if (obj_collision(self, Player, self.spdMax)[0]):
            if (player.scoty == False):
                pygame.time.set_timer(Alarm1, 1000)
                player.vida -= self.damage
                sndHurt.play()
                player.scoty = True
                    #print(player.vida)
                player.spdH += cos * self.spdMax*10
                player.spdV += sen * self.spdMax*10
                player.checkVida()
        else:
            self.applyMovement(self.spdH, self.spdV, True)

#Items
class Item(Object):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, depth = 0, id = 0, subId = 0, subAmmo = 0):

        #constructor Object
        Object.__init__(self, x, y, width, height, depth)

        #atributos especiales
        self.name = "Item"
        self.color = ORANGE

        self.id = id
        self.subId = subId #(para las armas)
        self.subAmmo = subAmmo #(para las armas)
        self.Toque = False

        if (self.id == 0): #Botiquin
            self.color = WHITE
        elif (self.id == 1): #Munición
            self.color = ORANGE
        elif (self.id == 2): #weapon
            self.color = PURPLE
            if (self.subId == 0): #pistol 
                self.subId = random.randint(1, len(weaponAmmo)-1)
                self.subAmmo = weaponAmmo[self.subId][0]

    def colision(self):
        if (obj_collision(self, Player)[0]):
            #Hacer algo
            print("COLISION CON ITEM")
            if (self.id == 0): #Botiquin
                player.vida += 5
                if (player.vida > player.vidaMax):
                    player.vida = player.vidaMax
                sndPick.play()
                fixLstMaster[Jsel][Isel][0].remove(self)
            elif (self.id == 1): #Munición
                player.ammo = weaponAmmo[player.weapon][0]
                fixLstMaster[Jsel][Isel][0].remove(self)
                sndPick.play()
            elif (self.id == 2): #Munición
                if (self.Toque == True):
                    _backId   = self.subId
                    _backAmmo = self.subAmmo

                    if (player.weapon != 0): #intercambiar el arma
                        self.subId   = player.weapon
                        self.subAmmo = player.ammo
                    if (player.weapon == self.subId) or (player.ammo <= 0):
                        fixLstMaster[Jsel][Isel][0].remove(self)


                    #reemplazar arma
                    player.weapon = _backId
                    player.ammo   = _backAmmo
                    sndPick.play()

            self.Toque = False
        else:
            self.Toque = True 

def GAMESTART():
    global Jsel, Isel, Jboss, Iboss, countBoss, lstMaster, fixLstMaster, habMax, habSize, listLevel, guides, lstDoors, lstClosedDoors, player

    #START
    player.vivo = True

    Jsel = 6
    Isel = 6

    Jboss = -1 #boss
    Iboss = -1
    countBoss = -1

    #Debug
    lstMaster = []
    fixLstMaster = []

    habMax = 8 -1
    habSize = 10

    #Niveles
    listLevel = niveles()
    guides = [] #
    MasterCreate()


    #Crear Habitaciones (DATOS)
    while (habMax > 0):
        for guide in guides:
            
            guide.count += 1

            if (guide.count > 1):
                guide.step()


    for guide in guides:
        _indice = setStructureLevel(checkLevelsAround(guide.y, guide.x, lstMaster))
        if (_indice != None):
            _lev = random.choice(listLevel[_indice])
            lstMaster[guide.y][guide.x][0] = extractLevel(_lev) #objetos extraidos

    #Room start
    lstMaster[Jsel][Isel][0] = extractLevel(emptyLevel)

    #CREAR FIX MASTER LIST
    fixMasterList()

    #PUERTAS
    lstDoors = []
    lstClosedDoors = []
    createDoors()

#START
lstWalls = []

#crear objetos permanentes
#Pared Izquierda
lstWalls.append(Wall(x = 0, y = 0, height = (16)*4+16))
lstWalls.append(Wall(x = 0 -2, y = (16)*4+8, height = 16*2))
lstWalls.append(Wall(x = 0, y = (16)*6, height = 16*4 *8 +8))

#Pared Arriba
lstWalls.append(Wall(x = 0, y = 0, width = (16)*4+16))
lstWalls.append(Wall(x = (16)*4+8, y = 0 -2, width = 16*2))
lstWalls.append(Wall(x = (16)*6, y = 0, width = (16)*4+16))

#Pared Derecha
lstWalls.append(Wall(x = 160, y = 0, height = (16)*4+16))
lstWalls.append(Wall(x = 160 +2, y = (16)*4+8, height = 16*2, width = 16 -2))
lstWalls.append(Wall(x = 160, y = (16)*6, height = 16*4 *8+8))

#Pared Abajo
lstWalls.append(Wall(x = 0, y = 160, width = (16)*4+16))
lstWalls.append(Wall(x = (16)*4+8, y = 160 +2, width = 16*2))
lstWalls.append(Wall(x = (16)*6, y = 160, width = (16)*4+16))

player = Player(x = 80, y = 80, width = 10, height = 10)
lstWalls.append(player)

#START
Jsel = 6
Isel = 6

Jboss = -1 #boss
Iboss = -1
countBoss = -1

#Debug
lstMaster = []
fixLstMaster = []

habMax = 8 -1
habSize = 10

#Niveles
listLevel = niveles()
guides = [] #
MasterCreate()


#Crear Habitaciones (DATOS)
while (habMax > 0):
    for guide in guides:
        
        guide.count += 1

        if (guide.count > 1):
            guide.step()


for guide in guides:
    _indice = setStructureLevel(checkLevelsAround(guide.y, guide.x, lstMaster))
    if (_indice != None):
        _lev = random.choice(listLevel[_indice])
        lstMaster[guide.y][guide.x][0] = extractLevel(_lev) #objetos extraidos

#Room start
lstMaster[Jsel][Isel][0] = extractLevel(emptyLevel)

#CREAR FIX MASTER LIST
fixMasterList()

#PUERTAS
lstDoors = []
lstClosedDoors = []
createDoors()

#Alarms
Alarm1 = pygame.USEREVENT +1
pygame.time.set_timer(Alarm1, 0)
Alarm2 = Alarm1 +1
pygame.time.set_timer(Alarm2, 1000)
Alarm3 = Alarm2 +1
pygame.time.set_timer(Alarm3, 1000)
Alarm4 = Alarm3 +1
pygame.time.set_timer(Alarm4, 1000)
Alarm5 = Alarm4 +1
pygame.time.set_timer(Alarm5, 50)
Alarm6 = Alarm5 +1
pygame.time.set_timer(Alarm6, 100)
Alarm7 = Alarm6 +1

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
        if event.type == Alarm1: #Escudo Escoty
            player.scoty = False
            pygame.time.set_timer(Alarm1, 0)
            #print("AAAAA")

        if event.type == Alarm2: #Random Movement
            for obj in fixLstMaster[Jsel][Isel][0]:
                if (type(obj) == Enemy0Dumb):
                    obj.randomMovement()

        if event.type == Alarm4: #AutoShoot
            player.ableToShoot = True
            pass

        if event.type == Alarm7: #PERDER
            player.piso = 1
            lstMaster = []
            GAMESTART()

        if event.type == Alarm6: #Parpadear
            if (player.vivo):
                if (player.color == WHITE):
                    player.color = player.color1
                else:
                    player.color = WHITE

                for obj in fixLstMaster[Jsel][Isel][0]:
                    if (type(obj) == Enemy0Dumb or type(obj) == Enemy1Hunter):
                        if (obj.color != obj.color1):
                            obj.color = obj.color1


        if event.type == Alarm5: #Bullet Parpadear
            for obj in fixLstMaster[Jsel][Isel][0]:
                if (type(obj) == Bullet):
                    if (obj.color == obj.color1):
                        obj.color = obj.color2
                    else:
                        obj.color = obj.color1


        if event.type == pygame.MOUSEBUTTONDOWN: #mouse
            pass #player.shoot()


    #movimiento
    player.movimiento()
    if pygame.mouse.get_pressed()[0]:
        player.shoot()
    #enemy.movimiento()


    #print(player.x)

    #if (obj_collision(player, Enemy)):
    #    level_delete()
    #    print("enemigo")

    #print(habMax)


    

    #fondo
    drawSurface.fill(BLACK)
        
    #fondo
    #pygame.draw.rect(drawSurface, FLOOR, [0, 0, 176*GlobalScale, 176*GlobalScale])

    #cuadricula
    #draw_grid()

    #dibujar objetos
    
    #Paredes Limites y player
    for obj in lstWalls:
        pygame.draw.rect(drawSurface, obj.color, [obj.x*GlobalScale, obj.y*GlobalScale, obj.width*GlobalScale, obj.height*GlobalScale])


    #Puertas (DISPONIBLES)
    for obj in lstClosedDoors:
        pygame.draw.rect(drawSurface, obj.color, [obj.x*GlobalScale, obj.y*GlobalScale, obj.width*GlobalScale, obj.height*GlobalScale])

    for obj in lstDoors:
        if type(obj) == Door:
            obj.colPlayer()
            if (fixLstMaster[Jsel][Isel][3] == 1):
                _color = obj.color
            else:
                _color = RED
            pygame.draw.rect(drawSurface, _color, [obj.x*GlobalScale, obj.y*GlobalScale, obj.width*GlobalScale, obj.height*GlobalScale])

    #Objetos del nivel
    #print(Jsel, Isel)
    for obj in fixLstMaster[Jsel][Isel][0]:

        if (type(obj) == Enemy0Dumb or type(obj) == Enemy1Hunter): #Movimiento Enemigo
            obj.movimiento()
        elif type(obj) == Bullet:#Bala
            obj.movimiento()
        elif type(obj) == Item: #Item
            obj.colision()
        elif type(obj) == Stair: #Item
            obj.colPlayer()
        pygame.draw.rect(drawSurface, obj.color, [obj.x*GlobalScale, obj.y*GlobalScale, obj.width*GlobalScale, obj.height*GlobalScale])


    #UI

    #HEALTH
    _width = 12
    for i in range(0, 5):
        pygame.draw.rect(drawSurface, WHITE, [(160+16+8+17*i)*GlobalScale, 18*GlobalScale, _width*GlobalScale, _width*GlobalScale])
        for j in range(0, 2):
            if (player.vida >= (i*2)+j+1):
                    pygame.draw.rect(drawSurface, RED, [(160+16+8+17*i +_width/2*j +1 -j)*GlobalScale, (18+1)*GlobalScale, (_width/2 -1)*GlobalScale , (_width-2)*GlobalScale])


    #Mapa
    _ls = showMap()
    _g  = int(((16*17*GlobalScale)-(16*11*GlobalScale)-20)/((len(_ls[0])+1)/2)) +1


    #for o in _ls:
        #print(o)

    if (_g*((len(_ls)+1)/2) > ((16*11*GlobalScale)-87*GlobalScale)):
        _gh = ((16*11*GlobalScale)-87*GlobalScale) / ((len(_ls)+1)/2)
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
                #print("Prueba _ls", _ls[j*2][i*2+1][1])
                if (_ls[j*2][i*2+1][1] == 1):
                    if (_ls[j*2][i*2+1][0] == 1) :
                        _color = WHITE
                        pygame.draw.rect(drawSurface, _color, [((16*11*GlobalScale) +_g*(i+1) +12 -_g2/2), 87*GlobalScale +_gh*j +_gh2/2, _g2, _gh2])

            #Verticales
            if ((j*2+1 < len(_ls)) and i*2 < len(_ls[0])):
                _color = GREEN
                #print("Prueba _ls", _ls[j*2+1][i*2][1])
                if (_ls[j*2+1][i*2][1] == 1):
                    
                    if (_ls[j*2+1][i*2][0] == 1) :
                        _color = WHITE
                        pygame.draw.rect(drawSurface, _color, [((16*11*GlobalScale) +_g*i +_g/2 +12 -_g2/2), 87*GlobalScale +_gh*(j+1) -_gh2/2, _g2, _gh2])

                #Habitacion
            if (_ls[j*2][i*2][1] == 1): #Visto
                _color = BLUE
                if ((Jboss == j*2) and (Iboss == i*2)): #Boss Room #(_ls[j*2][i*2][0] == 11): 
                    _color = RED
                elif (_ls[j*2][i*2][0] == 9): #Current Room
                    _color = YELLOW
                if (_ls[j*2][i*2][0] != 0):
                    pygame.draw.rect(drawSurface, _color, [((16*11*GlobalScale) +_g*i +12), (87*GlobalScale +_gh*j), (_g-5), (_gh-5)])
            else:
                pygame.draw.rect(drawSurface, BLACK, [((16*11*GlobalScale) +_g*i +12), (87*GlobalScale +_gh*j), (_g-5), (_gh-5)])

    #Weapon Background
    _x = 176*GlobalScale          
    _y = 40*GlobalScale  
    pygame.draw.rect(drawSurface, GRAY2, [_x, _y +5*GlobalScale, _x+50*GlobalScale, 22*GlobalScale])    
        
    #actualizar
    pygame.transform.scale(drawSurface, screenhabSize, screen)
    
    #Texto
    screen.blit(font1.render("HEALTH", 0, WHITE), ((160+16+8)*GlobalScale, 10*GlobalScale))
    screen.blit(font1.render("WEAPON", 0, WHITE), ((160+16+8)*GlobalScale, 38*GlobalScale))
    screen.blit(font1.render("MAP                                  Piso: " +str(player.piso), 0, WHITE), ((160+16+8)*GlobalScale, 78*GlobalScale))
 

    #Images

    #FIXMASTER
    for obj in fixLstMaster[Jsel][Isel][0]:
        if type(obj) == Item: #Item
            if (obj.id == 2): #arma
                screen.blit(imgWeaponItem[obj.subId], ((obj.x -16/2)*GlobalScale, (obj.y+1)*GlobalScale))
            else:
                screen.blit(imgItem[obj.id], ((obj.x -16/2 -0.1)*GlobalScale, (obj.y+1)*GlobalScale))
   

    _x = 176*GlobalScale
    _y = 40*GlobalScale
    

    if (player.weapon == 0): #pistol
        _x += 28*GlobalScale
        _y += 2*GlobalScale
    elif (player.weapon == 1): #uzi
        _x += 29*GlobalScale
        _y += 2*GlobalScale
    elif (player.weapon == 2): #shotgun
        _x += 28*GlobalScale
        _y += 2*GlobalScale
    screen.blit(imgWeapon[player.weapon], (_x, _y))

    #_x += 70*GlobalScale
    _x = 176*GlobalScale
    _y = 40*GlobalScale
    _x += 13*GlobalScale
    _y += 10*GlobalScale

    #Ammo
    _txt = str(player.ammo)
    if (player.weapon == 0):
        _txt = "000"

    #Paredes
    #screen.blit(imgWall, (0, 0))


    #Puertas (DISPONIBLES)
    """
    for obj in lstDoors:
        if type(obj) == Door:
            if (fixLstMaster[Jsel][Isel][3] == 1):
                if obj.x > 160:
                    screen.blit(imgDoor0[0], (obj.x *GlobalScale, obj.y *GlobalScale))
            else:
                if obj.x > 159:
                    screen.blit(imgDoor0[1], (obj.x *GlobalScale, obj.y *GlobalScale))
                elif obj.x <"""

    screen.blit(font2.render(_txt, 0, WHITE), (_x, _y))
    pygame.display.flip()
    clock.tick(60)

