from animal import *
from plants import *
from maps import *
import indexes as ind
import random_new as rnd
import objects as obj
import pointOfView as pov


class Ecosystem(pygame.sprite.Sprite):
    def __init__(self):
        self.animals = {}
        self.plants = {}
        self.objects = {}

    # Функция добавления животного в экосистему
    def addAnim(self, game, x, y, col, c):
        anim = Animal(game)
        anim.placeAt(x, y)
        anim.colorAnim(col)
        anim.ecoAddType(c, game)
        anim1 = AnimalObject(ind.animalInd)
        if ind.animalInd < 1000000:
            ind.animalInd += 1
        else:
            ind.animalInd = 0
        anim1.placeAtMap(x, y, ind.mapNo)
        self.animals[anim.index] = anim

    def loadAnim(self, game, sanim):
        anim = Animal(game)
        anim.index = sanim.index
        anim.color = sanim.color
        anim.status = sanim.status
        anim.ecoT = sanim.ecoT
        anim.tileFrom = sanim.tileFrom
        anim.tileTo = sanim.tileTo
        anim.tilePurpose = sanim.tilePurpose
        anim.courseLast = sanim.courseLast
        anim.courseNext = sanim.courseNext
        anim.liveTime = sanim.liveTime
        anim.tYang = sanim.tYang
        anim.told = sanim.told
        anim.deathTime = sanim.deathTime
        anim.tZero = sanim.tZero
        anim.startEnergy = sanim.startEnergy
        anim.energy = sanim.energy
        anim.maxEnergy = sanim.maxEnergy
        anim.stepEnergy = sanim.stepEnergy
        anim.moveEnergy = sanim.moveEnergy
        anim.sleepEnergy = sanim.sleepEnergy
        anim.piece = sanim.piece
        anim.food = sanim.food
        anim.pAttackEnergy = sanim.pAttackEnergy
        anim.pSpawnEnergy = sanim.pSpawnEnergy
        anim.timeMoved = sanim.timeMoved
        anim.delayMove = sanim.delayMove
        anim.dimensions = sanim.dimensions
        anim.position = sanim.position
        anim.spriteDirect = sanim.spriteDirect
        anim1 = AnimalObject(anim.index)
        anim1.placeAtMap(anim.tileFrom[0], anim.tileFrom[1], ind.mapNo)
        self.animals[anim.index] = anim

    # Функция добавления растения в экосистему
    def addPlant(self, game, x, y, c):
        plant = Plant(game)
        plant.placeAt(x, y)
        plant.ecoAddType(c, game)
        plnt1 = PlantObject(ind.plantInd)
        if ind.plantInd < 1000000:
            ind.plantInd += 1
        else:
            ind.plantInd = 0
        plnt1.placeAtMap(x, y, ind.mapNo)
        self.plants[plant.index] = plant

    def loadPlant(self, game, splnt):
        plant = Plant(game)
        plant.X = splnt.X
        plant.Y = splnt.Y
        plant.index = splnt.index
        plant.ecoT = splnt.ecoT
        plant.liveTime = splnt.liveTime
        plant.deathTime = splnt.deathTime
        plant.berryTime = splnt.berryTime
        plant.told = splnt.told
        plant.piece = splnt.piece
        plant.food = splnt.food
        plant.status = splnt.status
        plant.sprites = splnt.sprites
        plnt1 = PlantObject(plant.index)
        plnt1.placeAtMap(plant.X, plant.Y, ind.mapNo)
        self.plants[plant.index] = plant

    def addObject(self, game, x, y, type_o):
        object11 = obj.ObjectInfo(game, type_o)
        object11.placeAt(x, y)
        object1 = obj.MapObject(game)
        if ind.objectInd < 1000000:
            ind.objectInd += 1
        else:
            ind.ObjectInd = 0
        object1.placeAt(x, y, ind.mapNo)
        self.objects[object11.index] = object11

    def loadObject(self, game, sobj):
        object11 = obj.ObjectInfo(game, sobj.type)
        object11.x = sobj.x
        object11.y = sobj.y
        object11.index = sobj.index
        object11.sprites = sobj.sprites
        object1 = obj.MapObject(game)
        object1.placeAt(sobj.x, sobj.y, ind.mapNo)
        self.objects[object11.index] = object11

    # Функция удаления животного из экосистемы
    def delAnim(self, inds):
        x_cur = self.animals[inds].tileTo[0]
        y_cur = self.animals[inds].tileTo[1]
        flag_a = mapTileData[ind.mapNo].map[toIndex(x_cur, y_cur)].animal
        if flag_a is not None:
            flag_a.deleteAtMap(x_cur, y_cur, ind.mapNo)
        # Удаляем спрайт
        self.animals[inds].kill()
        del self.animals[inds]

    # Функция удаления растения из экосистемы
    def delPlant(self, inds):
        x_cur = self.plants[inds].X
        y_cur = self.plants[inds].Y
        flag_p = mapTileData[ind.mapNo].map[toIndex(x_cur, y_cur)].plant
        if flag_p is not None:
            flag_p.deleteAtMap(x_cur, y_cur, ind.mapNo)
        self.plants[inds].kill()
        del self.plants[inds]

    # Функция удаления объекта из экосистемы
    def delObject(self, inds):
        x_cur = self.objects[inds].x
        y_cur = self.objects[inds].y
        flag_o = mapTileData[ind.mapNo].map[toIndex(x_cur, y_cur)].object
        if flag_o is not None:
            flag_o.deleteAtMap(x_cur, y_cur, ind.mapNo)
        self.objects[inds].kill()
        del self.objects[inds]

    # Функция нахождения индекса животного в массиве по заданным координатам
    def indAnim(self, a):
        flag_p = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].animal
        inds = -1
        if self.animals[flag_p.index]:
            inds = self.animals[flag_p.index].index
        return inds

    # Функция нахождения индекса растения в массиве по заданным координатам
    def indPlant(self, a):
        flag_p = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].plant
        inds = -1
        if self.plants[flag_p.index]:
            inds = self.plants[flag_p.index].index
        return inds

    # Функция очищения экосистемы от всех объектов
    def clear(self):
        for ann in self.animals:
            self.animals[ann].kill()
        for plt in self.plants:
            self.plants[plt].kill()
        for obb in self.objects:
            self.objects[obb].kill()
        self.animals.clear()
        self.plants.clear()
        self.objects.clear()
        ind.animalInd = 0
        ind.plantInd = 0
        plnt1 = PlantObject(ind.plantInd)
        anim1 = AnimalObject(ind.animalInd)
        obj1 = obj.MapObject(0)
        for iii in range(mapW[ind.mapNo] - 1):
            for j in range(mapH[ind.mapNo] - 1):
                plnt1.deleteAtMap(iii, j, ind.mapNo)
                anim1.deleteAtMap(iii, j, ind.mapNo)
                obj1.deleteAtMap(iii, j, ind.mapNo)

    # Функция возвращения индекса ближайшего врага-животного из списка для защиты
    def attacked(self, game, anim):
        iii = -1
        for indexA in game.view.nearAnim:
            aa1 = anim.enemy(self.animals[indexA])
            aa2 = self.animals[indexA].status != statusAnim["DEATH"]
            aa3 = self.animals[indexA].status != statusAnim["ZERO"]
            if aa1 and aa2 and aa3:
                iii = indexA
                return iii
        return iii

    # Функция возвращения индекса ближайшего врага-животного из списка для атаки
    def attack(self, game, anim):
        iii = -1
        for indexA in game.view.nearAnim:
            aa1 = anim.enemy(self.animals[indexA])
            aa2 = self.animals[indexA].status != statusAnim["DEATH"]
            aa3 = self.animals[indexA].status != statusAnim["ZERO"]
            if aa1 and aa2 and aa3:
                iii = indexA
                return iii
        return iii

    # Функция возвращения индекса ближайшего не врага-животного с которым можно спариться.
    def spawn(self, game, anim):
        iii = -1
        for indexA in game.view.nearAnim:
            anim1 = self.animals[indexA]
            aa1 = not (anim.enemy(anim1))
            aa2 = anim1.status != statusAnim["DEATH"]
            aa3 = anim1.status != statusAnim["ZERO"]
            aa4 = anim1.liveTime > anim1.tYang
            if aa1 and aa2 and aa3 and aa4:
                iii = indexA
                return iii
        return iii

    # Функция возвращения индекса ближайшего мертвого животного из списка
    def eat(self, game):
        iii = -1
        for indexA in game.view.nearAnim:
            if self.animals[indexA].status == statusAnim["DEATH"]:
                iii = indexA
                return iii
        return iii

    # Функция выбора в какую сторону смотреть
    def lookWay(self, game, iii, p):  # p - смещение относительно животного, i - индекс животного в массиве
        a111 = self.animals[iii].tileFrom[0]
        b111 = self.animals[iii].tileFrom[1]
        c111 = self.animals[iii].courseLast
        self.animals[iii].tileTo = [a111, b111]
        self.animals[iii].courseNext = 1 * c111
        pos1 = [2, 2]
        pos2 = [p[0] + pos1[0], p[1] + pos1[1]]
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        myCourse = self.animals[iii].courseLast
        while (abs(dx) + abs(dy)) != 1:
            nx = 0
            ny = 0
            if dx != 0:
                nx = math.floor(dx / abs(dx))
            if dy != 0:
                ny = math.floor(dy / abs(dy))
            aa1 = (game.view.lookTile[pos2[0]][pos2[1] - ny] == statusCell["CLEAR"])
            aa2 = (game.view.lookTile[pos2[0] - nx][pos2[1]] == statusCell["CLEAR"])
            if (dx != 0) and (dy != 0) and aa1 and aa2:
                if (myCourse % 2) != 0:
                    pos3 = [pos2[0], pos2[1] - ny]
                else:
                    pos3 = [pos2[0] - nx, pos2[1]]
            else:
                if (dx != 0) and (game.view.lookTile[pos2[0] - nx][pos2[1]] == statusCell["CLEAR"]):
                    pos3 = [pos2[0] - nx, pos2[1]]
                else:
                    if (dy != 0) and (game.view.lookTile[pos2[0]][pos2[1] - ny] == statusCell["CLEAR"]):
                        pos3 = [pos2[0], pos2[1] - ny]
                    else:
                        return False
            pos2 = pos3
            dx = pos2[0] - pos1[0]
            dy = pos2[1] - pos1[1]
        course = -1
        if (pos1[0] - pos2[0]) == 0:
            if (pos1[1] - pos2[1]) == -1:
                course = 0
                self.animals[iii].spriteDirect = animalSprite["down"]
            else:
                if (pos1[1] - pos2[1]) == 1:
                    course = 2
                    self.animals[iii].spriteDirect = animalSprite["up"]
        else:
            if (pos1[1] - pos2[1]) == 0:
                if (pos1[0] - pos2[0]) == -1:
                    course = 3
                    self.animals[iii].spriteDirect = animalSprite["right"]
                else:
                    if (pos1[0] - pos2[0]) == 1:
                        course = 1
                        self.animals[iii].spriteDirect = animalSprite["left"]
        if myCourse == course:
            if game.view.lookTile[pos2[0]][pos2[1]] != statusCell["CLEAR"]:
                return False
            self.animals[iii].tileTo[0] = pos2[0] + self.animals[iii].tileFrom[0] - 2
            self.animals[iii].tileTo[1] = pos2[1] + self.animals[iii].tileFrom[1] - 2
        else:
            self.animals[iii].courseNext = course
        self.animals[iii].status = statusAnim["WALK"]
        return True

    # Функция выбора цели для существа
    def choosePurpose(self, game, iii):  # i - индекс существа в массиве
        j = self.attacked(game, self.animals[iii])  # DEFENSE and ATTACK
        if j >= 0:
            indexA = j
            delta = abs(self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]) + \
                abs(self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1])
            if delta < 2:
                poX = self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]
                poY = self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1]
                if not (self.lookWay(game, iii, [poX, poY])):
                    self.animals[indexA].attacked()
                    self.animals[iii].spriteDirect = 8 + self.animals[iii].courseNext
                    return self.animals[iii].statusUpdate(statusAnim["ATTACK"])
                if self.animals[iii].courseLast != self.animals[iii].courseNext:
                    return statusAnim["WALK"]

        if self.animals[iii].hungry():  # EAT
            if len(game.view.nearFood) != 0:
                poX = game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]
                poY = game.view.nearFood[0][1] - self.animals[iii].tileFrom[1]
                if not (self.lookWay(game, iii, [poX, poY])):
                    self.animals[iii].statusUpdate(statusAnim["EAT"])
                    q = 0
                    for numb in range(len(game.view.nearFood)):
                        r = game.view.nearFood[numb]
                        if (r[0] == game.view.nearFood[0][0]) and (r[1] == game.view.nearFood[0][1]):
                            break
                        q += 1
                    indexP = self.indPlant(game.view.nearFood[q])
                    food = self.plants[indexP].eat()
                    return statusAnim["EAT"]
            j = self.eat(game)
            if j >= 0:
                indexA = j
                poX = self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]
                poY = self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1]
                if not (self.lookWay(game, iii, [poX, poY])):
                    self.animals[iii].statusUpdate(statusAnim["EAT"])
                    self.animals[indexA].eat()
                    return statusAnim["EAT"]

        j = self.attack(game, self.animals[iii])  # WALK->ATTACK
        if self.animals[iii].attackEnergy() and (j >= 0):
            indexA = j
            poX = self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]
            poY = self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1]
            self.lookWay(game, iii, [poX, poY])
            shadAnim = AnimalObject(self.animals[iii].index)
            posTo = self.animals[iii].tileTo
            posFrom = self.animals[iii].tileFrom
            if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
            self.animals[iii].tilePurpose = self.animals[iii].tileTo
            return statusAnim["WALK"]

        j = self.spawn(game, self.animals[iii])  # SPAWN and WALK->SPAWN
        if self.animals[iii].spawnEnergy() and (j >= 0):
            indexA = j
            # indexA = self.lookAnim(game.view.nearAnim[j])
            delta = abs(self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]) \
                + abs(self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1])
            if delta < 2:
                if len(game.view.nearClear) == 0:
                    self.animals[iii].abortion()
                else:
                    animbaby = Animal(game)
                    animbaby.Born(self.animals[iii], self.animals[indexA], game.view.nearClear[0][0],
                                  game.view.nearClear[0][1])
                    animbaby.ecoAddType(self.animals[iii].ecoT, game)
                    if ind.animalInd < 1000000:
                        ind.animalInd += 1
                    else:
                        ind.animalInd = 0
                    self.animals[animbaby.index] = animbaby
                    shadAnim = AnimalObject(animbaby.index)
                    shadAnim.placeAtMap(animbaby.tileTo[0], animbaby.tileTo[1], ind.mapNo)
                    self.animals[iii].birth(animbaby)
                self.animals[iii].tilePurpose = self.animals[iii].tileFrom
                self.animals[iii].tileTo = self.animals[iii].tileFrom
                self.animals[iii].courseNext = self.animals[iii].courseLast
                return self.animals[iii].statusUpdate(statusAnim["SLEEP"])
            poX = self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]
            poY = self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1]
            self.lookWay(game, iii, [poX, poY])
            # Движение
            shadAnim = AnimalObject(self.animals[iii].index)
            posTo = self.animals[iii].tileTo
            posFrom = self.animals[iii].tileFrom
            if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
            self.animals[iii].tilePurpose = self.animals[iii].tileTo
            return statusAnim["WALK"]

        if self.animals[iii].hungry():  # WALK->EAT
            j = self.eat(game)
            df = 100
            db = 100
            if len(game.view.nearFood) != 0:
                df = abs(game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]) \
                     + abs(game.view.nearFood[0][1] - self.animals[iii].tileFrom[1])
            if j >= 0:
                indexA = j
                db = abs(self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]) \
                    + abs(self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1])
            if (df < 100) or (db < 100):
                if df < db:
                    poX = game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]
                    poY = game.view.nearFood[0][1] - self.animals[iii].tileFrom[1]
                    self.lookWay(game, iii, [poX, poY])
                else:
                    indexA = j
                    poX = self.animals[indexA].tileTo[0] - self.animals[iii].tileFrom[0]
                    poY = self.animals[indexA].tileTo[1] - self.animals[iii].tileFrom[1]
                    self.lookWay(game, iii, [poX, poY])
                shadAnim = AnimalObject(self.animals[iii].index)
                posTo = self.animals[iii].tileTo
                posFrom = self.animals[iii].tileFrom
                if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                    shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                    shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
                self.animals[iii].tilePurpose = self.animals[iii].tileTo
                return statusAnim["WALK"]
        if self.animals[iii].fewEnergy() or (len(game.view.nearClear) == 0):  # SLEEP
            self.animals[iii].tileTo = self.animals[iii].tileFrom
            self.animals[iii].courseNext = self.animals[iii].courseLast
            return self.animals[iii].statusUpdate(statusAnim["SLEEP"])

        poX = self.animals[iii].tilePurpose[0] - self.animals[iii].tileFrom[0]
        poY = self.animals[iii].tilePurpose[1] - self.animals[iii].tileFrom[1]
        flag = self.lookWay(game, iii, [poX, poY])  # WALK
        flag2 = pov.statReturn([self.animals[iii].tilePurpose[0], self.animals[iii].tilePurpose[1]],
                               self.animals[iii].ecoT, self)
        if flag and (flag2 == statusCell["CLEAR"]):
            shadAnim = AnimalObject(self.animals[iii].index)
            posTo = self.animals[iii].tileTo
            posFrom = self.animals[iii].tileFrom
            if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
            return statusAnim["WALK"]
        nerlen = len(game.view.nearClear)
        if len(game.view.nearClear) != 0:
            q = 0
            if nerlen > 1:
                q = rnd.getRandomInt(len(game.view.nearClear) - 1)  # WALK
            poX = game.view.nearClear[q][0] - self.animals[iii].tileFrom[0]
            poY = game.view.nearClear[q][1] - self.animals[iii].tileFrom[1]
            self.lookWay(game, iii, [poX, poY])
            self.animals[iii].tilePurpose = game.view.nearClear[q]
            shadAnim = AnimalObject(self.animals[iii].index)
            posTo = self.animals[iii].tileTo
            posFrom = self.animals[iii].tileFrom
            if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
            return statusAnim["WALK"]
        return statusAnim["SLEEP"]
