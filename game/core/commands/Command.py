import pygame


class Command:
    def __init__(self, active, name, rect, color, image=None):
        self.active = active
        self.name = name
        self.rect = rect  # Прямоугольник кнопки
        # self.text = text  # Текст на кнопке
        self.block = False
        self.color = color  # Цвет кнопки
        self.image = image  # Изображение для отображения в центре кнопки
        self.border_line_width = 4
        self.border_color = (0, 0, 0)
        self.radius = 15

    def draw(self, screen):
        # Отрисовка кнопки
        pygame.draw.rect(
            screen, self.color_define(), self.rect, border_radius=self.radius
        )
        # Отрисовка рамки
        pygame.draw.rect(
            screen,
            self.border_color,
            self.rect,
            self.border_line_width,
            self.radius,
        )
        # Отрисовка изображения, если оно задано
        if self.image:
            image_rect = self.image.get_rect()
            image_rect.center = self.rect.center
            screen.blit(self.image, image_rect)

        # Отрисовка текста
        # text_surface = font.render(self.text, True, self.text)
        # text_rect = text_surface.get_rect()
        # text_rect.center = self.rect.center
        # screen.blit(text_surface, text_rect)

    def handle_click(self, mouse_x, mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.active = not self.active

    def color_define(self):
        if self.active:
            return (255, 255, 204, 128)
        elif self.block:
            return (150, 150, 150, 128)
        else:
            return self.color

    def play_sound(self,sound):
        sound.play()
        