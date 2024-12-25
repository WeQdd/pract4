import pygame
import time

class Shinobi:
    """
    Класс Shinobi представляет собой главного героя игры, который может двигаться, прыгать, атаковать и умирать.
    """
    def __init__(self):
        """
        Инициализация героя с заданными параметрами.
        """
        self.x = 70
        self.y = 500
        self.walk_speed = 10
        self.run_speed = 20
        self.speed = self.walk_speed
        self.anim_count = 0
        self.anim_count_stay = 0
        self.jump_anim_count = 0
        self.attack_anim_count = 0
        self.death_anim_count = 0
        self.direction = 'right'
        self.is_jumping = False
        self.is_attacking = False
        self.is_dead = False
        self.jump_count = 10
        self.update_count = 0  
        self.is_moving = False  
        self.is_running = False  
        self.screen_width = 1200  
        self.screen_height = 720  
        self.health = 100  
        self.attack_power = 100  
        self.death_frame_time = time.time()
        self.moved_on_death = False  

        self.walk_right = [
            pygame.image.load('src/images/main_hero/walker/walk/walk_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/walk/walk_8.png').convert_alpha()
        ]

        self.walk_left = [
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/walker/reverse_walk/rev_walk_8.png').convert_alpha()
        ]

        self.run_right = [
            pygame.image.load('src/images/main_hero/run/run_right/run_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_right/run_8.png').convert_alpha()
        ]

        self.run_left = [
            pygame.image.load('src/images/main_hero/run/run_left/run_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/run/run_left/run_8.png').convert_alpha()
        ]

        self.stay = [
            pygame.image.load('src/images/main_hero/stay/stay_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/stay/stay_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/stay/stay_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/stay/stay_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/stay/stay_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/stay/stay_6.png').convert_alpha()
        ]

        self.jump_left = [
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_8.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_9.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_10.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_11.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_left/jump_12.png').convert_alpha()
        ]

        self.jump_right = [
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_5.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_6.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_7.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_8.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_9.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_10.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_11.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/jump/jump_right/jump_12.png').convert_alpha()
        ]

        self.attack_right = [
            pygame.image.load('src/images/main_hero/attack/attack_right/attack_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_right/attack_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_right/attack_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_right/attack_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_right/attack_5.png').convert_alpha()
        ]

        self.attack_left = [
            pygame.image.load('src/images/main_hero/attack/attack_left/attack_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_left/attack_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_left/attack_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_left/attack_4.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/attack/attack_left/attack_5.png').convert_alpha()
        ]

        self.death = [
            pygame.image.load('src/images/main_hero/death/death_1.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/death/death_2.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/death/death_3.png').convert_alpha(),
            pygame.image.load('src/images/main_hero/death/death_4.png').convert_alpha()
        ]

    def update(self):
        """
        Обновление состояния героя, включая анимации и проверку состояния.
        """
        self.update_count += 1
        if self.update_count % 2 == 0 or self.is_running:  # Обновляем анимацию через раз, кроме бега
            self.anim_count += 1
            if self.anim_count >= len(self.walk_right):
                self.anim_count = 0

            self.anim_count_stay += 1
            if self.anim_count_stay >= len(self.stay):
                self.anim_count_stay = 0

        if self.is_jumping:
            self.jump()
        else:
            self.jump_anim_count = 0  # Сброс анимации прыжка, если не прыгает

        if self.is_attacking:
            self.attack_anim_count += 1
            if self.attack_anim_count >= len(self.attack_right):
                self.attack_anim_count = 0
                self.is_attacking = False

        if self.is_dead:
            if time.time() - self.death_frame_time >= 1:  # Перерыв в 1 секунду между фреймами
                self.death_anim_count += 1
                self.death_frame_time = time.time()
            if self.death_anim_count >= len(self.death):
                self.death_anim_count = len(self.death) - 1  # Оставляем последний кадр анимации смерти

    def draw(self, screen):
        """
        Отрисовка героя на экране.

        :param screen: Экран, на котором будет отрисован герой.
        """
        if self.is_dead:
            screen.blit(self.death[self.death_anim_count], (self.x, self.y))
        elif self.is_jumping:
            if self.direction == 'right':
                if self.jump_anim_count >= len(self.jump_right):
                    self.jump_anim_count = 0
                screen.blit(self.jump_right[self.jump_anim_count], (self.x, self.y))
            elif self.direction == 'left':
                if self.jump_anim_count >= len(self.jump_left):
                    self.jump_anim_count = 0
                screen.blit(self.jump_left[self.jump_anim_count], (self.x, self.y))
            self.jump_anim_count += 1
        elif self.is_attacking:
            if self.direction == 'right':
                screen.blit(self.attack_right[self.attack_anim_count], (self.x, self.y))
            elif self.direction == 'left':
                screen.blit(self.attack_left[self.attack_anim_count], (self.x, self.y))
        elif self.is_moving:
            if self.is_running:
                if self.direction == 'right':
                    screen.blit(self.run_right[self.anim_count], (self.x, self.y))
                elif self.direction == 'left':
                    screen.blit(self.run_left[self.anim_count], (self.x, self.y))
            else:
                if self.direction == 'right':
                    screen.blit(self.walk_right[self.anim_count], (self.x, self.y))
                elif self.direction == 'left':
                    screen.blit(self.walk_left[self.anim_count], (self.x, self.y))
        else:
            screen.blit(self.stay[self.anim_count_stay], (self.x, self.y))

    def move_right(self):
        """
        Движение героя вправо.
        """
        self.x += self.speed
        self.direction = 'right'
        self.is_moving = True

    def move_left(self):
        """
        Движение героя влево.
        """
        self.x -= self.speed
        self.direction = 'left'
        self.is_moving = True

    def stop(self):
        """
        Остановка движения героя.
        """
        self.is_moving = False

    def start_run(self):
        """
        Начало бега героя.
        """
        self.is_running = True
        self.speed = self.run_speed

    def stop_run(self):
        """
        Остановка бега героя.
        """
        self.is_running = False
        self.speed = self.walk_speed

    def jump(self):
        """
        Прыжок героя.
        """
        if self.jump_count >= -10:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            self.y -= (self.jump_count ** 2) * 0.5 * neg
            self.jump_count -= 1
        else:
            self.is_jumping = False
            self.jump_count = 10

    def start_jump(self):
        """
        Начало прыжка героя вправо.
        """
        if not self.is_jumping:
            self.is_jumping = True

    def start_jump_left(self):
        """
        Начало прыжка героя влево.
        """
        if not self.is_jumping:
            self.is_jumping = True
            self.direction = 'left'

    def attack(self):
        """
        Атака героя.

        :return: Зона атаки героя.
        """
        self.is_attacking = True
        self.attack_anim_count = 0
        attack_size = 100
        attack_zone = pygame.Rect(
            self.x - (attack_size - 50) // 2,
            self.y - (attack_size - 50) // 2,
            attack_size,
            attack_size
        )
        return attack_zone

    def die(self):
        """
        Обработка смерти героя.
        """
        self.is_dead = True
        self.death_anim_count = 0
        self.death_frame_time = time.time()
        self.moved_on_death = False  