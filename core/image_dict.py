import os

import pygame

# Определение пути к папке с изображениями
image_folder = os.path.join(
    os.path.dirname(__file__), "..", "images"
)  # 'images' - это имя папки с изображениями

# Загрузка изображений для каждого типа юнита
unit_images = {
    "swordsman": pygame.image.load(
        os.path.join(image_folder, "swordsman.png")
    ),  # noqa: E501
    "knight": pygame.image.load(os.path.join(image_folder, "knight.png")),
    "spearman": pygame.image.load(os.path.join(image_folder, "spearman.png")),
}
