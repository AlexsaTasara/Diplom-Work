# Окно
# screen_width = 1300
# screen_height = 868
FPS = 30
# Размеры клетки
# tileW = 32
# tileH = 32


# Цвета
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
pink = (255, 0, 255)
teal = (0, 255, 255)
white = (255, 255, 255)
light_green = (160, 255, 100)

# Шрифты
font1 = "fonts/EBENYA.ttf"
font2 = "fonts/Linerama.ttf"
font3 = "fonts/gwent_extrabold.ttf"
font4 = "fonts/BuyanThin.ttf"
font5 = "fonts/bezpredmetizm.ttf"
font6 = "fonts/Aerovista.ttf"

# Информация для животных
animalSprite = {
    "down": 0,
    "left": 1,
    "up": 2,
    "right": 3,
    "attack_down": 4,
    "attack_left": 5,
    "attack_up": 6,
    "attack_right": 7,
    "hurt_down": 8,
    "hurt_left": 9,
    "hurt_up": 10,
    "hurt_right": 11,
    "kid_down": 12,
    "kid_left": 13,
    "kid_up": 14,
    "kid_right": 15,
    "kid_attack_down": 16,
    "kid_attack_left": 17,
    "kid_attack_up": 18,
    "kid_attack_right": 19,
    "kid_hurt_down": 20,
    "kid_hurt_left": 21,
    "kid_hurt_up": 22,
    "kid_hurt_right": 23,
    "dead": 24
}
statusCell = {
    "CLEAR": 0,
    "ANIM": 1,
    "FOOD": 2,
    "ROCK": 3
}
statusAnim = {
    "DEATH": 0,
    "ATTACK": 1,
    "EAT": 2,
    "WALK": 3,
    "SLEEP": 4,
    "ZERO": 5
}
animalColor = {
    "RED": [255, 0, 0],
    "GREEN": [0, 255, 0],
    "BLUE": [0, 0, 255],
    "YELLOW": [255, 255, 0],
    "PINK": [255, 0, 255],
    "LIGHTBLUE": [0, 255, 255],
    "WHITE": [255, 255, 255]
}
anspritesparam = {
    animalSprite["down"]: {"x": 0, "y": 0, "w": 40, "h": 40},
    animalSprite["up"]: {"x": 40, "y": 0, "w": 40, "h": 40},
    animalSprite["right"]: {"x": 80, "y": 0, "w": 40, "h": 40},
    animalSprite["left"]: {"x": 120, "y": 0, "w": 40, "h": 40},
    animalSprite["hurt_down"]: {"x": 0, "y": 40, "w": 40, "h": 40},
    animalSprite["hurt_up"]: {"x": 40, "y": 40, "w": 40, "h": 40},
    animalSprite["hurt_right"]: {"x": 80, "y": 40, "w": 40, "h": 40},
    animalSprite["hurt_left"]: {"x": 120, "y": 40, "w": 40, "h": 40},
    animalSprite["attack_down"]: {"x": 0, "y": 80, "w": 40, "h": 40},
    animalSprite["attack_up"]: {"x": 40, "y": 80, "w": 40, "h": 40},
    animalSprite["attack_right"]: {"x": 80, "y": 80, "w": 40, "h": 40},
    animalSprite["attack_left"]: {"x": 120, "y": 80, "w": 40, "h": 40},
    animalSprite["dead"]: {"x": 160, "y": 0, "w": 40, "h": 40}}
old_age = 200
live_age = 0
yang_age = 25
death_age = 0
zero_age = 20
startEnergy = 200
energy_basic = 200
maxEnergy = 200
moveEnergy = 5
sleepEnergy = 1
stepEnergy = 12
tanimation = 0.0
pAttackEnergy = 0.8
pSpawnEnergy = 0.7

# Информация для растений
plantStatus = {
    "sprout": "sprout",
    "berry": "berry",
    "wither": "wither"
}
objectStatus = {
    "rock": 0
}
piece = 50
food = 100


# Тип экосистемы
ecoType = {
    "Land": "Land",
    "Water": "Water"
}

et_type = {
    0: "Land",
    1: "Water"
}

plantType = {
    "Land": "plant",
    "Water": "plant_water"
}

objectCollision = {
    "none": 0,
    "solid": 1,
    "moveable": 2
}

# Направления
directions = {
    "up": 0,
    "right": 1,
    "down": 2,
    "left": 3
}

# Типы поверхностей
floorTypes = {
    "solid": 0,
    "path": 1,
    "water": 2,
    "ice": 3,
    "sand": 4
}

tileTypes = {
    0: {"floor": floorTypes["path"], "sprite": "grass"},
    1: {"floor": floorTypes["solid"], "sprite": "grassRock"},
    2: {"floor": floorTypes["sand"], "sprite": "sand"},
    3: {"floor": floorTypes["solid"], "sprite": "sandRock"},
    4: {"floor": floorTypes["water"], "sprite": "water"},
    5: {"floor": floorTypes["solid"], "sprite": "waterRock"},
    6: {"floor": floorTypes["ice"], "sprite": "ice"},
    7: {"floor": floorTypes["solid"], "sprite": "iceRock"}
}

# Время
gameSpeeds = [
    {
        'name': "Paused",
        'mult': 0
    },
    {
        'name': "Normal",
        'mult': 1
    },
    {
        'name': "FasterX1.25",
        'mult': 1.25
    },
    {
        'name': "FasterX1.5",
        'mult': 1.5
    },
    {
        'name': "FasterX1.75",
        'mult': 1.75
    },
    {
        'name': "FasterX2",
        'mult': 2
    },
    {
        'name': "FasterX4",
        'mult': 4
    },
    {
        'name': "FasterX8",
        'mult': 8
    },
    {
        'name': "SlowerX0.5",
        'mult': 0.5
    },
    {
        'name': "SlowerX0.75",
        'mult': 0.75
    }
]

# Спрайты
grass_IMG = "sprites/tile/grass.png"
grassRock_IMG = "sprites/tile/rock_grass.png"
sand_IMG = "sprites/tile/sand.png"
sandRock_IMG = "sprites/tile/rock_sand.png"
water_IMG = "sprites/tile/water.png"
waterRock_IMG = "sprites/tile/rock_water.png"
ice_IMG = "sprites/tile/ice.png"
iceRock_IMG = "sprites/tile/rock_ice.png"

objectRock_IMG = "sprites/objects/rock.png"
plantDraw_IMG = "sprites/plantFood/plant.png"
plantDraw2_IMG = "sprites/plantFood/plant2.png"
cursorDraw_IMG = "sprites/objects/cursor.png"
hero_IMG = "sprites/characters/robot.png"
animalDraw_IMG = "sprites/animals/animalsprite.png"
animalDraw2_IMG = "sprites/animals/animalsprite2.png"
