import random
import math

import pygame

from core.constants import (
    HEX_HEIGHT,
    HEX_WIDTH,
    BLUE,
    GREEN,
    ORANGE,
    RED,
    WHITE,
    SCALE,
)
from core.image_dict import scaled_unit_images, scaled_command_images
from core.fonts_dict import scaled_font_dict


# Создание класса для представления юнита
class Unit:
    def __init__(self, x, y, row, col, side):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.side = side
        self.active = False
        self.protected = False
        self.unit_type = self.generate_unit_type()
        self.number_soldiers = self.generate_number_soldiers()
        # self.form = self.form_selection()

    # Генерируем случайный тип юнита
    def generate_unit_type(self):
        unit_types = ["knight", "spearman", "swordsman"]
        return random.choice(unit_types)

    # Визуальное отображение юнитов
    def form_selection(self):
        if self.side == "enemy":
            return RED if self.active else ORANGE  # Красный или оранжевый
        elif self.side == "player":
            return GREEN if self.active else BLUE
        # Зеленый или синий
        elif self.side is None:
            return WHITE
            # if self.active else (255, 255, 255)
        # белый

    # Генерируем случайное число солдат при создании юнита
    def generate_number_soldiers(self):
        return random.randint(25, 30)

    def can_swap_with(self, other_unit):
        # Проверка условий для обмена местами
        if (
            self.side == other_unit.side and self.side is not None
        ):  # Оба юнита принадлежат одному игроку
            return (
                # # Оба юнита принадлежат одному игроку
                # self.side == other_unit.side
                # # Если второй выбеленный объект пустой, а первый нет
                # or other_unit.side is None
                # and self.side is not None
                self.active
                and other_unit.active  # Оба юнита активны
                and abs(self.x - other_unit.x) < HEX_WIDTH * 1.1
                and abs(self.y - other_unit.y)
                < HEX_HEIGHT * 1.1  # Проверка расстояния между гексами
            )
        elif self.side is not None and other_unit.side is None:
            return (
                # # Оба юнита принадлежат одному игроку
                # self.side == other_unit.side
                # # Если второй выбеленный объект пустой, а первый нет
                # or other_unit.side is None
                # and self.side is not None
                self.active
                and other_unit.active  # Оба юнита активны
                and abs(self.x - other_unit.x) < HEX_WIDTH * 1.1
                and abs(self.y - other_unit.y)
                < HEX_HEIGHT * 1.1  # Проверка расстояния между гексами
            )

    # Расчет урона
    def damage_calculation(self, other_unit):
        if self.unit_type == "spearman":
            if other_unit.unit_type == "knight":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers / 1.5)
            elif other_unit.unit_type == "swordsman":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers * 1.5)
            elif other_unit.unit_type == "hero":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers*2)
            else:
                return self.number_soldiers - other_unit.number_soldiers
        elif self.unit_type == "swordsman":
            if other_unit.unit_type == "spearman":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers / 1.5)
            elif other_unit.unit_type == "knight":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers * 1.5)
            elif other_unit.unit_type == "hero":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers * 2)
            else:
                return self.number_soldiers - other_unit.number_soldiers
        elif self.unit_type == "knight":
            if other_unit.unit_type == "swordsman":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers / 1.5)
            elif other_unit.unit_type == "spearman":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers * 1.5)
            elif other_unit.unit_type == "hero":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers * 2)
            else:
                return self.number_soldiers - other_unit.number_soldiers
        elif self.unit_type == "hero":
            if other_unit.unit_type != "hero":
                return self.number_soldiers - math.ceil(other_unit.number_soldiers / 2)
            else:
                return self.number_soldiers - other_unit.number_soldiers

        # return self.number_soldiers - other_unit.number_soldiers

    # # Меняем тип юнита на Хероя, если юнит принадлежит врагу и находится на row=3
    # def check_for_promotion(self, hex_row):
    #     if self.side == "enemy" and hex_row == 3:
    #         self.unit_type = "hero"
    #     if self.side == "player" and hex_row == 0:
    #         self.unit_type = "hero"

    def move_to(self, target_unit, units):
        # Поменять местами координаты текущего юнита и целевого юнита
        self.x, target_unit.x = (target_unit.x, self.x)
        self.y, target_unit.y = (target_unit.y, self.y)

        # Замена координат после перемещения
        self.row, target_unit.row = (target_unit.row, self.row)
        self.col, target_unit.col = (target_unit.col, self.col)

        # Поменять местами их расположение в сетке
        units[self.row][self.col], units[target_unit.row][target_unit.col] = (
            units[target_unit.row][target_unit.col],
            units[self.row][self.col],
        )

        return units

    def attack(self, target_unit):
        if (
            self.side != target_unit.side
            and self.side is not None
            and target_unit.side is not None
            and self.active
            and target_unit.active
            and abs(self.x - target_unit.x) < HEX_WIDTH * 1.1
            and abs(self.y - target_unit.y) < HEX_HEIGHT * 1.1
        ):
            # Рассчитать урон для обоих юнитов и обновить их состояние
            self.number_soldiers, target_unit.number_soldiers = (
                self.damage_calculation(target_unit),
                target_unit.damage_calculation(self),
            )

            # Убрать мертвые юниты из игры
            # if self.number_soldiers <= 0:
            #     self.side = None
            #     self.number_soldiers = 0
            # if target_unit.number_soldiers <= 0:
            #     target_unit.side = None
            #     self.number_soldiers = 0

    def draw_unit(self, screen, font):
        # Рисуем units
        if self.side is not None:
            # pygame.draw.polygon(
            #     screen,
            #     self.form_selection(),
            #     [
            #         (self.x, self.y - UNIT_SIZE),
            #         (self.x + UNIT_HEIGHT // 2, self.y - UNIT_SIZE // 2),
            #         (self.x + UNIT_HEIGHT // 2, self.y + UNIT_SIZE // 2),
            #         (self.x, self.y + UNIT_SIZE),
            #         (self.x - UNIT_HEIGHT // 2, self.y + UNIT_SIZE // 2),
            #         (self.x - UNIT_HEIGHT // 2, self.y - UNIT_SIZE // 2),
            #     ],
            # )

            pygame.draw.circle(
                screen, self.form_selection(), (self.x, self.y + 12 * SCALE), 20 * SCALE
            )

            # Отрисовка числа солдат внутри юнита (черным цветом)
            scaled_font = scaled_font_dict.get("oswald_font_28")
            if scaled_font:
                text_surface = scaled_font.render(
                    str(self.number_soldiers),
                    True,
                    (0, 0, 0),
                )
                text_rect = text_surface.get_rect()
                text_rect.center = (self.x, self.y + 11 * SCALE)
                screen.blit(text_surface, text_rect)

            # Отрисовка изображения для типа юнита
            unit_image = scaled_unit_images.get(self.unit_type)
            if unit_image:
                image_rect = unit_image.get_rect()
                image_rect.center = (
                    self.x,
                    self.y,
                )  # Под текстом
                screen.blit(unit_image, image_rect)

    def draw_unit_protected(self, screen):
        # Отрисовка изображения защиты для юнита
        unit_image = scaled_command_images.get("Protection")
        if unit_image:
            image_rect = unit_image.get_rect()
            image_rect.center = (
                self.x,
                self.y,
            )  # Под текстом
            screen.blit(unit_image, image_rect)

    # Проверка на жизнеспособность
    def is_alive(self):
        return self.number_soldiers > 0

    # Уничтожаем юнит
    def destroy_unit(self):
        del self
