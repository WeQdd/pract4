import pygame
import time

class Monster:
    """
    Класс Monster представляет собой врага в игре, который может двигаться, атаковать и умирать.
    """

    def __init__(self, x, y, speed, health, attack_power):
        """
        Инициализация монстра с заданными параметрами.

        :param x: Начальная координата X монстра.
        :param y: Начальная координата Y монстра.
        :param speed: Скорость движения монстра.
        :param health: Здоровье монстра.
        :param attack_power: Сила атаки монстра.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.attack_power = attack_power
        self.is_dead = False
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_cooldown = 3000  
        self.attack_images = [pygame.image.load(f'src/images/enemies/skeleton/attack/attack_{i}.png') for i in range(1, 8)]
        self.attack_index = 0
        self.attack_time = 0
        self.attack_interval = 1000  
        self.death_anim_count = 0
        self.death_frame_time = time.time()  # Время последнего обновления фрейма смерти
        self.anim_count = 0

        self.skeleton_walk = [
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w1.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w2.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w3.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w4.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w5.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w6.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w7.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/left_walk/skeleton_w8.png').convert_alpha()
        ]
        
        self.skeleton_death = [
            pygame.image.load('src/images/enemies/skeleton/death/death_1.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/death/death_2.png').convert_alpha(),
            pygame.image.load('src/images/enemies/skeleton/death/death_3.png').convert_alpha()
        ]

    def update(self, hero_x, hero_y):
        """
        Обновление состояния монстра, включая движение, атаку и анимацию смерти.

        :param hero_x: Координата X героя.
        :param hero_y: Координата Y героя.
        """
        if not self.is_dead:
            self.anim_count += 1
            if self.anim_count >= len(self.skeleton_walk):
                self.anim_count = 0

            distance_to_hero = ((self.x - hero_x) ** 2 + (self.y - hero_y) ** 2) ** 0.5

            if distance_to_hero <= 20 and not self.is_attacking:  
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= self.attack_cooldown:
                    self.is_attacking = True
                    self.last_attack_time = current_time

            if self.is_attacking:
                # Обновление анимации атаки
                current_time = pygame.time.get_ticks()
                if current_time - self.attack_time > self.attack_interval:
                    self.attack_time = current_time
                    self.attack_index = (self.attack_index + 1) % len(self.attack_images)
                    if self.attack_index == 0:
                        self.is_attacking = False
            else:
                self.move_towards(hero_x, hero_y)
        else:
            if time.time() - self.death_frame_time >= 1:  # Перерыв в 1 секунду между фреймами
                self.death_anim_count += 1
                self.death_frame_time = time.time()
            if self.death_anim_count >= len(self.skeleton_death):
                self.death_anim_count = len(self.skeleton_death) - 1  # Оставляем последний кадр анимации смерти

    def move_towards(self, hero_x, hero_y):
        """
        Движение монстра в направлении героя.

        :param hero_x: Координата X героя.
        :param hero_y: Координата Y героя.
        """
        if self.x < hero_x:
            self.x += self.speed
        elif self.x > hero_x:
            self.x -= self.speed

        if self.y < hero_y:
            self.y += self.speed
        elif self.y > hero_y:
            self.y -= self.speed

    def draw(self, screen):
        """
        Отрисовка монстра на экране.

        :param screen: Экран, на котором будет отрисован монстр.
        """
        if not self.is_dead:
            if self.is_attacking:
                screen.blit(self.attack_images[self.attack_index], (self.x, self.y))
            else:
                screen.blit(self.skeleton_walk[self.anim_count], (self.x, self.y))
        else:
            screen.blit(self.skeleton_death[self.death_anim_count], (self.x, self.y))

    def die(self):
        """
        Обработка смерти монстра.
        """
        self.is_dead = True

class Monsters:
    """
    Класс Monsters управляет списком всех монстров в игре.
    """

    def __init__(self):
        """
        Инициализация списка монстров.
        """
        self.monster_list_in_game = []

    def add_monster(self, monster):
        """
        Добавление монстра в список.

        :param monster: Объект монстра для добавления в список.
        """
        self.monster_list_in_game.append(monster)

    def update(self, hero_x, hero_y):
        """
        Обновление состояния всех монстров в списке.

        :param hero_x: Координата X героя.
        :param hero_y: Координата Y героя.
        """
        for monster in self.monster_list_in_game:
            monster.update(hero_x, hero_y)

    def draw(self, screen):
        """
        Отрисовка всех монстров в списке на экране.

        :param screen: Экран, на котором будут отрисованы монстры.
        """
        for monster in self.monster_list_in_game:
            monster.draw(screen)