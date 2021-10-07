import pygame
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 800))

# фон рисунка
pygame.draw.rect(screen, 'skyblue', (0, 0, 1000, 400))
pygame.draw.rect(screen, 'lightgreen', (0, 400, 1000, 400))

# разницу углов лучше не делать маленькой (работать при delta > 30), тк будет непропорционально тонкий рожок
alpha1 = 22  # угол от горизонтали нижней линии рожка мороженого
alpha2 = 75  # угол от горизонтали верхней линии рожка мороженого
# не рекомендую менять gamma парметры, тк сердце станет совсем непропорциональным
gamma1 = 20  # угол от горизонтали нижней линии сердца
gamma2 = 85  # угол от горизонтали верхней линии сердца


def woman(x, y, sh, vis, zerkalo):
    """
    рисует женщину

    :param x: координата x середины тела
    :param y: координата y верхней точки тела
    :param sh: ширина тела женщины
    :param vis: высота тела + головы женщины
    :param zerkalo: отзеркаливание рисунка (0 или 1)
    :return: ничего
    """
    y += 0.15 * vis  # смещение координаты y на высоту головы, чтобы опорная точка была на самом верху центра тела
    pygame.draw.polygon(screen, 'MediumOrchid1', ((x, y), (x - sh / 2, y + vis), (x + sh / 2, y + vis)))  # тело
    pygame.draw.circle(screen, 'peach puff', (x, y), vis * 0.15)  # голова
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh / 2, y + vis), (x - 0.4 * sh / 2, y + 1.4 * vis))  # левая нога
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh / 2, y + 1.4 * vis),
                       (x - 0.55 * sh / 2, y + 1.4 * vis))  # левая стопа
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh / 2, y + vis), (x + 0.4 * sh / 2, y + 1.4 * vis))  # правая нога
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh / 2, y + 1.4 * vis),
                       (x + 0.55 * sh / 2, y + 1.4 * vis))  # правая стопа
    if zerkalo == 0:
        zerkalo = -1
    pygame.draw.aalines(screen, 'black', False,
                        [[x + zerkalo * 0.2 * (sh / 2), y + 0.2 * vis], [x + zerkalo * 0.8 * (sh / 2), y + 0.3 * vis],
                         [x + zerkalo * 1.6 * (sh / 2), y + 0.2 * vis]])  # правая рука
    pygame.draw.aaline(screen, 'black', (x - zerkalo * 0.2 * (sh / 2), y + 0.2 * vis),
                       (x - zerkalo * 0.8 * sh, y + 0.7 * vis))  # левая рука


def man(x, y, sh, vis, zerkalo):
    """
    рисует мужчину

    :param x: координата x середины тела
    :param y: координата y верхней точки тела
    :param sh: ширина тела женщины
    :param vis: высота тела + головы женщины
    :param zerkalo: отзеркаливание рисунка (0 или 1)
    :return: ничего
    """
    y += 0.35 * sh + 0.13 * vis  # смещение координаты y на константу, чтобы опорная точка была
    # на самом верху центра тела
    pygame.draw.ellipse(screen, 'grey', (x - sh / 2, y, sh, vis))  # тело
    pygame.draw.circle(screen, 'peach puff', (x, y - 0.13 * vis), 0.35 * sh)  # голова
    pygame.draw.aaline(screen, 'black', (x + 0.4 * sh, y + 0.2 * vis), (x + 0.8 * sh, y + 0.7 * vis))  # правая рука
    pygame.draw.aaline(screen, 'black', (x - 0.4 * sh, y + 0.2 * vis), (x - 0.8 * sh, y + 0.7 * vis))  # левая рука
    if zerkalo == 0:
        zerkalo = -1  # при отзеркаливании меняется знак добавочной координаты => запихнём этот минус в формулу
    pygame.draw.aalines(screen, 'black', False,
                        [[x + zerkalo * 0.3 * sh, y + 0.9 * vis], [x + zerkalo * 0.4 * sh, y + 1.4 * vis],
                         [x + zerkalo * 0.5 * sh, y + 1.4 * vis]])  # правая нога при zerkalo = 1
    pygame.draw.aalines(screen, 'black', False,
                        [[x - zerkalo * 0.3 * sh, y + 0.9 * vis], [x - zerkalo * 0.55 * sh, y + 1.43 * vis],
                         [x - zerkalo * 0.65 * sh, y + 1.43 * vis]])  # левая нога при zerkalo = 1


