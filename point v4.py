from random import *
import pygame
import math

pygame.init()

# parametrs
res = wid, hei = 1920, 1080
fps = 70
col_point = 0
speed = 8

blue = pygame.Color('#063971')
brown = pygame.Color('#914626')
green = pygame.Color('#008f0e')
gray = pygame.Color('#a8a8a8')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []
neutrons = []
urans = []


class Point: # creating class for points

    def __init__(self, x, y, ax, ay, color, pulse=0):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay
        self.color = color
        self.pulse = pulse

    def update(self):
        # moving
        self.x += self.ax
        self.y += self.ay

        # reflection from the wall
        if self.x <= 0 or self.x >= wid:
            self.ax = -self.ax
        if self.y <= 0 or self.y >= hei:
            self.ay = -self.ay

        # pulse fading
        if self.pulse <= 0 and self.color == brown:
            self.ax, self.ay = 0, 0
        else:
            self.pulse -= 1

        # defining a point
        if self.color == green:
            pygame.draw.circle(win, self.color, (self.x, self.y), 10)
        elif self.color == blue:
            pygame.draw.circle(win, self.color, (self.x, self.y), 3)
        else:
            pygame.draw.circle(win, self.color, (self.x, self.y), 5)

    def decay(self):
        if self.color == green:
            for n in neutrons:
                if math.sqrt((n.x - self.x)**2 + (n.y - self.y)**2) <= 7:
                    points.remove(n)
                    neutrons.remove(n)

                    for i in range(randint(2, 3)):
                        neu = Point(self.x, self.y, randint(-speed, speed), randint(-speed, speed), blue)
                        points.append(neu)
                        neutrons.append(neu)
                    
                    for i in range(2):
                        points.append(Point(self.x, self.y, randint(-speed, speed), randint(-speed, speed), brown, 10))
                    
                    points.remove(self)
                    break



# creating points on window
for i in range(col_point):
    points.append(
        Point(randint(10, wid - 10), randint(10, hei - 10), 0, 0, green))

# initiation text
pygame.font.init()
font1 = pygame.font.Font(None, 30)

# main cycle
go = True
while True:
    xt, yt = pygame.mouse.get_pos() # find coordinate cursor
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
                p = Point(xt, yt, randint(-speed, speed), randint(-speed, speed), blue)
                points.append(p)
                neutrons.append(p)
            if i.button == 3: # RMB
                p = Point(xt, yt, 0, 0, green)
                points.append(p)
                urans.append(p)

    if go: # updating points
        win.fill(gray)
        [p.update() for p in points]
        [p.decay() for p in points]

        col_u = 0
        col_n = 0
        for i in points:
            if i.color == green:
                col_u += 1
            if i.color == blue:
                col_n += 1

        # itself text
        uran = font1.render('Количество урана: ' + str(col_u), 1, (0, 0, 0))
        win.blit(uran, (3, 3))
        neutron = font1.render('Количество нейтронов: ' + str(col_n), 1, (0, 0, 0))
        win.blit(neutron, (3, 23))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)
