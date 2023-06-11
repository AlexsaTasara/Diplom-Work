import pygame
import indexes as ind
import maps
from constants import *
import sprite_sheet as spsh


def sprite_update(image, param):
    sprite_s = spsh.SpriteSheet(image)
    new_image = sprite_s.get_image(param["x"], param["y"], param["w"], param["h"], 1, black)
    return new_image


class Plant(pygame.sprite.Sprite):
    def __init__(self, game):
        self.X = 0
        self.Y = 0
        self.index = ind.plantInd
        self.ecoT = ecoType["Land"]
        self.liveTime = 0
        self.deathTime = 40
        self.berryTime = 8
        self.told = 23

        # Спрайты
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.sprites_list = game.spritelist[plantType[self.ecoT]]

        # Еда
        self.piece = 50
        self.food = 150
        self.status = plantStatus["sprout"]

        self.sprites = {
            plantStatus["sprout"]: {
                'x': 0,
                'y': 0,
                'w': 40,
                'h': 40
            },
            plantStatus["berry"]: {
                'x': 40,
                'y': 0,
                'w': 40,
                'h': 40
            },
            plantStatus["wither"]: {
                'x': 80,
                'y': 0,
                'w': 40,
                'h': 40
            }}

        self.image = sprite_update(self.sprites_list, self.sprites[self.status])
        self.rect = self.image.get_rect()

    def placeAt(self, x, y):
        self.X = x
        self.Y = y

    def update(self):
        self.image = sprite_update(self.sprites_list, self.sprites[self.status])
        self.rect = self.image.get_rect()
        self.rect.x = self.X * ind.tileW
        self.rect.y = self.Y * ind.tileH

    def ecoAddType(self, c, game):
        self.ecoT = c
        self.sprites_list = game.spritelist[plantType[self.ecoT]]

    def eat(self):
        self.food -= self.piece
        if (self.food <= 0) and (self.liveTime < self.told):
            self.liveTime = self.told
        return self.food

    def timeUpdate(self):
        self.liveTime += 1
        return self.liveTime < self.deathTime

    def statusUpdate(self):
        if self.liveTime < self.berryTime:
            self.status = plantStatus["sprout"]
        else:
            if (self.liveTime < self.told) and (self.food > 0):
                self.status = plantStatus["berry"]
            else:
                if (self.food <= 0) or (self.liveTime < self.deathTime):
                    self.status = plantStatus["wither"]

    def eq(self, x, y):
        return (self.X == x) and (self.Y == y)

    def pos(self):
        return self.X, self.Y


# Объект хранящий индекс растения в массиве и его координаты на карте
class PlantObject:
    def __init__(self, indexes):
        self.x = 0
        self.y = 0
        self.index = indexes

    def placeAtMap(self, nx, ny, mapN):
        if maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].plant == self:
            maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].plant = None
        self.x = nx
        self.y = ny
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].plant = self
        ind.mapNo = tmp

    def deleteAtMap(self, nx, ny, mapN):
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].plant = None
        ind.mapNo = tmp
