import math
from math import sin, cos, tan
from random import randint
from random import random
import pygame

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Game:
    def __init__(self):
        """
        Конструктор класса "Игра"
        """
        self.screen = screen
        self.FPS = 50
        # эталонный малый отрезок времени
        self.delta_time = 1 / self.FPS
        self.targets_massive = []
        self.list_of_simple_projectile = []
        self.list_of_shrapnel_projectiles = []
        self.explosion_waves_massive = []
        self.bombs_massive = []
        # тип выбранного снаряда 1 или 2 (по умолчанию стоит первый)
        self.projectile_type = 1
        # отвечате за движение танка(1 вправо, 0 стоит, -1 влеов)
        self.moving_command = 0
        self.acceleration = 80
        self.y_line_of_ground = 580

    # Функция основного цикла игры
    def mainloop(self):
        """
        Функция основного цикла игры. По сути объединяет под одну крышу все остальные функции
        """
        clock = pygame.time.Clock()
        tank = Tank()
        self.targets_massive.append(SimpleTarget())
        self.targets_massive.append(HardTarget())
        finished = False
        while not finished:
            clock.tick(self.FPS)
            self.screen.fill(WHITE)
            # проверка попаданий
            self.main_hit_function()
            # рисование, перемещение, движение танка
            if self.main_move_and_draw_function(tank):
                finished = True
            # обработка событий
            if self.event_analysis_function(tank):
                finished = True
            tank.power_up()
            pygame.display.update()
        pygame.quit()

    # Группа функций отвечающая за то была ли уничтожена мишень
    def target_hit_test(self, target):
        """
        Функция проверяющая всевозможные случаи попадания в определенную мишень задаваемой переменной target.
        В случае попадания выдаёт ТРУ, иначе Фолс
        :param target: переменная мишени
        """
        for simple_projectile in self.list_of_simple_projectile:
            if simple_projectile.hit_test(target, simple_projectile.x, simple_projectile.y):
                self.list_of_simple_projectile.remove(simple_projectile)
                return True
        for shrapnel in self.list_of_shrapnel_projectiles:
            if shrapnel.hit_test(target, shrapnel.x, shrapnel.y):
                self.list_of_shrapnel_projectiles.remove(shrapnel)
                return True
        for explosion_wave in self.explosion_waves_massive:
            if explosion_wave.hit_test(target):
                return True
        return False

    def main_hit_function(self):
        """
        Функция отвечающая за действия при попадании в мишень каким то из способов. Создаёт из уничтоженной мишени
        бомбу, которая падает вниз и взырвается.
        """
        for target in self.targets_massive:
            if self.target_hit_test(target):
                if isinstance(target, HardTarget):
                    self.targets_massive.append(HardTarget())
                else:
                    self.targets_massive.append(SimpleTarget())
                self.bombs_massive.append(Bomb(target.x, target.y))
                self.targets_massive.remove(target)

    # Группа функций отвечающих за отрисовывание, перемещение и некоторые взаимодействия объектов на поле игры
    def main_move_and_draw_function(self, tank):
        """
        Объединяет под одну "крышу" функции отрисовывающие отдельные объекты или группы объектов
        :param tank: переменная танка
        """
        if self.explosion_move_and_draw_function(tank):
            return True
        self.projectiles_move_and_draw_function()
        self.target_and_bombs_move_and_draw_function()

    def projectiles_move_and_draw_function(self):
        """
        Функция отвечающая за отрисовывание перемещение снарядов
        """
        for simple_projectile in self.list_of_simple_projectile:
            simple_projectile.draw()
            simple_projectile.move()
            if simple_projectile.life_time_control() == 1:
                self.list_of_simple_projectile.remove(simple_projectile)
        for shrapnel in self.list_of_shrapnel_projectiles:
            shrapnel.main_draw()
            auxiliary_massive, auxiliary_param = shrapnel.move()
            if auxiliary_param == 1:
                self.list_of_shrapnel_projectiles.remove(shrapnel)
            for element in auxiliary_massive:
                self.explosion_waves_massive.append(element)

    def explosion_move_and_draw_function(self, tank):
        """
        Функция отвечающая за отрисовывание перемещение взырвной волны и танка(совмещены тк взрывая волна можнт
        нанаосить урон танку)
        :param tank:
        """
        tank.draw()
        tank.move(self.moving_command)
        if tank.health():
            return True
        for explosion in self.explosion_waves_massive:
            explosion.hit_test(tank)
        for explosion_wave in self.explosion_waves_massive:
            explosion_wave.draw()
            if explosion_wave.r >= 100:
                self.explosion_waves_massive.remove(explosion_wave)

    def target_and_bombs_move_and_draw_function(self):
        """
        Функция отвечающая за отрисовывание и перемещение мишеней и бомб
        """
        for target in self.targets_massive:
            target.draw(target.color)
            target.move()
        for bomb in self.bombs_massive:
            bomb.draw()
            auxiliary_massive, auxiliary_param = bomb.move()
            if auxiliary_param == 1:
                self.bombs_massive.remove(bomb)
            for element in auxiliary_massive:
                self.explosion_waves_massive.append(element)

    # Функция анализирующая события в игре
    def event_analysis_function(self, tank):
        """
        Функция анализирующая игровые события и принимающая решения в зависимости от их вида
        :param tank: танк
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.projectile_type = 1
                elif event.key == pygame.K_2:
                    self.projectile_type = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.moving_command = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.moving_command = 1
                elif event.key == pygame.K_LEFT:
                    self.moving_command = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tank.fire2_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                new_ball = tank.fire2_end(self.projectile_type)
                if isinstance(new_ball, Simple):
                    self.list_of_simple_projectile.append(new_ball)
                else:
                    self.list_of_shrapnel_projectiles.append(new_ball)
            elif event.type == pygame.MOUSEMOTION:
                tank.targeting(event)


class Projectile(Game):
    def __init__(self):
        """
        Конструктор класса "Снаряд"
        """
        super().__init__()

    @staticmethod
    def hit_test(obj, projectile_x, projectile_y):
        """
        Метод выдающий ТРУ если снаряд попал в опрделенную мишень и ФОЛСЕ в случае обратного
        :param obj: объект, попадание в который собственно и проверяется
        :param projectile_x: координа по иксу снаряда
        :param projectile_y: координата по игрику снаряда
        """
        if isinstance(obj, Target):
            distance = math.sqrt((projectile_x - obj.x) ** 2 + (projectile_y - obj.y) ** 2)
            if distance <= obj.r:
                return True
        return False


class Simple(Projectile):
    def __init__(self, x, y):
        """
        Конструктор класса "Простой снаряд"
        :param x: наяальная координата снаряда по горизонтали
        :param y: начальная координат снаряда по игрику
        """
        super().__init__()
        self.x = x
        self.y = y
        self.r = 6
        self.vx = 0
        self.vy = 0
        self.color = GREY
        self.energy = 0.9
        self.an = 1
        self.time = 0

    def move(self):
        """
        Метод отвечающий за характер движения простого снаряда (отбивание от левой правой и нижней стенок, гравитация,
        "потеря энергии" и остановка)
        """
        if (self.y_line_of_ground - self.y) <= self.r and self.energy > 0:
            self.y -= self.vy
            self.vy = - self.energy * self.vy
            self.energy -= 0.15
        elif self.x <= self.r or (800 - self.x) <= self.r:
            self.x -= self.vx
            self.vx = - 0.8 * self.vx
        else:
            self.x += self.vx
            self.y += self.vy
            if self.energy > 0:
                self.vy += self.acceleration * self.delta_time
            else:
                self.vy = 0
                self.vx = 0.95 * self.vx

    def life_time_control(self):
        """
        Метод отвечающий за жизненный цикл простого снаряда. Выдаст 1 если ег пора прервать
        """
        if self.time >= 0.1 * self.FPS:
            return 1
        else:
            self.time += self.delta_time
            return 0

    def draw(self):
        """
        Метод отрисовывающий простой снаряд
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, width=1)


