from constants import *
import indexes as ind
import pickle


class GetAnimals:
    def __init__(self, anim):
        self.index = anim.index
        self.color = anim.color
        self.status = anim.status
        self.ecoT = anim.ecoT

        # Позиция на карте
        self.tileFrom = anim.tileFrom
        self.tileTo = anim.tileTo
        self.tilePurpose = anim.tilePurpose
        self.courseLast = anim.courseLast
        self.courseNext = anim.courseNext

        # Время жизни
        self.liveTime = anim.liveTime
        self.tYang = anim.tYang
        self.told = anim.told
        self.deathTime = anim.deathTime
        self.tZero = anim.tZero

        # Энергия
        self.startEnergy = anim.startEnergy
        self.energy = anim.energy
        self.maxEnergy = anim.maxEnergy
        self.stepEnergy = anim.stepEnergy
        self.moveEnergy = anim.moveEnergy
        self.sleepEnergy = anim.sleepEnergy

        # Еда
        self.piece = anim.piece
        self.food = anim.food

        # Энергия поведения
        self.pAttackEnergy = anim.pAttackEnergy
        self.pSpawnEnergy = anim.pSpawnEnergy

        # Анимация
        self.timeMoved = anim.timeMoved
        self.delayMove = anim.delayMove

        # Нужно изменить, связано с рисованием спрайта
        self.dimensions = anim.dimensions
        self.position = anim.position
        self.spriteDirect = anim.spriteDirect


class GetPlants:
    def __init__(self, plant):
        self.X = plant.X
        self.Y = plant.Y
        self.index = plant.index
        self.ecoT = plant.ecoT
        self.liveTime = plant.liveTime
        self.deathTime = plant.deathTime
        self.berryTime = plant.berryTime
        self.told = plant.told

        # Еда
        self.piece = plant.piece
        self.food = plant.food
        self.status = plant.status

        self.sprites = plant.sprites


class GetObjects:
    def __init__(self, obj):
        self.x = obj.x
        self.y = obj.y
        self.type = obj.type
        self.index = obj.index
        self.sprites = obj.sprites


