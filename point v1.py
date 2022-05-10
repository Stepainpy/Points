import pygame
import math
from random import *

pygame.init()

# for revers press B
# for pause/start press Space
# for exit press Esc

# parametrs
res = wid, hie = 1920, 1080
fps = 60
col_point = 125
speed = 3
dist = 150

brown = pygame.Color('#914626')
green = pygame.Color('#008f0e')
blue = pygame.Color('#063971')
gray = pygame.Color('#a8a8a8')

# creating window
win = pygame.display.set_mode(res)
clock = pygame.time.Clock()
win.fill(gray)

points = [] # itself list points


class Point: # creating class for points

    def __init__(self, x, y, ax, ay):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay

    def update(self):
        # moving
        self.x += self.ax
        self.y += self.ay

        # reflection from the wall
        if self.x <= 0 or self.x >= wid:
            self.ax = -self.ax
        if self.y <= 0 or self.y >= hie:
            self.ay = -self.ay

        if self.ax == 0 and self.ay == 0:
            pygame.draw.circle(win, green, (self.x, self.y), 5)
        else:
            pygame.draw.circle(win, brown, (self.x, self.y), 5)


# creating points on window
for i in range(col_point):
    points.append(
        Point(randint(10, wid - 10), randint(10, hie - 10),
              randint(-speed, speed), randint(-speed, speed)))


# connection between points
def drawing():
    for point_1 in points:
        for point_2 in points:
            if (point_2.x, point_2.y) != (point_1.x, point_1.y):
                if math.sqrt((point_2.x - point_1.x)**2 +
                             (point_2.y - point_1.y)**2) <= dist:
                    pygame.draw.aaline(win,
                                       blue, (point_1.x, point_1.y),
                                       (point_2.x, point_2.y),
                                       blend=1)


def revers(point):
    for p in point:
        p.ax, p.ay = -p.ax, -p.ay


# main cycle
go = True
while True:
    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                exit()
            if i.key == pygame.K_b:
                revers(points)
            if i.key == pygame.K_SPACE:
                if go:
                    go = False
                else:
                    go = True

    if go: # updating points
        win.fill(gray)
        [p.update() for p in points]
        drawing()

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)