class Shrapnel(Projectile):
    def __init__(self, x, y):
        """
        Конструктор класса "Фугасного снаряда"
        :param x: координата по иксу
        :param y: по игрику
        """
        super().__init__()
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.energy = 1
        self.length = 30
        self.width = 10

    def main_draw(self):
        """
        Функция объединяющая функции необходимые для рисования снаряда
        """
        phi = self.angle()
        self.draw(self.x, self.y, self.length, self.width, phi)

    def draw(self, x, y, length, width, phi):
        """
        Функция необходимая для отрисовывания тела снаряда, повернутого носом против часовй стрелки на угол фи
        :param x: координата снаряда по икс
        :param y: по игрик
        :param length: длина снаряда
        :param width: максимальная ширина снаряда
        :param phi: угол поповрота снаряда против часовй стрелки
        """
        pygame.draw.polygon(self.screen, YELLOW, [[x - (width / 2) * sin(phi), y + (width / 2) * cos(phi)],
                                                  [x + length * cos(phi), y + length * sin(phi)],
                                                  [x + (width / 2) * sin(phi), y - (width / 2) * cos(phi)]])
        pygame.draw.aalines(self.screen, self.color, True, [[x - (width / 2) * sin(phi), y + (width / 2) * cos(phi)],
                                                            [x + length * cos(phi), y + length * sin(phi)],
                                                            [x + (width / 2) * sin(phi), y - (width / 2) * cos(phi)]])

    def angle(self):
        """
        Функция определяющая угол поворота фугасного снаряда
        :return:
        """
        if self.vx != 0:
            if self.vx > 0:
                angle = math.atan(self.vy / self.vx)
            else:
                angle = math.atan(self.vy / self.vx) + math.pi
        elif self.vy != 0 and self.vx == 0:
            if self.vy > 0:
                angle = math.pi / 2
            else:
                angle = - math.pi / 2
        else:
            angle = - math.pi / 2
        return angle

    def move(self):
        """
        Метод отвечающий за передвижение фугасного снаряда, в случае его столновения со стенами создаёт объект
        класса Ехплоужен, моделирующий взрыв снаряда. При этом выдаёт 1 чтобы метод вызывающий данный метод удалил
        снаряд, а также массив local_massive, в котором записана переменная взырвной волны, чтобы метод вызывающий
        данный записал её в основной список взырвных волн. В случае отсутсвия столкновения выдает пустой массив и 0,
        а также опредляет простой баллистический характер движения снаряда
        """
        local_massive = []
        if (self.y_line_of_ground - self.y) <= self.r or self.x <= self.r or (800 - self.x) <= self.r:
            explosion_wave = ExplosionWave(self.x, self.y)
            local_massive.append(explosion_wave)
            return local_massive, 1
        else:
            self.x += self.vx
            self.y += self.vy
            if self.energy > 0:
                self.vy += (self.acceleration * 0.8) * self.delta_time
        return local_massive, 0


