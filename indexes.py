from constants import *
from strings import *

# ---------- Параметры что используются и меняются во время работы программы

# Игровая скорость
gameTime = 0
currentSpeed = 0
pastSpeed = 1
timeEcosystem = 1000  # Время экосистемы
tTime = 0  # Текущее время
tak = 0  # Текущий такт
currentSecond = 0
frameCount = 0
framesLastSecond = 0
lastFrameTime = 0
tileW = 32
tileH = 32

# Тип поведения агентов
typeOfBehavior = 0
# Выбор поведения агента
chooseBehavior = 0

# Язык
userLang = lang["RUS"]

# Скорость появления еды
tPlantL = 0
tPlantW = 0
PLT = 2
PLW = 2

# Индекс информации
amInfInd = 0
# Номер карты сейчас
mapNo = 0
# Номер карты на который перейдет
mapCh = 0
# Индекс существа
animalInd = 0
# Индекс растения
plantInd = 0
# Индекс предмета
objectInd = 0
# Индекс экосистемы
et = 0
# Индекс цвета
chosenColorInd = "RED"
# Выбранный цвет
chosenColor = animalColor[chosenColorInd]
# Предыдущая локация
prewLoc = [0, 0]

#
ctx = None


# Какой режим включен
cBehavior = True
mapChange = False
objectSpawn = False
animalSpawn = False
plantSpawn = False
heroVisible = False
info = False
animInfo = 0

# Нажатия клавиш
keysDown = {
    16: False,

    37: False,
    38: False,
    39: False,
    40: False,

    101: False,

    87: False,
    83: False,
    65: False,
    68: False,

    69: False,

    81: False,
    27: False,

    72: False,
    84: False
}
