import os
import pygame

# Определение пути к папке с музыкой
sounds_folder = os.path.join(os.path.dirname(__file__), "..", "sounds")


# Загрузка шрифтов
sounds_dict = {
    "preview_music": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "preview_music.mp3")),
    "main_music": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "main_music.mp3")),
    "click": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "click.mp3")),
    "attack": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "attack.mp3")),
    "move": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "move.mp3")),
    "catapult": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "catapult.mp3")),
    "crossbow": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "crossbow.mp3")),
    "reserve": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "reserve.mp3")),
    "protection": 
        pygame.mixer.Sound(os.path.join(sounds_folder, "protection.mp3")),
}

