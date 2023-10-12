import random
import pygame
import math


from core.hexagon import Hexagon
from core.units import Unit

# Меню
from core.menu import Menu
from core.win_menu import WinMenu
from core.Preview import Preview
from core.InfoPanel import InfoPanel

# Команды
from core.commands.Catapult import Catapult
from core.commands.CrossbowVolley import CrossbowVolley
from core.commands.ArmyReserve import ArmyReserve
from core.commands.Protection import Protection

# # Определение констант
from core.constants import (
    SCREEN_WIDTH,
    ORANGE,
    BLUE,
    BLACK,
    WHITE,
    SCREEN_HEIGHT,
    HEX_SIZE,
    HEX_WIDTH,
    HEX_HEIGHT,
    BUTTON_BONUS_HEIGHT,
    BUTTON_BONUS_WIDTH,
    BUTTON_BONUS_COLOR,
)

from core.image_dict import scaled_command_images, scaled_menu_images
from core.fonts_dict import scaled_font_dict
from core.sounds_dict import sounds_dict


class HexagonalGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hexagonal Grid")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_status = "menu"
        self.return_game_status = ""
        # self.icon = scaled_menu_images.get("Logo")  # Загрузка иконки из файла

        #загрузка музыки
        self.click_sound = sounds_dict.get("click")
        self.main_music = sounds_dict.get("main_music")
        self.preview_music = sounds_dict.get("preview_music")
        #игровые звуки
        self.attack_sound = sounds_dict.get("attack")
        self.move_sound = sounds_dict.get("move")
        self.catapult_sound = sounds_dict.get("catapult")
        self.crossbow_sound = sounds_dict.get("crossbow")
        self.reserve_sound = sounds_dict.get("reserve")
        self.protection_sound = sounds_dict.get("protection")

        # константы
        # Размер экрана
        self.white = WHITE
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        # Размеры гексагональных тайлов
        self.hex_size = HEX_SIZE
        self.hex_width = HEX_WIDTH
        self.hex_height = HEX_HEIGHT

        self.button_bonus_height = BUTTON_BONUS_HEIGHT
        self.button_bonus_width = BUTTON_BONUS_WIDTH
        self.button_bonus_color = BUTTON_BONUS_COLOR

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Инициализация меню
        self.menu = Menu(self.screen)
        self.preview = Preview(self.screen)
        self.win_menu = WinMenu(self.screen)
        self.info_panel = InfoPanel(self.screen)

        # Инициализация игровых объектов
        self.hexagons = self.create_hexagons()
        self.units = self.create_units()
        self.commands = self.create_commands()

        # Другие переменные состояния игры
        self.font = pygame.font.Font(None, 24)
        self.start_x = self.get_start_x()
        self.start_y = self.get_start_y()
        self.selected_units = []
        self.active_command = False
        self.selected_units_command = []
        self.selected_hex_command = []
        self.current_player = "unknown"
        self.protected_unit = []
        self.command_block = False

        #инфо + дом кнопки
        self.info = scaled_menu_images.get("Info")
        self.info_scaled = self.get_size_button(self.info)
        self.info_rect = self.info_scaled.get_rect()
        self.info_rect.center = (self.screen_width*0.1, self.screen_height*0.12)

        self.home = scaled_menu_images.get("Home")
        self.home_scaled = self.get_size_button(self.home)
        self.home_rect = self.home_scaled.get_rect()
        self.home_rect.center = (self.screen_width*0.9, self.screen_height*0.12)

    def get_size_button(self, img):
        if SCREEN_HEIGHT > SCREEN_WIDTH:
            desired_width = int(img.get_width() * 0.6)
            desired_height = int(img.get_height() * 0.6)
            return pygame.transform.scale(img, (desired_width, desired_height))
        else:
            return img



    def get_start_x(self):
        return (self.screen_width - 3 * self.hex_width) / 2

    def get_start_y(self):
        return (self.screen_height - 3 * self.hex_height - self.hex_height * 0.5) / 2

    def create_hexagons(self):
        hexagons = []
        for row in range(4):
            hexagons_row = []
            for col in range(4):
                x = self.get_start_x() + col * self.hex_width
                y = self.get_start_y() + row * self.hex_height
                if row % 2 == 1:
                    x += self.hex_width * 0.5
                hexagon = Hexagon(x * 0.9, y * 0.9)
                hexagons_row.append(hexagon)
            hexagons.append(hexagons_row)
        return hexagons

    def create_units(self):
        units = []
        for row in range(4):
            units_row = []
            for col in range(4):
                x = self.get_start_x() + col * self.hex_width
                y = self.get_start_y() + row * self.hex_height
                if row % 2 == 1:
                    x += self.hex_width * 0.5
                unit = Unit(
                    x * 0.9,
                    y * 0.9,
                    row,
                    col,
                    side="enemy" if row < 2 else "player",
                )
                units_row.append(unit)
            units.append(units_row)
        return units

    def create_commands(self):
        commands = []
        top = (
            (self.screen_height - self.button_bonus_height) * 0.8
            if self.screen_width < self.screen_height
            else (self.screen_height - self.button_bonus_height) * 0.95
        )
        catapult = Catapult(
            False,
            "Catapult",
            pygame.Rect(
                self.screen_width * 0.01,
                top,
                self.button_bonus_width,
                self.button_bonus_height,
            ),
            self.button_bonus_color,
            scaled_command_images.get("Catapult"),
        )

        crossbow_volley = CrossbowVolley(
            False,
            "CrossbowVolley",
            pygame.Rect(
                self.screen_width * 0.26,
                top,
                self.button_bonus_width,
                self.button_bonus_height,
            ),
            self.button_bonus_color,
            scaled_command_images.get("CrossbowVolley"),
        )

        army_reserve = ArmyReserve(
            False,
            "ArmyReserve",
            pygame.Rect(
                self.screen_width * 0.51,
                top,
                self.button_bonus_width,
                self.button_bonus_height,
            ),
            self.button_bonus_color,
            scaled_command_images.get("ArmyReserve"),
        )

        protection = Protection(
            False,
            "Protection",
            pygame.Rect(
                self.screen_width * 0.76,
                top,
                self.button_bonus_width,
                self.button_bonus_height,
            ),
            self.button_bonus_color,
            scaled_command_images.get("Protection"),
        )

        commands.append(catapult)
        commands.append(crossbow_volley)
        commands.append(army_reserve)
        commands.append(protection)

        return commands

    def restart_game(self):
        # Восстановите начальные значения игровых объектов и переменных
        self.selected_units = []
        self.active_command = False
        self.selected_units_command = []
        self.current_player = "unknown"
        self.protected_unit = []
        self.command_block = False

        # Очистите экран и перерисуйте начальное состояние игры
        self.screen.fill((0, 0, 0))  # Очистить экран черным цветом

        self.units = self.create_units()
        self.commands = self.create_commands()
        self.draw()  # Перерисовать начальное состояние

    def run(self):
        # pygame.display.set_icon(self.icon)
        self.preview_music.play()
        self.preview.show()
        self.main_music.play(-1)
        while self.running:

            match self.game_status:
                case "menu":
                    self.game_status = self.menu.show()
                    if self.game_status == "info":
                        self.return_game_status = "menu"

                    game = True

                case "info":
                    self.game_status = self.info_panel.show(self.return_game_status)
                    game = True

                case "game":
                    game = True
                    while game:
                        if self.current_player == "unknown":
                            self.player_switch()

                        for command in self.commands:
                            if command.active:
                                self.execute_command(command)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game = False
                                self.running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if self.home_rect.collidepoint(event.pos):
                                    game = False
                                    self.click_sound.play()
                                    self.game_status = "menu"
                                    self.restart_game()
                                elif self.info_rect.collidepoint(event.pos):
                                    game = False
                                    self.click_sound.play()
                                    self.game_status = "info"
                                    self.return_game_status = "game"

                                self.handle_mouse_click()



                        self.update()
                        self.draw()
                        if self.win_units_check("player") or self.win_units_check(
                            "enemy"
                        ):
                            game = False
                            self.game_status = "win_menu"

                        pygame.display.flip()
                        self.clock.tick(30)

                case "win_menu":
                    # win_menu_shown = True
                    # while win_menu_shown:
                    win = self.win_units_counter()
                    self.game_status = self.win_menu.show(win)
                    self.restart_game()
                    game = True
                    # w in_menu_shown = False

        pygame.quit()

    def player_switch(self):
        if self.current_player == "player":
            self.current_player = "enemy"
        elif self.current_player == "enemy":
            self.current_player = "player"
        elif self.current_player == "unknown":
            self.current_player = random.choice(["player", "enemy"])
        self.choice_rnd_command()

    def enemy_units_counter(self):
        enemy_units_count = 0
        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]
                if (
                    unit.side != self.current_player
                    and unit.side is not None
                    and unit.protected is False
                ):
                    enemy_units_count += 1
        return enemy_units_count

    def player_units_counter(self):
        player_units_count = 0
        enemy_units_count = 0
        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]
                if (
                    unit.side == self.current_player
                    and unit.side is not None
                    and unit.protected is False
                ):
                    player_units_count += 1

                if (
                    unit.side != self.current_player
                    and unit.side is not None
                    and unit.protected is False
                ):
                    enemy_units_count += 1
        if player_units_count ==1 or enemy_units_count == 1:
            return True

    def win_units_counter(self):
        blue_units_count = 0
        orange_units_count = 0
        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]
                if (
                    unit.side == "player"
                    and unit.side is not None
                    and unit.protected is False
                ):
                    blue_units_count += 1

                if (
                    unit.side == "enemy"
                    and unit.side is not None
                    and unit.protected is False
                ):
                    orange_units_count += 1
        if blue_units_count == 0:
            return "enemy"        
        elif orange_units_count == 0:
            return "player"

    def win_units_check(self, side):
        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]
                if unit.side == side:
                    return False
        return True

    # def execute_command(self, command):
    #     if command.name == "Catapult" and len(self.selected_units_command) == 1:
    #         if self.selected_units_command[0].side != self.current_player:
    #             command.apply(
    #                 self.selected_units_command[0]
    #             )  # Вызов функции применения бонуса
    #             command.active = False
    #             self.active_command = False
    #             self.command_block = True
    #         self.clear_selected_units_command()

    #     elif command.name == "CrossbowVolley":
    #         enemy_count = self.enemy_units_counter()
    #         if enemy_count >= 3 and len(self.selected_units_command) == 3:
    #             for unit in self.selected_units_command:
    #                 if unit.side != self.current_player:
    #                     command.apply(
    #                         unit
    #                     )  # Вызов функции применения бонуса если выбранно 3 гекса
    #                     command.active = False
    #                     self.active_command = False
    #                     self.command_block = True
    #             self.clear_selected_units_command()

    #         elif len(self.selected_units_command) == enemy_count:
    #             for unit in self.selected_units_command:
    #                 if unit.side != self.current_player:
    #                     command.apply(
    #                         unit
    #                     )  # Вызов функции применения бонуса если противника < 3
    #                     command.active = False
    #                     self.active_command = False
    #                     self.command_block = True
    #             self.clear_selected_units_command()

    #     elif command.name == "ArmyReserve" and len(self.selected_units_command) == 1:
    #         for unit in self.selected_units_command:
    #             if unit.side == self.current_player:
    #                 command.apply(
    #                     self.selected_units_command[0]
    #                 )  # Вызов функции применения бонуса
    #                 command.active = False
    #                 self.active_command = False
    #                 self.command_block = True
    #             elif unit.side == None:
    #                 if self.current_player == "player" and unit.row in [2, 3]:
    #                     unit.side = self.current_player
    #                     unit.generate_unit_type()
    #                     command.apply(self.selected_units_command[0])
    #                 elif self.current_player == "enemy" and unit.row in [0, 1]:
    #                     unit.side = self.current_player
    #                     unit.generate_unit_type()
    #                     command.apply(self.selected_units_command[0])
    #                 command.active = False
    #                 self.active_command = False
    #                 self.command_block = True
    #         self.clear_selected_units_command()

    #     elif command.name == "Protection" and len(self.selected_units_command) == 1:
    #         for unit in self.selected_units_command:
    #             if unit.side == self.current_player:
    #                 self.protected_unit.append(
    #                     {
    #                         "side": self.current_player,
    #                         "value": True,
    #                         "unit": self.selected_units_command[0],
    #                     }
    #                 )
    #                 command.apply(
    #                     self.selected_units_command[0]
    #                 )  # Вызов функции применения бонуса
    #                 command.active = False
    #                 self.active_command = False
    #                 self.command_block = True

    #         self.clear_selected_units_command()

    def execute_command(self, command):
        if command.name == "CrossbowVolley":
            for _ in range(3):
                self.rnd_choice_hex()
        else:
            self.rnd_choice_hex()
        self.draw()
        command.play_sound(command.sound_name)
        pygame.time.delay(3000)

        if command.name == "Catapult":

            command.apply(
                self.selected_units_command[0]
            )  # Вызов функции применения бонуса
            command.active = False
            self.active_command = False
            self.command_block = True
            
            self.clear_selected_units_command()

        elif command.name == "CrossbowVolley":
            for unit in self.selected_units_command:

                command.apply(
                    unit
                )  # Вызов функции применения бонуса если выбранно 3 гекса
                command.active = False
                self.active_command = False
                self.command_block = True
                
            
            self.clear_selected_units_command()

        elif command.name == "ArmyReserve":
            for unit in self.selected_units_command:
                if unit.side is not None:
                    command.apply(
                        self.selected_units_command[0]
                    )  # Вызов функции применения бонуса
                    command.active = False
                    self.active_command = False
                    self.command_block = True
                elif unit.side is None:
                    unit.unit_type = unit.generate_unit_type()
                    unit.number_soldiers = 0
                    if unit.row in [2, 3]:
                        unit.side = "player"
                    elif unit.row in [0, 1]:
                        unit.side = "enemy"
                    command.apply(self.selected_units_command[0])

                    command.active = False
                    self.active_command = False
                    self.command_block = True
            
            self.clear_selected_units_command()

        elif command.name == "Protection":
            for unit in self.selected_units_command:
                self.protected_unit.append(
                    {
                        "side": self.current_player,
                        "value": True,
                        "unit": self.selected_units_command[0],
                    }
                )

                command.apply(
                    self.selected_units_command[0]
                )  # Вызов функции применения бонуса
                command.active = False
                self.active_command = False
                self.command_block = True
            
            self.clear_selected_units_command()

        for hex in self.selected_hex_command:
            hex.active = False
        self.selected_hex_command = []
        self.update()
        self.draw()

    def clear_selected_units(self):
        if len(self.selected_units) > 0:
            for unit in self.selected_units:
                unit.active = False
            self.selected_units = []  # Очищаем список выбранных юнитов

    def clear_selected_units_command(self):
        if len(self.selected_units_command) > 0:
            for unit in self.selected_units_command:
                unit.active = False
            self.selected_units_command = []  # Очищаем список выбранных юнитов

    def add_unit_selected_list(self, hexagon):
        for row in self.units:
            for unit in row:
                if unit.x == hexagon.x and unit.y == hexagon.y:
                    if (
                        unit.side == self.current_player
                        or len(self.selected_units) == 1
                    ):
                        if unit not in self.selected_units and unit.protected is False:
                            self.selected_units.append(unit)  # Добавляем выбранный юнит
                            unit.active = True
                        elif unit in self.selected_units:
                            # Если юнит уже был выбран, убираем его из выбранных
                            self.selected_units.remove(unit)
                            unit.active = False

    def add_unit_selected_list_command(self, hexagon):
        for row in self.units:
            for unit in row:
                if unit.x == hexagon.x and unit.y == hexagon.y:
                    if unit not in self.selected_units_command:
                        if unit.protected is False:
                            self.selected_units_command.append(
                                unit
                            )  # Добавляем выбранный юнит
                            unit.active = True
                    else:
                        # Если юнит уже был выбран, убираем его из выбранных
                        self.selected_units_command.remove(unit)
                        unit.active = False

    def check_click_command_button(self, event):
        for command in self.commands:
            if command.rect.collidepoint(event.pos) and command.active:
                self.clear_selected_units()
                self.clear_selected_units_command()
                command.active = not command.active
                self.active_command = command.active
            elif command.rect.collidepoint(event.pos):
                for c in self.commands:
                    c.active = False
                self.clear_selected_units()
                command.active = not command.active
                self.active_command = command.active

    def choice_rnd_command(self):
        command = random.choice(self.commands)
        if command.name == "Protection":
            while command.name == "Protection" and self.player_units_counter():
                command = random.choice(self.commands)
        for c in self.commands:
            if command == c:
                self.clear_selected_units()
                self.clear_selected_units_command()
                command.active = not command.active
                self.active_command = command.active
                self.command_block = True
            # else:
            #     c.block = True

    def check_click(self):
        # self.check_click_command_button(event)  # проверяем нажатие кнопки комантд

        if self.active_command:
            # проверяем клики по гексам
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for row in self.hexagons:
                for hexagon in row:
                    # Вычисляем расстояние от точки нажатия до центра гексагона
                    distance = math.sqrt(
                        (mouse_x - hexagon.x) ** 2 + (mouse_y - hexagon.y) ** 2
                    )
                    if distance < self.hex_size:
                        # Проверяем, был ли выбран юнит на этом гексе
                        self.add_unit_selected_list_command(hexagon)

    def rnd_choice_hex(self):
        # Случайно выбираем строку и столбец из таблицы
        repeat_hex = True
        while repeat_hex:
            random_row = random.randint(0, 3)  # Выбор случайной строки от 0 до 3
            random_column = random.randint(0, 3)  # Выбор случайного столбца от 0 до 3
            random_hexagon = self.hexagons[random_row][random_column]
            if random_hexagon not in self.selected_hex_command:
                random_hexagon.active = True
                self.selected_hex_command.append(random_hexagon)

                unit = self.units[random_row][random_column]
                if unit not in self.selected_units_command:
                    if unit.protected is False:
                        self.selected_units_command.append(
                            unit
                        )  # Добавляем выбранный юнит
                        unit.active = True
                        repeat_hex = False

    def hex_click_check(self):
        # проверяем клики по гексам
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row in self.hexagons:
            for hexagon in row:
                # Вычисляем расстояние от точки нажатия до центра гексагона
                distance = math.sqrt(
                    (mouse_x - hexagon.x) ** 2 + (mouse_y - hexagon.y) ** 2
                )
                if distance < self.hex_size:
                    # Проверяем, был ли выбран юнит на этом гексе
                    self.add_unit_selected_list(hexagon)

    def handle_mouse_click(self):
        # Обработка клика мыши
        # if event.button == 1:  # Левая кнопка мыши
        # self.check_click()
        # for command in self.commands:
        #     if command.active:
        #         self.execute_command(command)

        if not self.active_command:
            self.hex_click_check()

        # Если выбрано два юнита, проверьте, можно ли переместить или атаковать
        if len(self.selected_units) == 2:
            active_unit, target_unit = (
                self.selected_units[0],
                self.selected_units[1],
            )

            # Попробовать переместить юниты
            if active_unit.can_swap_with(target_unit):
                self.move_sound.play()
                self.units = active_unit.move_to(target_unit, self.units)
                self.additional_actions()

            # Попробовать атаковать юниты
            if (
                active_unit.side != target_unit.side
                and active_unit.side is not None
                and target_unit.side is not None
            ):
                self.attack_sound.play()
                active_unit.attack(target_unit)
                if active_unit.number_soldiers > 0 and target_unit.number_soldiers <= 0:
                    self.units = active_unit.move_to(target_unit, self.units)
                self.additional_actions()

            self.clear_selected_units()

    def additional_actions(self):
        # Очистить выбранные юниты после действия
        self.clear_selected_units()
        # Принудительный апдейт, чтобы пересчитать перед сменой игрока
        self.update()
        # Поменять игрока
        self.player_switch()
        # проверка на защиту
        for p_unit in self.protected_unit:
            if p_unit["side"] == self.current_player:
                p_unit["value"] = False

        # включить возможность выбора приказа
        self.command_block = False

    def update_coord_units(self):
        units_update = self.units.copy()
        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]
                units_update[unit.row][unit.col] = unit

        self.units = units_update

    def update(self):
        for command in self.commands:
            if self.command_block is True and not command.active:
                command.block = True
            else:
                False

        for row in range(4):
            for col in range(4):
                unit = self.units[row][col]

                if unit.side is not None and not unit.is_alive():
                    unit.side = None
                    unit.number_soldiers = 0

                # Меняем тип юнита на Хероя
                if row == 3 and unit.side == "enemy":
                    unit.unit_type = "hero"
                elif row == 0 and unit.side == "player":
                    unit.unit_type = "hero"

                # Забираем защиту у юнита
                for p_unit in self.protected_unit:
                    if p_unit["value"] is False and p_unit["unit"] == unit:
                        unit.protected = False
                        self.protected_unit.remove(p_unit)

    def draw_info_text(self, screen):
        oswald_font = scaled_font_dict.get("oswald_font")

        # Определяем текст и цвет в зависимости от текущего игрока
        text = (
            "Blue Commander" if self.current_player == "player" else "Orange Commander"
        )
        text_color = BLUE if self.current_player == "player" else ORANGE

        # Создаем объект Font для отображения текста

        # Создаем текстовую поверхность
        text_surface = oswald_font.render(text, True, text_color)

        # Определяем позицию для отображения текста (над гексовым полем)
        text_x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
        text_y = 20  # Вы можете настроить вертикальное положение под свой дизайн

        # Создаем прямоугольник для текста с белым фоном
        text_rect = pygame.Rect(
            text_x - 5,
            text_y - 5,
            text_surface.get_width() + 10,
            text_surface.get_height() + 5,
        )

        # Заполняем прямоугольник белым цветом (фон)
        pygame.draw.rect(screen, WHITE, text_rect, border_radius=15)

        # Рисуем черную границу вокруг прямоугольника текста
        pygame.draw.rect(screen, BLACK, text_rect, 3, 15)

        # Отображаем текстовую поверхность на экране
        screen.blit(text_surface, (text_x, text_y))
        self.screen.blit(self.info_scaled,self.info_rect)
        self.screen.blit(self.home_scaled,self.home_rect)

    def draw_top_border(self, screen):
        # Цвет линии верхней границы гексовой сетки
        line_color = ORANGE if self.current_player == "enemy" else BLUE

        # Создаем список для хранения точек верхних границ гексов
        top_border_points = []

        # Собираем точки верхних границ гексов
        for hexagon in self.hexagons[0]:
            top_border_points.append(
                hexagon.border_points("top", self.hexagons[0].index(hexagon))[2]
            )  # Верхний левый угол гекса
            top_border_points.append(
                hexagon.border_points("top", self.hexagons[0].index(hexagon))[1]
            )  # Верхний правый угол гекса

        # Соединяем верхние границы гексов, создавая непрерывную линию
        pygame.draw.lines(
            screen,
            line_color,
            False,  # Замкнутая линия (False для открытой линии)
            top_border_points,  # Исключаем самую левую и самую правую точки
            6,  # Толщина линии
        )

    def draw_bottom_border(self, screen):
        # Цвет линии нижней границы гексовой сетки
        line_color = ORANGE if self.current_player == "enemy" else BLUE

        # Создаем список точек для нижней границы
        bottom_border_points = []

        # Обходим гексы в нижнем ряду
        for hexagon in self.hexagons[-1]:
            # Добавляем верхний правый и верхний левый угол гекса в список точек
            bottom_border_points.append(
                hexagon.border_points("bottom", self.hexagons[-1].index(hexagon))[4]
            )  # Верхний правый угол гекса
            bottom_border_points.append(
                hexagon.border_points("bottom", self.hexagons[-1].index(hexagon))[5]
            )  # Верхний левый угол гекса

        # Отрисовка нижней границы гексовой сетки
        pygame.draw.lines(
            screen,
            line_color,
            False,  # Замкнутая линия (False для открытой линии)
            bottom_border_points,  # Исключаем самую левую и самую правую точки
            6,  # Толщина линии
        )

    def draw(self):
        
        # Отрисовка состояния игры
        self.screen.fill(self.white)
        if SCREEN_HEIGHT > SCREEN_WIDTH:
            bg_image = scaled_menu_images.get("BG_4")
        else:
            bg_image = scaled_menu_images.get("BG_5")

        background_image = pygame.transform.scale(
            bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.screen.blit(background_image, (0, 0))

        for row in range(4):
            for col in range(4):
                hexagon = self.hexagons[row][col]
                unit = self.units[row][col]
                hexagon.draw_hexagon(self.screen)
                unit.draw_unit(self.screen, self.font)

                if unit.protected is True:
                    unit.draw_unit_protected(self.screen)

        for command in self.commands:
            command.draw(self.screen)

        # Отрисовка верхней и нижней границ гексовой сетки и теста
        # self.draw_top_border(self.screen)
        # self.draw_bottom_border(self.screen)
        self.draw_info_text(self.screen)

        pygame.display.flip()


# if __name__ == "__main__":
#     game = HexagonalGame()
#     game.run()
