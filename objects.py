import maps
import indexes as ind
objectCollision = {
    "none": 0,
    "solid": 1,
    "moveable": 2
}

objectTypes = {
    0: {
        #"sp": objectRock,
        "sprite": [{
            "x": 0, "y": 0, "w": 40, "h": 40
        }],
        "offset": [0, 0],
        "collision": objectCollision["solid"],
        "zIndex": 1
    }
}


class MapObject:
    def __init__(self, a):
        self.x = 0
        self.y = 0
        self.type = a

    def placeAt(self, nx, ny, mapN):
        if  maps.mapTileData[mapN].map[ maps.toIndex(self.x, self.y)].object == self:
            maps.mapTileData[mapN].map[ maps.toIndex(self.x, self.y)].object = None
        self.x = nx
        self.y = ny
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[ maps.toIndex(nx, ny)].object = self
        ind.mapNo = tmp

    def deleteAt(self, nx, ny, mapN):
        tmp = ind.mapNo
        ind.mapNo = mapN
        maps.mapTileData[mapN].map[ maps.toIndex(nx, ny)].object = None
        ind.mapNo = tmp