class SavedData:
    def __init__(self, index, eco):
        # Игровая скорость
        self.gameTime = ind.gameTime
        self.currentSpeed = ind.currentSpeed
        self.pastSpeed = ind.pastSpeed
        self.timeEcosystem = ind.timeEcosystem  # Время экосистемы
        self.tTime = ind.tTime # Текущее время
        self.tak = ind.tak  # Текущий такт
        self.currentSecond = ind.currentSecond
        self.frameCount = ind.frameCount
        self.framesLastSecond = ind.framesLastSecond
        self.lastFrameTime = ind.lastFrameTime
        self.tileW = ind.tileW
        self.tileH = ind.tileH

        # Язык
        self.userLang = ind.userLang

        # Скорость появления еды
        self.tPlantL = ind.tPlantL
        self.tPlantW = ind.tPlantW
        self.PLT = ind.PLT
        self.PLW = ind.PLW

        # Индекс информации
        self.amInfInd = ind.amInfInd
        # Номер карты сейчас
        self.mapNo = ind.mapNo
        # Номер карты на который перейдет
        self.mapCh = ind.mapCh
        # Индекс существа
        self.animalInd = ind.animalInd
        # Индекс растения
        self.plantInd = ind.plantInd
        # Индекс предмета
        self.objectInd = ind.objectInd
        # Индекс экосистемы
        self.et = ind.et
        # Индекс цвета
        self.chosenColorInd = ind.chosenColorInd
        # Выбранный цвет
        self.chosenColor = ind.chosenColor
        # Предыдущая локация
        self.prewLoc = ind.prewLoc

        #
        self.ctx = ind.ctx

        # Какой режим включен
        self.mapChange = ind.mapChange
        self.clientSpawn = ind.clientSpawn
        self.objectSpawn = ind.objectSpawn
        self.animalSpawn = ind.animalSpawn
        self.plantSpawn = ind.plantSpawn
        self.heroVisible = ind.heroVisible
        self.info = ind.info
        self.animInfo = ind.animInfo

        self.animals = self.getAllAnim(eco.animals)
        self.plants = self.getAllPlants(eco.plants)
        self.objects = self.getAlObjects(eco.objects)

        self.index = index

    def updateData(self, llll):
        self.gameTime = llll.gameTime
        self.currentSpeed = llll.currentSpeed
        self.pastSpeed = llll.pastSpeed
        self.timeEcosystem = llll.timeEcosystem  # Время экосистемы
        self.tTime = llll.tTime  # Текущее время
        self.tak = llll.tak  # Текущий такт
        self.currentSecond = llll.currentSecond
        self.frameCount = llll.frameCount
        self.framesLastSecond = llll.framesLastSecond
        self.lastFrameTime = llll.lastFrameTime
        self.tileW = llll.tileW
        self.tileH = llll.tileH
        self.userLang = llll.userLang
        self.tPlantL = llll.tPlantL
        self.tPlantW = llll.tPlantW
        self.PLT = llll.PLT
        self.PLW = llll.PLW
        self.amInfInd = llll.amInfInd
        self.mapNo = llll.mapNo
        self.mapCh = llll.mapCh
        self.animalInd = llll.animalInd
        self.plantInd = llll.plantInd
        self.objectInd = llll.objectInd
        self.et = llll.et
        self.chosenColorInd = llll.chosenColorInd
        self.chosenColor = llll.chosenColor
        self.prewLoc = llll.prewLoc
        self.ctx = llll.ctx
        self.mapChange = llll.mapChange
        self.clientSpawn = llll.clientSpawn
        self.objectSpawn = llll.objectSpawn
        self.animalSpawn = llll.animalSpawn
        self.plantSpawn = llll.plantSpawn
        self.heroVisible = llll.heroVisible
        self.info = llll.info
        self.animInfo = llll.animInfo
        self.animals = llll.animals
        self.plants = llll.plants
        self.objects = llll.objects
        self.index = llll.index

    def loadBack(self):
        # Игровая скорость
        ind.gameTime = self.gameTime
        ind.currentSpeed = self.currentSpeed
        ind.pastSpeed = self.pastSpeed
        ind.timeEcosystem = self.timeEcosystem  # Время экосистемы
        ind.tTime = self.tTime  # Текущее время
        ind.tak = self.tak  # Текущий такт
        ind.currentSecond = self.currentSecond
        ind.frameCount = self.frameCount
        ind.framesLastSecond = self.framesLastSecond
        ind.lastFrameTime = self.lastFrameTime
        ind.tileW = self.tileW
        ind.tileH = self.tileH

        # Язык
        ind.userLang = self.userLang

        # Скорость появления еды
        ind.tPlantL = self.tPlantL
        ind.tPlantW = self.tPlantW
        ind.PLT = self.PLT
        ind.PLW = self.PLW

        # Индекс информации
        ind.amInfInd = self.amInfInd
        # Номер карты сейчас
        ind.mapNo = self.mapNo
        # Номер карты на который перейдет
        ind.mapCh = self.mapCh
        # Индекс существа
        ind.animalInd = self.animalInd
        # Индекс растения
        ind.plantInd = self.plantInd
        # Индекс предмета
        ind.objectInd = self.objectInd
        # Индекс экосистемы
        ind.et = self.et
        # Индекс цвета
        ind.chosenColorInd = self.chosenColorInd
        # Выбранный цвет
        ind.chosenColor = self.chosenColor
        # Предыдущая локация
        ind.prewLoc = self.prewLoc

        #
        ind.ctx = self.ctx

        # Какой режим включен
        ind.mapChange = self.mapChange
        ind.clientSpawn = self.clientSpawn
        ind.objectSpawn = self.objectSpawn
        ind.animalSpawn = self.animalSpawn
        ind.plantSpawn = self.plantSpawn
        ind.heroVisible = self.heroVisible
        ind.info = self.info
        ind.animInfo = self.animInfo
        return self.animals, self.plants, self.objectSpawn

    def getAllAnim(self, animals):
        anlist = []
        for an in animals:
            an1 = GetAnimals(animals[an])
            anlist.append(an1)
        return anlist

    def getAllPlants(self, plants):
        pllist = []
        for an in plants:
            an1 = GetPlants(plants[an])
            pllist.append(an1)
        return pllist

    def getAlObjects(self, objects):
        oblist = []
        for an in objects:
            an1 = GetObjects(objects[an])
            oblist.append(an1)
        return oblist


class SaveAndLoad:
    def __init__(self):
        self.files = {}

    def saveF(self, slot, eco):
        sd = SavedData(slot, eco)
        self.files[slot] = sd
        with open('savefiles/savefile' + str(slot) + '.dat', 'wb') as f:
            pickle.dump([sd], f, protocol=2)

    def loadF(self, slot, eco):
        sd = self.files[slot]
        with open('savefiles/savefile' + str(slot) + '.dat', 'rb') as f:
            listsd = pickle.load(f)
        if not (listsd is None):
            sd.updateData(listsd[0])
            return sd
        else:
            return "Пустое сохранение"

    def clearF(self, slot):
        self.files[slot].kill()
        with open('savefiles/savefile' + str(slot) + '.dat', 'wb') as f:
            pickle.dump([], f, protocol=2)

