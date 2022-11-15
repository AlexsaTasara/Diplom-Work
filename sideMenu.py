import pygame
import indexes as ind
from constants import *


def text_format(message, tfont, tsize, tcolor):
    new_font = pygame.font.Font(tfont, tsize)
    new_text = new_font.render(message, True, tcolor)
    return new_text


def type_texts(game, screen, screen_width):
    textsss = {}
    title_rects = {}
    textsss[0] = text_format("Поменять карту[m]: " + str(ind.mapChange), font6, 20, white)
    textsss[1] = text_format("Добавить животное[i]: " + str(ind.animalSpawn), font6, 20, white)
    textsss[2] = text_format("Добавить растение[p]: " + str(ind.plantSpawn), font6, 20, white)
    textsss[3] = text_format("Поменять объект[o]: " + str(ind.objectSpawn), font6, 20, white)
    textsss[4] = text_format("Число животных: " + str(len(game.eco.animals)), font6, 20, white)
    textsss[5] = text_format("Число растений: " + str(len(game.eco.plants)), font6, 20, white)
    textsss[6] = text_format("Число объектов: " + str(len(game.eco.objects)), font6, 20, white)
    textsss[7] = text_format("Число тактов: " + str(ind.tak), font6, 20, white)
    textsss[8] = text_format("Скорость модели[t]: " + str(gameSpeeds[ind.currentSpeed]["name"]), font6, 20, white)
    textsss[9] = text_format("Очистить модель[с]", font6, 20, white)
    textsss[10] = text_format("Запустить модель[z]", font6, 20, white)
    for i in range(len(textsss)):
        title_rects[i] = textsss[i].get_rect()
    for i in range(len(textsss)):
        screen.blit(textsss[i], (screen_width - (title_rects[i][2]) - 40, 50 + i*30))


