import pygame

import indexes as ind
from maps import *
from constants import *


class Cursor(pygame.sprite.Sprite):
    def __init__(self, game):

        self.groups = game.curs_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = game.spritelist["cur"]
        self.rect = self.image.get_rect()

        self.tileFrom = [1, 1]
        self.tileTo = [1, 1]
        self.x = 1
        self.y = 1
        self.rect.x = 1 * ind.tileW
        self.rect.y = 1 * ind.tileH

    # def __init__(self):
    #     self.tileFrom = [1, 1]
    #     self.tileTo = [1, 1]
    #     # this.position = [41, 30]
    #     self.sprite = [{
    #         "x": 0,
    #         "y": 0,
    #         "w": 40,
    #         "h": 40
    #     }]

    def placeAt(self, x, y):
        self.tileFrom = [x, y]
        self.tileTo = [x, y]
        self.x = x
        self.y = y
        self.rect.x = 1 * ind.tileW
        self.rect.y = 1 * ind.tileH


    def canMoveTo(self, x, y):
        if (x < 0) | (x >= mapW[ind.mapNo]) | (y < 0) | (y >= mapH[ind.mapNo]):
            return False
        else:
            return True

    def MoveLeft(self):
        self.tileTo[0] -= 1
        self.tileFrom[0] -= 1
        self.x -= 1

    def MoveRight(self):
        self.tileTo[0] += 1
        self.tileFrom[0] += 1
        self.x += 1

    def MoveDown(self):
        self.tileTo[1] += 1
        self.tileFrom[1] += 1
        self.y += 1

    def MoveUp(self):
        self.tileTo[1] -= 1
        self.tileFrom[1] -= 1
        self.y -= 1

    def canMoveLeft(self):
        return self.canMoveTo(self.tileFrom[0] - 1, self.tileFrom[1])

    def canMoveRight(self):
        return self.canMoveTo(self.tileFrom[0] + 1, self.tileFrom[1])

    def canMoveDown(self):
        return self.canMoveTo(self.tileFrom[0], self.tileFrom[1] + 1)

    def canMoveUp(self):
        return self.canMoveTo(self.tileFrom[0], self.tileFrom[1] - 1)

    def update(self):
        self.rect.x = self.x * ind.tileW
        self.rect.y = self.y * ind.tileH
