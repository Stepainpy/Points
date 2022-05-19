from random import *
import pygame
import math

pygame.init()

# for create blue portal press LMB
# for create orange portal press RMB
# for create point press mouse wheel
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hei = 1920, 1080
fps = 70
col_point = 0
speed = 8

blue = pygame.Color('#063971')
orange = pygame.Color('#ff7b00')
brown = pygame.Color('#914626')
green = pygame.Color('#008f0e')
white = pygame.Color('#ffffff')
gray = pygame.Color('#a8a8a8')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []
blue_portals = []
orange_portals = []


class Point: # creating class for points

    def __init__(self, x, y, ax, ay, color):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay
        self.color = color

    def update(self):
        # moving
        self.x += self.ax
        self.y += self.ay

        # reflection from the wall
        if self.x <= 0 or self.x >= wid:
            self.ax = -self.ax
        if self.y <= 0 or self.y >= hei:
            self.ay = -self.ay

        pygame.draw.circle(win, self.color, (self.x, self.y), 5)

    def tp(self, b, o):
        xa = self.x - b.x
        ya = self.y - b.y

        xa = -xa
        ya = -ya

        xa = xa + self.ax + o.x
        ya = ya + self.ay + o.y

        self.x = xa
        self.y = ya


class Portal(Point): # using class Point creating class Portal

    def __init__(self, x, y, ax, ay, color):
        super().__init__(x, y, ax, ay, color)
        self.connection = False
        self.partner = None

    def update(self):
        if not self.connection:
            if self.color == blue:
                for i in orange_portals:
                    if not i.connection:
                        self.partner = i
                        self.connection = True

                        i.partner = self
                        i.connection = True
                        break
            elif self.color == orange:
                for i in blue_portals:
                    if not i.connection:
                        self.partner = i
                        self.connection = True

                        i.partner = self
                        i.connection = True
                        break
        else:
            for p in points:
                if math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2) <= 26:
                    p.tp(self, self.partner)

        if self.connection:
            pygame.draw.circle(win, white, (self.x, self.y), 20)
        else:
            pygame.draw.circle(win, gray, (self.x, self.y), 20)

        pygame.draw.circle(win, self.color, (self.x, self.y), 20, 3)

            

# creating points on window
for i in range(col_point):
    points.append(
        Point(randint(10, wid - 10), randint(10, hei - 10),
              randint(-speed, speed), randint(-speed, speed), brown))
              
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
                blue_portals.append(Portal(xt, yt, 0, 0, blue))
            if i.button == 2: # mouse wheel
                points.append(Point(xt, yt, randint(-speed, speed), randint(-speed, speed), brown))
            if i.button == 3: # RMB
                orange_portals.append(Portal(xt, yt, 0, 0, orange))

    if go: # updating points and portals
        win.fill(gray)
        [p.update() for p in points]
        [b.update() for b in blue_portals]
        [o.update() for o in orange_portals]

        # itself text
        colm = font1.render('Количество точек: ' + str(len(points)), 1, (0, 0, 0))
        win.blit(colm, (3, 3))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)