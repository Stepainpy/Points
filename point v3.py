from random import *
import pygame
import math

pygame.init()

# for create charge point press LMB
# for create no charge point press RMB or mouse wheel for package
# for stopping a point when it is created and vice versa press S
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hei = 1920, 1080
fps = 70
dist = 50
col_point = 2000
speed = 8

blue = pygame.Color('#063971')
brown = pygame.Color('#914626')
cyan = pygame.Color('#00a6ed')
gray = pygame.Color('#a8a8a8')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []
charge_points = []


class Point: # creating class for points

    def __init__(self, x, y, ax, ay, color, charge=False, wears=False):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay
        self.color = color
        self.r = 5 # radius

        self.charge = charge
        #self.wears = wears

    def update(self):
        # moving
        self.x += self.ax
        self.y += self.ay

        # reflection from the wall
        if self.x <= 0 or self.x >= wid:
            self.ax = -self.ax
        if self.y <= 0 or self.y >= hei:
            self.ay = -self.ay

        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

        if self.charge: # visualization of the action field
            pygame.draw.circle(win, cyan, (self.x, self.y), dist - 2, 2)

    def killing(self):
        for i in charge_points:
            if i.charge and i != self and not self.charge: # checking for their difference and the charge of one
                if math.sqrt((i.x - self.x)**2 + (i.y - self.y)**2) <= dist: # check distance
                    pygame.draw.line(win, cyan, (i.x, i.y), (self.x, self.y), 2)
                    self.charge = True
                    #self.wears = True
                    self.color = blue

                    charge_points.append(self)
                    points.remove(i)
                    charge_points.remove(i)


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
    pressed = pygame.mouse.get_pressed()
    xt, yt = pygame.mouse.get_pos() # find coordinate cursor
    if pressed[2]: # RMB
        points.append(
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
                p = Point(xt, yt, randint(-speed, speed),
                          randint(-speed, speed), blue, True, True)
                points.append(p)
                charge_points.append(p)
            if i.button == 2: # mouse wheel
                for i in range(100):
                    points.append(
                        Point(xt + randint(-30, 30), yt + randint(-30, 30),
                              randint(-speed, speed), randint(-speed, speed),
                              brown))

    if go: # updating points
        win.fill(gray)
        [p.update() for p in points]
        [p.killing() for p in points]

        # itself text
        colm = font1.render('Количество точек: ' + str(len(points)), 1, (0, 0, 0))
        win.blit(colm, (3, 3))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)
