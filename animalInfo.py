import pygame
from constants import *
from strings import *


def text_format(message, tfont, tsize, tcolor):
    new_font = pygame.font.Font(tfont, tsize)
    new_text = new_font.render(message, True, tcolor)
    return new_text


def animal_info_texts(screen, screen_width, anim):
    textsss = {}
    title_rects = {}
    textsss[0] = text_format("Индекс: " + str(anim.index), font6, 20, white)
    textsss[1] = text_format("Возраст: " + str(anim.liveTime), font6, 20, white)
    textsss[2] = text_format("Возраст старости: " + str(anim.told), font6, 20, white)
    textsss[3] = text_format("Энергия: " + str(anim.energy), font6, 20, white)
    textsss[4] = text_format("Максимальная энергия: " + str(anim.maxEnergy), font6, 20, white)
    textsss[5] = text_format("Цвет: " + str(anim.color), font6, 20, white)
    textsss[6] = text_format("Веса: " + str(anim.birthWeight) + ", " + str(anim.walkWeight) + ", " + str(anim.eatWeight)
                             + ", " + str(anim.interactionWeight) + ", " + str(anim.runWeight), font6, 20, white)

    for i in range(len(textsss)):
        title_rects[i] = textsss[i].get_rect()
    for i in range(len(textsss)):
        screen.blit(textsss[i], (screen_width - (title_rects[i][2]) - 40, 50 + (i+14)*30))
