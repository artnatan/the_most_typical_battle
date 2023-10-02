import random
import pygame
from core.constants import (
    HEX_HEIGHT,
    BLACK,
    RED,
    HEX_SIZE,
    LINE_WIDTH,
    WHITE,
)
from core.image_dict import scaled_background_images


# Создание класса для представления гексагональных тайлов
class Hexagon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False
        self.random_background = random.choice(scaled_background_images)
        self.points = self.calculate_points()

    def calculate_points(self):
        # Вычисляем координаты вершин гексагона на основе x и y
        points = [
            (self.x, self.y - HEX_SIZE),
            (self.x + HEX_HEIGHT // 2, self.y - HEX_SIZE // 2),
            (self.x + HEX_HEIGHT // 2, self.y + HEX_SIZE // 2),
            (self.x, self.y + HEX_SIZE),
            (self.x - HEX_HEIGHT // 2, self.y + HEX_SIZE // 2),
            (self.x - HEX_HEIGHT // 2, self.y - HEX_SIZE // 2),
        ]
        return points

    def border_points(self, side, col_num):
        points = [
            (self.x, self.y - HEX_SIZE),
            (self.x + HEX_HEIGHT // 2, self.y - HEX_SIZE // 2),
            (self.x + HEX_HEIGHT // 2, self.y + HEX_SIZE // 2),
            (self.x, self.y + HEX_SIZE),
            (self.x - HEX_HEIGHT // 2, self.y + HEX_SIZE // 2),
            (self.x - HEX_HEIGHT // 2, self.y - HEX_SIZE // 2),
        ]
        return points

    def draw_hexagon(self, screen):
        # Получаем координаты вершин гексагона из атрибута points
        hexagon_points = self.points

        # Рисуем гексагон с обводкой
        pygame.draw.polygon(screen, WHITE, hexagon_points)

        # Рисуем случайное изображение фона
        screen.blit(
            self.random_background, (self.x - HEX_SIZE * 0.9, self.y - HEX_SIZE * 1.05)
        )

        pygame.draw.polygon(
            screen, self.color_define(), hexagon_points, self.line_width_define()
        )

    def color_define(self):
        if self.active:
            return RED
        else:
            return BLACK

    def line_width_define(self):
        if self.active:
            return LINE_WIDTH + 4
        else:
            return LINE_WIDTH
