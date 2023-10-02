import os
import pygame.font
from core.constants import SCALE

original_font_size = 42

pygame.font.init()

# Определение пути к папке с шрифтами
font_folder = os.path.join(os.path.dirname(__file__), "..", "fonts")
font = os.path.join(font_folder, "OSWALD-SEMIBOLD.TTF")

# Определение пути к папке с изображениями внутри сборки для apk
# font_folder = "/data/data/MyMostTypicalBattle.mybattle/files/app/fonts"

# Загрузка шрифтов
font_dict = {
    "oswald_font": [
        os.path.join(font_folder, "OSWALD-SEMIBOLD.TTF"),
        original_font_size,
    ],
    "oswald_font_46": [
        os.path.join(font_folder, "OSWALD-SEMIBOLD.TTF"),
        original_font_size + 4,
    ],
    "oswald_font_28": [
        os.path.join(font_folder, "OSWALD-SEMIBOLD.TTF"),
        original_font_size - 14,
    ],
    "oswald_font_86": [
        os.path.join(font_folder, "OSWALD-SEMIBOLD.TTF"),
        original_font_size + 46,
    ],
}

scaled_font_dict = {}
for key, original_font in font_dict.items():
    # Масштабирование шрифта
    scaled_font_size = int(original_font[1] * SCALE)
    scaled_font = pygame.font.Font(original_font[0], scaled_font_size)
    scaled_font_dict[key] = scaled_font
