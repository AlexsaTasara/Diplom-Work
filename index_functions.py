import indexes as ind
import maps
from constants import *
import random_new as rnd


def object_spawn_flag():
    if ind.objectSpawn:
        ind.objectSpawn = not ind.objectSpawn
    else:
        ind.animalSpawn = False
        ind.plantSpawn = False
        ind.objectSpawn = not ind.objectSpawn
        ind.info = False


def animal_spawn_flag():
    if ind.animalSpawn:
        ind.animalSpawn = not ind.animalSpawn
    else:
        ind.animalSpawn = not ind.animalSpawn
        ind.plantSpawn = False
        ind.objectSpawn = False
        ind.info = False


def plant_spawn_flag():
    if ind.plantSpawn:
        ind.plantSpawn = not ind.plantSpawn
    else:
        ind.animalSpawn = False
        ind.plantSpawn = not ind.plantSpawn
        ind.objectSpawn = False
        ind.info = False


def map_flag():
    ind.mapChange = not ind.mapChange
    ind.animalSpawn = False
    ind.plantSpawn = False
    ind.objectSpawn = False
    ind.info = False


def info_flag(game):
    if ind.info:
        ind.info = not ind.info
    else:
        ind.animalSpawn = False
        ind.plantSpawn = False
        ind.objectSpawn = False
        ind.info = not ind.info
        if len(game.eco.animals) == 0:
            ind.animInfo = -1


def confirm_function(game):
    xcur = game.curs.tileTo[0]
    ycur = game.curs.tileTo[1]
    flagO = maps.mapTileData[ind.mapNo].map[maps.toIndex(xcur, ycur)].object
    flagP = maps.mapTileData[ind.mapNo].map[maps.toIndex(xcur, ycur)].plant
    flagA = maps.mapTileData[ind.mapNo].map[maps.toIndex(xcur, ycur)].animal
    flagU = maps.mapTileData[ind.mapNo].map[maps.toIndex(xcur, ycur)].user
    flagT = tileTypes[maps.mapTileData[ind.mapNo].map[maps.toIndex(xcur, ycur)].type]["floor"]
    if ind.objectSpawn:
        if (flagA is None) and (flagP is None) and (flagU is None):
            if flagO is None:
                game.eco.addObject(game, xcur, ycur, 0)
            else:
                flagO.deleteAtMap(xcur, ycur, ind.mapNo)
                game.eco.delObject(flagO.index)
    if ind.animalSpawn:
        if (flagO is None) and (flagP is None) and (flagU is None) and (flagT != floorTypes["solid"]):
            if ((flagT != floorTypes["water"]) and (et_type[ind.et] == ecoType["Land"])) or (
                    (flagT != floorTypes["path"]) and (et_type[ind.et] == ecoType["Water"])):
                if flagA is None:
                    game.eco.addAnim(game, xcur, ycur, ind.chosenColor, et_type[ind.et])
                else:
                    flagA.deleteAtMap(xcur, ycur, ind.mapNo)
                    game.eco.delAnim(flagA.index)
    if ind.plantSpawn:
        if (flagO is None) and (flagU is None) and (flagA is None):
            if ((flagT == floorTypes["path"]) and (et_type[ind.et] == ecoType["Land"])) or (
                    (flagT == floorTypes["water"]) and (et_type[ind.et] == ecoType["Water"])):
                if flagP is None:
                    game.eco.addPlant(game, xcur, ycur, et_type[ind.et])
                else:
                    flagP.deleteAtMap(xcur, ycur, ind.mapNo)
                    game.eco.delPlant(flagP.index)
    if ind.info and flagA is not None:
        ind.animInfo = flagA.index
    else:
        ind.animInfo = -1


def put_plant(game, eco_type):
    point = rnd.RandomPoint(ind.mapNo, eco_type, game.eco)
    if (point[0] != 0) and (point[1] != 0):
        game.eco.addPlant(game, point[0], point[1], eco_type)
