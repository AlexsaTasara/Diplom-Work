import pygame
import indexes as ind
from constants import *
from strings import *


def text_format(message, tfont, tsize, tcolor):
    new_font = pygame.font.Font(tfont, tsize)
    new_text = new_font.render(message, True, tcolor)
    return new_text


def type_texts(game, screen, screen_width):
    textsss = {}
    title_rects = {}
    textsss[0] = text_format(sideMenuTexts[0][ind.userLang] + str(ind.mapChange), font6, 20, white)
    textsss[1] = text_format(sideMenuTexts[1][ind.userLang] + str(ind.animalSpawn), font6, 20, white)
    textsss[2] = text_format(sideMenuTexts[2][ind.userLang] + str(ind.plantSpawn), font6, 20, white)
    textsss[3] = text_format(sideMenuTexts[3][ind.userLang] + str(ind.objectSpawn), font6, 20, white)
    textsss[4] = text_format(sideMenuTexts[4][ind.userLang] + str(len(game.eco.animals)), font6, 20, white)
    textsss[5] = text_format(sideMenuTexts[5][ind.userLang] + str(len(game.eco.plants)), font6, 20, white)
    textsss[6] = text_format(sideMenuTexts[6][ind.userLang] + str(len(game.eco.objects)), font6, 20, white)
    textsss[7] = text_format(sideMenuTexts[7][ind.userLang] + str(ind.tak), font6, 20, white)
    textsss[8] = text_format(sideMenuTexts[8][ind.userLang] + stPlS[ind.PLT][ind.userLang], font6, 20, white)
    textsss[9] = text_format(sideMenuTexts[9][ind.userLang] + stPlS[ind.PLW][ind.userLang], font6, 20, white)
    textsss[10] = text_format(sideMenuTexts[10][ind.userLang] + str(gameSpeeds[ind.currentSpeed]["name"]), font6, 20, white)
    textsss[11] = text_format(sideMenuTexts[11][ind.userLang], font6, 20, white)
    textsss[12] = text_format(sideMenuTexts[12][ind.userLang], font6, 20, white)
    textsss[13] = text_format(sideMenuTexts[13][ind.userLang], font6, 20, white)
    for i in range(len(textsss)):
        title_rects[i] = textsss[i].get_rect()
    for i in range(len(textsss)):
        screen.blit(textsss[i], (screen_width - (title_rects[i][2]) - 40, 50 + i*30))


