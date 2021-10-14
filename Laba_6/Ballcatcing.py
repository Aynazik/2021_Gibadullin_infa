import pygame
from pygame.draw import *
from random import randint

pygame.init()
pygame.font.init()
new_font = pygame.font.SysFont('arial', 30, bold=2)

# Задаем экран рисования
FPS = 60
screen = pygame.display.set_mode((1200, 860))

# Задаем цвета рисования
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def cached_balls_deleting(massive_of_parameters, massive_of_speeds, event_x, event_y, score_num):
    """
    проверяет попал ли пользователь по какому_нибудь шарику, если попал то удаляет шарик данные этого шарика из массивов
    описывающих его, возвращает измененные массивы
    :param score_num:
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :param event_x: координаты события по вериткали
    :param event_y: координаты события по горизонтали
    """
    i, cached_true_parameter = 0, 0
    while i <= len(massive_of_parameters) - 1 and cached_true_parameter != 1:
        if ((massive_of_parameters[i][0] - event_x) ** 2 + (massive_of_parameters[i][1] - event_y) ** 2) ** 0.5 <= \
                massive_of_parameters[i][2]:
            massive_of_parameters.pop(i)
            massive_of_speeds.pop(i)
            cached_true_parameter = 1
        i += 1
    score_num += cached_true_parameter
    return massive_of_parameters, massive_of_speeds, score_num


def new_ball(x, y, r, color):
    """
    делает шарик по указанным параметрам
    :param x: центр шарика по горизонтали
    :param y: центр шарика оп вертикали
    :param r: радиус шарика
    :param color: цвет шарика
    """
    circle(screen, color, (x, y), r)


def balls_creating(massive_of_parameters, massive_of_speeds, how_many):
    """
    Делает указанное число шариков и заполняет массивами их данных массивы скоростей и параметров. Возвращает эти
    измененные массивы
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :param how_many: описывает количество шариков которые будут сделаны
    """
    for _ in range(how_many):
        x = randint(100, 1100)
        y = randint(100, 760)
        r = randint(30, 100)
        color = COLORS[randint(0, 5)]
        massive_of_parameters.append([x, y, r, color])
        massive_of_speeds.append([randint(-5, 5), randint(-5, 5)])
        new_ball(x, y, r, color)
    return massive_of_parameters, massive_of_speeds


def new_ball_having(massive_of_parameters, massive_of_speeds):
    """
    Создает один новый шарик. Заполняет его данными входящие масссивы, возвращает эти измененные массивы
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    """
    balls_creating(massive_of_parameters, massive_of_speeds, 1)
    return massive_of_parameters, massive_of_speeds


def ball_new_position(x_cor, y_cor, radius, ball_color):
    """
    Меняет позицию шарика, не меняя его цвет и форму
    :param x_cor: новая координата по горизонтали шарика
    :param y_cor:новая координата по вертикали шарика
    :param radius: радус шарика
    :param ball_color: цвет шарика
    """
    circle(screen, ball_color, (x_cor, y_cor), radius)


def balls_moving(massive_of_parameters, massive_of_speeds):
    """
    Метод, отвечающий за движение шариков. Возвращет измененный массив параметров шариков
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :return:
    """
    for j in range(len(massive_of_parameters)):
        massive_of_parameters[j][0] += massive_of_speeds[j][0]
        massive_of_parameters[j][1] += massive_of_speeds[j][1]
        ball_new_position(massive_of_parameters[j][0], massive_of_parameters[j][1], massive_of_parameters[j][2],
                          massive_of_parameters[j][3])
    return massive_of_parameters


def old_ball_dying(massive_of_parameters, massive_of_speeds):
    """
    Удаляет с поля рандомный шарик, возвращает соответствующим образом измененные массивы данных
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :return:
    """
    if len(massive_of_parameters) >= 3:
        i = randint(0, len(massive_of_parameters) - 3)
        massive_of_parameters.pop(i)
        massive_of_speeds.pop(i)
    return massive_of_parameters, massive_of_speeds


def collisions_with_walls(massive_of_parameters, massive_of_speeds):
    """
    Метод определяющий рандомную траекторию шариков при столкновении со стенами. Возвращает измененные массивы координат
    и скоростей
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :return:
    """
    for i in range(len(massive_of_parameters)):
        rho = massive_of_parameters[i][2]
        if massive_of_parameters[i][0] <= rho or 1200 - massive_of_parameters[i][0] <= rho:
            massive_of_parameters[i][0] -= massive_of_speeds[i][0]
            massive_of_speeds[i][0] = - (massive_of_speeds[i][0] / abs(massive_of_speeds[i][0])) * randint(1, 6)
        elif massive_of_parameters[i][1] <= rho or 860 - massive_of_parameters[i][1] <= rho:
            massive_of_parameters[i][1] -= massive_of_speeds[i][1]
            massive_of_speeds[i][1] = - (massive_of_speeds[i][1] / abs(massive_of_speeds[i][1])) * randint(1, 6)
    return massive_of_speeds, massive_of_parameters


def balls_appearance_and_dying(massive_of_parameters, massive_of_speeds, num_of_tics, appearance_tics, dying_tics):
    """
    Функция отвещающая за уничтожение и появление шариков через определенные промежутки времени. возвращет измененные
    массивы скоростей и параметров
    :param massive_of_parameters: массив параметров шаров ([координыта по горизонтали, координата по вертикали, радиус,
    цвет])
    :param massive_of_speeds: массив малых перемещений шариков по осям ([dx, dy])
    :param num_of_tics: число тиков с начала программы
    :param appearance_tics: промежуток через который появляется новый шарик на поле (в тиках)
    :param dying_tics: прмежуток чрезе котроый удаляется рандомный шарик с поля (в тиках)
    """
    if num_of_tics % appearance_tics == 0:
        new_ball_having(massive_of_parameters, massive_of_speeds)
    if num_of_tics % dying_tics == 0:
        old_ball_dying(massive_of_parameters, massive_of_speeds)
    return massive_of_parameters, massive_of_speeds


cached_num = 0
# Переменная для отсчета коичества тиков часов
program_working_timer = 0

pygame.display.update()
clock = pygame.time.Clock()
finished = False
# Задаём переменную ведущую счет пойманных шариков и описывапем переменные вывода на экран
score = 0
score_table = new_font.render("SCORE:", False, (255, 255, 255))
num = new_font.render(str(score), False, (255, 255, 255))

# Зададим массивы скоростей и массив параметров каждого отдельного шарика, пока пустые
ball_speeds = []
ball_parameters = []
# сделаем некоторое начальное количество шариков
balls_creating(ball_parameters, ball_speeds, 3)
# Опишем переменные частоты появления, смерти, и время начала усложнения игры соотвтетсвенно в количествах тиков
time_of_appearance = int(FPS * 1)
time_of_dying = int(FPS * 3)
time_of_hard_level = int(FPS * 15)
# Запускаем основной цикл
while not finished:
    clock.tick(FPS)
    program_working_timer = pygame.time.get_ticks()
    balls_appearance_and_dying(ball_parameters, ball_speeds, program_working_timer, time_of_appearance, time_of_dying)
    screen.blit(score_table, (10, 10))
    screen.blit(num, (125, 10))
    collisions_with_walls(ball_parameters, ball_speeds)
    balls_moving(ball_parameters, ball_speeds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            ball_parameters, ball_speeds, score = cached_balls_deleting(ball_parameters, ball_speeds, event.x, event.y,
                                                                        score)
            num = new_font.render(str(score), False, (255, 255, 255))
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()
