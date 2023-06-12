import math
import pygame
import random_new as rand
import indexes as ind
import maps
from constants import *
import sprite_sheet as spsh
import copy


def changColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
    return finalImage


def sprite_update(image, param):
    sprite_s = spsh.SpriteSheet(image)
    new_image = sprite_s.get_image(param["x"], param["y"], param["w"], param["h"], 1, black)
    return new_image


class Animal(pygame.sprite.Sprite):
    def __init__(self, game):
        # Уникальные параметры
        self.index = copy.deepcopy(ind.animalInd)
        self.color = copy.deepcopy([ind.chosenColor[0], ind.chosenColor[1], ind.chosenColor[2]])
        self.status = statusAnim["SLEEP"]
        self.ecoT = ecoType["Land"]
        self.species = 0
        self.gotDamaged = False

        # Веса агента
        self.birthWeight = 0.0
        self.walkWeight = 0.0
        self.eatWeight = 0.0
        self.interactionWeight = 0.0

        # Спрайты
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.sprites_list = game.spritelist[self.ecoT]

        # Позиция на карте
        self.tileFrom = [1, 1]
        self.tileTo = [1, 1]
        self.tilePurpose = [1, 1]
        self.courseLast = 0
        self.courseNext = 0

        # Время жизни
        self.liveTime = live_age
        self.tYang = yang_age
        self.told = old_age  # изменяется мутацией
        self.deathTime = death_age
        self.tZero = zero_age

        # Энергия
        self.startEnergy = 200  # изменяется мутацией
        self.energy = 200
        self.maxEnergy = 200
        self.stepEnergy = 12
        self.moveEnergy = 5
        self.sleepEnergy = 1

        # Еда
        self.piece = 50
        self.food = 800

        # Энергия поведения
        self.pAttackEnergy = pAttackEnergy
        self.pSpawnEnergy = pSpawnEnergy

        # Анимация
        self.timeMoved = 0
        self.delayMove = 150

        # Нужно изменить, связано с рисованием спрайта
        self.dimensions = [40, 40]
        self.position = [40, 40]
        self.spriteDirect = animalSprite["down"]

        self.sprites = anspritesparam
        self.image = sprite_update(self.sprites_list, self.sprites[self.spriteDirect])
        color_image = changColor(self.image, self.color)
        self.image = color_image
        self.rect = self.image.get_rect()

    def typeOfSpecies(self):
        index = 0
        for i1 in range(3):
            if self.color[i1] > 127:
                index += 2 ^ i1
        self.species = index

    def randomWeights(self):
        rndw1 = round(rand.random.uniform(0.2, 0.3), 2)
        rndw2 = round(rand.random.uniform(0.2, 0.3), 2)
        rndw3 = round(rand.random.uniform(0.2, 0.3), 2)
        rndw4 = round((1 - rndw1 - rndw2 - rndw3), 2)
        self.birthWeight = rndw1
        self.walkWeight = rndw2
        self.eatWeight = rndw3
        self.interactionWeight = rndw4

    def update(self):
        self.image = sprite_update(self.sprites_list, self.sprites[self.spriteDirect])
        color_image = changColor(self.image, self.color)
        self.image = color_image
        self.rect = self.image.get_rect()
        self.rect.x = self.tileTo[0] * ind.tileW
        self.rect.y = self.tileTo[1] * ind.tileH

    # Ставим агента в заданную точку
    def placeAt(self, x, y):
        self.tileFrom = copy.deepcopy([x, y])
        self.tileTo = copy.deepcopy([x, y])
        self.tilePurpose = copy.deepcopy([x, y])
        self.position = copy.deepcopy([((ind.tileW * x) + ((ind.tileW - self.dimensions[0]) / 2)),
                                       ((ind.tileH * y) + ((ind.tileH - self.dimensions[1]) / 2))
                                       ])

    def ecoAddType(self, c, game):
        self.ecoT = copy.deepcopy(c)
        self.sprites_list = game.spritelist[self.ecoT]

    # Задаем определенный цвет
    def colorAnim(self, col):
        self.color = copy.deepcopy(col)

    # Создание нового агента на основе двух родителей
    def Born(self, anim1, anim2, x, y):
        self.tileFrom = [x, y]
        self.tileTo = [x, y]
        self.tilePurpose = [x, y]
        self.position = [((ind.tileW * x) + ((ind.tileW - self.dimensions[0]) / 2)),
                         ((ind.tileH * y) + ((ind.tileH - self.dimensions[1]) / 2))
                         ]
        self.courseLast = 0
        self.courseNext = 0
        maxRandom = -100
        # Мутация цвета
        for i in range(3):
            random = (rand.getRandomInt(20) - 10)
            self.color[i] = copy.deepcopy(math.floor((anim1.color[i] + anim2.color[i]) / 2) + random)
            if self.color[i] > 255:
                self.color[i] = 255
            if self.color[i] < 0:
                self.color[i] = 0
        # Мутация максимального возраста и начальной энергии
        for i in range(1):
            random1 = rand.getRandomInt(5) - 2
            random2 = rand.getRandomInt(5) - 2
            if maxRandom < (random1 + random2):
                maxRandom = random1 + random2
                self.told = copy.deepcopy(math.floor((anim1.told + anim2.told + 1) / 2) + random1)
                self.startEnergy = copy.deepcopy(math.floor((anim1.startEnergy + anim2.startEnergy + 1) / 2) + random2)

        # Мутация весов
        # Веса агента
        self.birthWeight = round((anim1.birthWeight+anim2.birthWeight)/2, 3)
        self.walkWeight = round((anim1.walkWeight+anim2.walkWeight)/2, 3)
        self.eatWeight = round((anim1.eatWeight+anim2.eatWeight)/2, 3)
        self.interactionWeight = round((anim1.interactionWeight + anim2.interactionWeight) / 2, 3)

        self.energy = copy.deepcopy(self.startEnergy)
        self.maxEnergy = copy.deepcopy(self.startEnergy)

        self.stepEnergy = 12
        self.moveEnergy = 5
        self.sleepEnergy = 1

        self.pAttackEnergy = pAttackEnergy
        self.pSpawnEnergy = pSpawnEnergy
        self.piece = piece
        self.food = food

        self.timeMoved = 0
        self.delayMove = 150
        self.spriteDirect = animalSprite["down"]

        self.sprites = anspritesparam

        self.index = ind.animalInd
        self.ecoT = anim1.ecoT

        self.image = sprite_update(self.sprites_list, self.sprites[self.spriteDirect])
        color_image = changColor(self.image, self.color)
        self.image = color_image
        self.rect = self.image.get_rect()

    # Неудачное рождение агента
    def abortion(self):
        self.energy = copy.deepcopy(self.energy - self.startEnergy)

    # Затрата энергии на рождение нового агента
    def birth(self, anim):
        self.energy = copy.deepcopy(self.energy - anim.startEnergy)

    # Агента атаковали. Урон случайный.
    def attacked(self):
        self.spriteDirect = copy.deepcopy(8 + self.courseNext)
        randDamage = rand.random.randint(-25, 25)
        self.energy -= (self.piece + randDamage)

    # От тела агента откусили кусок
    def eat(self):
        self.food -= self.piece
        if self.food <= 0:
            self.status = statusAnim["ZERO"]
            self.deathTime = copy.deepcopy(self.tZero)

    # Возвращает куда, собирается направляться агент
    def pos(self):
        return self.tileTo

    # Проверка является ли этот агент врагом
    def enemy(self, anim1):
        q = 0
        for i in range(3):
            q += abs(self.color[i] - anim1.color[i])
        return q >= 355

    # Проверка можно ли спариваться с существом
    def canBreed(self, anim1):
        q = 0
        for i in range(3):
            q += abs(self.color[i] - anim1.color[i])
        return q >= 355

    # Проверка принадлежит ли агент тому же виду
    def sameSpecies(self, anim1):
        return self.species == anim1.species

    # Проверка, что у агента определенный индекс
    def eqI(self, i):
        return self.index == i

    # Проверка, что выбранная точка равна точки куда направляется агент
    def eq(self, a):
        return a.eq(self.tileTo)

    # Возвращает предыдущую цель
    def myCourse(self):
        return self.courseLast

    # Обновляем статус агента
    def statusUpdate(self, stat):
        self.status = copy.deepcopy(stat)
        if stat == ind.statusAnim["EAT"]:
            self.spriteDirect = copy.deepcopy(4 + self.courseNext)
            # Cколько энергии существо получает от поедания еды
            self.energy += energy_eat
        return stat

    # Обновляем параметры времени агента
    def timeUpdate(self):
        self.liveTime += 1
        if (self.status == statusAnim["SLEEP"]) or (self.status == statusAnim["EAT"]):
            self.energy = copy.deepcopy(self.energy - self.sleepEnergy)
        else:
            if (self.status == statusAnim["ATTACK"]) or (self.status == statusAnim["WALK"]):
                self.energy = copy.deepcopy(self.energy - self.moveEnergy)
        if self.energy <= 0:
            self.status = statusAnim["DEATH"]
            self.spriteDirect = animalSprite["dead"]
            self.deathTime += 1
            if self.deathTime >= self.tZero:
                return False
            return True
        if self.liveTime <= self.tYang:
            self.maxEnergy = copy.deepcopy(self.maxEnergy + self.stepEnergy)
        if self.liveTime > self.told:
            self.moveEnergy += 1
            self.sleepEnergy += 1
        return True

    # Проверка голода
    def hungry(self):
        return (self.maxEnergy - self.energy) >= 50

    # Проверка много ли энергии
    def fewEnergy(self):
        return self.energy < 50

    # Проверка можно ли атаковать
    def attackEnergy(self):
        ae = self.energy / self.maxEnergy
        return (self.liveTime > self.tYang) and (ae > self.pAttackEnergy)

    # Проверка можно ли произвести потомство
    def spawnEnergy(self):
        se = self.energy / self.maxEnergy
        return (self.liveTime > self.tYang) and (se > self.pSpawnEnergy)


class AnimalObject:
    def __init__(self, inds):
        self.x = 0
        self.y = 0
        self.index = inds

    def placeAtMap(self, nx, ny, mapN):
        if maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].animal == self:
            maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].animal = None
        self.x = copy.deepcopy(nx)
        self.y = copy.deepcopy(ny)
        tmp = copy.deepcopy(ind.mapNo)
        ind.mapNo = copy.deepcopy(mapN)
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].animal = self
        ind.mapNo = tmp

    def deleteAtMap(self, nx, ny, mapN):
        tmp = copy.deepcopy(ind.mapNo)
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].animal = None
        ind.mapNo = tmp
