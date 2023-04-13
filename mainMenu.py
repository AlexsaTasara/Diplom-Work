import math
import os
from sideMenu import *
from animalInfo import *
import sys
import cursor as curr
import ecosystem as ecoo
import saveAndLoad as sal
import pointOfView as pov
from strings import *
import time
import xlsxwriter
from index_functions import *

# Инициализация игры
pygame.init()
# Размещаем экран по центру
os.environ['SDL_VIDEO_CENTERED'] = '1'
# Разрешение игрового окна
# screen_width = 1024
# screen_height = 768
infoObject = pygame.display.Info()
screen_height = infoObject.current_h
screen_width = infoObject.current_w
screen = pygame.display.set_mode((screen_width, screen_height))


# Функция настройки размера клетки.
def set_tile_size(map_data):
    biggest_par = len(map_data)
    line_size = len(map_data[0])
    screen_size = screen_height
    a = ind.tileH*len(map_data) - screen_height
    b = ind.tileW*line_size - screen_width
    if b > a:
        biggest_par = line_size
        screen_size = screen_width
    newTile = screen_size//biggest_par
    return newTile, newTile


# Количество кадров в секунду
clock = pygame.time.Clock()
FPS = 30


# Стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, nomer):
        self.groups = game.background_sprite, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.spritelist[nomer]

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * ind.tileW
        self.rect.y = y * ind.tileH


# Клетки земли
class GroundTyle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, nomer):
        self.groups = game.background_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spritelist[nomer]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * ind.tileW
        self.rect.y = y * ind.tileH


