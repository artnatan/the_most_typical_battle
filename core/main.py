import pygame
import math

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Размер экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Размеры гексагональных тайлов
HEX_SIZE = 50
HEX_WIDTH = int(2 * HEX_SIZE)
HEX_HEIGHT = int(math.sqrt(3) * HEX_SIZE)

# Размеры юнита
UNIT_SIZE = 40
UNIT_WIDTH = int(2 * UNIT_SIZE)
UNIT_HEIGHT = int(math.sqrt(3) * UNIT_SIZE)

# Толщина линии для обводки гексагонов
LINE_WIDTH = 2

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hexagonal Grid")


# Создание класса для представления гексагональных тайлов
class Hexagon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False


# Создание класса для представления юнита
class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False


# Создание списка для хранения гексагональных тайлов и юнитов
hexagons = []
units = []

# Создание гексагональной сетки 4x4
for row in range(4):
    hexagons_row = []
    units_row = []

    start_x = (SCREEN_WIDTH - 4 * HEX_WIDTH * 0.75) / 2
    start_y = (SCREEN_HEIGHT - 4 * HEX_HEIGHT - HEX_HEIGHT * 0.5) / 2
    for col in range(4):
        x = start_x + col * HEX_WIDTH * 0.75
        y = start_y + row * HEX_HEIGHT
        if col % 2 < 1:
            y += HEX_HEIGHT * 0.5
        hexagon = Hexagon(x, y)
        hexagons_row.append(hexagon)

        # Создание юнита в центре гексагона
        unit = Unit(x, y)
        units_row.append(unit)
    hexagons.append(hexagons_row)
    units.append(units_row)

# Основной цикл игры
running = True
selected_unit = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Проверяем, на каком гексагоне было нажатие мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row in range(4):
                    for col in range(4):
                        hexagon = hexagons[row][col]
                        unit = units[row][col]

                        # Вычисляем расстояние от точки нажатия до центра гексагона
                        distance = math.sqrt(
                            (mouse_x - hexagon.x) ** 2 + (mouse_y - hexagon.y) ** 2
                        )
                        if distance < HEX_SIZE:
                            # Если юнит активен, делаем его неактивным, и наоборот
                            unit.active = not unit.active
                            if selected_unit is not None and selected_unit is not unit:
                                selected_unit.active = False
                            selected_unit = unit

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
                RED if unit.active else BLUE,
                [
                    (unit.x + UNIT_SIZE, unit.y),
                    (unit.x + UNIT_SIZE // 2, unit.y - UNIT_HEIGHT // 2),
                    (unit.x - UNIT_SIZE // 2, unit.y - UNIT_HEIGHT // 2),
                    (unit.x - UNIT_SIZE, unit.y),
                    (unit.x - UNIT_SIZE // 2, unit.y + UNIT_HEIGHT // 2),
                    (unit.x + UNIT_SIZE // 2, unit.y + UNIT_HEIGHT // 2),
                ],
            )
    pygame.display.flip()

pygame.quit()
