# Определение цветов
import math

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Размер экрана
SCREEN_WIDTH = 400
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