class Game:
    def __init__(self):
        self.background_sprite = None
        self.spritelist = None
        self.view = None
        self.eco = None
        self.curs = None
        self.dt = None
        self.playing = None
        self.map_data = None
        self.walls = None
        self.curs_sprites = None
        self.all_sprites = None
        self.object_sprites = None
        self.mapTileData = None
        self.save = None
        self.workbook = None
        self.worksheetEnergy = None
        self.worksheetMaxEnergy = None
        self.worksheetLiveTime = None
        self.worksheetStatus = None
        self.worksheetNumbers = None
        self.eCol = None
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Модель искусственной жизни")
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    # Функция загрузки сохраненных файлов
    def load_save_file(self, save1):
        self.eco.clear()
        save1.loadBack()
        for annn in save1.animals:
            self.eco.loadAnim(self, annn)
        for i in self.eco.animals:
            self.eco.animals[i].update()
        for plll in save1.plants:
            self.eco.loadPlant(self, plll)
        for i in self.eco.plants:
            self.eco.plants[i].update()
        for objj in save1.objects:
            self.eco.loadObject(self, objj)
        for i in self.eco.objects:
            self.eco.objects[i].update()

    def load_data(self):
        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, 'sprites')
        self.map_data = []
        with open(os.path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        # ind.tileW, ind.tileH = set_tile_size(self.map_data)
        self.spriteupdate()

    def spriteupdate(self):
        GRASS_IMG = pygame.image.load(grass_IMG).convert_alpha()
        GRASSROCK_IMG = pygame.image.load(grassRock_IMG).convert_alpha()
        SAND_IMG = pygame.image.load(sand_IMG).convert_alpha()
        SANDROCK_IMG = pygame.image.load(sandRock_IMG).convert_alpha()
        WATER_IMG = pygame.image.load(water_IMG).convert_alpha()
        WATERROCK_IMG = pygame.image.load(waterRock_IMG).convert_alpha()
        ICE_IMG = pygame.image.load(ice_IMG).convert_alpha()
        ICEROCK_IMG = pygame.image.load(iceRock_IMG).convert_alpha()
        CURSOR_IMG = pygame.image.load(cursorDraw_IMG).convert_alpha()
        OBJROCK_IMG = pygame.image.load(objectRock_IMG).convert_alpha()
        PLANT_IMG = pygame.image.load(plantDraw_IMG).convert_alpha()
        PLANT2_IMG = pygame.image.load(plantDraw2_IMG).convert_alpha()
        HERO_IMG = pygame.image.load(hero_IMG).convert_alpha()
        ANIMAL_IMG = pygame.image.load(animalDraw_IMG).convert_alpha()
        ANIMAL2_IMG = pygame.image.load(animalDraw2_IMG).convert_alpha()

        GRASS_IMG = pygame.transform.scale(GRASS_IMG, (ind.tileW, ind.tileH))
        GRASSROCK_IMG = pygame.transform.scale(GRASSROCK_IMG, (ind.tileW, ind.tileH))
        SAND_IMG = pygame.transform.scale(SAND_IMG, (ind.tileW, ind.tileH))
        SANDROCK_IMG = pygame.transform.scale(SANDROCK_IMG, (ind.tileW, ind.tileH))
        WATER_IMG = pygame.transform.scale(WATER_IMG, (ind.tileW, ind.tileH))
        WATERROCK_IMG = pygame.transform.scale(WATERROCK_IMG, (ind.tileW, ind.tileH))
        ICE_IMG = pygame.transform.scale(ICE_IMG, (ind.tileW, ind.tileH))
        ICEROCK_IMG = pygame.transform.scale(ICEROCK_IMG, (ind.tileW, ind.tileH))
        CURSOR_IMG = pygame.transform.scale(CURSOR_IMG, (ind.tileW, ind.tileH))

        self.spritelist = {
            0: GRASS_IMG,
            1: GRASSROCK_IMG,
            2: SAND_IMG,
            3: SANDROCK_IMG,
            4: WATER_IMG,
            5: WATERROCK_IMG,
            6: ICE_IMG,
            7: ICEROCK_IMG,
            "cur": CURSOR_IMG,
            "Land": ANIMAL_IMG,
            "plant": PLANT_IMG,
            "plant_water": PLANT2_IMG,
            "rock": OBJROCK_IMG,
            "hero": HERO_IMG,
            "Water": ANIMAL2_IMG
        }

    # Инициализируем все переменные
    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.curs_sprites = pygame.sprite.Group()
        self.mapTileData = maps.mapTileData
        self.background_sprite = pygame.sprite.Group()

        self.eco = ecoo.Ecosystem()
        self.view = pov.PointOfView()
        self.save = sal.SaveAndLoad()
        self.workbook = xlsxwriter.Workbook('AgentsStatuses.xlsx')
        self.worksheetEnergy = self.workbook.add_worksheet()
        self.worksheetMaxEnergy = self.workbook.add_worksheet()
        self.worksheetLiveTime = self.workbook.add_worksheet()
        self.worksheetStatus = self.workbook.add_worksheet()
        self.worksheetNumbers = self.workbook.add_worksheet()

        currentmap = maps.gameMap[ind.mapNo]
        ind.tileW, ind.tileH = set_tile_size(currentmap)
        self.spriteupdate()
        for row, tiles in enumerate(currentmap):
            for col, tile in enumerate(tiles):
                if (tile == 1) or (tile == 3) or (tile == 5) or (tile == 7):
                    Wall(self, col, row, tile)
                if (tile == 0) or (tile == 2) or (tile == 4) or (tile == 6):
                    GroundTyle(self, col, row, tile)
        # self.player.placeAt(2, 2)
        self.curs = curr.Cursor(self)

    # Для завершения программы playing = False
    def run(self):
        self.playing = True
        self.eCol = 0
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.simulation()
            self.update()
            self.draw()

    # Выход из программы
    def quit(self):
        self.workbook.close()
        pygame.quit()
        sys.exit()

    # Обновляем спрайты
    def update(self):
        self.background_sprite.update()
        self.all_sprites.update()
        self.curs_sprites.update()
        self.object_sprites.update()

    # Рисуем сетку
    def draw_grid(self):
        for x in range(0, screen_width, ind.tileW):
            pygame.draw.line(self.screen, gray, (x, 0), (x, screen_height))
        for y in range(0, screen_height, ind.tileH):
            pygame.draw.line(self.screen, gray, (0, y), (screen_width, y))

    # Рисуем экран
    def draw(self):
        self.screen.fill(black)
        self.draw_grid()
        self.background_sprite.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.object_sprites.draw(self.screen)
        animsKeys = self.eco.animals.copy().keys()
        if ind.animInfo in animsKeys and ind.currentSpeed != 0:
            self.curs.placeAt(self.eco.animals[ind.animInfo].tileTo[0], self.eco.animals[ind.animInfo].tileTo[1])
        if ind.objectSpawn or ind.plantSpawn or ind.animalSpawn or ind.info:
            self.curs_sprites.draw(self.screen)
        type_texts(self, screen, screen_width)
        if ind.info and ind.animInfo in animsKeys:
            animal_info_texts(self, screen, screen_width, self.eco.animals[ind.animInfo])
        #
        # self.type_texts()
        if ind.mapChange:
            self.draw_map_change()

        pygame.display.flip()

    # Ивенты клавиатуры
    def events(self):
        # Ловим все ивенты здесь
        for event in pygame.event.get():
            # Закрытие приложения
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                # Остановка / Запуск модели
                if event.key == pygame.K_z:
                    stop_start_model()
                # Изменение скорости появления растений в воде
                if event.key == pygame.K_k:
                    if ind.PLW == 4:
                        ind.PLW = 0
                    else:
                        ind.PLW += 1
                # Изменение скорости появления растений на суше
                if event.key == pygame.K_j:
                    if ind.PLT == 4:
                        ind.PLT = 0
                    else:
                        ind.PLT += 1
                # Добавление / Удаление животных
                if (event.key == pygame.K_i) and (not ind.mapChange) and (ind.currentSpeed == 0):
                    animal_spawn_flag()
                # Добавление / Удаление растений
                if (event.key == pygame.K_p) and (not ind.mapChange) and (ind.currentSpeed == 0):
                    plant_spawn_flag()
                # Добавление / Удаление объектов
                if (event.key == pygame.K_o) and (not ind.mapChange) and (ind.currentSpeed == 0):
                    object_spawn_flag()
                # Информация
                if (event.key == pygame.K_y) and (not ind.mapChange):
                    info_flag(self)
                # Смена языка
                if (event.key == pygame.K_l) and (not ind.mapChange):
                    if ind.userLang < lang["ENG"]:
                        ind.userLang += 1
                    else:
                        ind.userLang = 0
                # Смена карты
                if (event.key == pygame.K_m) and (not ind.mapChange) and (ind.currentSpeed == 0):
                    map_flag()
                # Перемещение курсора
                if ind.objectSpawn or ind.animalSpawn or ind.plantSpawn or ind.info:
                    if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):  # Вправо
                        if self.curs.canMoveRight():
                            self.curs.MoveRight()
                    if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):  # влево
                        if self.curs.canMoveLeft():
                            self.curs.MoveLeft()
                    if (event.key == pygame.K_w) or (event.key == pygame.K_UP):  # Вверх
                        if self.curs.canMoveUp():
                            self.curs.MoveUp()
                    if (event.key == pygame.K_s) or (event.key == pygame.K_DOWN):  # Вниз
                        if self.curs.canMoveDown():
                            self.curs.MoveDown()
                    # Выбираем цвет животного
                    if ind.animalSpawn:
                        # Красный
                        if event.key == pygame.K_1:
                            ind.chosenColorInd = "RED"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Зеленый
                        if event.key == pygame.K_2:
                            ind.chosenColorInd = "GREEN"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Синий
                        if event.key == pygame.K_3:
                            ind.chosenColorInd = "BLUE"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Желтый
                        if event.key == pygame.K_4:
                            ind.chosenColorInd = "YELLOW"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Розовый
                        if event.key == pygame.K_5:
                            ind.chosenColorInd = "PINK"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Голубой
                        if event.key == pygame.K_6:
                            ind.chosenColorInd = "LIGHTBLUE"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break
                        # Белый
                        if event.key == pygame.K_7:
                            ind.chosenColorInd = "WHITE"
                            ind.chosenColor = animalColor[ind.chosenColorInd]
                            break

                    if (event.key == pygame.K_h) and (ind.animalSpawn or ind.plantSpawn):  # Вид экосистемы
                        if ind.et == 0:
                            ind.et = 1
                        else:
                            ind.et = 0
                    # Подтвердить
                    if (event.key == pygame.K_e) or (event.key == pygame.K_KP_ENTER) or (event.key == pygame.K_SPACE):
                        confirm_function(self)
                # Меняем карту
                if ind.mapChange:
                    if event.key == pygame.K_q:
                        ind.mapChange = not ind.mapChange
                    if event.key == pygame.K_0:
                        ind.mapCh = 0
                    if event.key == pygame.K_1:
                        ind.mapCh = 1
                    if event.key == pygame.K_2:
                        ind.mapCh = 2
                    if event.key == pygame.K_3:
                        ind.mapCh = 3
                    if event.key == pygame.K_4:
                        ind.mapCh = 4
                    if event.key == pygame.K_5:
                        ind.mapCh = 5
                    if event.key == pygame.K_6:
                        ind.mapCh = 6
                    if event.key == pygame.K_7:
                        ind.mapCh = 7
                    if event.key == pygame.K_8:
                        ind.mapCh = 8
                    if event.key == pygame.K_9:
                        ind.mapCh = 9
                    if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):
                        if ind.mapCh < 9:
                            ind.mapCh += 1
                        else:
                            ind.mapCh = 0
                    if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT):
                        if ind.mapCh > 0:
                            ind.mapCh -= 1
                        else:
                            ind.mapCh = 9
                    # Выбрали карту
                    if event.key == pygame.K_e:
                        self.curs.placeAt(0, 0)
                        ind.mapChange = False
                        self.eco.clear()
                        ind.pastSpeed = 1
                        ind.currentSpeed = 0
                        ind.tak = 0
                        ind.mapNo = ind.mapCh
                        self.background_sprite.empty()
                        self.update_map()

                # Работа со временем
                if (event.key == pygame.K_t) and (ind.currentSpeed != 0):
                    if ind.currentSpeed < 9:
                        ind.currentSpeed += 1
                    else:
                        ind.currentSpeed = 1
                # Очистка
                if event.key == pygame.K_c:
                    self.eco.clear()
                    ind.tak = 0
                    ind.pastSpeed = 1
                    ind.currentSpeed = 0
                # Закрыть программу
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                # Сохраняем модель
                if event.key == pygame.K_f:
                    self.save.saveF(0, self.eco)
                # Загружаем модель
                if event.key == pygame.K_g:
                    ss1 = self.save.loadF(0, self.eco)
                    if ss1 != "Пустое сохранение":
                        self.load_save_file(ss1)
                # Удаляем сохранение
                if event.key == pygame.K_r:
                    self.save.clearF(0)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def plant_status_update(self):
        # Случайное появление новых растений
        ind.tPlantL += 1
        ind.tPlantW += 1
        if ind.PLT == 2:
            put_plant(self, ecoType["Land"])
        else:
            if ind.PLT > 2:
                for m in range(2, ind.PLT + 1):
                    put_plant(self, ecoType["Land"])
            else:
                if ind.tPlantL > (2 - ind.PLT):
                    ind.tPlantL = 0
                    put_plant(self, ecoType["Land"])
        if ind.PLW == 2:
            put_plant(self, ecoType["Water"])
        else:
            if ind.PLW > 2:
                for m in range(2, ind.PLW + 1):
                    put_plant(self, ecoType["Water"])
            else:
                if ind.tPlantW > (2 - ind.PLW):
                    ind.tPlantW = 0
                    put_plant(self, ecoType["Water"])
        # Обновление состояния растений
        listdelLater = []
        for h in self.eco.plants:
            checkT = self.eco.plants[h].timeUpdate()
            if not checkT:
                listdelLater.append(h)
                continue
            self.eco.plants[h].statusUpdate()
        for h in listdelLater:
            self.eco.delPlant(self.eco.plants[h].index)

    def simulation(self):
        currentFrameTime = int(time.time() * 1000)
        timeElapsed = currentFrameTime - ind.lastFrameTime
        ind.gameTime += math.floor(timeElapsed * gameSpeeds[ind.currentSpeed]["mult"])
        sec = math.floor(int(time.time()))
        if sec != ind.currentSecond:
            ind.currentSecond = sec
            ind.framesLastSecond = ind.frameCount
            ind.frameCount = 1
        else:
            ind.frameCount += 1

        if ind.tTime >= ind.timeEcosystem:
            self.plant_status_update()
            # Перемещение животных
            for h in self.eco.animals:
                self.eco.animals[h].tileFrom = self.eco.animals[h].tileTo
                self.eco.animals[h].courseLast = self.eco.animals[h].courseNext
            # Обновление списков приоритета/ смерть/ рождение новых особей
            hlist = self.eco.animals
            keylisth = hlist.copy().keys()
            for h in keylisth:
                if not self.eco.animals[h].timeUpdate():
                    self.eco.delAnim(self.eco.animals[h].index)
            hlist = self.eco.animals
            keylisth = hlist.copy().keys()
            for h in keylisth:
                stat = self.eco.animals[h].status
                if (stat != statusAnim["ZERO"]) and (stat != statusAnim["DEATH"]):
                    self.view.updateLook(self.eco.animals[h].tileFrom, self.eco.animals[h].ecoT, self.eco)
                    self.view.updateLists(self.eco.animals[h].myCourse(), self.eco.animals[h].tileFrom, self.eco)
                    stat = self.eco.choosePurpose(self, h)
                    self.worksheetEnergy.write(h, self.eCol, self.eco.animals[h].energy)
                    self.worksheetMaxEnergy.write(h, self.eCol, self.eco.animals[h].maxEnergy)
                    self.worksheetLiveTime.write(h, self.eCol, self.eco.animals[h].liveTime)
                    self.worksheetStatus.write(h, self.eCol, self.eco.animals[h].status)
            self.worksheetNumbers.write(0, self.eCol, len(self.eco.animals))
            self.eCol = self.eCol + 1
            ind.tTime = 0
            ind.tak += 1
        ind.tTime += math.floor(timeElapsed * gameSpeeds[ind.currentSpeed]["mult"])
        ind.lastFrameTime = currentFrameTime

    def draw_map_change(self):
        xsize = 600
        ysize = 240
        xxx1 = (screen_width - xsize) / 2
        yyy1 = (screen_height - ysize) / 2
        pygame.draw.rect(self.screen, gray, pygame.Rect(xxx1, yyy1, xsize, ysize))
        text1 = text_format(stchosemapInf[ind.userLang], font6, 20, white)
        ttt = stmapchoice9
        if ind.mapCh == 0:
            ttt = stmapchoice0
        else:
            if ind.mapCh == 1:
                ttt = stmapchoice1
            else:
                if ind.mapCh == 2:
                    ttt = stmapchoice2
                else:
                    if ind.mapCh == 3:
                        ttt = stmapchoice3
                    else:
                        if ind.mapCh == 4:
                            ttt = stmapchoice4
                        else:
                            if ind.mapCh == 5:
                                ttt = stmapchoice5
                            else:
                                if ind.mapCh == 6:
                                    ttt = stmapchoice6
                                else:
                                    if ind.mapCh == 7:
                                        ttt = stmapchoice7
                                    else:
                                        if ind.mapCh == 8:
                                            ttt = stmapchoice8

        text2 = text_format(ttt, font6, 20, white)
        text3 = text_format(stwi[ind.userLang] + str(maps.mapW[ind.mapCh]), font6, 20, white)
        text4 = text_format(sthe[ind.userLang] + str(maps.mapH[ind.mapCh]), font6, 20, white)
        text5 = text_format(stmapchchose[ind.userLang], font6, 20, white)
        # text9 = text_format("Число объектов: " + str(ind.heroVisible), font6, 20, white)
        title_rect1 = text1.get_rect()
        title_rect2 = text2.get_rect()
        title_rect3 = text3.get_rect()
        title_rect4 = text4.get_rect()
        title_rect5 = text5.get_rect()
        screen.blit(text1, (screen_width / 2 - (title_rect1[2] / 2), yyy1 + 10))
        screen.blit(text2, (screen_width / 2 - (title_rect2[2] / 2), yyy1 + 40))
        screen.blit(text3, (screen_width / 2 - (title_rect3[2] / 2), yyy1 + 70))
        screen.blit(text4, (screen_width / 2 - (title_rect4[2] / 2), yyy1 + 100))
        screen.blit(text5, (screen_width / 2 - (title_rect5[2] / 2), yyy1 + 130))

    def update_map(self):
        currentmap = maps.gameMap[ind.mapNo]
        ind.tileW, ind.tileH = set_tile_size(currentmap)
        self.spriteupdate()
        for row, tiles in enumerate(currentmap):
            for col, tile in enumerate(tiles):
                if (tile == 1) or (tile == 3) or (tile == 5) or (tile == 7):
                    Wall(self, col, row, tile)
                if (tile == 0) or (tile == 2) or (tile == 4) or (tile == 6):
                    GroundTyle(self, col, row, tile)


