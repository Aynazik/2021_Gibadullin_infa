import pygame
from pygame.draw import *
from random import randint

pygame.init()
pygame.font.init()
new_font = pygame.font.SysFont('arial', 30, bold=2)

# Задаем экран рисования
FPS = 80
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


def simple_balls_cached(massive_of_parameters, event_x_cor, event_y_cor, score_num, game_over_tic_nums):
    """
    Функция проверяет был ли пойман простой мячик. если да то начисляет за него очки и увеличивает время
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param event_x_cor: координата события по горизонатли
    :param event_y_cor: координата события по вертикали
    :param score_num: число набранных очков
    :param game_over_tic_nums: время дляительности одной игры
    """
    index_num, cached_is_true_parameter = 0, 0
    while index_num <= len(massive_of_parameters) - 1 and cached_is_true_parameter != 1:
        if ((massive_of_parameters[index_num][0] - event_x_cor) ** 2 + (
                massive_of_parameters[index_num][1] - event_y_cor) ** 2) ** 0.5 <= \
                massive_of_parameters[index_num][2]:
            massive_of_parameters.pop(index_num)
            game_over_tic_nums += 5 * 80
            cached_is_true_parameter = 1
        index_num += 1
    score_num += cached_is_true_parameter
    return massive_of_parameters, score_num, game_over_tic_nums


def hard_ball_cached(massive_of_parameters, hard_ball_parameter, event_x_cor, event_y_cor, score_num, tics_of_hard_ball,
                     working_time, stop_true_parameter, game_over_tic_nums):
    """
    Функция проверяет был ли пойман сложный мячик. Если да то начисляет за него очки и увеличивает время. Распыляет из
    него каскад простых мячик с помощью функции snitch_caching(). Возвращает измененные параметры массивов и времени и
    количества очков
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param event_x_cor: координата события по горизонатли
    :param event_y_cor: координата события по вертикали
    :param score_num: число набранных очков
    :param tics_of_hard_ball: параметр тиков сложного мяча
    :param working_time: время работы программы (в тиках)
    :param stop_true_parameter: парметр отвечающий за то совершил ли сложный мячик остновку во время своей жизни,
    или нет (0 - нет, 1 - соврешил, 2 - соврешил и продолжил своё движение)
    :param game_over_tic_nums: время дляительности одной игры
    """
    for hard_ball in hard_ball_parameter:
        if ((hard_ball[0] - event_x_cor) ** 2 + (hard_ball[1] - event_y_cor) ** 2) ** 0.5 <= hard_ball[2]:
            score_num += 20
            hard_ball_parameter, massive_of_parameters = snitch_caching(hard_ball_parameter, massive_of_parameters)
            tics_of_hard_ball = working_time
            game_over_tic_nums += 100 * 80
            stop_true_parameter = 0
    return hard_ball_parameter, massive_of_parameters, score_num, tics_of_hard_ball, stop_true_parameter, \
           game_over_tic_nums


def new_ball(x, y, r, color):
    """
    делает шарик по указанным параметрам
    :param x: центр шарика по горизонтали
    :param y: центр шарика оп вертикали
    :param r: радиус шарика
    :param color: цвет шарика
    """
    circle(screen, color, (x, y), r)


def hard_ball_appearance(hard_ball_parameter):
    """
    Делает сложный мячик или снитч
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    """
    hard_balls_creating(hard_ball_parameter, 1)
    return hard_ball_parameter


def hard_balls_creating(hard_ball_parameter, how_many_balls):
    """
    Делает сложный мячик("снитч"). Заполняет  его массив необходимыми параметрами
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param how_many_balls: параметр, отвечающий за количество делаемых мячиков
    """
    for _ in range(how_many_balls):
        x = randint(100, 1100)
        y = randint(100, 760)
        r = randint(30, 100)
        color = COLORS[randint(0, 5)]
        hard_ball_parameter.append(
            [x, y, r, color, randint(15, 30) * (-1) ** randint(2, 3), randint(15, 30) * (-1) ** randint(2, 3), -1])
        new_ball(x, y, r, color)
    return hard_ball_parameter


