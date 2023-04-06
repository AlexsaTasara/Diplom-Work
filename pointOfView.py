from constants import *
from maps import *
import indexes as ind


trans = [
    [0, 1], [-1, 0], [0, -1], [1, 0],
    [0, 2], [-2, 0], [0, -2], [2, 0],
    [-1, 1], [-1, -1], [1, -1], [1, 1],
    [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1], [2, 1], [1, 2],
    [-2, 2], [-2, -2], [2, -2], [2, 2]
]


# Работа со статусами
def statusAnd(a, b):
    if (a == statusCell["ROCK"]) | (b != statusCell["CLEAR"]):
        return statusCell["ROCK"]
    return a


def statusOr(a, b):
    if (a == statusCell["CLEAR"]) | (b == statusCell["CLEAR"]):
        return statusCell["CLEAR"]
    return statusCell["ROCK"]


# Возвращает статус клетки карты с заданными координатами.
def statReturn(a, b, eco):
    o1 = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].object
    o2 = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].plant
    o3 = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].animal
    o4 = mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].user
    flag_t = tileTypes[mapTileData[ind.mapNo].map[toIndex(a[0], a[1])].type]["floor"]
    if (o1 is not None) or (o4 is not None) or (flag_t == floorTypes["solid"]):
        return statusCell["ROCK"]
    if ((flag_t == floorTypes["water"]) and (b == ecoType["Land"])) \
            or ((flag_t == floorTypes["path"]) and (b == ecoType["Water"])):
        return statusCell["ROCK"]
    if o2 is not None:
        inds = o2.index
        coord = eco.plants[inds].status
        if coord != plantStatus["berry"]:
            return statusCell["ROCK"]
        else:
            return statusCell["FOOD"]
    if o3 is not None:
        return statusCell["ANIM"]
    return statusCell["CLEAR"]


class PointOfView:
    def __init__(self):
        # Поле видимости размером 5 на 5
        self.lookTile = [[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        # Заполняем их всех значением CLEAR
        self.nearAnim = []
        self.nearFood = []
        self.nearClear = []

    # Обновление поля видимости
    def updateLook(self, a, b, eco):
        for iii in range(4):
            t = trans[iii]
            p = [t[0] + a[0], t[1] + a[1]]
            if (p[0] < 0) or (p[1] < 0) or (p[0] > (mapW[ind.mapNo] - 1)) or (p[1] > (mapH[ind.mapNo] - 1)):
                self.lookTile[t[0] + 2][t[1] + 2] = statusCell["ROCK"]
                continue
            st1 = statReturn(p, b, eco)
            self.lookTile[t[0] + 2][t[1] + 2] = st1
        for iii in range(4, 8):
            t = trans[iii]
            p = [t[0] + a[0], t[1] + a[1]]
            if (p[0] < 0) or (p[1] < 0) or (p[0] > (mapW[ind.mapNo] - 1)) or (p[1] > (mapH[ind.mapNo] - 1)):
                self.lookTile[t[0] + 2][t[1] + 2] = statusCell["ROCK"]
                continue
            st1 = statReturn(p, b, eco)
            st2 = self.lookTile[trans[iii - 4][0] + 2][trans[iii - 4][1] + 2]
            self.lookTile[t[0] + 2][t[1] + 2] = statusAnd(st1, st2)
        q1 = 0
        q2 = 1
        for iii in range(8, 12):
            t = trans[iii]
            p = [t[0] + a[0], t[1] + a[1]]
            if (p[0] < 0) or (p[1] < 0) or (p[0] > (mapW[ind.mapNo] - 1)) or (p[1] > (mapH[ind.mapNo] - 1)):
                self.lookTile[t[0] + 2][t[1] + 2] = statusCell["ROCK"]
                continue
            st1 = statReturn(p, b, eco)
            if q2 == 4:
                q2 = 0
            st2 = self.lookTile[trans[q1][0] + 2][trans[q1][1] + 2]
            st3 = self.lookTile[trans[q2][0] + 2][trans[q2][1] + 2]
            self.lookTile[t[0] + 2][t[1] + 2] = statusAnd(st1, statusOr(st2, st3))
            q1 += 1
            q2 += 1
        q1 = 4
        q2 = 8
        d1 = 1
        d2 = 0
        for iii in range(12, 20):
            t = trans[iii]
            p = [t[0] + a[0], t[1] + a[1]]
            if (p[0] < 0) or (p[1] < 0) or (p[0] > (mapW[ind.mapNo] - 1)) or (p[1] > (mapH[ind.mapNo] - 1)):
                self.lookTile[t[0] + 2][t[1] + 2] = statusCell["ROCK"]
                continue
            st1 = statReturn(p, b, eco)
            if q1 == 8:
                q1 = 4
            st2 = self.lookTile[trans[q1][0] + 2][trans[q1][1] + 2]
            st3 = self.lookTile[trans[q2][0] + 2][trans[q2][1] + 2]
            self.lookTile[t[0] + 2][t[1] + 2] = statusAnd(st1, statusOr(st2, st3))
            q1 += d1
            q2 += d2
            d1 = 1 - d1
            d2 = 1 - d2
        q1 = 12
        q2 = 13
        q3 = 8
        for iii in range(20, 24):
            t = trans[iii]
            p = [t[0] + a[0], t[1] + a[1]]
            if (p[0] < 0) or (p[1] < 0) or (p[0] > (mapW[ind.mapNo] - 1)) or (p[1] > (mapH[ind.mapNo] - 1)):
                self.lookTile[t[0] + 2][t[1] + 2] = statusCell["ROCK"]
                continue
            st1 = statReturn(p, b, eco)
            st2 = self.lookTile[trans[q1][0] + 2][trans[q1][1] + 2]
            st3 = self.lookTile[trans[q2][0] + 2][trans[q2][1] + 2]
            st4 = self.lookTile[trans[q3][0] + 2][trans[q3][1] + 2]
            self.lookTile[t[0] + 2][t[1] + 2] = statusAnd(st1, statusAnd(st4, statusOr(st2, st3)))
            q1 += 2
            q2 += 2
            q3 += 1
        self.lookTile[2][2] = statusCell["ANIM"]

    # Обновление списка целей животного
    def updateLists(self, course, a, eco):
        self.nearFood.clear()
        self.nearClear.clear()
        self.nearAnim.clear()
        for n in range(5):
            lll = n * 4
            size = 4
            if n == 3:
                size = 8
            if n == 4:
                lll = 20
            j = lll + course
            r = lll + size
            k = +1
            for iii in range(0, size):
                if j < lll:
                    j = r - (lll - j)
                if j >= r:
                    j = lll + j - r
                p = trans[j]
                st = self.lookTile[p[0] + 2][p[1] + 2]
                if st == statusCell["FOOD"]:
                    p2 = [a[0] + p[0], a[1] + p[1]]
                    self.nearFood.append(p2)
                else:
                    if st == statusCell["CLEAR"]:
                        p2 = [a[0] + p[0], a[1] + p[1]]
                        self.nearClear.append(p2)
                    else:
                        if st == statusCell["ANIM"]:
                            p2 = [a[0] + p[0], a[1] + p[1]]
                            c2 = mapTileData[ind.mapNo].map[toIndex(p2[0], p2[1])].animal
                            q = c2.index
                            q2 = eco.animals[q].index
                            self.nearAnim.append(q2)
                j -= k * (iii+1)
                k = -k
