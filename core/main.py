import math

import pygame
from constants import (BLACK, HEX_HEIGHT, HEX_SIZE, HEX_WIDTH, LINE_WIDTH,
                       SCREEN_HEIGHT, SCREEN_WIDTH, UNIT_HEIGHT, UNIT_SIZE,
                       WHITE)
from functions import attack, move
from hexagon import Hexagon
from image_dict import unit_images
from units import Unit

# Инициализация Pygame
pygame.init()

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hexagonal Grid")

# Создание списка для хранения гексагональных тайлов и юнитов
hexagons = []
units = []

start_x = (SCREEN_WIDTH - 3 * HEX_WIDTH * 0.75) / 2
start_y = (SCREEN_HEIGHT - 3 * HEX_HEIGHT - HEX_HEIGHT * 0.5) / 2

font = pygame.font.Font(None, 24)

# Создание юнитов игрока 1 (верхние 8 гексов)
for row in range(2):
    hexagons_row = []
    units_row = []
    for col in range(4):
        x = start_x + col * HEX_WIDTH * 0.75
        y = start_y + row * HEX_HEIGHT
        if col % 2 < 1:
            y += HEX_HEIGHT * 0.5
        hexagon = Hexagon(x, y)
        hexagons_row.append(hexagon)

        # Создание юнита игрока 1
        unit = Unit(
            x,
            y,
            side="enemy",
        )
        units_row.append(unit)
    hexagons.append(hexagons_row)
    units.append(units_row)

# Создание юнитов игрока 2 (нижние 8 гексов)
for row in range(2, 4):
    hexagons_row = []
    units_row = []
    for col in range(4):
        x = start_x + col * HEX_WIDTH * 0.75
        y = start_y + row * HEX_HEIGHT
        if col % 2 < 1:
            y += HEX_HEIGHT * 0.5
        hexagon = Hexagon(x, y)
        hexagons_row.append(hexagon)

        # Создание юнита игрока 2
        unit = Unit(
            x,
            y,
            side="player",
        )
        units_row.append(unit)
    hexagons.append(hexagons_row)
    units.append(units_row)

# Основной цикл игры
running = True
selected_units = []  # Список выбранных юнитов


def add_unit_selected_list(units, hexagon, selected_units):
    for row in units:
        for unit in row:
            if unit.x == hexagon.x and unit.y == hexagon.y:
                if unit not in selected_units:
                    selected_units.append(unit)  # Добавляем выбранный юнит
                    unit.active = True
                else:
                    # Если юнит уже был выбран, убираем его из выбранных
                    selected_units.remove(unit)
                    unit.active = False


def check_hexagon_on_click(hexagons):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for row in hexagons:
        for hexagon in row:
            # Вычисляем расстояние от точки нажатия до центра гексагона
            distance = math.sqrt(
                (mouse_x - hexagon.x) ** 2 + (mouse_y - hexagon.y) ** 2
            )
            if distance < HEX_SIZE:
                # Проверяем, был ли выбран юнит на этом гексе
                add_unit_selected_list(units, hexagon, selected_units)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Проверяем, на каком гексагоне было нажатие мыши
                check_hexagon_on_click(hexagons)

    # Если выбрано два юнита и они могут обменяться местами
    if len(selected_units) == 2:
        active_unit, target_unit = selected_units[0], selected_units[1]

        if active_unit.can_swap_with(target_unit):
            move(active_unit, target_unit)
            for unit in selected_units:
                unit.active = False
            selected_units = []  # Очищаем список выбранных юнитов

        # Взаимодействие между враждебными юнитами
        if (
            active_unit.side != target_unit.side
            and active_unit.side is not None
            and target_unit.side is not None
        ):
            attack(active_unit, target_unit)
            for unit in selected_units:
                unit.active = False
            selected_units = []  # Очищаем список выбранных юнитов

    for row in range(4):
        for col in range(4):
            unit = units[row][col]
            if unit and not unit.is_alive():
                unit.side = None
                unit.number_soldiers = 0

    # Отрисовка гексагонов и юнитов
    screen.fill(WHITE)
    for row in range(4):
        for col in range(4):
            hexagon = hexagons[row][col]
            unit = units[row][col]

            # Рисуем гексагон с обводкой
            pygame.draw.polygon(
                screen,
                WHITE,
                [
                    (hexagon.x + HEX_SIZE, hexagon.y),
                    (hexagon.x + HEX_SIZE // 2, hexagon.y - HEX_HEIGHT // 2),
                    (hexagon.x - HEX_SIZE // 2, hexagon.y - HEX_HEIGHT // 2),
                    (hexagon.x - HEX_SIZE, hexagon.y),
                    (hexagon.x - HEX_SIZE // 2, hexagon.y + HEX_HEIGHT // 2),
                    (hexagon.x + HEX_SIZE // 2, hexagon.y + HEX_HEIGHT // 2),
                ],
            )
            pygame.draw.polygon(
                screen,
                BLACK,
                [
                    (hexagon.x + HEX_SIZE, hexagon.y),
                    (hexagon.x + HEX_SIZE // 2, hexagon.y - HEX_HEIGHT // 2),
                    (hexagon.x - HEX_SIZE // 2, hexagon.y - HEX_HEIGHT // 2),
                    (hexagon.x - HEX_SIZE, hexagon.y),
                    (hexagon.x - HEX_SIZE // 2, hexagon.y + HEX_HEIGHT // 2),
                    (hexagon.x + HEX_SIZE // 2, hexagon.y + HEX_HEIGHT // 2),
                ],
                LINE_WIDTH,
            )
            # Рисуем units
            pygame.draw.polygon(
                screen,
                unit.form_selection(),
                [
                    (unit.x + UNIT_SIZE, unit.y),
                    (unit.x + UNIT_SIZE // 2, unit.y - UNIT_HEIGHT // 2),
                    (unit.x - UNIT_SIZE // 2, unit.y - UNIT_HEIGHT // 2),
                    (unit.x - UNIT_SIZE, unit.y),
                    (unit.x - UNIT_SIZE // 2, unit.y + UNIT_HEIGHT // 2),
                    (unit.x + UNIT_SIZE // 2, unit.y + UNIT_HEIGHT // 2),
                ],
            )

            if unit.side is not None:
                # Отрисовка числа солдат внутри юнита (черным цветом)
                text_surface = font.render(
                    str(unit.number_soldiers),
                    True,
                    (0, 0, 0),
                )
                text_rect = text_surface.get_rect()
                text_rect.center = (unit.x, unit.y - 20)
                screen.blit(text_surface, text_rect)

                # Отрисовка изображения для типа юнита
                unit_image = unit_images.get(unit.unit_type)
                if unit_image:
                    image_rect = unit_image.get_rect()
                    image_rect.center = (
                        unit.x,
                        unit.y + 10,
                    )  # Под текстом
                    screen.blit(unit_image, image_rect)

    pygame.display.flip()

pygame.quit()