def hard_balls_collisions_with_walls(hard_ball_parameter):
    """
    Функция механики столкновения сложного мяча со стенками
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    """
    for hard_ball in hard_ball_parameter:
        rho = hard_ball[2]
        if hard_ball[0] <= rho or 1200 - hard_ball[0] <= rho:
            hard_ball[0] -= 4 * hard_ball[4]
            hard_ball[4] = - (hard_ball[4] / abs(hard_ball[4])) * randint(10, 20) * (-1) ** randint(2, 3)
            hard_ball[5] = randint(10, 20) * (-1) ** randint(2, 3)
        elif hard_ball[1] <= rho or 860 - hard_ball[1] <= rho:
            hard_ball[1] -= 4 * hard_ball[5]
            hard_ball[5] = - (hard_ball[5] / abs(hard_ball[5])) * randint(10, 20) * (-1) ** randint(2, 3)
            hard_ball[4] = randint(10, 20) * (-1) ** randint(2, 3)
    return hard_ball_parameter


def hard_ball_stopping(working_time, tics_of_hard_ball, hard_ball_parameter, fps, stop_true_parameter):
    """
    Функция останвки сложного мяча для "заигрывания"
    :param working_time: время работы программы (в тиках)
    :param tics_of_hard_ball: параметр тиков сложного мяча
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param fps: фпс
    :param stop_true_parameter: парметр отвечающий за то совершил ли сложный мячик остновку во время своей жизни,
    или нет (0 - нет, 1 - соверешил, 2 - соврешил и продолжил своё движение)
    """
    for hard_ball in hard_ball_parameter:
        if stop_true_parameter == 0 and (working_time - tics_of_hard_ball) >= int(50 * fps):
            hard_ball[4] = 0.1
            hard_ball[5] = 0.1
            stop_true_parameter = 1
        if stop_true_parameter == 1 and (working_time - tics_of_hard_ball) >= int(60 * fps):
            hard_ball[4] = randint(15, 25) * (-1) ** randint(2, 3)
            hard_ball[5] = randint(15, 25) * (-1) ** randint(2, 3)
            stop_true_parameter = 2
    return hard_ball_parameter, stop_true_parameter


def hard_ball_changing(hard_ball_parameters):
    """
    Функция, изменяющая радиус и цвет сложного мячика
    :param hard_ball_parameters: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    """
    dr = 1
    for hard_ball in hard_ball_parameters:
        if hard_ball[6] > 0:
            hard_ball[2] += dr
            if hard_ball[2] >= 90:
                hard_ball[6] = -1
        else:
            hard_ball[2] -= dr
            if hard_ball[2] <= 2:
                hard_ball[6] = 1
        hard_ball[3] = COLORS[randint(0, 5)]
    return hard_ball_parameters


def balls_creating(massive_of_parameters, how_many_balls):
    """
    Делает мячики
    :param massive_of_parameters:  масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param how_many_balls: количество мячиков
    """
    for _ in range(how_many_balls):
        x = randint(100, 1100)
        y = randint(100, 760)
        r = randint(30, 100)
        color = COLORS[randint(0, 5)]
        massive_of_parameters.append(
            [x, y, r, color, randint(1, 7) * (-1) ** randint(2, 3), randint(1, 7) * (-1) ** randint(2, 3)])
        new_ball(x, y, r, color)
    return massive_of_parameters


def new_ball_having(massive_of_parameters):
    """
    Делает новый мячик
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    """
    balls_creating(massive_of_parameters, 1)
    return massive_of_parameters


def ball_new_position(x_cor, y_cor, radius, ball_color):
    """
    Меняет позицию шарика, не меняя его цвет и форму
    :param x_cor: новая координата по горизонтали шарика
    :param y_cor:новая координата по вертикали шарика
    :param radius: радус шарика
    :param ball_color: цвет шарика
    """
    circle(screen, ball_color, (x_cor, y_cor), radius)


