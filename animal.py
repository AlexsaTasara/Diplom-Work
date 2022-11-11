import math
import pygame
import random_new as rand
import indexes as ind
import maps
from constants import *
import sprite_sheet as spsh


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
        self.index = ind.animalInd
        self.color = [ind.chosenColor[0], ind.chosenColor[1], ind.chosenColor[2]]
        self.status = statusAnim["SLEEP"]
        self.ecoT = ecoType["Land"]

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
        self.food = 100

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

    # def sp_upd(self, game):
    #     self.sprites_list = game.spritelist[self.ecoT]
    #     self.image = sprite_update(self.sprites_list, self.sprites[self.spriteDirect])
    #     color_image = changColor(self.image, self.color)
    #     self.image = color_image
    #     self.rect = self.image.get_rect()

    def update(self):
        self.image = sprite_update(self.sprites_list, self.sprites[self.spriteDirect])
        color_image = changColor(self.image, self.color)
        self.image = color_image
        self.rect = self.image.get_rect()
        self.rect.x = self.tileTo[0] * ind.tileW
        self.rect.y = self.tileTo[1] * ind.tileH

    # Ставим существо в заданную точку
    def placeAt(self, x, y):
        self.tileFrom = [x, y]
        self.tileTo = [x, y]
        self.tilePurpose = [x, y]
        self.position = [((ind.tileW * x) + ((ind.tileW - self.dimensions[0]) / 2)),
                         ((ind.tileH * y) + ((ind.tileH - self.dimensions[1]) / 2))
                         ]

    def ecoAddType(self, c, game):
        self.ecoT = c
        self.sprites_list = game.spritelist[self.ecoT]

    # Задаем определенный цвет
    def colorAnim(self, col):
        self.color = col

    # Создание нового существа на основе двух родителей
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
            self.color[i] = math.floor((anim1.color[i] + anim2.color[i]) / 2) + random
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
                self.told = math.floor((anim1.told + anim2.told + 1) / 2) + random1
                self.startEnergy = math.floor((anim1.startEnergy + anim2.startEnergy + 1) / 2) + random2

        self.energy = self.startEnergy
        self.maxEnergy = self.startEnergy

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
        # print("Рожден: ", self.index, ", Энергии: ", self.energy, ", ", self.maxEnergy, "Макс возраст: ", self.told)

    # Неудачное рождение особи
    def abortion(self):
        self.energy -= self.startEnergy

    # Затрата энергии на рождение новой особи
    def birth(self, anim):
        self.energy -= anim.startEnergy

    # Животное атаковали
    def attacked(self):
        self.spriteDirect = 8 + self.courseNext
        self.energy -= self.piece

    # От животного откусили кусок
    def eat(self):
        self.food -= self.piece
        if self.food <= 0:
            self.status = statusAnim["ZERO"]
            self.deathTime = self.tZero

    # Возвращает куда, собирается направляться животное
    def pos(self):
        return self.tileTo

    # Проверка является ли это животное врагом
    def enemy(self, anim1):
        q = 0
        for i in range(3):
            q += abs(self.color[i] - anim1.color[i])
        return q >= 355

    # Проверка, что у существа определенный индекс
    def eqI(self, i):
        return self.index == i

    # Проверка что выбранная точка равна точки куда направляется существо
    def eq(self, a):
        return a.eq(self.tileTo)

    # Возвращает предыдущую цель
    def myCourse(self):
        return self.courseLast

    # Обновляем статус животного
    def statusUpdate(self, stat):
        self.status = stat
        if stat == ind.statusAnim["EAT"]:
            self.spriteDirect = 4 + self.courseNext
            self.energy += 50
        return stat

    # Обновляем параметры времени животного (Проблем нет)
    def timeUpdate(self):
        self.liveTime += 1
        if (self.status == statusAnim["SLEEP"]) | (self.status == statusAnim["EAT"]):
            self.energy = (self.energy - self.sleepEnergy)
        else:
            if (self.status == statusAnim["ATTACK"]) | (self.status == statusAnim["WALK"]):
                self.energy = (self.energy - self.moveEnergy)
        if self.energy <= 0:
            self.status = statusAnim["DEATH"]
            self.spriteDirect = animalSprite["dead"]
            self.deathTime += 1
            if self.deathTime >= self.tZero:
                return False
            return True
        if self.liveTime <= self.tYang:
            self.maxEnergy = (self.maxEnergy + self.stepEnergy)
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

    # Проверка можно ли аткавать
    def attackEnergy(self):
        ae = self.energy / self.maxEnergy
        return (self.liveTime > self.tYang) & (ae > self.pAttackEnergy)

    # Проверка можно ли произвести потомство
    def spawnEnergy(self):
        se = self.energy / self.maxEnergy
        return (self.liveTime > self.tYang) & (se > self.pSpawnEnergy)


class AnimalObject:
    def __init__(self, inds):
        self.x = 0
        self.y = 0
        self.index = inds

    def placeAtMap(self, nx, ny, mapN):
        if maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].animal == self:
            maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].animal = None
        self.x = nx
        self.y = ny
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].animal = self
        ind.mapNo = tmp

    def deleteAtMap(self, nx, ny, mapN):
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].animal = None
        ind.mapNo = tmp
