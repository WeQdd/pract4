import pygame

class Controller:
    """
    Класс Controller обрабатывает ввод с клавиатуры и управляет действиями игрока.
    """

    def __init__(self, player):
        """
        Инициализация контроллера с привязкой к объекту игрока.

        :param player: Объект игрока, которым будет управлять контроллер.
        """
        self.player = player

    def handle_keys(self):
        """
        Обработка нажатий клавиш и выполнение соответствующих действий игрока.

        :return: Зона атаки игрока, если была выполнена атака, иначе None.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.start_run()
        else:
            self.player.stop_run()

        if keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop()

        if keys[pygame.K_SPACE]:
            self.player.start_jump()

        if keys[pygame.K_RETURN]:
            return self.player.attack()
        return None