def balls_moving(massive_of_parameters):
    """
    Функция отвечающая за движение определнных мячиков
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    """
    for ball in massive_of_parameters:
        ball[0] += ball[4]
        ball[1] += ball[5]
        ball_new_position(ball[0], ball[1], ball[2], ball[3])
    return massive_of_parameters


def old_ball_dying(massive_of_parameters):
    """
    Удаление с поля определенного мячика
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    """
    if len(massive_of_parameters) >= 3:
        index_num = randint(0, len(massive_of_parameters) - 3)
        massive_of_parameters.pop(index_num)
    return massive_of_parameters


def collisions_with_walls(massive_of_parameters):
    """
    Столкновение простых мчиков со стенами
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    """
    for ball in massive_of_parameters:
        rho = ball[2] + 5 * (2 ** 0.5)
        if ball[0] <= rho or 1200 - ball[0] <= rho:
            ball[0] -= 2 * ball[4]
            ball[4] = - (ball[4] / abs(ball[4])) * randint(1, 5) * (-1) ** randint(2, 3)
            # ball[5] = randint(1, 5) * (-1) ** randint(2, 3)
        elif ball[1] <= rho or 860 - ball[1] <= rho:
            ball[1] -= 2 * ball[5]
            ball[5] = - (ball[5] / abs(ball[5])) * randint(1, 5) * (-1) ** randint(2, 3)
            # ball[4] = randint(1, 5) * (-1) ** randint(2, 3)
    return massive_of_parameters


def snitch_caching(hard_ball_parameters, massive_of_parameters):
    """
    Функция делающая каскад разлетающихся простых шариков при пойманном "снитче"
    :param hard_ball_parameters: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    """
    num_of_new_balls = randint(10, 30)
    for _ in range(num_of_new_balls):
        color = COLORS[randint(0, 5)]
        new_ball(hard_ball_parameters[0][0], hard_ball_parameters[0][1], hard_ball_parameters[0][2], color)
        massive_of_parameters.append(
            [hard_ball_parameters[0][0], hard_ball_parameters[0][1], hard_ball_parameters[0][2],
             color, randint(10, 20) * (-1) ** randint(2, 3), randint(10, 20) * (-1) ** randint(2, 3)])
    hard_ball_parameters.pop(0)
    return hard_ball_parameters, massive_of_parameters


def hard_ball_live(working_time, tics_of_hard_ball, hard_ball_parameters, fps, stop_true_parameter):
    """
    Появление и исчезновение сложного мячика("снитча")
    :param working_time: время работы программы (в тиках)
    :param tics_of_hard_ball: параметр тиков сложного мяча
    :param hard_ball_parameters: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param fps: фпс
    :param stop_true_parameter: парметр отвечающий за то совершил ли сложный мячик остновку во время своей жизни,
    или нет (0 - нет, 1 - соврешил, 2 - соврешил и продолжил своё движение)
    """
    if (working_time - tics_of_hard_ball) >= int(200 * fps) and len(hard_ball_parameters) == 0:
        hard_balls_creating(hard_ball_parameters, 1)
        tics_of_hard_ball = working_time
    if working_time - tics_of_hard_ball >= int(260 * fps):
        hard_ball_parameters = []
        tics_of_hard_ball = working_time
        stop_true_parameter = 0
    return hard_ball_parameters, tics_of_hard_ball, stop_true_parameter


def balls_appearance_and_dying(massive_of_parameters, working_time, tics_of_simple_balls_appearing,
                               tics_of_simple_balls_dying, fps):
    """
    Появление и исчезновение простых мячиков
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param working_time: время работы программы (в тиках)
    :param tics_of_simple_balls_appearing: время появления простыхь мячиков
    :param tics_of_simple_balls_dying: время смерти простых мячиков
    :param fps: фсп
    """
    if (working_time - tics_of_simple_balls_appearing) >= int(fps * 40):
        new_ball_having(massive_of_parameters)
        tics_of_simple_balls_appearing = working_time
    if (working_time - tics_of_simple_balls_dying) >= int(fps * 60):
        old_ball_dying(massive_of_parameters)
        tics_of_simple_balls_dying = program_work_time
    return massive_of_parameters, tics_of_simple_balls_appearing, tics_of_simple_balls_dying


