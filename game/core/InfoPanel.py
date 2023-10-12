from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from core.fonts_dict import scaled_font_dict
from core.image_dict import scaled_menu_images
from core.sounds_dict import sounds_dict


import pygame


import sys


class InfoPanel:
    def __init__(self, screen):
        self.screen = screen
        self.ok_img = self.get_scale_img()

        self.click_sound = sounds_dict.get("click")

        self.ok_rect = self.ok_img.get_rect()
        self.ok_rect.center = (SCREEN_WIDTH // 2, self.get_height())

        self.font = scaled_font_dict.get("oswald_font")
        self.radius = 15

    def get_scale_img(self):
        img = scaled_menu_images.get("Ok")
        if SCREEN_HEIGHT > SCREEN_WIDTH:
            return pygame.transform.scale(
                img, (img.get_width() * 0.7, img.get_height() * 0.7)
            )
        else:
            return img

    def get_height(self):
        return (
            SCREEN_HEIGHT * 0.9
            if SCREEN_WIDTH < SCREEN_HEIGHT
            else SCREEN_HEIGHT * 0.85
        )

    def show(self, return_back):
        info_panel_running = True
        while info_panel_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ok_rect.collidepoint(event.pos):
                        self.click_sound.play()
                        info_panel_running = False
                        return return_back

            if SCREEN_HEIGHT > SCREEN_WIDTH:
                bg_image = scaled_menu_images.get("Info_manual_1")
            else:
                bg_image = scaled_menu_images.get("Info_manual_2")

            background_image = pygame.transform.scale(
                bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            self.screen.blit(background_image, (0, 0))

            self.screen.blit(self.ok_img, self.ok_rect)

            pygame.display.flip()
