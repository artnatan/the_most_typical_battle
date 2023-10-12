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
from core.sounds_dict import sounds_dict


class WinMenu:
    def __init__(self, screen):
        self.screen = screen
        self.repeat_image = scaled_menu_images.get("Repeat")
        self.home_image = scaled_menu_images.get("Home")

        self.click_sound = sounds_dict.get("click")

        self.repeat_rect = self.repeat_image.get_rect()
        self.repeat_rect.center = (SCREEN_WIDTH * 0.25, self.get_height())
        self.home_rect = self.home_image.get_rect()
        self.home_rect.center = (SCREEN_WIDTH * 0.75, self.get_height())
        self.font = scaled_font_dict.get("oswald_font")
        self.radius = 15

    def get_height(self):
        return (
            (SCREEN_HEIGHT - self.repeat_rect.height) * 0.8
            if SCREEN_WIDTH < SCREEN_HEIGHT
            else SCREEN_HEIGHT * 0.85
        )

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
                        self.click_sound.play()
                        menu_running = False
                        return "game"
                    elif self.home_rect.collidepoint(event.pos):
                        # выход в меню
                        self.click_sound.play()
                        menu_running = False
                        return "menu"

            self.screen.fill(UNKNOWN_1)

            if SCREEN_HEIGHT > SCREEN_WIDTH:
                bg_image = scaled_menu_images.get("BG_pre")
            else:
                bg_image = scaled_menu_images.get("BG_pre_1")

            background_image = pygame.transform.scale(
                bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )


            text = "Blue WIN" if current_player == "player" else "Orange WIN"
            text_color = BLUE if current_player == "player" else ORANGE

            # Получаем размеры текста
            text_surface = self.font.render(text, True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (SCREEN_WIDTH //2, SCREEN_HEIGHT//2)

            # рисуем фон и кнопки
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(self.repeat_image, self.repeat_rect)
            self.screen.blit(self.home_image, self.home_rect)
            # Отображаем текст
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
