import math


# Подлежит будущему удалению.



import pygame
#from pygame.locals import *
import os
import indexes as ind
# from ecosystem import *
# from maps import *
# from strings import *
from pointOfView import *
from cursor import *
from mainCharacter import *

# Инициализация игры
pygame.init()
# Размещаем экран по центру
os.environ['SDL_VIDEO_CENTERED'] = '1'
# Разрешение игрового окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Рендер текста
def text_format(message, tfont, tsize, tcolor):
    new_font = pygame.font.Font(tfont, tsize)
    new_text = new_font.render(message, True, tcolor)
    return new_text

# Количество кадров в секунду
clock = pygame.time.Clock()
FPS = 30

# Главное меню
def main_menu():
    menu = True
    selected = "start"
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        print("Start")
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(ind.light_green)
        title = text_format("Модель искусственной жизни", ind.font6, 50, ind.blue)
        if selected == "start":
            text_start = text_format("START", ind.font2, 75, ind.white)
        else:
            text_start = text_format("START", ind.font2, 75, ind.black)
        if selected == "quit":
            text_quit = text_format("QUIT", ind.font1, 75, ind.white)
        else:
            text_quit = text_format("QUIT", ind.font1, 75, ind.black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Модель искусственной жизни")


'use strict'

class Tile:
    def __init__(self, tx, ty, tt):
        self.x = tx
        self.y = ty
        self.type = tt
        self.eventEnter = None
        self.object = None
        self.plant = None
        self.animal = None
        self.user = None

class TileMap:
    def __init__(self):
        self.map = []
        self.w = 0
        self.h = 0
        self.layer = 4

    def buildMapFromData(self, d, w, h):
        self.w = w
        self.h = h
        if d.length != (w * h):
            return False
        self.map.length = 0
        for y in range(h):
            for x in range(w):
                self.map.append(Tile(x, y, d[((y * w) + x)]))
        return True

mapTileData = {
    0: TileMap(),
    1: TileMap(),
    2: TileMap(),
    3: TileMap(),
    4: TileMap(),
    5: TileMap(),
    6: TileMap(),
    7: TileMap(),
    8: TileMap(),
    9: TileMap()}

player = Character()
curs = Cursor()
eco = Ecosystem()
view = PointOfView()


viewport = {
    'screen': [0, 0],
    'startTile': [0, 0],
    'endTile': [0, 0],
    'offset': [0, 0],
    'update': def function(px, py):
        this.offset[0] = math.floor((this.screen[0] / 2) - px)
        this.offset[1] = math.floor((this.screen[1] / 2) - py)

        tile = [
            math.floor(px / ind.tileW),
            math.floor(py / ind.tileH)
        ]

        this.startTile[0] = tile[0] - 5 - Math.ceil((this.screen[0]) / ind.tileW)
        this.startTile[1] = tile[1] - 5 - Math.ceil((this.screen[1]) / ind.tileH)
        if this.startTile[0] < 0:
            this.startTile[0] = 0
        if this.startTile[1] < 0:
            this.startTile[1] = 0
        this.endTile[0] = tile[0] + 5 + Math.ceil((this.screen[0] / 2) / ind.tileW)
        this.endTile[1] = tile[1] + 5 + Math.ceil((this.screen[1] / 2) / ind.tileH)
        if this.endTile[0] >= mapW[ind.mapNo]:
            this.endTile[0] = mapW[ind.mapNo] - 1
        if this.endTile[1] >= mapH[ind.mapNo]:
            this.endTile[1] = mapH[ind.mapNo] - 1
}

def toIndex(x, y):
    return (y * mapW[ind.mapNo]) + x


def getCursorPosition(canvas, event):
    rect = canvas.getBoundingClientRect()
    x = event.clientX - rect.left
    y = event.clientY - rect.top
    if x < 0 | y < 0 | event.clientX > rect.right | event.clientY > rect.bottom:
        console.log("За пределами карты")
        return [-1, -1]
    else:
        xReal = math.floor((x - viewport.offset[0]) / ind.tileW)
        yReal = math.floor((y - viewport.offset[1]) / ind.tileH)
        console.log("x: " + xReal + " y: " + yReal)
        return [xReal, yReal]


window.onload = function(){
    ctx = document.getElementById('game').getContext('2d')
    audio = document.getElementById("audio")
    canvas = document.querySelector('canvas')
    audio.play()
    requestAnimationFrame(drawGame)
    window.addEventListener('mousedown', function(e):
        pxy = getCursorPosition(canvas, e)
        if (pxy[0] > -1 & pxy[0] < mapW[mapNo] & pxy[1] > -1 & pxy[1] < mapH[mapNo]):
            if ind.clientSpawn | ind.objectSpawn  | ind.animalSpawn | ind.plantSpawn:
                xcur = pxy[0]
                ycur = pxy[1]
                flagO = mapTileData[mapNo].map[toIndex(xcur, ycur)].object
                flagP = mapTileData[mapNo].map[toIndex(xcur, ycur)].plant
                flagA = mapTileData[mapNo].map[toIndex(xcur, ycur)].animal
                flagU = mapTileData[mapNo].map[toIndex(xcur, ycur)].user
                flagT = tileTypes[mapTileData[mapNo].map[toIndex(xcur, ycur)].type].floor
            if clientSpawn:
                if ((flagO == null) & (flagP == null) & (flagA == null) & (flagT != floorTypes.water)
                        & (flagT != floorTypes.solid)):
                    if (flagU == null):
                        prewLoc[0] = player.tileFrom[0]
                        prewLoc[1] = player.tileFrom[1]
                        player.placeAt(xcur, ycur)
                        heroVisible = true
                        mapTileData[mapNo].map[toIndex(xcur, ycur)].user = player
                        mapTileData[mapNo].map[toIndex(prewLoc[0], prewLoc[1])].user = null
                    else:
                        heroVisible = False
                        mapTileData[mapNo].map[toIndex(xcur, ycur)].user = null
            if objectSpawn:
                shadowRock = MapObject(0);
                if ((flagA == null) & (flagP == null) & (flagU == null)):
                    if (flagO == null):
                        shadowRock.placeAt(xcur, ycur, mapNo)
                    } else {
                        shadowRock.deleteAt(xcur, ycur, mapNo)
                    }
                }
            }
            if (animalSpawn):
                if ((flagO == null) & (flagP == null) & (flagU == null) & (flagT != floorTypes.solid)):
                    if ((flagT != floorTypes.water) & (et == ecoType.Land)) | ((flagT != floorTypes.path) & (et == ecoType.Water)):
                        if (flagA == null):
                            eco.addAnim(xcur, ycur, chosenColor, et)
                        else:
                            flagA.deleteAtMap(xcur, ycur, mapNo)
                            eco.delAnim(flagA.index)
            if (plantSpawn){
                if ((flagO == null) & (flagU == null) & (flagA == null)){
                    if (((flagT == floorTypes.path) &  (et == ecoType.Land)) | ((flagT == floorTypes.water) & & (et == ecoType.Water))){
                        if (flagP == null){
                            eco.addPlant(xcur, ycur, et)
                        } else:
                            flagP.deleteAtMap(xcur, ycur, mapNo)
                            eco.delPlant(flagP.index)
                        }
                    }
                }
            }
        }
