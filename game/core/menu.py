import pygame
import sys

from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH

from core.image_dict import scaled_menu_images
from core.fonts_dict import scaled_font_dict
from core.sounds_dict import sounds_dict


# Класс для меню
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.singleplayer_image = scaled_menu_images.get("Info")
        self.multiplayer_image = scaled_menu_images.get("MultiPlayer")

        self.click_sound = sounds_dict.get("click")

        self.singleplayer_rect = self.singleplayer_image.get_rect()
        self.singleplayer_rect.center = (SCREEN_WIDTH * 0.25, self.get_height())
        self.multiplayer_rect = self.multiplayer_image.get_rect()
        self.multiplayer_rect.center = (SCREEN_WIDTH * 0.75, self.get_height())
        self.font = scaled_font_dict.get("oswald_font")
        self.radius = 15

    def get_height(self):
        return (
            SCREEN_HEIGHT * 0.85
            if SCREEN_WIDTH < SCREEN_HEIGHT
            else SCREEN_HEIGHT * 0.85
        )

    def show(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.singleplayer_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        # открыть инфо о игре
                        menu_running = False
                        return "info"
                    elif self.multiplayer_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        # Запускаем игру в режиме MultiPlayer
                        menu_running = False
                        return "game"

            if SCREEN_HEIGHT > SCREEN_WIDTH:
                bg_image = scaled_menu_images.get("BG")
            else:
                bg_image = scaled_menu_images.get("BG_1")

            background_image = pygame.transform.scale(
                bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(self.singleplayer_image,self.singleplayer_rect)
            self.screen.blit(self.multiplayer_image,self.multiplayer_rect)
            # pygame.draw.rect(
            #     self.screen, WHITE, self.singleplayer_rect, border_radius=15
            # )
            # pygame.draw.rect(
            #     self.screen, BLACK, self.singleplayer_rect, 5, 15
            # )  # Рамка вокруг кнопки SinglePlayer
            # pygame.draw.rect(
            #     self.screen, WHITE, self.multiplayer_rect, border_radius=15
            # )
            # pygame.draw.rect(
            #     self.screen, BLACK, self.multiplayer_rect, 5, 15
            # )  # Рамка вокруг кнопки MultiPlayer
            # self.screen.blit(self.singleplayer_image, self.singleplayer_rect)
            # self.screen.blit(self.multiplayer_image, self.multiplayer_rect)
            # text = self.font.render("My Most Typical Battle", True, ORANGE)
            # text_rect = text.get_rect()
            # text_rect.center = (SCREEN_WIDTH // 2, 50)
            # self.screen.blit(text, text_rect)
            pygame.display.flip()


