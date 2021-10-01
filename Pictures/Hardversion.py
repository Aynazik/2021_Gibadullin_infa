import pygame
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 800))

# фон рисунка
pygame.draw.rect(screen, 'skyblue', (0, 0, 1000, 400))
pygame.draw.rect(screen, 'lightgreen', (0, 400, 1000, 400))


def woman(x, y, sh, vis, parside):
    '''
    рисует женщину

    :param x: координата x середины тела
    :param y: координата y верхней точки тела
    :param sh: ширина тела женщины
    :param vis: высота тела + головы женщины
    :param parside: отзеркаливание рисунка (0 или 1)
    :return: ничего
    '''
    y += 0.15 * vis  # смещение координаты y на высоту головы, чтобы опорная точка была на самом верху центра тела
    pygame.draw.polygon(screen, 'MediumOrchid1', ((x, y), (x - sh / 2, y + vis), (x + sh / 2, y + vis)))  # тело
    pygame.draw.circle(screen, 'peach puff', (x, y), vis * 0.15)  # голова
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh / 2, y + vis), (x - 0.4 * sh / 2, y + 1.4 * vis))  # левая нога
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh / 2, y + 1.4 * vis),
                       (x - 0.55 * sh / 2, y + 1.4 * vis))  # левая стопа
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh / 2, y + vis), (x + 0.4 * sh / 2, y + 1.4 * vis))  # правая нога
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh / 2, y + 1.4 * vis),
                       (x + 0.55 * sh / 2, y + 1.4 * vis))  # правая стопа
    if parside == 1:
        pygame.draw.aalines(screen, 'black', False,
                            [[x + 0.2 * (sh / 2), y + 0.2 * vis], [x + 0.8 * (sh / 2), y + 0.3 * vis],
                             [x + 1.6 * (sh / 2), y + 0.2 * vis]])  # правая рука
        pygame.draw.aaline(screen, 'black', (x - 0.2 * (sh / 2), y + 0.2 * vis),
                           (x - 0.8 * sh, y + 0.7 * vis))  # левая рука
    else:
        pygame.draw.aalines(screen, 'black', False,
                            [[x - 0.1 * sh, y + 0.2 * vis], [x - 0.4 * sh, y + 0.3 * vis],
                             [x - 0.8 * sh, y + 0.2 * vis]])  # левая рука
        pygame.draw.aaline(screen, 'black', (x + 0.2 * (sh / 2), y + 0.2 * vis),
                           (x + 0.8 * sh, y + 0.7 * vis))  # правая рука


def man(x, y, sh, vis, parside):
    '''
    рисует мужчину

    :param x: координата x середины тела
    :param y: координата y верхней точки тела
    :param sh: ширина тела женщины
    :param vis: высота тела + головы женщины
    :param parside: отзеркаливание рисунка (0 или 1)
    :return: ничего
    '''
    y += 0.35 * sh + 0.13 * vis  # смещение координаты y на константу, чтобы опорная точка была
    # на самом верху центра тела
    pygame.draw.ellipse(screen, 'grey', (x - sh / 2, y, sh, vis))  # тело
    pygame.draw.circle(screen, 'peach puff', (x, y - 0.13 * vis), 0.35 * sh)  # голова
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh, y + 0.2 * vis), (x + 0.8 * sh, y + 0.7 * vis))  # правая рука
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh, y + 0.2 * vis), (x - 0.8 * sh, y + 0.7 * vis))  # левая рука
    if parside == 1:
        pygame.draw.aalines(screen, 'black', False,
                            [[x + 0.3 * sh, y + 0.9 * vis], [x + 0.4 * sh, y + 1.4 * vis],
                             [x + 0.5 * sh, y + 1.4 * vis]])  # правая нога
        pygame.draw.aalines(screen, 'black', False,
                            [[x - 0.3 * sh, y + 0.9 * vis], [x - 0.55 * sh, y + 1.43 * vis],
                             [x - 0.65 * sh, y + 1.43 * vis]])  # левая нога
    else:
        pygame.draw.aalines(screen, 'black', False,
                            [[x - 0.3 * sh, y + 0.9 * vis], [x - 0.4 * sh, y + 1.4 * vis],
                             [x - 0.5 * sh, y + 1.4 * vis]])  # левая нога
        pygame.draw.aalines(screen, 'black', False,
                            [[x + 0.3 * sh, y + 0.9 * vis], [x + 0.55 * sh, y + 1.43 * vis],
                             [x + 0.65 * sh, y + 1.43 * vis]])  # правая нога


