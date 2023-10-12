import os

import pygame

from core.constants import SCALE

# Определение пути к папке с изображениями
image_folder = os.path.join(os.path.dirname(__file__), "..", "images")

# Определение пути к папке с изображениями фона гекса
background_folder = os.path.join(
    os.path.dirname(__file__), "..", "images", "background_grass"
)


# Определение пути к папке с изображениями внутри сборки для apk
# image_folder = "/data/data/MyMostTypicalBattle.mybattle/files/app/images"

# получаем список файлов фона
background_images = [
    os.path.join(background_folder, filename)
    for filename in os.listdir(background_folder)
    if filename.endswith((".png"))
]

scaled_background_images = []
for img_path in background_images:
    img = pygame.image.load(img_path)  # Загружаем изображение из пути
    scaled_image = pygame.transform.scale(
        img,
        (
            int(img.get_width() * SCALE * 0.75),
            int(img.get_height() * SCALE * 0.75),
        ),
    )
    scaled_background_images.append(scaled_image)


# Загрузка изображений для каждого типа юнита
unit_images = {
    "swordsman": pygame.image.load(
        os.path.join(image_folder, "sword_64.png")
    ),  # noqa: E501
    "knight": pygame.image.load(os.path.join(image_folder, "axe_64.png")),
    "spearman": pygame.image.load(os.path.join(image_folder, "pike_64.png")),
    "hero": pygame.image.load(os.path.join(image_folder, "hero_64.png")),
}

scaled_unit_images = {}
for unit_type, original_image in unit_images.items():
    scaled_image = pygame.transform.scale(
        original_image,
        (
            int(original_image.get_width() * SCALE),
            int(original_image.get_height() * SCALE),
        ),
    )
    scaled_unit_images[unit_type] = scaled_image


command_images = {
    "Catapult": pygame.image.load(
        os.path.join(image_folder, "command_catapult.png")
    ),  # noqa: E501
    "CrossbowVolley": pygame.image.load(
        os.path.join(image_folder, "command_crossbow_volley.png")
    ),  # noqa: E501
    "ArmyReserve": pygame.image.load(
        os.path.join(image_folder, "army_64.png")
    ),  # noqa: E501
    "Protection": pygame.image.load(
        os.path.join(image_folder, "protection_64.png")
    ),  # noqa: E501
}

scaled_command_images = {}
for command_type, original_image in command_images.items():
    scaled_image = pygame.transform.scale(
        original_image,
        (
            int(original_image.get_width() * SCALE),
            int(original_image.get_height() * SCALE),
        ),
    )
    scaled_command_images[command_type] = scaled_image

menu_images = {
    "Logo": pygame.image.load(os.path.join(image_folder, "logo.png")),  # noqa: E501
    "Info": pygame.image.load(os.path.join(image_folder, "info.png")),  # noqa: E501
    "Info_manual_1": pygame.image.load(
        os.path.join(image_folder, "info_1.png")
    ),  # noqa: E501
    "Info_manual_2": pygame.image.load(
        os.path.join(image_folder, "info_2.png")
    ),  # noqa: E501
    "Ok": pygame.image.load(os.path.join(image_folder, "ok.png")),  # noqa: E501
    "MultiPlayer": pygame.image.load(
        os.path.join(image_folder, "play.png")
    ),  # noqa: E501
    "Repeat": pygame.image.load(
        os.path.join(image_folder, "repeat_128.png")
    ),  # noqa: E501
    "Home": pygame.image.load(os.path.join(image_folder, "home_128.png")),  # noqa: E501
    "BG": pygame.image.load(os.path.join(image_folder, "bg_1.png")),  # noqa: E501
    "BG_2": pygame.image.load(os.path.join(image_folder, "bg_2.png")),  # noqa: E501
    "BG_1": pygame.image.load(os.path.join(image_folder, "bg_3.png")),  # noqa: E501
    "BG_win_1": pygame.image.load(
        os.path.join(image_folder, "bg_win_1.png")
    ),  # noqa: E501
    "BG_win_2": pygame.image.load(
        os.path.join(image_folder, "bg_win_2.png")
    ),  # noqa: E501
    "BG_4": pygame.image.load(os.path.join(image_folder, "bg_4.png")),  # noqa: E501
    "BG_5": pygame.image.load(os.path.join(image_folder, "bg_5.png")),  # noqa: E501
    "BG_pre": pygame.image.load(os.path.join(image_folder, "bg_pre.png")),  # noqa: E501
    "BG_pre_1": pygame.image.load(
        os.path.join(image_folder, "bg_pre_1.png")
    ),  # noqa: E501
}

scaled_menu_images = {}
for menu_type, original_image in menu_images.items():
    scaled_image = pygame.transform.scale(
        original_image,
        (
            int(original_image.get_width() * SCALE),
            int(original_image.get_height() * SCALE),
        ),
    )
    scaled_menu_images[menu_type] = scaled_image
