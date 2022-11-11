import maps
import indexes as ind
import pygame
from constants import *
import sprite_sheet as spsh

objectCollision = {
    "none": 0,
    "solid": 1,
    "moveable": 2
}

objectTypes = {
    0: {
        # Камень
        "sprite": [{
            "x": 0, "y": 0, "w": 40, "h": 40
        }],
        "offset": [0, 0],
        "collision": objectCollision["solid"],
        "zIndex": 1
    }
}


def sprite_update(image, param):
    sprite_s = spsh.SpriteSheet(image)
    new_image = sprite_s.get_image(param["x"], param["y"], param["w"], param["h"], 1, black)
    return new_image


class MapObject:
    def __init__(self, a):
        self.x = 0
        self.y = 0
        self.type = a
        self.index = ind.objectInd

    def placeAt(self, nx, ny, mapN):
        if maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].object == self:
            maps.mapTileData[mapN].map[maps.toIndex(self.x, self.y)].object = None
        self.x = nx
        self.y = ny
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].object = self
        ind.mapNo = tmp

    def deleteAtMap(self, nx, ny, mapN):
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[maps.toIndex(nx, ny)].object = None
        ind.mapNo = tmp


class ObjectInfo(pygame.sprite.Sprite):
    def __init__(self, game, a):
        self.x = 0
        self.y = 0
        self.type = a
        self.index = ind.objectInd
        self.sprites = {
            objectStatus["rock"]: {
                'x': 0,
                'y': 0,
                'w': 40,
                'h': 40
            }
        }

        # Спрайты

        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.sprites_list = game.spritelist["rock"]
        self.image = sprite_update(self.sprites_list, self.sprites[self.type])

    def placeAt(self, nx, ny):
        self.x = nx
        self.y = ny

    def update(self):
        self.image = sprite_update(self.sprites_list, self.sprites[self.type])
        self.rect = self.image.get_rect()
        self.rect.x = self.x * ind.tileW
        self.rect.y = self.y * ind.tileH