def simple_balls_main_function(massive_of_parameters, working_time, tics_of_simple_balls_appearing,
                               tics_of_simple_balls_dying, fps):
    """
    Функция объеденияющая функции относящиеся к простым мячикам
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param working_time: время работы программы (в тиках)
    :param tics_of_simple_balls_appearing: время появления простыхь мячиков
    :param tics_of_simple_balls_dying: время смерти простых мячиков
    :param fps: фсп
    """
    massive_of_parameters, tics_of_simple_balls_appearing, tics_of_simple_balls_dying = balls_appearance_and_dying(
        massive_of_parameters, working_time, tics_of_simple_balls_appearing, tics_of_simple_balls_dying, fps)
    collisions_with_walls(massive_of_parameters)
    balls_moving(massive_of_parameters)
    return massive_of_parameters, tics_of_simple_balls_appearing, tics_of_simple_balls_dying


def hard_ball_main_function(hard_ball_parameter, working_time, tics_of_hard_ball,
                            stop_true_parameter, fps):
    """
    Функция объеденияющая функции относящиеся к сложным мячикам
    :param hard_ball_parameter: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param working_time: время работы программы (в тиках)
    :param tics_of_hard_ball: параметр тиков сложного мяча
    :param stop_true_parameter: парметр отвечающий за то совершил ли сложный мячик остновку во время своей жизни,
    или нет (0 - нет, 1 - соверешил, 2 - соврешил и продолжил своё движение)
    :param fps: фпс
    """
    hard_ball_parameter, tics_of_hard_ball, stop_true_parameter = hard_ball_live(working_time, tics_of_hard_ball,
                                                                                 hard_ball_parameter, fps,
                                                                                 stop_true_parameter)
    hard_ball_changing(hard_ball_parameter)
    hard_balls_collisions_with_walls(hard_ball_parameter)
    balls_moving(hard_ball_parameter)
    hard_ball_parameter, stop_true_parameter = hard_ball_stopping(working_time, tics_of_hard_ball,
                                                                  hard_ball_parameter, fps, stop_true_parameter)
    return hard_ball_parameter, tics_of_hard_ball, stop_true_parameter


def game_event_main_analysis_function(massive_of_parameters, hard_ball_parameters, event_x_cor, event_y_cor,
                                      working_time, tics_of_hard_ball, score_num, game_over_tic_nums,
                                      stop_true_parameter):
    """
    Функция анализирующая влияние событий происходящихвнутри игры на игру(был ли пойман тот или иной мячик, оюновление
    счётчика)
    :param massive_of_parameters: масссив параметров простых мячиков. Каждый элемент массива есть подмасссив вида
    [координата х, координата у, радиус, цвет, малое премещение по х, малое перемещение по у]
    :param hard_ball_parameters: массив параметров сложного мячика, или "снитча" ([координата х, координата у,
    радиус(в данный момент), цвет(в данный момент), малое премещение по х, малое перемещение по у, параметр увеличения
    или уменьшения (+1 - увеличение или -1 - уменьшение)] )
    :param event_x_cor: координата события по горизонатли
    :param event_y_cor: координата события по вертикали
    :param working_time: время работы программы (в тиках)
    :param tics_of_hard_ball: параметр тиков сложного мяча
    :param score_num: счёт
    :param game_over_tic_nums: время дляительности одной игры
    :param stop_true_parameter: парметр отвечающий за то совершил ли сложный мячик остновку во время своей жизни,
    или нет (0 - нет, 1 - соверешил, 2 - соврешил и продолжил своё движение)
    """
    massive_of_parameters, score_num, game_over_tic_nums = simple_balls_cached(massive_of_parameters, event_x_cor,
                                                                               event_y_cor, score, game_over_tic_nums)
    hard_ball_parameters, massive_of_parameters, score_num, tics_of_hard_ball, stop_true_parameter, game_over_tic_nums \
        = hard_ball_cached(massive_of_parameters, hard_ball_parameters, event_x_cor, event_y_cor, score_num,
                           tics_of_hard_ball, working_time, stop_true_parameter, game_over_tic_nums)
    return massive_of_parameters, hard_ball_parameters, game_over_tic_nums, score_num, stop_true_parameter


