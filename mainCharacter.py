import pygame

import maps
import indexes as ind
from constants import *
from objects import *


class Character(pygame.sprite.Sprite):
    def __init__(self, game):
        self.tileFrom = [1, 1]
        self.tileTo = [1, 1]
        self.timeMoved = 0
        self.dimensions = [40, 40]
        self.position = [40, 40]
        self.delayMove = 150
        self.direction = directions["down"]
        self.groups = game.mch_sprite

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((ind.tileW, ind.tileH))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

        self.sprites = {
            directions["down"]: [{
                'x': 0,
                'y': 0,
                'w': 40,
                'h': 40
            }], directions["up"]: [{
                'x': 0,
                'y': 40,
                'w': 40,
                'h': 40
            }], directions["left"]: [{
                'x': 40,
                'y': 40,
                'w': 40,
                'h': 40
            }], directions["right"]: [{
                'x': 40,
                'y': 0,
                'w': 40,
                'h': 40
            }]}

    def placeAt(self, x, y):
        self.tileFrom = [x, y]
        self.tileTo = [x, y]
        self.x = x
        self.y = y
        self.position = [((ind.tileW * x) + ((ind.tileW - self.dimensions[0]) / 2)),
                         ((ind.tileH * y) + ((ind.tileH - self.dimensions[1]) / 2))
                         ]

    def update(self):
        self.rect.x = self.x * ind.tileW
        self.rect.y = self.y * ind.tileH

    def processMovement(self, t):
        if self.tileFrom[0] == self.tileTo[0] & self.tileFrom[1] == self.tileTo[1]:
            return False
        if (t - self.timeMoved) >= self.delayMove:
            self.placeAt(self.tileTo[0], self.tileTo[1])
            if maps.mapTileData[ind.mapNo].map[maps.toIndex(self.tileTo[0], self.tileTo[1])].eventEnter is not None:
                maps.mapTileData[ind.mapNo].map[maps.toIndex(self.tileTo[0], self.tileTo[1])].eventEnter(self)
            tileFloor = tileTypes[maps.mapTileData[ind.mapNo].map[maps.toIndex(self.tileFrom[0], self.tileFrom[1])].type]["floor"]
            if tileFloor == floorTypes.ice:
                if self.canMoveDirection(self.direction):
                    self.moveDirection(self.direction, t)
            else:
                self.position[0] = (self.tileFrom[0] * ind.tileW) + ((ind.tileW - self.dimensions[0]) / 2)
                self.position[1] = (self.tileFrom[1] * ind.tileH) + ((ind.tileH - self.dimensions[1]) / 2)
            if self.tileTo[0] != self.tileFrom[0]:
                diff = (ind.tileW / self.delayMove) * (t - self.timeMoved)
                if self.tileTo[0] < self.tileFrom[0]:
                    self.position[0] += 0 - diff
                else:
                    self.position[0] += diff
            if self.tileTo[1] != self.tileFrom[1]:
                diff = (ind.tileH / self.delayMove) * (t - self.timeMoved)
                if self.tileTo[1] < self.tileFrom[1]:
                    self.position[1] += 0 - diff
                else:
                    self.position[1] += diff
            self.position[0] = round(self.position[0])
            self.position[1] = round(self.position[1])
        return True

    def canMoveTo(self, x, y):
        if x < 0 | x >= maps.mapW[ind.mapNo] | y < 0 | y >= maps.mapH[ind.mapNo]:
            return False
        if (tileTypes[maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].type]["floor"] != floorTypes["path"] &
                tileTypes[maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].type]["floor"] != floorTypes["ice"] &
                tileTypes[maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].type]["floor"] != floorTypes["sand"]):
            return False
        if maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].object is not None:
            o = maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].object
            if objectTypes[o.type].collision == objectCollision.solid:
                return False
        if maps.mapTileData[ind.mapNo].map[maps.toIndex(x, y)].plant is not None:
            return False
        return True

    def canMoveLeft(self):
        return self.canMoveTo(self.tileFrom[0] - 1, self.tileFrom[1])

    def canMoveRight(self):
        return self.canMoveTo(self.tileFrom[0] + 1, self.tileFrom[1])

    def canMoveDown(self):
        return self.canMoveTo(self.tileFrom[0], self.tileFrom[1] + 1)

    def canMoveUp(self):
        return self.canMoveTo(self.tileFrom[0], self.tileFrom[1] - 1)

    def canMoveDirection(self, d):
        if d == directions.up:
            return self.canMoveUp()
        if d == directions.down:
            return self.canMoveDown()
        if d == directions.left:
            return self.canMoveLeft()
        if d == directions.right:
            return self.canMoveRight()

    def MoveLeft(self, t):
        self.tileTo[0] -= 1
        self.x -= 1
        self.timeMoved = t
        self.direction = directions.left

    def MoveRight(self, t):
        self.tileTo[0] += 1
        self.x += 1
        self.timeMoved = t
        self.direction = directions.right

    def MoveDown(self, t):
        self.tileTo[1] += 1
        self.y += 1
        self.timeMoved = t
        self.direction = directions.down

    def MoveUp(self, t):
        self.tileTo[1] -= 1
        self.y -= 1
        self.timeMoved = t
        self.direction = directions.up

    def moveDirection(self, d, t):
        if d == directions.up:
            return self.MoveUp(t)
        if d == directions.down:
            return self.MoveDown(t)
        if d == directions.left:
            return self.MoveLeft(t)
        if d == directions.right:
            return self.MoveRight(t)
