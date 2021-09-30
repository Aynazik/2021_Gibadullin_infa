import pygame
from pygame.draw import *
import math as mt

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 800))

# фон рисунка
rect(screen, 'skyblue', (0, 0, 1000, 400), width=0)
rect(screen, 'lightgreen', (0, 400, 1000, 400), width=0)


# В дальнейшем параметр parside в функциях отвечает за разворот рисунка относительно вертикальной оси (регулируется двумя значениями 0 и 1)
# Функция задающая женщину. Здесь sh и vis максимальная ширина и высота туловища соответсвенно
def woman(x, y, sh, vis, parside):
    polygon(screen, 'MediumOrchid1', ((x, y), (x - sh / 2, y + vis), (x + sh / 2, y + vis)), width=0)
    circle(screen, 'peach puff', (x, y), vis * 0.15)
    aaline(screen, 'black', (x - 0.4 * sh / 2, y + vis), (x - 0.4 * sh / 2, y + 1.4 * vis))
    aaline(screen, 'black', (x - 0.4 * sh / 2, y + 1.4 * vis), (x - 0.55 * sh / 2, y + 1.4 * vis))
    aaline(screen, 'black', (x + 0.4 * sh / 2, y + vis), (x + 0.4 * sh / 2, y + 1.4 * vis))
    aaline(screen, 'black', (x + 0.4 * sh / 2, y + 1.4 * vis), (x + 0.55 * sh / 2, y + 1.4 * vis))
    if parside == 1:
        aalines(screen, 'black', False, [[x + 0.2 * (sh / 2), y + 0.2 * vis], [x + 0.8 * (sh / 2), y + 0.3 * vis],
                                         [x + 1.6 * (sh / 2), y + 0.2 * vis]])
        aaline(screen, 'black', (x - 0.2 * (sh / 2), y + 0.2 * vis), (x - 0.8 * sh, y + 0.7 * vis))
    else:
        aalines(screen, 'black', False, [[x - 0.2 * (sh / 2), y + 0.2 * vis], [x - 0.8 * (sh / 2), y + 0.3 * vis],
                                         [x - 1.6 * (sh / 2), y + 0.2 * vis]])
        aaline(screen, 'black', (x + 0.2 * (sh / 2), y + 0.2 * vis), (x + 0.8 * sh, y + 0.7 * vis))


# "Каждой бабе нужен мужик"
def man(x, y, sh, vis, parside):
    ellipse(screen, 'grey', (x - sh / 2, y, sh, vis))
    circle(screen, 'peach puff', (x, y - 0.13 * vis), 0.35 * sh)
    aaline(screen, 'black', (x + 0.4 * sh, y + 0.2 * vis), (x + 0.8 * sh, y + 0.7 * vis))
    aaline(screen, 'black', (x - 0.4 * sh, y + 0.2 * vis), (x - 0.8 * sh, y + 0.7 * vis))
    if parside == 1:
        aalines(screen, 'black', False,
                [[x + 0.3 * sh, y + 0.9 * vis], [x + 0.4 * sh, y + 1.4 * vis], [x + 0.5 * sh, y + 1.4 * vis]])
        aalines(screen, 'black', False,
                [[x - 0.3 * sh, y + 0.9 * vis], [x - 0.55 * sh, y + 1.43 * vis], [x - 0.65 * sh, y + 1.43 * vis]])
    else:
        aalines(screen, 'black', False,
                [[x - 0.3 * sh, y + 0.9 * vis], [x - 0.4 * sh, y + 1.4 * vis], [x - 0.5 * sh, y + 1.4 * vis]])
        aalines(screen, 'black', False,
                [[x + 0.3 * sh, y + 0.9 * vis], [x + 0.55 * sh, y + 1.43 * vis], [x + 0.65 * sh, y + 1.43 * vis]])


# Мороженка
def icecream(x, y, a, parside):
    i = mt.sin((5 / 180) * mt.pi)
    j = mt.cos((5 / 180) * mt.pi)
    i1 = mt.sin((25 / 180) * mt.pi)
    j1 = mt.cos((25 / 180) * mt.pi)
    phi = mt.atan(1 / (4 * mt.cos(mt.pi / 6)))
    if parside == 1:
        polygon(screen, 'gold2', ((x, y), (x + j1 * a, y - i1 * a), (x + i * a, y - j * a)), width=0)
        circle(screen, 'cyan2', (x + 1.28 * a * mt.cos(mt.radians(55)), y - 1.28 * a * mt.sin(mt.radians(55))), a * 0.3)
        circle(screen, 'red', (x + a * mt.cos(phi + mt.radians(53)), y - a * mt.sin(phi + mt.radians(53))), a * 0.28)
        circle(screen, 'green', (x + a * mt.cos(mt.radians(57) - phi), y - a * mt.sin(mt.radians(57) - phi)), a * 0.28)
    else:
        polygon(screen, 'gold2', ((x, y), (x - j1 * a, y - i1 * a), (x - i * a, y - j * a)), width=0)
        circle(screen, 'cyan2', (x - 1.28 * a * mt.cos(mt.radians(55)), y - 1.28 * a * mt.sin(mt.radians(55))), a * 0.3)
        circle(screen, 'red', (x - a * mt.cos(phi + mt.radians(53)), y - a * mt.sin(phi + mt.radians(53))), a * 0.28)
        circle(screen, 'green', (x - a * mt.cos(mt.radians(57) - phi), y - a * mt.sin(mt.radians(57) - phi)), a * 0.28)


# Сердечко (оно не так выглядит, спросите у биологов)
def heart(x, y, a, parside):
    i = mt.sin((5 / 180) * mt.pi)
    j = mt.cos((5 / 180) * mt.pi)
    i1 = mt.sin((25 / 180) * mt.pi)
    j1 = mt.cos((25 / 180) * mt.pi)
    phi = mt.atan(1 / (4 * mt.cos(mt.pi / 6)))
    if parside == 1:
        polygon(screen, 'red', ((x, y), (x + j1 * a, y - i1 * a), (x + i * a, y - j * a)), width=0)
        circle(screen, 'red', (x + a * mt.cos(phi + mt.radians(53)), y - a * mt.sin(phi + mt.radians(53))), a * 0.28)
        circle(screen, 'red', (x + a * mt.cos(mt.radians(57) - phi), y - a * mt.sin(mt.radians(57) - phi)), a * 0.28)
    else:
        polygon(screen, 'red', ((x, y), (x - j1 * a, y - i1 * a), (x - i * a, y - j * a)), width=0)
        circle(screen, 'red', (x - a * mt.cos(phi + mt.radians(53)), y - a * mt.sin(phi + mt.radians(53))), a * 0.28)
        circle(screen, 'red', (x - a * mt.cos(mt.radians(57) - phi), y - a * mt.sin(mt.radians(57) - phi)), a * 0.28)


# Подбирая необходимые параметры составляем нужный рисунок
man(400, 300, 100, 200, 1)
woman(600, 300, 150, 200, 1)
heart(750, 280, 80, 1)
icecream(400 - 0.8 * 100, 300 + 0.7 * 200, 60, 0)
aaline(screen, 'black', (750, 280), (600 + 1.6 * (150 / 2), 300 + 0.2 * 200))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