if (info){
    xcur = pxy[0];
    ycur = pxy[1];
    # let flagP = mapTileData[mapNo].map[toIndex(xcur, ycur)].plant;
    flagA = mapTileData[mapNo].map[toIndex(xcur, ycur)].animal;
    if (flagA != null){
        animInfo = true;
        amInfInd = flagA.index;
    } else {
        animInfo = false;
    }
}
}
})
window.addEventListener("keydown", function(e) {
    if ((e.keyCode >= 37 & & e.keyCode <= 40) | | (e.keyCode == 16) | |
    (e.keyCode == 83) | | (e.keyCode == 87) | | (e.keyCode == 65) | | (e.keyCode == 68)) {
        keysDown[e.keyCode] = true;
    }
});
window.addEventListener("keyup", function(e) {
if ((e.keyCode >= 37 & & e.keyCode <= 40) | | (e.keyCode == 16) | |
(e.keyCode == 83) | | (e.keyCode == 87) | | (e.keyCode == 65) | | (e.keyCode == 68)) {
keysDown[e.keyCode] = false;
}
# Остановка / Воспроизведение модели
if (e.keyCode == 90) {
if (currentSpeed != 0){
pastSpeed = currentSpeed;
currentSpeed = 0;
} else {
currentSpeed = pastSpeed;
clientSpawn = false;
objectSpawn = false;
animalSpawn = false;
plantSpawn = false;
mapChange = false;
}
}
# Изменение скорости появления растений в воде
if (e.keyCode == 75) {
if (PLW == 4){
PLW = 0
} else {
PLW++;
}
}
# Изменение скорости появления растений на суше
if (e.keyCode == 74) {
if (PLT == 4){
PLT = 0;
} else {
PLT++;
}
}
# Добавление / Удаление животных
if (e.keyCode == 73 & & !mapChange & & currentSpeed == 0) {
if (animalSpawn){
animalSpawn = !animalSpawn;
} else {
animalSpawn = !animalSpawn;
plantSpawn = false;
objectSpawn = false;
clientSpawn = false;
info = false;
}
}
# Добавление / Удаление растений
if (e.keyCode == 80 & & !mapChange & & currentSpeed == 0) {
if (plantSpawn){
plantSpawn = !plantSpawn;
} else {
animalSpawn = false;
plantSpawn = !plantSpawn;
objectSpawn = false;
clientSpawn = false;
info = false;
}
}
# Добавление / Удаление объектов
if (e.keyCode == 79 & & !mapChange & & currentSpeed == 0) {
if (objectSpawn){
objectSpawn = !objectSpawn;
} else {
animalSpawn = false;
plantSpawn = false;
objectSpawn = !objectSpawn;
clientSpawn = false;
info = false;
}
}
# Добавление / Удаление пользователя
if (e.keyCode == 85 & & !mapChange & & currentSpeed == 0) {
if (clientSpawn){
clientSpawn = !clientSpawn;
} else {
animalSpawn = false;
plantSpawn = false;
objectSpawn = false;
clientSpawn = !clientSpawn;
info = false;
}
}
# Информация
if (e.keyCode == 89 & & !mapChange) {
if (info){
info = !info;
} else {
animalSpawn = false;
plantSpawn = false;
objectSpawn = false;
clientSpawn = false;
info = !info;
if (eco.animals.length == 0){
animInfo = false;
}
}
}
# Смена языка
if (e.keyCode == 76 & & !mapChange) {
if (userLang < lang.ENG){
userLang++;
} else {
userLang = 0;
}
}

# Смена карты
if (e.keyCode == 77 & & !mapChange & & currentSpeed == 0) {
mapChange = !mapChange;
}
if (clientSpawn | objectSpawn | animalSpawn | plantSpawn){
if ((e.keyCode == 39) | | (e.keyCode == 68) ) {# Вправо
if (curs.canMoveRight()){
curs.MoveRight();
}
}
if ((e.keyCode == 37) | | (e.keyCode == 65)) {# влево
if (curs.canMoveLeft()){
curs.MoveLeft();
}
}
if ((e.keyCode == 38) | | (e.keyCode == 87) ) {# Вверх
if (curs.canMoveUp()){
curs.MoveUp();
}
}
if ((e.keyCode == 40) | | (e.keyCode == 83)) {# Вниз
if (curs.canMoveDown()){
curs.MoveDown();
}
}
if ((e.keyCode >= 49) & & (e.keyCode <= 55) & & animalSpawn){
switch(e.keyCode){
case 49:
    chosenColorInd = 0;
    chosenColor = animalColor.RED;
    break;
case
50:
chosenColorInd = 1;
chosenColor = animalColor.GREEN;
break;
case
51:
chosenColorInd = 2;
chosenColor = animalColor.BLUE;
break;
case
52:
chosenColorInd = 3;
chosenColor = animalColor.YELLOW;
break;
case
53:
chosenColorInd = 4;
chosenColor = animalColor.PINK;
break;
case
54:
chosenColorInd = 5;
chosenColor = animalColor.LIGHTBLUE;
break;
case
55:
chosenColorInd = 6;
chosenColor = animalColor.WHITE;
break;
}
}
if ((e.keyCode == 72) & & (animalSpawn | | plantSpawn)) {# Вниз
    if (et == 0){
        et = 1;
    } else {
        et = 0;
    }
}
if ((e.keyCode == 69) | (e.keyCode == 13) | (e.keyCode == 32)) {# Подтвердить
    let xcur = curs.tileTo[0];
    let ycur = curs.tileTo[1];
    let flagO = mapTileData[mapNo].map[toIndex(xcur, ycur)].object;
    let flagP = mapTileData[mapNo].map[toIndex(xcur, ycur)].plant;
    let flagA = mapTileData[mapNo].map[toIndex(xcur, ycur)].animal;
    let flagU = mapTileData[mapNo].map[toIndex(xcur, ycur)].user;
    let flagT = tileTypes[mapTileData[mapNo].map[toIndex(xcur, ycur)].type].floor;
    if (clientSpawn){
        if ((flagO == null) & & (flagP == null) & & (flagA == null) & & (flagT != floorTypes.water) & & (
                flagT != floorTypes.solid)){
        if (flagU == null){
            prewLoc[0] = player.tileFrom[0];
            prewLoc[1] = player.tileFrom[1];
            player.placeAt(xcur, ycur);
            heroVisible = true;
            mapTileData[mapNo].map[toIndex(xcur, ycur)].user = player;
            mapTileData[mapNo].map[toIndex(prewLoc[0], prewLoc[1])].user = null;
        } else {
            heroVisible = false;
            mapTileData[mapNo].map[toIndex(xcur, ycur)].user = null;
        }

    }
}
if objectSpawn{
    shadowRock = new MapObject(0);
    if (flagA == null) & (flagP == null) & (flagU == null){
        if (flagO == null){
            shadowRock.placeAt(xcur, ycur, mapNo);
        } else {
            shadowRock.deleteAt(xcur, ycur, mapNo);
        }
    }
}
if (animalSpawn){
    if ((flagO == null) & (flagP == null) & (flagU == null) & (flagT != floorTypes.solid)){
        if (((flagT != floorTypes.water) & (et == ecoType.Land)) | ((flagT != floorTypes.path) & (et == ecoType.Water))){
            if (flagA == null){
                eco.addAnim(xcur, ycur, chosenColor, et);
            } else {
                flagA.deleteAtMap(xcur, ycur, mapNo);
                eco.delAnim(flagA.index);
            }
        }
    }
}
if (plantSpawn){
    if ((flagO == null) & (flagU == null) & (flagA == null)){
        if (((flagT == floorTypes.path) & (et == ecoType.Land)) | ((flagT == floorTypes.water) & (et == ecoType.Water))){
            if (flagP == null){
                eco.addPlant(xcur, ycur, et);
            } else {
                flagP.deleteAtMap(xcur, ycur, mapNo);
                eco.delPlant(flagP.index);
            }
        }
    }
}
}
}
    if (mapChange):
        if (e.keyCode == 81):
            mapChange =! mapChange
        if (e.keyCode == 48):
            mapCh = 0
        if (e.keyCode == 49):
            mapCh = 1
        if (e.keyCode == 50):
            mapCh = 2
        if (e.keyCode == 51):
            mapCh = 3
        if (e.keyCode == 52):
            mapCh = 4
        if (e.keyCode == 53):
            mapCh = 5
        if (e.keyCode == 54):
            mapCh = 6
        if (e.keyCode == 55):
            mapCh = 7
        if (e.keyCode == 56):
            mapCh = 8
        if (e.keyCode == 57):
            mapCh = 9
        if ((e.keyCode == 39) | (e.keyCode == 68) ):
            if (mapCh < 9):
                mapCh ++
            else:
                mapCh = 0
        if ((e.keyCode == 37) | (e.keyCode == 65)):
            if (mapCh > 0):
                mapCh --
            else:
                mapCh = 9
        if (e.keyCode == 69):
            mapChange = False
            eco.clear()
            heroVisible = False
            mapTileData[mapNo].map[toIndex(player.tileTo[0], player.tileTo[1])].user = None
            pastSpeed = 1
            currentSpeed = 0
            mapNo = mapCh

        # Работа со временем
        if e.keyCode == 84 & currentSpeed != 0:
            if (currentSpeed < 9):
                currentSpeed += 1
            else:
                currentSpeed = 1

        # Включить / Выключить музыку
        if e.keyCode == 88:
            if(!audio.paused):
                audio.pause()
            else:
                audio.play()

        # Очистка
        if (e.keyCode == 67):
            eco.clear();
            heroVisible = false;
            mapTileData[mapNo].map[toIndex(xcur, ycur)].user = null;
            pastSpeed = 1;
            currentSpeed = 0;
})

    viewport.screen =[
        document.getElementById('game').width,
        document.getElementById('game').height
    ]

    mapTileData[0].buildMapFromData(gameMap[0], mapW[0], mapH[0])
    mapTileData[1].buildMapFromData(gameMap[1], mapW[1], mapH[1])
    mapTileData[2].buildMapFromData(gameMap[2], mapW[2], mapH[2])
    mapTileData[3].buildMapFromData(gameMap[3], mapW[3], mapH[3])
    mapTileData[4].buildMapFromData(gameMap[4], mapW[4], mapH[4])
    mapTileData[5].buildMapFromData(gameMap[5], mapW[5], mapH[5])
    mapTileData[6].buildMapFromData(gameMap[6], mapW[6], mapH[6])
    mapTileData[7].buildMapFromData(gameMap[7], mapW[7], mapH[7])
    mapTileData[8].buildMapFromData(gameMap[8], mapW[8], mapH[8])
    mapTileData[9].buildMapFromData(gameMap[9], mapW[9], mapH[9])



if __name__ == '__main__':
    main_menu()
    pygame.quit()
    #quit()