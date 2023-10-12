# Класс для меню
from core.constants import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, ORANGE
from core.fonts_dict import scaled_font_dict
from core.image_dict import scaled_menu_images


import pygame


class Preview:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.get_font()
        self.start_time = pygame.time.get_ticks()  # Получаем время в миллисекундах

    def get_font(self):
        font = "oswald_font" if SCREEN_HEIGHT > SCREEN_WIDTH else "oswald_font_86"
        return scaled_font_dict.get(font)

    def show(self):
        preview = True
        while preview:
            if SCREEN_HEIGHT > SCREEN_WIDTH:
                bg_image = scaled_menu_images.get("BG_pre")
            else:
                bg_image = scaled_menu_images.get("BG_pre_1")

            background_image = pygame.transform.scale(
                bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            self.screen.blit(background_image, (0, 0))

            # Определяем текст и его цвет в зависимости от времени
            current_time = pygame.time.get_ticks()  # Получаем текущее время

            if (
                current_time - self.start_time < 6000
            ):  # Показываем первый текст в течение 3 секунд
                text = "Calabaraburus"
                text_color = BLACK

            else:
                text = "presents"
                text_color = BLACK

            text = self.font.render(text, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(text, text_rect)

            pygame.display.flip()  # Обновляем отображение

            if current_time - self.start_time > 8000:
                preview = False