pygame.display.update()
clock = pygame.time.Clock()
finished = False
# Переменная для отсчета количества тиков часов с начала времени раобы основного цикла
program_work_time = 0
# Задаём переменную ведущую счет пойманных шариков и описывапем переменные вывода её на экран
score = 0
score_table = new_font.render("SCORE:", False, (255, 255, 255))
# Переменная вывода самого числа пойманных шариков
num = new_font.render(str(score), False, (255, 255, 255))
# описываем переменную вывода табла времени на экран
time_table = new_font.render("TIME:", False, (255, 255, 255))
# Задаем пустой массива сложных мячиков ("снитчей")
hard_ball_param = []
# Параметр отвечающий за то сдела ли "снитч" остановку
stop_true = 0
# Зададим массив параметров простых мячей, пока что пустой
ball_params = []
# Параметр необходимый для произведения определнных действий со "снитчем"
time_of_hard_ball = 0
# Параметр необходимый некоторым функциям понять в какой момент создавать новый мячик
time_of_simple_balls_appearing = 0
# Параметр необходимый некоторым функциям понять в какой момент убирать один из мячиков на поле
time_of_simple_balls_dying = 0
# Начальное время продолжительности программы (1 минута)
game_over_time = 609 * FPS
# Сделаем три начальных шарика
balls_creating(ball_params, 3)
# Запускаем основной цикл
while not finished:
    clock.tick(FPS)
    if game_over_time - program_work_time <= 0:
        finished = True
    num2 = new_font.render(str(int((game_over_time - program_work_time) / FPS) // 10 + (
            int((game_over_time - program_work_time) / FPS) % 10) / 10), False, (255, 255, 255))
    num = new_font.render(str(score), False, (255, 255, 255))
    screen.blit(num2, (1130, 10))
    screen.blit(time_table, (1040, 10))
    screen.blit(score_table, (10, 10))
    screen.blit(num, (125, 10))
    program_work_time = pygame.time.get_ticks()
    hard_ball_param, time_of_hard_ball, stop_true = hard_ball_main_function(hard_ball_param, program_work_time,
                                                                            time_of_hard_ball, stop_true, FPS)
    ball_params, time_of_simple_balls_appearing, time_of_simple_balls_dying = simple_balls_main_function(
        ball_params,
        program_work_time,
        time_of_simple_balls_appearing,
        time_of_simple_balls_dying,
        FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x = event.pos[0]
            event.y = event.pos[1]
            ball_params, hard_ball_param, game_over_time, score, stop_true = game_event_main_analysis_function(
                ball_params, hard_ball_param, event.x, event.y, program_work_time, time_of_hard_ball, score,
                game_over_time, stop_true)
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()

with open("results.txt", "r+") as records:
    A = records.readlines()
    names_with_results = []
    for a in A:
        names_with_results.append(a.split())
    for name_and_result in names_with_results:
        # noinspection PyTypeChecker
        name_and_result[3] = int(name_and_result[3])
        name_and_result.pop(0)
    new_player = str(input("Please, write your name and surname here:"))
    new_player = new_player.split()
    names_with_results.append([new_player[0], new_player[1], score])
    j = -1
    for i in range(len(names_with_results)):
        j += 1
        for o in range(j, len(names_with_results)):
            if names_with_results[i][2] < names_with_results[o][2]:
                names_with_results[i], names_with_results[o] = names_with_results[o], names_with_results[i]

with open("results.txt", "w") as records:
    place_number = 1
    for name_and_result in names_with_results:
        if place_number == 11:
            break
        # noinspection PyTypeChecker
        name_and_result.insert(0, place_number)
        name_and_result.append("\n")
        name_and_result = " ".join(map(str, name_and_result))
        records.write(name_and_result)
        place_number += 1
