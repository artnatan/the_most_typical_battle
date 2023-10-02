import pygame
import sys

from core.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    UNKNOWN_1,
    ORANGE,
    BLACK,
    BLUE,
)

from core.image_dict import scaled_menu_images
from core.fonts_dict import scaled_font_dict


class WinMenu:
    def __init__(self, screen):
        self.screen = screen
        self.repeat_image = scaled_menu_images.get("Repeat")
        self.home_image = scaled_menu_images.get("Home")

        self.repeat_rect = self.repeat_image.get_rect()
        self.repeat_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.4)
        self.home_rect = self.home_image.get_rect()
        self.home_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 0.6)
        self.font = scaled_font_dict.get("oswald_font")
        self.radius = 15

    def show(self, current_player):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.repeat_rect.collidepoint(event.pos):
                        # перезапуск игры
                        menu_running = False
                        return "game"
                    elif self.home_rect.collidepoint(event.pos):
                        # выход в меню
                        menu_running = False
                        return "menu"

            self.screen.fill(UNKNOWN_1)

            if SCREEN_HEIGHT > SCREEN_WIDTH:
                bg_image = scaled_menu_images.get("BG_win_1")
            else:
                bg_image = scaled_menu_images.get("BG_win_2")

            background_image = pygame.transform.scale(
                bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            self.screen.blit(background_image, (0, 0))
            pygame.draw.rect(self.screen, WHITE, self.repeat_rect, border_radius=15)
            pygame.draw.rect(
                self.screen, ORANGE, self.repeat_rect, 5, 15
            )  # Рамка вокруг кнопки повтор
            pygame.draw.rect(self.screen, WHITE, self.home_rect, border_radius=15)
            pygame.draw.rect(
                self.screen, ORANGE, self.home_rect, 5, 15
            )  # Рамка вокруг кнопки домой

            text = "Blue WIN" if current_player == "player" else "Orange WIN"
            text_color = BLUE if current_player == "player" else ORANGE

            # Получаем размеры текста
            text_surface = self.font.render(text, True, text_color)
            text_rect = text_surface.get_rect()

            # Создаем прямоугольник для текста с белым фоном
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            # Заполняем прямоугольник белым цветом (фон)
            pygame.draw.rect(self.screen, WHITE, text_rect, border_radius=15)

            # Рисуем черную границу вокруг прямоугольника текста
            pygame.draw.rect(self.screen, BLACK, text_rect, 3, 15)

            self.screen.blit(self.repeat_image, self.repeat_rect)
            self.screen.blit(self.home_image, self.home_rect)

            # Отображаем текстовую поверхность внутри прямоугольника
            self.screen.blit(text_surface, text_rect.topleft)

            pygame.display.flip()
