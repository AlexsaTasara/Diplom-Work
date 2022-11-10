import random
import maps
import pointOfView as pov

from maps import *
from constants import *


def getRandomInt(max_a):
    ans = random.randrange(max_a)
    return ans


def RandomPoint(mN, ect, eco):
    i1 = 0
    fl = True
    a1 = [0, 0]
    currnum = maps.mapH[ind.mapNo]*maps.mapW[ind.mapNo]
    while fl:
        x = getRandomInt(mapW[mN] - 2) + 1
        y = getRandomInt(mapH[mN] - 2) + 1
        a1 = [x, y]
        i1 += 1
        flagC = pov.statReturn(a1, ect, eco)
        flagT = tileTypes[mapTileData[ind.mapNo].map[toIndex(x, y)].type]["floor"]
        tr1 = (flagT == ind.floorTypes["path"]) & (ect == ind.ecoType["Land"])
        tr2 = (flagT == ind.floorTypes["water"]) & (ect == ind.ecoType["Water"])
        fl = ((not ((flagC == statusCell["CLEAR"]) & (tr1 | tr2))) & (i1 < currnum))
    if i1 < currnum:
        return a1
    return [0, 0]