class ExplosionWave(Game):
    def __init__(self, x, y):
        """
        Конструктор класса "взыраня волна"
        :param x: координата эпицентра взырва по иксу
        :param y: координата эписцентра взырва по игрику
        """
        super().__init__()
        self.x = x
        self.y = y
        self.r = 10
        self.color = YELLOW

    def draw(self):
        """
        Метод рисующий взырвную волну в определнном состоянии
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        self.r += 10

    def hit_test(self, obj):
        """
        метод проверяющий попал ли какой-либо объект (из классов мишень или танк) в зону действия взырвной волны.
        В случае с мишенью юничтожает мишень, в случае с танком отнимает хп
        :param obj:
        :return:
        """
        if isinstance(obj, Target):
            distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
            if distance <= obj.r + self.r:
                return True
        if isinstance(obj, Tank):
            distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
            if distance <= self.r:
                obj.healthy -= 10
        return False


class Tank(Game):
    def __init__(self):
        """
        Конструктор класса танк
        """
        super().__init__()
        self.x = 100
        self.y = 550
        self.high = 50
        self.length = 120
        self.f2_power = 40
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.healthy = 250

    def health(self):
        """
        Метод отвечающий отрисовку хп танка на экране и само хп. В случае заканчивания хп вернет ТРУ, что задаст
        механизм для вызывающей данную функцию функции закончить игру
        """
        if self.healthy <= 0:
            print("GAME OVER")
            return True
        pygame.draw.rect(self.screen, RED, (5, 10, self.healthy, 10))

    def move(self, moving_command):
        """
        Параметр отвечающий за движение танка(1 вправо, 0 стоит, -1 влеов)
        :param moving_command:
        """
        if moving_command == 1:
            self.x += 5
        if moving_command == -1:
            self.x -= 5

    def fire2_start(self):
        """
        При нажатии на клавишу мыши включает соответствующий параметр
        """
        self.f2_on = 1

    def fire2_end(self, projectile_type_parameter):
        """

        :param projectile_type_parameter: параметр определяющий тип снаряда заряжаемогов орудие (1 - обыденный,
        2 фугасный)
        """
        if projectile_type_parameter == 1:
            new_ball = Simple(self.x, self.y)
        else:
            new_ball = Shrapnel(self.x, self.y)
        new_ball.r += 5
        new_ball.vx = 0.7 * self.f2_power * math.cos(self.an)
        new_ball.vy = 0.7 * self.f2_power * math.sin(self.an)
        self.f2_on = 0
        self.f2_power = 40
        return new_ball

    def targeting(self, game_event):
        """
        Прицеливание. Зависит от положения мыши. Работает для активной пушки
        :param game_event:
        """
        delta_x = (game_event.pos[0] - self.x)
        delta_y = (game_event.pos[1] - self.y)
        if delta_x > 0:
            if delta_y >= 0:
                self.an = 0
            else:
                self.an = math.atan(delta_y / delta_x)
        elif delta_x < 0:
            if delta_y >= 0:
                self.an = math.pi
            else:
                self.an = math.pi + math.atan(delta_y / delta_x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def power_up(self):
        """
        Увеличивает силу выстрела при зажатии леовй клавиши мыши
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    # drawing
    def gun_draw(self):
        """
        Отрисовывает пушку танка
        """
        length = self.f2_power
        phi = self.an
        width = 5
        pygame.draw.polygon(self.screen, self.color,
                            [[self.x, self.y], [self.x + length * math.cos(phi), self.y + length * math.sin(phi)],
                             [self.x + length * math.cos(phi) + width * math.sin(phi),
                              self.y + length * math.sin(phi) - width * math.cos(phi)],
                             [self.x + width * math.sin(phi), self.y - width * math.cos(phi)]])

    def tank_tower(self, x, y, length, high):
        """
        Отрисовывает башню танка
        :param x: координаты основания пушки по икс
        :param y: по игрик
        :param length: длина танка
        :param high: высота танка
        """
        pygame.draw.ellipse(self.screen, GREEN, (x - 0.2 * length, y - 0.25 * high, 0.4 * length, 0.5 * high))
        pygame.draw.ellipse(self.screen, BLACK, (x - 0.2 * length, y - 0.25 * high, 0.4 * length, 0.5 * high),
                            width=2)

    def tank_body(self, x, y, length, high):
        """
        корпус танка
        :param x: координат основания ствола танка по икс
        :param y: по игрик
        :param length: длина танка
        :param high: высота танка
        """
        k = tan(math.pi / 3)
        pygame.draw.polygon(self.screen, GREEN,
                            [[x - 0.5 * length, y], [x + 0.5 * length, y],
                             [x + 0.5 * length - high * (1 / k), y + k * high],
                             [x - 0.5 * length + high * (1 / k), y + k * high]])
        pygame.draw.polygon(self.screen, BLACK,
                            [[x - 0.5 * length, y], [x + 0.5 * length, y],
                             [x + 0.5 * length - high * (1 / k), y + k * high],
                             [x - 0.5 * length + high * (1 / k), y + k * high]], width=2)

    def draw(self):
        """
        Отрисовывает весь танк вызвая методы отрисовывающие его отдельные части
        """
        x = self.x
        y = self.y
        length = self.length
        width = self.high
        self.gun_draw()
        self.tank_tower(x, y, length, width)
        self.tank_body(x, y, 0.8 * length, 0.2 * width)