def icecream(x, y, a, zerkalo):
    """
    рисует мороженое

    :param x: координата x острия рожка
    :param y: координата y острия рожка
    :param a: коэффициент увеличения размера мороженого
    :param zerkalo: отзеркаливание рисунка (0 или 1)
    :return: ничего
    """
    a *= 60  # получаем итоговый размер в виде стороны умноженной на увеличение
    phi1 = math.radians(alpha1)  # переводим углы из градусов в радианы
    phi2 = math.radians(alpha2)
    if zerkalo == 0:
        zerkalo = -1  # отзеркаливание отличается лишь знаком. Запихнём минус внутрь, чтобы сам считал
    # рисуем рожок через углы наклона
    pygame.draw.polygon(screen, 'gold2',
                        ((x, y), (x + zerkalo * math.cos(phi1) * a, y - math.sin(phi1) * a),
                         (x + zerkalo * math.cos(phi2) * a, y - math.sin(phi2) * a)))
    # рисуем шарики мороженого через углы: средний по биссектрисе, крайние смещены от края на 1/4 угла рожка
    pygame.draw.circle(screen, 'blue',
                       (x + zerkalo * 1.32 * a * math.cos((phi1 + phi2) / 2),
                        y - 1.32 * a * math.sin((phi1 + phi2) / 2)), a * 0.3)
    pygame.draw.circle(screen, 'red',
                       (x + zerkalo * a * math.cos((phi1 + phi2) / 2 + (phi2 - phi1) / 4),
                        y - a * math.sin((phi1 + phi2) / 2 + (phi2 - phi1) / 4)), a * 0.3)
    pygame.draw.circle(screen, 'green',
                       (x + zerkalo * a * math.cos((phi1 + phi2) / 2 - (phi2 - phi1) / 4),
                        y - a * math.sin((phi1 + phi2) / 2 - (phi2 - phi1) / 4)), a * 0.3)


def heart(x, y, a, zerkalo):
    """
    рисует красное сердечко

    :param x: координата x острия сердца
    :param y: координата y острия сердца
    :param a: коэффициент увеличения сердца
    :param zerkalo: отзеркаливание рисунка (0 или 1)
    :return: ничего
    """
    phi1 = math.radians(gamma1)
    phi2 = math.radians(gamma2)
    a *= 80  # умножаем увеличение на изначальную длину края сердца (от острия до касания круга)
    r = a / math.cos(math.atan(math.tan((phi2 - phi1) / 2) / 2))  # расстояние от острия до центра кругов
    r_circle = a * math.tan((phi2 - phi1) / 2) / 2  # радиус кругов
    if zerkalo == 0:
        zerkalo = -1  # отзеркаливание отличается лишь знаком. Запихнём минус внутрь, чтобы сам считал
    # рисуем треугольник ограниченный углами gamma1 и gamma2
    pygame.draw.polygon(screen, 'red', ((x, y), (x + zerkalo * math.cos(phi1) * a, y - math.sin(phi1) * a),
                                        (x + zerkalo * math.cos(phi2) * a, y - math.sin(phi2) * a)))
    # рисуем 2 круга, касающиеся сторон (которые под углами gamma1 и gamma2) на расстоянии a от острия и пересекающиеся
    # на перпендикуляре к этой точке
    pygame.draw.circle(screen, 'red',
                       (x + zerkalo * r * math.cos(phi2 - math.atan(math.tan((phi2 - phi1) / 2) / 2)),
                        y - a * math.sin(phi2 - math.atan(math.tan((phi2 - phi1) / 2) / 2))), r_circle)
    pygame.draw.circle(screen, 'red',
                       (x + zerkalo * a * math.cos(phi1 + math.atan(math.tan((phi2 - phi1) / 2) / 2)),
                        y - r * math.sin(phi1 + math.atan(math.tan((phi2 - phi1) / 2) / 2))), r_circle)


# Подбирая необходимые параметры составляем нужный рисунок
man(220, 250, 80, 175, 0)
woman(384, 275, 126, 175, 1)
woman(640, 275, 126, 175, 0)
man(804, 250, 80, 175, 1)
heart(105, 280, 1, 0)
icecream(804 + 0.8 * 80, 300 + 0.7 * 175, 1.25, 1)
pygame.draw.aaline(screen, 'black', (105, 280), (220 - 0.8 * 80, 300 + 0.7 * 175))

# totalitarizm
image = pygame.image.load('cerp.jpg').convert_alpha()
new_image = pygame.transform.scale(image, (110, 110))
new_image.set_colorkey('white')  # убираем белый фон
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