# Функция остановки / запуска модели
def stop_start_model():
    if ind.currentSpeed != 0:
        ind.pastSpeed = ind.currentSpeed
        ind.currentSpeed = 0
    else:
        ind.currentSpeed = ind.pastSpeed
        ind.objectSpawn = False
        ind.animalSpawn = False
        ind.plantSpawn = False
        ind.mapChange = False


# Главное меню
def main_menu():
    menu = True
    game_emulation = True
    draw_emulation = False
    option_list = [
        "start new",
        "load old",
        "settings",
        "quit"
    ]
    menu_index = 0
    selected = option_list[menu_index]
    # Пока работает программа
    while game_emulation:
        # Главное меню
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if menu_index > 0:
                            menu_index -= 1
                        else:
                            menu_index = len(option_list) - 1
                        selected = option_list[menu_index]
                    elif event.key == pygame.K_DOWN:
                        if menu_index < len(option_list) - 1:
                            menu_index += 1
                        else:
                            menu_index = 0
                        selected = option_list[menu_index]
                    if event.key == pygame.K_RETURN:
                        if selected == "start new":
                            print("Start")
                            gamess()
                            draw_emulation = True
                        if selected == "quit":
                            pygame.quit()
                            quit()

            # UI Главного меню
            screen.fill(light_green)
            title = text_format(stmodelname[ind.userLang], font6, 50, blue)
            if selected == "start new":
                text_start = text_format("Новая модель", font1, 75, white)
            else:
                text_start = text_format("Новая модель", font1, 75, black)
            if selected == "load old":
                text_load = text_format("Загрузить модель", font1, 75, white)
            else:
                text_load = text_format("Загрузить модель", font1, 75, black)
            if selected == "settings":
                text_sett = text_format("Настройки", font1, 75, white)
            else:
                text_sett = text_format("Настройки", font1, 75, black)
            if selected == "quit":
                text_quit = text_format("Выйти", font1, 75, white)
            else:
                text_quit = text_format("Выйти", font1, 75, black)

            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            load_rect = text_load.get_rect()
            sett_rect = text_sett.get_rect()
            quit_rect = text_quit.get_rect()

            # Текст главного меню
            screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), 80))
            screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2), 200))
            screen.blit(text_load, (screen_width / 2 - (load_rect[2] / 2), 300))
            screen.blit(text_sett, (screen_width / 2 - (sett_rect[2] / 2), 400))
            screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2), 500))
            pygame.display.update()
            clock.tick(FPS)
            pygame.display.set_caption(stmodelname[ind.userLang])
        # Рисование модели


def gamess():
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()


if __name__ == '__main__':
    main_menu()
    # gamess()
    pygame.quit()
    # quit()
