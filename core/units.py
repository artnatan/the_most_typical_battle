import random
from constants import HEX_HEIGHT, HEX_WIDTH


# Создание класса для представления юнита
class Unit:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side
        self.active = False
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
            return (
                (255, 0, 0) if self.active else (255, 165, 0)
            )  # Красный или оранжевый
        elif self.side == "player":
            return (0, 128, 0) if self.active else (0, 0, 255)  # Зеленый или синий
        elif self.side == None:
            return (255, 255, 255) if self.active else (255, 255, 255)  # ,белый

    # Генерируем случайное число солдат при создании юнита
    def generate_number_soldiers(self):
        return random.randint(20, 30)

    def can_swap_with(self, other_unit):
        # Проверка условий для обмена местами
        return (
            self.side == other_unit.side  # Оба юнита принадлежат одному игроку
            or other_unit.side
            == None  # Если второй выбеленный объект пустой, а первый нет
            and self.side != None
            and self.active
            and other_unit.active  # Оба юнита активны
            and abs(self.x - other_unit.x) < HEX_WIDTH * 1.1
            and abs(self.y - other_unit.y)
            < HEX_HEIGHT * 1.1  # Проверка расстояния между гексами
        )

    # Расчет урона
    def damage_calculation(self, damage):
        self.number_soldiers -= damage

    # Проверка на жизнеспособность
    def is_alive(self):
        return self.number_soldiers > 0

    # Уничтожаем юнит
    def destroy_unit(self):
        del self
