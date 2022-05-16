from random import *
from time import *
import pygame

pygame.init()

# for create growthfull point press LMB
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hei = 1920, 1080
fps = 70
col_point = 0
speed = 6

green = pygame.Color('#008f0e')
gray = pygame.Color('#a8a8a8')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []


class Point: # creating class for points

    def __init__(self, x, y, ax, ay, color, pulse):
        self.x = x
        self.y = y
        self.ax = ax
        self.ay = ay
        self.color = color
        self.pulse = pulse

        self.radius = 5
        self.stage = 5
        self.timer = 0
        self.growth = 5/self.stage

    def update(self):
        if self.pulse != 0:
            # moving
            self.x += self.ax
            self.y += self.ay

            # reflection from the wall
            if self.x <= 0 or self.x >= wid:
                self.ax = -self.ax
            if self.y <= 0 or self.y >= hei:
                self.ay = -self.ay

            self.pulse -= 1
        else:
            self.ax, self.ay = 0, 0

        self.timer += 1

        if self.timer - fps > 0: # checking time
            if self.stage != 0: # cheching on division
                self.radius += self.growth
                self.stage -= 1
                self.timer = 0
            else:
                self.division()

        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def division(self):
        sx, sy = randint(-speed, speed), randint(-speed, speed)
        p = randint(1, 20)
        
        points.append(Point(self.x, self.y, sx, sy, green, p))
        points.append(Point(self.x, self.y, -sx, -sy, green, p))

        points.remove(self)


# creating points on window
for i in range(col_point):
    points.append(
        Point(randint(10, wid - 10), randint(10, hei - 10), 0, 0, green, 0))

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
                points.append(Point(xt, yt, 0, 0, green, 0))

    if go: # updating points
        win.fill(gray)
        [p.update() for p in points]

        # itself text
        colm = font1.render('Количество точек: ' + str(len(points)), 1, (0, 0, 0))
        win.blit(colm, (3, 3))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)