class Target(Game):

    def __init__(self):
        """
        конструктор класса Target
        """
        super().__init__()
        self.screen = screen
        self.x = randint(100, 700)
        self.y = randint(100, 400)
        self.color = RED
        self.r = randint(20, 40)
        self.vx = randint(100, 200)
        self.vy = (-1) ** randint(2, 3) * randint(100, 200)
        self.ax = randint(100, 200)
        self.ay = ((-1) ** randint(2, 3)) * randint(100, 300)
        self.equilibrium_pos_x = self.x
        self.equilibrium_pos_y = self.y
        self.live = 1
        self.ratio = randint(3, 5) * random()

    def draw(self, color):
        """
        Отрисовывает мишень
        :param color: цвет мишени
        """
        if self.live > 0:
            pygame.draw.circle(self.screen, color, (self.x, self.y), self.r)
            pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, width=2)

    def collisions_with_walls(self):
        """
        Механика столкновения со стенами
        """
        if (self.y_line_of_ground - self.y) <= self.r:
            self.vy = - self.vy
        elif self.x <= self.r or (800 - self.x) <= self.r:
            self.vx = - self.vx


class SimpleTarget(Target):

    def __init__(self):
        """
        Конструктор простых мишеней
        """
        super().__init__()

    def move(self):
        """
        Движение простых мишеней
        """
        self.collisions_with_walls()
        if self.x <= self.equilibrium_pos_x:
            self.ax = abs(self.ax)
        else:
            self.ax = - abs(self.ax)
        self.vx += self.ax * self.delta_time
        self.x += self.ratio * self.vx * self.delta_time


