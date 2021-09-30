import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 600))
screen.fill('white')

# тело
circle(screen, 'yellow', (500, 300), 200)
circle(screen, 'black', (500, 300), 200, width=1)

# глазки
circle(screen, 'red', (420, 250), 40)
circle(screen, 'black', (420, 250), 40, width=1)
circle(screen, 'black', (420, 250), 22)
circle(screen, 'red', (580, 250), 30)
circle(screen, 'black', (580, 250), 30, width=1)
circle(screen, 'black', (580, 250), 22)

# броовки
rect(screen, 'black', (420, 400, 160, 30))
polygon(screen, 'black', [(350, 150), (360, 140), (470, 220), (460, 230)])
polygon(screen, 'black', [(650, 170), (640, 160), (530, 230), (540, 240)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
