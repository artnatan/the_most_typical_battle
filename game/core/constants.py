# Определение цветов
import math

import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 191, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
UNKNOWN_1 = (255, 255, 204)

# Размер экрана
pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h * 0.915

# SCREEN_WIDTH = 400
# SCREEN_HEIGHT = 800

ORIG_SCREEN_WIDTH = 400
ORIG_SCREEN_HEIGHT = 600

# Коэффициенты масштабирования
# SCALE_X = SCREEN_WIDTH / ORIG_SCREEN_WIDTH
# SCALE_Y = SCREEN_HEIGHT / ORIG_SCREEN_HEIGHT


if SCREEN_WIDTH < SCREEN_HEIGHT:
    SCALE = SCREEN_WIDTH / ORIG_SCREEN_WIDTH
else:
    SCALE = SCREEN_HEIGHT / ORIG_SCREEN_HEIGHT


# Размеры гексагональных тайлов
# HEX_SIZE = 50
if SCREEN_WIDTH < SCREEN_HEIGHT:
    HEX_SIZE = SCREEN_WIDTH / 8
else:
    HEX_SIZE = SCREEN_HEIGHT / 12

HEX_WIDTH = int(2 * HEX_SIZE)
HEX_HEIGHT = int(math.sqrt(3) * HEX_SIZE)


# Размеры юнита
# UNIT_SIZE = 40
UNIT_SIZE = HEX_SIZE * 0.7
UNIT_WIDTH = int(2 * UNIT_SIZE)
UNIT_HEIGHT = int(math.sqrt(3) * UNIT_SIZE)

# Толщина линии для обводки гексагонов
LINE_WIDTH = 4

# Параметры кнопок бонусов
# BUTTON_BONUS_HEIGHT = 80
# BUTTON_BONUS_WIDTH = 80
if SCREEN_WIDTH < SCREEN_HEIGHT:
    BUTTON_BONUS_HEIGHT = SCREEN_WIDTH / 4.5
    BUTTON_BONUS_WIDTH = SCREEN_WIDTH / 4.5
else:
    BUTTON_BONUS_HEIGHT = SCREEN_HEIGHT / 6
    BUTTON_BONUS_WIDTH = SCREEN_HEIGHT / 6

BUTTON_BONUS_COLOR = WHITE