class HardTarget(Target):

    def __init(self):
        """
        Конструктор сложных мишеней
        """
        super().__init__()
        self.color = GREY

    def move(self):
        """
        Метод задающий характер движения сложных мишеней
        """
        self.collisions_with_walls()
        if self.x <= self.equilibrium_pos_x:
            self.ax = abs(self.ax)
        else:
            self.ax = - abs(self.ax)
        if self.y <= self.equilibrium_pos_y:
            self.ay = abs(self.ay)
        else:
            self.ay = - abs(self.ay)
        self.vx += self.ax * self.delta_time
        self.vy += self.ay * self.delta_time
        self.x += self.ratio * self.vx * self.delta_time
        self.y += self.ratio * self.vy * self.delta_time


class Bomb(Game):
    def __init__(self, x, y):
        """
        Конструктор класса бомба
        :param x: координата бомбы по иксу
        :param y: координата бомбы по игрику
        """
        super().__init__()
        self.position = [x, y]
        self.r = 13
        self.vy = 1
        self.vx = ((-1) ** randint(2, 3)) * random()
        self.color = RED

    def move(self):
        """
        Функция задающая движение бомбы, в случае столкновения бебры с полом создает объект класса "Взрывная волна"
        """
        local_massive = []
        if self.position[1] >= self.y_line_of_ground:
            local_massive.append(ExplosionWave(self.position[0], self.position[1]))
            return local_massive, 1
        else:
            self.vy += 0.2 * self.acceleration * self.delta_time
        self.position[0] += self.vx
        self.position[1] += self.vy
        return local_massive, 0

    def draw(self):
        """
        Отрисовывает бомбу по ее позиционным координатам
        """
        pygame.draw.line(self.screen, self.color, (self.position[0] - self.r, self.position[1]),
                         (self.position[0] + self.r, self.position[1]), width=10)
        pygame.draw.line(self.screen, self.color, (self.position[0], self.position[1] - self.r),
                         (self.position[0], self.position[1] + self.r), width=10)
        pygame.draw.line(self.screen, self.color, (self.position[0] - self.r * math.cos(math.pi / 4),
                                                   self.position[1] + self.r * math.cos(math.pi / 4)),
                         (self.position[0] + self.r * math.cos(math.pi / 4),
                          self.position[1] - self.r * math.cos(math.pi / 4)), width=10)
        pygame.draw.circle(self.screen, BLACK, self.position, self.r)


g = Game()
g.mainloop()
