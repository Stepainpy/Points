from random import *
import pygame
import math

pygame.init()

# for create standing point press LMB
# for create moving point press RMB
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hie = 1920, 1080
fps = 70
dist = 40
col_point = 300
speed = 10

blue = pygame.Color('#063971')
brown = pygame.Color('#914626')
gray = pygame.Color('#a8a8a8')
green = pygame.Color('#008f0e')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()
win.fill(gray)

move_points = []
stop_points = []


class Point: # creating class for points

    def __init__(self, x, y, ax, ay, color):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay
        self.color = color
        self.r = 5 # radius

    def update(self):
        # moving
        self.x += self.ax
        self.y += self.ay

        # reflection from the wall
        if self.x <= 0 or self.x >= wid:
            self.ax = -self.ax
        if self.y <= 0 or self.y >= hie:
            self.ay = -self.ay

        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

    def catch(self, list1, list2):
        for m in list1:
            if math.sqrt((m.x - self.x)**2 + (m.y - self.y)**2) <= dist: # check distance
                m.ax, m.ay = 0, 0
                m.color = green
                pygame.draw.line(win, blue, (self.x, self.y), (m.x, m.y), 2)
                list1.remove(m)
                list2.append(m)


def connection(): # temporarilly not work
    for i in stop_points:
        for j in stop_points:
            if math.sqrt((j.x - i.x)**2 + (j.y - i.y)**2) < dist:
                pygame.draw.line(win, blue, (i.x, i.y), (j.x, j.y), 2)


# creating points on window
for i in range(col_point):
    move_points.append(
        Point(randint(10, wid - 10), randint(10, hie - 10),
              randint(-speed, speed), randint(-speed, speed), brown))

# initiation text
pygame.font.init()
font1 = pygame.font.Font(None, 30)

# main cycle
go = True
while True:
    pressed = pygame.mouse.get_pressed()
    xt, yt = pygame.mouse.get_pos() # find coordinate cursor
    if pressed[2]: # RBM
        move_points.append(
            Point(xt, yt, randint(-speed, speed), randint(-speed, speed),
                  brown))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                exit()
            if i.key == pygame.K_SPACE:
                if go:
                    go = False
                else:
                    go = True
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1: # LMB
                stop_points.append(Point(xt, yt, 0, 0, green))

    if go: # updating points
        win.fill(gray)
        [p.update() for p in move_points]
        [p.update() for p in stop_points]
        [s.catch(move_points, stop_points) for s in stop_points]
        # connection()

        # itself text
        colm = font1.render('Количество двигающихся: ' + str(len(move_points)), 1, (0, 0, 0))
        win.blit(colm, (3, 3))
        cols = font1.render('Количество стоящих: ' + str(len(stop_points)), 1, (0, 0, 0))
        win.blit(cols, (3, 23))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)