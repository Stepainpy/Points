from random import *
import numpy as np
import pygame
import math

pygame.init()

# initiation text
pygame.font.init()
font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 18)

# for create big point press LMB
# for create point press RMB
# for delete point press mouse wheel
# for turn on gravity press g
# for turn on antigravity press a
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hei = 1920, 1080
fps = 70
step = 2
col_point = 1000

brown = pygame.Color('#914626')
white = pygame.Color('#ffffff')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []
big_points = []


class Point:  # creating class for points

    def __init__(self, x, y, r, color=brown):
        self.x = x
        self.y = y
        self.r = r
        self.near = None
        self.dist_near = 5000
        self.color = color

    def update(self):
        if not self.near in big_points:  # unconnect
            self.near = None
            self.dist_near = 5000

        if not self in big_points:  # find near big point and connection
            for b in big_points:
                dist = math.sqrt((b.x - self.x)**2 + (b.y - self.y)**2)
                if dist < self.dist_near:
                    self.near = b
                    self.dist_near = dist

        if self.near:  # drawing point
            pygame.draw.circle(win, self.near.color, (self.x, self.y), self.r)
        else:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.r)

        # fun function
        self.values_text()

    def gravity(self, g='n'):  # to bring points closer or push them away from large ones
        for i in points:
            if self == i.near:
                # relative coordinate
                ot_x = i.x - self.x
                ot_y = i.y - self.y

                r = math.sqrt(ot_x**2 + ot_y**2) # distance
                i.dist_near = r
                if g == 'n':
                    r -= step
                elif g == 'a':
                    r += step

                if r > -1:
                    try:
                        f = np.arctan(ot_y / ot_x)
                    except:
                        f = 1

                    xt = r * math.cos(f)
                    yt = r * math.sin(f)

                    if ot_x > 0:
                        i.x = self.x + xt
                        i.y = self.y + yt
                    else:
                        i.x = self.x - xt
                        i.y = self.y - yt

    # fun function in class:
    def values_text(self):
        if not self in big_points:
            txt = font2.render(str(round(self.dist_near)), 1, (0, 0, 0))
            win.blit(txt, (self.x+2, self.y+2))


# fun function outside class:
def connect_dist_near():
    objs = {}
    dists = []
    pos = []
    for i in points:
        if not i in big_points and i.near:
            objs[i.dist_near] = i

    if big_points:
        for j in objs:
            dists.append(j)
        dists.sort()

        for p in dists:
            pos.append([objs[p].x, objs[p].y])
        
        pygame.draw.aalines(win, (0, 0, 0), 0, pos, 1)


def delete_point(x, y):  # delete point
    for i in points:
        if math.sqrt((i.x - x)**2 + (i.y - y)**2) < 11:
            points.remove(i)
            if i in big_points:
                big_points.remove(i)


# creating points on window
for i in range(col_point):
    points.append(Point(randint(10, wid - 10), randint(10, hei - 10), 5))

# main cycle
go = True
while True:
    pressed = pygame.key.get_pressed()
    mpressed = pygame.mouse.get_pressed()
    xt, yt = pygame.mouse.get_pos()  # find coordinate cursor

    if pressed[pygame.K_g]:
        [p.gravity() for p in points if p in big_points]

    if pressed[pygame.K_a]:
        [p.gravity('a') for p in points if p in big_points]

    if mpressed[2] and pressed[pygame.K_LSHIFT]:
        points.append(Point(xt, yt, 5))

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
            if i.button == 1:  # LMB
                w = Point(xt, yt, 10,
                          (randint(0, 255), randint(0, 255), randint(0, 255)))
                points.append(w)
                big_points.append(w)
            if i.button == 2:  # mouse wheel
                delete_point(xt, yt)
            if i.button == 3:  # RMB
                points.append(Point(xt, yt, 5))

    if go:  # updating points
        win.fill(white)
        [p.update() for p in points]

    # connect_dist_near()

    # itself text
    colm = font1.render('Количество точек: ' + str(len(points)), 1, (0, 0, 0))
    win.blit(colm, (3, 3))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)