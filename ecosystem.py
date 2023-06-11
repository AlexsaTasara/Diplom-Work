from animal import *
from plants import *
from maps import *
import indexes as ind
import random_new as rnd
import objects as obj
import pointOfView as pov


def eating(eco, game, iii):
    # проверка, что агент голоден
    if eco.animals[iii].hungry():  # EAT
        # Если в поле видимости есть еда
        if len(game.view.nearFood) != 0:
            result = eco.eatPlant(game, iii)
            if result != -1:
                return result
        # Создание списка мертвых тел
        j = eco.eat(game)
        if j >= 0:
            result = eco.eatAgent(game, iii, j)
            if result != -1:
                return result


def lookBerry(eco, game, iii):
    if len(game.view.nearFood) != 0:
        result = eco.eatPlant(game, iii)
        if result != -1:
            return result


def lookBody(eco, game, iii):
    if len(game.view.nearBody) != 0:
        index = game.view.nearBody[0]
        result = eco.eatAgent(game, iii, index)
        if result != -1:
            return result


def lookAgent(eco, game, anim):
    index = -1
    for i1 in range(game.view.nearAnimal):
        if not (game.eco.animals[i1].sameSpecies(anim)):
            # Проверка хотим ли мы атаковать
            check = round(rand.random.uniform(0.0, 1.0), 2)
            aa1 = check > game.eco.relationship[anim.ecoT][i1][anim.index]
            aa2 = anim.attackEnergy
            if aa1 and aa2:
                index = i1
    return index


def interacting(eco, game, iii):
    # Проходимся по списку животных
    for indexA in game.view.nearAnim:
        anim1 = eco.animals[indexA]
        anim = eco.animals[iii]
        aa0 = not anim.sameSpecies(anim1)
        aaT = anim1.ecoT == anim.ecoT
        # Ищем существо не того же вида
        if aa0:
            # Если существо той же экосистемы
            if aaT:
                # Смотрим на отношение между этими видами
                relation = eco.relationship[anim.ecoT][anim.species][anim1.species]
                randomMood = round(rand.random.uniform(0.0, 1.0), 2)
                # Если положительное отношение
                if randomMood <= relation:
                    # Выбираем между: идти спариваться или игнорировать
                    # Достаточно взрослый
                    aa1 = anim1.liveTime > anim1.tYang
                    # Можно ли спариваться
                    aa2 = not (anim.canBreed(anim1))
                    # Не мертво
                    aa3 = (anim1.status != statusAnim["DEATH"]) and (anim1.status != statusAnim["ZERO"])
                    if aa1 and aa2 and aa3:
                        result = eco.walkAndSpawn(game, anim.index, indexA)
                        return result
                # Если отрицательное отношение
                else:
                    # Выбираем между: идти атаковать, игнорировать или убегать.
                    # Есть возможность атаковать
                    aa1 = anim.attackEnergy()
                    # Будет ли существо убегать
                    aa2 = not eco.chooseEscape(anim.index)
                    aa3 = anim1.liveTime > anim1.tYang
                    if aa1 and aa2 and aa3:
                        # Атакуем если противник совсем рядом в противном случае игнорируем
                        result = eco.defenceAgainstEnemy(game, iii, indexA)
                        if result != -1:
                            return result


def findPossiblePartner(game, anim):
    for indexA in game.view.nearAnim:
        anim1 = game.eco.animals[indexA]
        # Если существо того же вида
        aa0 = anim.sameSpecies(anim1)
        # Можно ли спариваться
        aa1 = not (anim.canBreed(anim1))
        # Не мертво
        aa2 = (anim1.status != statusAnim["DEATH"]) and (anim1.status != statusAnim["ZERO"])
        # Стоит ли взаимодействовать положительно
        key1 = anim.species
        key2 = anim1.species
        relation = game.eco.relationship[anim.ecoT][key1][key2]
        randomMood = round(rand.random.uniform(0.0, 1.0), 2)
        aa3 = randomMood <= relation
        # Подходящего возраста
        aa4 = anim1.liveTime > anim1.tYang
        aa5 = anim.ecoT == anim1.ecoT
        if (aa0 or aa1) and aa2 and aa3 and aa4 and aa5:
            return indexA
    return -1