def icecream(x, y, a, parside):
    '''
    рисует мороженое

    :param x:
    :param y:
    :param a: коэффициент увеличения размера мороженого
    :param parside: отзеркаливание рисунка (0 или 1)
    :return: ничего
    '''
    i = math.sin((5 / 180) * math.pi)
    j = math.cos((5 / 180) * math.pi)
    i1 = math.sin((25 / 180) * math.pi)
    j1 = math.cos((25 / 180) * math.pi)
    phi = math.atan(1 / (4 * math.cos(math.pi / 6)))
    if parside == 1:
        pygame.draw.polygon(screen, 'gold2', ((x, y), (x + j1 * a, y - i1 * a), (x + i * a, y - j * a)))
        pygame.draw.circle(screen, 'cyan2',
                           (x + 1.28 * a * math.cos(math.radians(55)), y - 1.28 * a * math.sin(math.radians(55))),
                           a * 0.3)
        pygame.draw.circle(screen, 'red',
                           (x + a * math.cos(phi + math.radians(53)), y - a * math.sin(phi + math.radians(53))),
                           a * 0.28)
        pygame.draw.circle(screen, 'green',
                           (x + a * math.cos(math.radians(57) - phi), y - a * math.sin(math.radians(57) - phi)),
                           a * 0.28)
    else:
        pygame.draw.polygon(screen, 'gold2', ((x, y), (x - j1 * a, y - i1 * a), (x - i * a, y - j * a)))
        pygame.draw.circle(screen, 'cyan2',
                           (x - 1.28 * a * math.cos(math.radians(55)), y - 1.28 * a * math.sin(math.radians(55))),
                           a * 0.3)
        pygame.draw.circle(screen, 'red',
                           (x - a * math.cos(phi + math.radians(53)), y - a * math.sin(phi + math.radians(53))),
                           a * 0.28)
        pygame.draw.circle(screen, 'green',
                           (x - a * math.cos(math.radians(57) - phi), y - a * math.sin(math.radians(57) - phi)),
                           a * 0.28)


# Сердечко (оно не так выглядит, спросите у биологов)
def heart(x, y, a, parside):
    i = math.sin((5 / 180) * math.pi)
    j = math.cos((5 / 180) * math.pi)
    i1 = math.sin((25 / 180) * math.pi)
    j1 = math.cos((25 / 180) * math.pi)
    phi = math.atan(1 / (4 * math.cos(math.pi / 6)))
    if parside == 1:
        pygame.draw.polygon(screen, 'red', ((x, y), (x + j1 * a, y - i1 * a), (x + i * a, y - j * a)))
        pygame.draw.circle(screen, 'red',
                           (x + a * math.cos(phi + math.radians(53)), y - a * math.sin(phi + math.radians(53))),
                           a * 0.28)
        pygame.draw.circle(screen, 'red',
                           (x + a * math.cos(math.radians(57) - phi), y - a * math.sin(math.radians(57) - phi)),
                           a * 0.28)
    else:
        pygame.draw.polygon(screen, 'red', ((x, y), (x - j1 * a, y - i1 * a), (x - i * a, y - j * a)))
        pygame.draw.circle(screen, 'red',
                           (x - a * math.cos(phi + math.radians(53)), y - a * math.sin(phi + math.radians(53))),
                           a * 0.28)
        pygame.draw.circle(screen, 'red',
                           (x - a * math.cos(math.radians(57) - phi), y - a * math.sin(math.radians(57) - phi)),
                           a * 0.28)


# Подбирая необходимые параметры составляем нужный рисунок
man(220, 250, 80, 175, 1)
woman(384, 275, 126, 175, 1)
woman(640, 275, 126, 175, 0)
man(804, 250, 80, 175, 1)
heart(105, 280, 80, 0)
icecream(804 + 0.8 * 80, 300 + 0.7 * 175, 60, 1)
pygame.draw.aaline(screen, 'black', (105, 280), (220 - 0.8 * 80, 300 + 0.7 * 175))

# totalitarizm
image = pygame.image.load('cerp.jpg').convert_alpha()
new_image = pygame.transform.scale(image, (110, 110))
new_image.set_colorkey((255, 255, 255))
screen.blit(new_image, (460, 250))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
