import pygame
from settings import Settings
from shinobi import Shinobi
from monster import Monster, Monsters
from controller import Controller
import time
import random

class FightersAdventures:
    """
    Класс FightersAdventures управляет основным игровым циклом, обработкой событий, обновлением состояния игры и отрисовкой.
    """

    def __init__(self):
        """
        Инициализация игры, загрузка ресурсов и установка начальных значений.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.load_resources()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Fighters Adventures")
        pygame.display.set_icon(self.settings.icon)
        self.player = Shinobi()
        self.controller = Controller(self.player)
        self.monsters = Monsters()
        self.running = True
        self.gameplay = False  # Начинаем с меню
        self.in_menu = True
        self.score = 0
        self.death_time = None
        self.bg_x = 0  # Положение фона по оси X
        self.bg_speed = 5  # Скорость движения фона
        self.next_monster_spawn_time = time.time() + random.randint(6, 10)  # Время до следующего спавна монстра
        self.killed_monsters_count = 0  # Счетчик убитых монстров

        # Загрузка изображения фона для меню
        self.menu_bg_image = pygame.image.load('src/images/PNG_bg/Battleground2/Bright/Battleground2.png').convert()
        # Загрузка изображения фона для экрана после смерти
        self.game_over_bg_image = pygame.image.load('src/images/PNG_bg/Battleground4/Bright/Battleground4.png').convert()
        # Загрузка изображения логотипа
        self.logo_image = pygame.image.load('src/images/logo.png').convert_alpha()

    def handle_events(self):
        """
        Обработка событий, таких как нажатия клавиш и закрытие окна.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.in_menu:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                elif not self.gameplay:
                    if event.key == pygame.K_RETURN:
                        self.restart_game()

    def update(self):
        """
        Обновление состояния игры, включая движение игрока, обновление монстров и проверку столкновений.
        """
        if self.gameplay:
            attack_zone = self.controller.handle_keys()
            self.player.update()
            self.monsters.update(self.player.x, self.player.y)

            # Проверить столкновения между игроком и монстрами
            for monster in self.monsters.monster_list_in_game:
                if not monster.is_dead and pygame.Rect(self.player.x, self.player.y, 50, 50).colliderect(pygame.Rect(monster.x, monster.y, 50, 50)):
                    self.player.health -= monster.attack_power
                    if self.player.health <= 0:
                        self.player.die()
                        self.gameplay = False

            # Уменьшение здоровья монстров, попавших в зону атаки
            if attack_zone:
                for monster in self.monsters.monster_list_in_game:
                    if not monster.is_dead and attack_zone.colliderect(pygame.Rect(monster.x, monster.y, 50, 50)):
                        monster.health -= self.player.attack_power
                        if monster.health <= 0:
                            monster.die()
                            self.killed_monsters_count += 1  # Увеличиваем счетчик убитых монстров

            self.score += 1

            # Движение фона и монстров при приближении героя к краю экрана
            current_bg_speed = self.bg_speed * 2 if self.player.is_running else self.bg_speed
            if self.player.x > self.settings.screen_width - 200:
                self.bg_x -= current_bg_speed
                self.player.x = self.settings.screen_width - 200
                for monster in self.monsters.monster_list_in_game:
                    monster.x -= current_bg_speed
            elif self.player.x < 200 and self.bg_x < 0:
                self.bg_x += current_bg_speed
                self.player.x = 200
                for monster in self.monsters.monster_list_in_game:
                    monster.x += current_bg_speed

            # Ограничение движения героя по оси X
            if self.player.x < 0:
                self.player.x = 0

            # Ограничение движения фона по оси X
            if self.bg_x > 0:
                self.bg_x = 0

            # Зацикливание фона
            if self.bg_x <= -self.settings.screen_width:
                self.bg_x = 0
            elif self.bg_x >= self.settings.screen_width:
                self.bg_x = 0

            # Спавн монстров каждые 6-10 секунд
            current_time = time.time()
            if current_time >= self.next_monster_spawn_time:
                self.monsters.add_monster(Monster(self.player.x + random.randint(700, 1200), 500, 2, 100, 10))
                self.next_monster_spawn_time = current_time + random.randint(6, 10)
        elif self.in_menu:
            self.show_menu()
        else:
            if self.player.death_anim_count < len(self.player.death) - 1:
                self.player.update()  # Обновляем игрока для анимации смерти
                if not self.player.moved_on_death:
                    self.player.x -= 10  # Перемещаем героя на 10 пикселей влево
                    self.player.moved_on_death = True
            else:
                if self.death_time is None:
                    self.death_time = time.time()
                elif time.time() - self.death_time >= 3:
                    self.show_game_over_screen()

    def draw(self):
        """
        Отрисовка всех элементов на экране, включая фон, игрока, монстров и счетчик убитых монстров.
        """
        # Отрисовка зацикленного фона
        self.screen.blit(self.settings.bg_image, (self.bg_x, 0))
        self.screen.blit(self.settings.bg_image, (self.bg_x + self.settings.screen_width, 0))
        if self.gameplay:
            self.player.draw(self.screen)
            self.monsters.draw(self.screen)
            self.draw_killed_monsters_count()  # Отрисовка счетчика убитых монстров
        elif self.in_menu:
            self.show_menu()
        else:
            self.show_game_over_screen()

    def draw_text_with_outline(self, text, font, text_color, outline_color, x, y):
        """
        Отрисовка текста с обводкой.

        :param text: Текст для отрисовки.
        :param font: Шрифт для текста.
        :param text_color: Цвет текста.
        :param outline_color: Цвет обводки.
        :param x: Координата X для отрисовки текста.
        :param y: Координата Y для отрисовки текста.
        """
        outline_offset = 2
        for dx in [-outline_offset, 0, outline_offset]:
            for dy in [-outline_offset, 0, outline_offset]:
                if dx != 0 or dy != 0:
                    outline_text = font.render(text, True, outline_color)
                    self.screen.blit(outline_text, (x + dx, y + dy))
        text_surface = font.render(text, True, text_color)
        self.screen.blit(text_surface, (x, y))

    def draw_killed_monsters_count(self):
        """
        Отрисовка счетчика убитых монстров в левом верхнем углу экрана.
        """
        font = pygame.font.Font(self.settings.font_path, self.settings.font_size)
        text = f'Убито монстров: {self.killed_monsters_count}'
        self.draw_text_with_outline(text, font, 'Yellow', 'Black', 10, 10)

    def show_menu(self):
        """
        Отображение главного меню игры.
        """
        # Отрисовка фона меню
        self.screen.blit(self.menu_bg_image, (0, 0))

        # Отрисовка логотипа
        self.screen.blit(self.logo_image, (self.settings.screen_width // 2 - self.logo_image.get_width() // 2, 50))

        # Отрисовка элементов меню
        label = pygame.font.Font(self.settings.font_path, self.settings.font_size)
        title_label = 'Fighters Adventures'
        start_label = 'Нажмите Enter, чтобы начать игру'
        title_x = self.settings.screen_width // 2 - label.size(title_label)[0] // 2
        title_y = self.settings.screen_height // 2 - 120
        start_x = self.settings.screen_width // 2 - label.size(start_label)[0] // 2
        start_y = self.settings.screen_height // 2 + 30
        self.draw_text_with_outline(title_label, label, 'Yellow', 'Black', title_x, title_y)
        self.draw_text_with_outline(start_label, label, 'Yellow', 'Black', start_x, start_y)

    def show_game_over_screen(self):
        """
        Отображение экрана проигрыша с результатами игры.
        """
        # Отрисовка фона экрана после смерти
        self.screen.blit(self.game_over_bg_image, (0, 0))

        # Отрисовка логотипа
        self.screen.blit(self.logo_image, (self.settings.screen_width // 2 - self.logo_image.get_width() // 2, 50))

        # Отрисовка элементов экрана проигрыша
        label = pygame.font.Font(self.settings.font_path, self.settings.font_size)
        lose_label = 'Вы проиграли!'
        restart_label = 'Нажмите Enter, чтобы начать заново'
        killed_monsters_label = f'Убито монстров: {self.killed_monsters_count}'
        lose_x = self.settings.screen_width // 2 - label.size(lose_label)[0] // 2
        lose_y = self.settings.screen_height // 2 - 50
        restart_x = self.settings.screen_width // 2 - label.size(restart_label)[0] // 2
        restart_y = self.settings.screen_height // 2 + 50
        killed_monsters_x = self.settings.screen_width // 2 - label.size(killed_monsters_label)[0] // 2
        killed_monsters_y = self.settings.screen_height // 2 + 100
        self.draw_text_with_outline(lose_label, label, 'Yellow', 'Black', lose_x, lose_y)
        self.draw_text_with_outline(restart_label, label, 'Yellow', 'Black', restart_x, restart_y)
        self.draw_text_with_outline(killed_monsters_label, label, 'Yellow', 'Black', killed_monsters_x, killed_monsters_y)

    def start_game(self):
        """
        Начало игры из главного меню.
        """
        self.in_menu = False
        self.gameplay = True

    def restart_game(self):
        """
        Перезапуск игры после проигрыша.
        """
        self.player = Shinobi()
        self.controller = Controller(self.player)
        self.monsters = Monsters()
        self.monsters.add_monster(Monster(1000, 500, 2, 100, 10))  # Пример добавления монстра
        self.gameplay = True
        self.in_menu = False
        self.score = 0
        self.death_time = None
        self.bg_x = 0  # Сброс положения фона
        self.next_monster_spawn_time = time.time() + random.randint(6, 10)  # Сброс времени до следующего спавна монстра
        self.killed_monsters_count = 0  # Сброс счетчика убитых монстров

    def run_game(self):
        """
        Основной игровой цикл, включающий обработку событий, обновление состояния игры и отрисовку.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(20)

def main():
    fa = FightersAdventures()
    fa.run_game()

if __name__ == '__main__':
    main()