# Вроде закончили с этим.
def spawning(eco, game, iii):
    anim = eco.animals[iii]
    canSpawn = anim.spawnEnergy()
    # Если существо не может скрещиваться или нет партнеров, возвращает -1
    check = -1
    if canSpawn:
        check = findPossiblePartner(game, anim)
    if check != -1:
        # Если нашли с кем скрещиваться, идем к нему
        result = eco.walkAndSpawn(game, iii, check)
        if result != -1:
            return result


functionDictionary = {
    "Eat": eating,
    "Interact": interacting,
    "Spawn": spawning
}

eatingDictionary = {
    "Berry": lookBerry,
    "Body": lookBody,
    "Agent": lookAgent
}


class Ecosystem(pygame.sprite.Sprite):
    def __init__(self):
        self.animals = {}
        self.plants = {}
        self.objects = {}
        # Массив отношений между видами
        self.relationship = {"Land": [[1.0] * 8 for i1 in range(8)],
                             "Water": [[1.0] * 8 for i1 in range(8)]}
        # Веса видов для роевого интеллекта
        self.hiveWeights = {"Land": [[0.3, 0.3, 0.4, 0.5, 0.5] for i1 in range(8)],
                            "Water": [[0.3, 0.3, 0.4, 0.5, 0.5] for i1 in range(8)]}
        self.totalEnergy = 0
        self.spEnergy = {"Land": [0, 0, 0, 0, 0, 0, 0, 0],
                         "Water": [0, 0, 0, 0, 0, 0, 0, 0]}

    # Создание массива отношений между разными видами
    def createRelationships(self):
        for i1 in range(8):
            for j1 in range(i1):
                if i1 == j1:
                    self.relationship["Land"][i1][j1] = 1.0
                    self.relationship["Water"][i1][j1] = 1.0
                else:
                    randRel = round(rand.random.uniform(0.4, 0.6), 2)
                    self.relationship["Land"][i1][j1] = copy.deepcopy(randRel)
                    self.relationship["Land"][j1][i1] = copy.deepcopy(randRel)
                    randRel = round(rand.random.uniform(0.4, 0.6), 2)
                    self.relationship["Water"][i1][j1] = copy.deepcopy(randRel)
                    self.relationship["Water"][j1][i1] = copy.deepcopy(randRel)

    # Подсчитываем общую энергию системы экосистемы
    def updateEnergy(self):
        self.totalEnergy = 0
        self.spEnergy = {"Land": [0, 0, 0, 0, 0, 0, 0, 0],
                         "Water": [0, 0, 0, 0, 0, 0, 0, 0]}
        for an in self.animals:
            anim = self.animals[an]
            self.totalEnergy += anim.energy
            self.spEnergy[anim.ecoT][anim.species] += anim.energy

    # Функция добавления животного в экосистему
    def addAnim(self, game, x, y, col, c):
        anim = Animal(game)
        anim.placeAt(x, y)
        anim.colorAnim(col)
        anim.ecoAddType(c, game)
        anim.randomWeights()
        anim.typeOfSpecies()
        anim1 = AnimalObject(ind.animalInd)
        if ind.animalInd < 1000000:
            ind.animalInd += 1
        else:
            ind.animalInd = 0
        anim1.placeAtMap(x, y, ind.mapNo)
        self.animals[anim.index] = anim

    # Нужно исправить.
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

    # Нужно исправить.
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

    # Нужно исправить.
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

    def positionsXY(self, agent1, agent2):
        poX = self.animals[agent1].tileTo[0] - self.animals[agent2].tileFrom[0]
        poY = self.animals[agent1].tileTo[1] - self.animals[agent2].tileFrom[1]
        return poX, poY

    # Расстояние
    def distance(self, agent1, agent2):
        dist = abs(self.animals[agent1].tileTo[0] - self.animals[agent2].tileFrom[0]) \
               + abs(self.animals[agent1].tileTo[1] - self.animals[agent2].tileFrom[1])
        return dist

    def relationshipRebalance(self, ecoT, sp1, sp2, balance):
        self.relationship[ecoT][sp1][sp2] += balance
        self.relationship[ecoT][sp2][sp1] += balance
        a = self.relationship[ecoT][sp1][sp2]
        if a > 1:
            self.relationship[ecoT][sp1][sp2] = 1
            self.relationship[ecoT][sp2][sp1] = 1
        if a < 0:
            self.relationship[ecoT][sp1][sp2] = 0
            self.relationship[ecoT][sp2][sp1] = 0

    # Ребаланс весов
    def weightRebalance(self, iii, balance, what):
        if what == "birth":
            self.animals[iii].birthWeight += balance
            if self.animals[iii].eatWeight > (balance / 2):
                self.animals[iii].eatWeight -= (balance / 2)
            else:
                self.animals[iii].birthWeight -= (balance / 2)
            if self.animals[iii].interactionWeight > (balance / 2):
                self.animals[iii].interactionWeight -= (balance / 2)
            else:
                self.animals[iii].birthWeight -= (balance / 2)
        if what == "inter":
            self.animals[iii].interactionWeight += balance
            if self.animals[iii].eatWeight > (balance / 2):
                self.animals[iii].eatWeight -= (balance / 2)
            else:
                self.animals[iii].interactionWeight -= (balance / 2)
            if self.animals[iii].birthWeight > (balance / 2):
                self.animals[iii].birthWeight -= (balance / 2)
            else:
                self.animals[iii].interactionWeight -= (balance / 2)
        if what == "eat":
            self.animals[iii].eatWeight += balance
            if self.animals[iii].birthWeight > (balance / 2):
                self.animals[iii].birthWeight -= (balance / 2)
            else:
                self.animals[iii].eatWeight -= (balance / 2)
            if self.animals[iii].interactionWeight > (balance / 2):
                self.animals[iii].interactionWeight -= (balance / 2)
            else:
                self.animals[iii].eatWeight -= (balance / 2)
        # Доделать баланс ягод и тела
        if what == "body":
            a1 = 1
        if what == "berry":
            a1 = 1

    # Функция возвращения индекса ближайшего врага-животного из списка для атаки
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

    # Функция возвращения индекса взрослого животного не того же вида
    def notSameAdult(self, game, animInd):
        for indexA in game.view.nearAnim:
            anim1 = self.animals[indexA]
            anim = self.animals[animInd]
            aa0 = not anim.sameSpecies(anim1)
            aa1 = anim1.liveTime > anim1.tYang
            if aa0 and aa1:
                return indexA
        return -1

    # Функция возвращения индекса ближайшего не врага-животного с которым можно спариться.
    def spawn(self, game, anim):
        iii = -1
        for indexA in game.view.nearAnim:
            anim1 = self.animals[indexA]
            aa1 = not (anim.enemy(anim1))
            aa2 = anim1.status != statusAnim["DEATH"]
            aa3 = anim1.status != statusAnim["ZERO"]
            aa4 = anim1.liveTime > anim1.tYang
            aa5 = anim.ecoT == anim1.ecoT
            if aa1 and aa2 and aa3 and aa4 and aa5:
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

    def defenceAgainstEnemy(self, game, iii, indexA):
        delta = self.distance(indexA, iii)
        # Если достаточно близок
        if delta < 2:
            poX, poY = self.positionsXY(indexA, iii)
            # Если смотрим в нужную сторону
            if not (self.lookWay(game, iii, [poX, poY])):
                self.animals[indexA].attacked()
                self.animals[iii].spriteDirect = 8 + self.animals[iii].courseNext
                self.weightRebalance(iii, 0.008, "inter")
                if self.animals[iii].ecoT == self.animals[indexA].ecoT:
                    self.relationshipRebalance(self.animals[iii].ecoT, self.animals[iii].species,
                                               self.animals[indexA].species, -0.02)
                return self.animals[iii].statusUpdate(statusAnim["ATTACK"])
            if self.animals[iii].courseLast != self.animals[iii].courseNext:
                return statusAnim["WALK"]
        return -1

    def eatPlant(self, game, iii):
        poX = game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]
        poY = game.view.nearFood[0][1] - self.animals[iii].tileFrom[1]
        # Если смотрим в нужную сторону
        if not (self.lookWay(game, iii, [poX, poY])):
            self.animals[iii].statusUpdate(statusAnim["EAT"])
            q = 0
            for numb in range(len(game.view.nearFood)):
                r = game.view.nearFood[numb]
                if (r[0] == game.view.nearFood[0][0]) and (r[1] == game.view.nearFood[0][1]):
                    break
                q += 1
            indexP = self.indPlant(game.view.nearFood[q])
            food1 = self.plants[indexP].eat()
            self.weightRebalance(iii, 0.002, "eat")
            return statusAnim["EAT"]
        return -1

    def eatAgent(self, game, iii, indexA):
        poX, poY = self.positionsXY(indexA, iii)
        # Если смотрим в нужную сторону
        if not (self.lookWay(game, iii, [poX, poY])):
            self.animals[iii].statusUpdate(statusAnim["EAT"])
            self.animals[indexA].eat()
            self.weightRebalance(iii, 0.002, "eat")
            return statusAnim["EAT"]
        return -1

    def moveToTheAgent(self, game, iii, indexA):
        poX, poY = self.positionsXY(indexA, iii)
        self.lookWay(game, iii, [poX, poY])
        shadAnim = AnimalObject(self.animals[iii].index)
        posTo = self.animals[iii].tileTo
        posFrom = self.animals[iii].tileFrom
        if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
            shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
            shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
        self.animals[iii].tilePurpose = self.animals[iii].tileTo
        return statusAnim["WALK"]

    def walkAndSpawn(self, game, iii, indexA):
        delta = self.distance(indexA, iii)
        # Если агенты достаточно близки - размножение
        if delta < 2:
            if len(game.view.nearClear) == 0:
                self.animals[iii].abortion()
                self.weightRebalance(iii, -0.004, "birth")
                self.weightRebalance(indexA, -0.004, "birth")
            else:
                animbaby = Animal(game)
                animbaby.Born(self.animals[iii], self.animals[indexA], game.view.nearClear[0][0],
                              game.view.nearClear[0][1])

                self.weightRebalance(iii, 0.004, "birth")
                self.weightRebalance(indexA, 0.004, "birth")
                if not self.animals[iii].sameSpecies(self.animals[indexA]):
                    self.weightRebalance(iii, 0.004, "inter")
                    self.weightRebalance(indexA, 0.004, "inter")
                    self.relationshipRebalance(self.animals[iii].ecoT, self.animals[iii].species,
                                               self.animals[indexA].species, 0.1)
                animbaby.ecoAddType(self.animals[indexA].ecoT, game)
                if ind.animalInd < 1000000:
                    ind.animalInd += 1
                else:
                    ind.animalInd = 0
                animbaby.typeOfSpecies()
                self.animals[animbaby.index] = animbaby
                shadAnim = AnimalObject(animbaby.index)
                shadAnim.placeAtMap(animbaby.tileTo[0], animbaby.tileTo[1], ind.mapNo)
                self.animals[iii].birth(animbaby)
            self.animals[iii].tilePurpose = self.animals[iii].tileFrom
            self.animals[iii].tileTo = self.animals[iii].tileFrom
            self.animals[iii].courseNext = self.animals[iii].courseLast
            return self.animals[iii].statusUpdate(statusAnim["SLEEP"])
        return -1

    def walkToEat(self, game, iii, indexA):
        df = 100
        db = 100
        if len(game.view.nearFood) != 0:
            df = abs(game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]) \
                 + abs(game.view.nearFood[0][1] - self.animals[iii].tileFrom[1])
        if indexA >= 0:
            db = self.distance(indexA, iii)
        if (df < 100) or (db < 100):
            if df < db:
                poX = game.view.nearFood[0][0] - self.animals[iii].tileFrom[0]
                poY = game.view.nearFood[0][1] - self.animals[iii].tileFrom[1]
                self.lookWay(game, iii, [poX, poY])
            else:
                poX, poY = self.positionsXY(indexA, iii)
                self.lookWay(game, iii, [poX, poY])
            shadAnim = AnimalObject(self.animals[iii].index)
            posTo = self.animals[iii].tileTo
            posFrom = self.animals[iii].tileFrom
            if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
                shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
            self.animals[iii].tilePurpose = self.animals[iii].tileTo
            return statusAnim["WALK"]
        return -1

    def lowEnergySleep(self, iii):
        self.animals[iii].tileTo = self.animals[iii].tileFrom
        self.animals[iii].courseNext = self.animals[iii].courseLast
        return self.animals[iii].statusUpdate(statusAnim["SLEEP"])

    def walkToCoordinate(self, game, iii, coord):
        poX = coord[0] - self.animals[iii].tileFrom[0]
        poY = coord[1] - self.animals[iii].tileFrom[1]
        self.lookWay(game, iii, [poX, poY])
        self.animals[iii].tilePurpose = coord
        shadAnim = AnimalObject(self.animals[iii].index)
        posTo = self.animals[iii].tileTo
        posFrom = self.animals[iii].tileFrom
        if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
            shadAnim.placeAtMap(self.animals[iii].tileTo[0], self.animals[iii].tileTo[1], ind.mapNo)
            shadAnim.deleteAtMap(self.animals[iii].tileFrom[0], self.animals[iii].tileFrom[1], ind.mapNo)
        return statusAnim["WALK"]

    def randomWalk(self, game, iii):
        q = 0
        if len(game.view.nearClear) > 1:
            q = rnd.getRandomInt(len(game.view.nearClear) - 1)  # WALK
        return self.walkToCoordinate(game, iii, game.view.nearClear[q])

    # Функция выбора цели для существа
    def choosePurpose(self, game, iii):  # i - индекс существа в массиве
        # Если противник совсем рядом, атакуем или поворачиваемся для атаки
        j = self.attacked(game, self.animals[iii])  # DEFENSE and ATTACK
        if j >= 0:
            result = self.defenceAgainstEnemy(game, iii, j)
            if result != -1:
                return result

        # Проверяем голод и едим еду что совсем рядом с агентом
        if self.animals[iii].hungry():  # EAT
            if len(game.view.nearFood) != 0:
                result = self.eatPlant(game, iii)
                if result != -1:
                    return result
            j = self.eat(game)
            if j >= 0:
                result = self.eatAgent(game, iii, j)
                if result != -1:
                    return result

        # Двигаемся ближе к врагу
        j = self.attacked(game, self.animals[iii])  # WALK->ATTACK
        if self.animals[iii].attackEnergy() and (j >= 0):
            result = self.moveToTheAgent(game, iii, j)
            return result

        # Размножаемся или движемся к размножению
        j = self.spawn(game, self.animals[iii])  # SPAWN and WALK->SPAWN
        if self.animals[iii].spawnEnergy() and (j >= 0):
            result = self.walkAndSpawn(game, iii, j)
            if result == -1:
                result = self.moveToTheAgent(game, iii, j)
            return result

        # Движение к ближайшему источнику пищи
        if self.animals[iii].hungry():  # WALK->EAT
            j = self.eat(game)
            result = self.walkToEat(game, iii, j)
            if result != -1:
                return result

        # Если недостаточно энергии или некуда идти - спим
        if self.animals[iii].fewEnergy() or (len(game.view.nearClear) == 0):  # SLEEP
            result = self.lowEnergySleep(iii)
            return result

        # Случайно бродим
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
        if len(game.view.nearClear) != 0:
            result = self.randomWalk(game, iii)
            return result
        return statusAnim["SLEEP"]

    # Возвращаем координаты точки чтобы, убежать от существа iii
    def runAwayRoad(self, game, iii):
        index = [-1, -1]
        dist = 0
        # Ищем свободную точку дальшую от существа от которого убегаем
        for i1 in game.view.nearClear:
            df = abs(i1[0] - self.animals[iii].tileFrom[0]) \
                 + abs(i1[1] - self.animals[iii].tileFrom[1])
            if df > dist:
                dist = df
                index = i1
        return index

    # Выбор между: бродить или спать.
    def chooseSleep(self, game, iii):
        aa0 = len(game.view.nearClear) == 0
        rand1 = round(rand.random.uniform(0, 1), 2)
        maxE = self.animals[iii].maxEnergy
        curE = self.animals[iii].energy
        chance = curE / (maxE * 0.9)
        if rand1 >= chance or aa0:
            return True
        else:
            return False

    # Выбираем между: продолжать или убегать
    def chooseEscape(self, iii):
        rand1 = round(rand.random.uniform(0, 0.5), 2)
        maxE = self.animals[iii].maxEnergy
        curE = self.animals[iii].energy
        chance = curE / maxE
        if rand1 < chance:
            return False
        else:
            return True

    def createWeightListAgent(self, iii):
        anim = self.animals[iii]
        WeightList = {"Eat": anim.eatWeight,
                      "Interact": anim.interactionWeight,
                      "Spawn": anim.birthWeight
                      }
        WeightList_by_goals = sorted(WeightList.items(), key=lambda x: x[1], reverse=True)
        converted_dict = dict(WeightList_by_goals)
        return converted_dict

    def createWeightListEco(self, iii, ecoT):
        list1 = self.hiveWeights[ecoT][iii]
        WeightList = {"Eat": list1[0],
                      "Interact": list1[1],
                      "Spawn": list1[2]
                      }
        WeightList_by_goals = sorted(WeightList.items(), key=lambda x: x[1], reverse=True)
        converted_dict = dict(WeightList_by_goals)
        return converted_dict

    def chooseCoevolutionPurpose(self, game, iii, weightList):
        # Если Агента атаковали
        if self.animals[iii].gotDamaged:
            j = self.attacked(game, self.animals[iii])  # DEFENSE and ATTACK
            if j >= 0:
                result = self.defenceAgainstEnemy(game, iii, j)
                if result != -1:
                    return result
        # Проходимся по списку функций: Поесть, Размножение, Взаимодействие с другим агентом другого вида.
        keylist = weightList.keys()
        for i1 in keylist:
            res = functionDictionary[i1](self, game, iii)
        # Если рядом ничего нет, выбираем в какую сторону идти или идти в случайное место или стоять на месте
        random_choosing = self.RandomChoosingOfTarget(game, iii, weightList)
        return random_choosing

    # Функция выбора куда идет существо
    def RandomChoosingOfTarget(self, game, indexA, listOfOptions):
        # Получаем на вход список весов
        a1 = listOfOptions["Spawn"]
        a2 = a1 + listOfOptions["Eat"]
        a3 = a2 + listOfOptions["Interact"]
        anim = self.animals[indexA]
        while True:
            randValue = round(rand.random.uniform(0.0, 1.0), 2)
            # Поиск партнера
            if (randValue <= a1) and anim.spawnEnergy():
                partner = findPossiblePartner(game, anim)
                if partner != -1:
                    result = self.moveToTheAgent(game, indexA, partner)
                    return result
            else:
                # Поиск пищи
                if (randValue <= a2) and anim.hungry():
                    j = self.eat(game)
                    result = self.walkToEat(game, indexA, j)
                    if result != -1:
                        return result
                else:
                    # Взаимодействие с другими видами
                    if randValue <= a3 and (anim.liveTime > anim.tYang):
                        j = self.notSameAdult(game, indexA)
                        if j != -1:
                            # Убегаем или движемся к ним
                            relation = self.relationship[anim.ecoT][anim.species][self.animals[j].species]
                            randValueRelation = round(rand.random.uniform(0.0, 1.0), 2)
                            # Позитивно и можно спариваться
                            if randValueRelation <= relation and anim.spawnEnergy():
                                result = self.moveToTheAgent(game, indexA, j)
                                return result
                            else:
                                # Убегаем или движемся к противнику
                                if self.chooseEscape(indexA):
                                    if len(game.view.nearClear) != 0:
                                        run_away = self.runAwayRoad(game, j)
                                        result = self.walkToCoordinate(game, indexA, run_away)
                                        return result
                                    else:
                                        result = self.lowEnergySleep(indexA)
                                        return result
                                else:
                                    result = self.moveToTheAgent(game, indexA, j)
                                    return result
                    else:
                        # Выбираем между случайным движением или сном
                        if self.chooseSleep(game, indexA):
                            result = self.lowEnergySleep(indexA)
                            return result
                        else:
                            poX = self.animals[indexA].tilePurpose[0] - self.animals[indexA].tileFrom[0]
                            poY = self.animals[indexA].tilePurpose[1] - self.animals[indexA].tileFrom[1]
                            flag = self.lookWay(game, indexA, [poX, poY])  # WALK
                            flag2 = pov.statReturn([self.animals[indexA].tilePurpose[0],
                                                    self.animals[indexA].tilePurpose[1]],
                                                   self.animals[indexA].ecoT, self)
                            if flag and (flag2 == statusCell["CLEAR"]):
                                shadAnim = AnimalObject(self.animals[indexA].index)
                                posTo = self.animals[indexA].tileTo
                                posFrom = self.animals[indexA].tileFrom
                                if (posTo[0] != posFrom[0]) or (posTo[1] != posFrom[1]):
                                    shadAnim.placeAtMap(self.animals[indexA].tileTo[0],
                                                        self.animals[indexA].tileTo[1],
                                                        ind.mapNo)
                                    shadAnim.deleteAtMap(self.animals[indexA].tileFrom[0],
                                                         self.animals[indexA].tileFrom[1],
                                                         ind.mapNo)
                                return statusAnim["WALK"]
                            if len(game.view.nearClear) != 0:
                                result = self.randomWalk(game, indexA)
                                return result
                            return statusAnim["SLEEP"]
