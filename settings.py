import os
import sys
import pygame

class Settings:
    """
    Класс Settings хранит все настройки игры, такие как размеры экрана, пути к ресурсам и параметры текста.
    """

    def __init__(self):
        """
        Инициализация настроек игры с заданными значениями по умолчанию.
        """
        self.screen_width = 1280
        self.screen_height = 720
        self.base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.bg_image_path = os.path.join(self.base_path, 'images', 'PNG_bg', 'Battleground2', 'Bright', 'Battleground2.png')
        self.icon_path = os.path.join(self.base_path, 'images', 'icon.png')
        self.font_path = os.path.join(self.base_path, 'fonts', 'Roboto-Bold.ttf')
        self.font_size = 40
        self.start_text = 'Hello, Player'
        self.text_color = 'White'
        self.text_bg_color = 'Purple'

    def load_resources(self):
        """
        Загрузка ресурсов игры, таких как изображения фона, иконка и шрифт.
        """
        self.bg_image = pygame.image.load(self.bg_image_path).convert_alpha()
        self.icon = pygame.image.load(self.icon_path).convert_alpha()
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.start_text_surface = self.font.render(self.start_text, True, self.text_color, self.text_bg_color)