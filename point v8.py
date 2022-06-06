from random import *
import pygame
import math

pygame.init()

# for create big point press LMB
# for create point press RMB
# for delete point press mouse wheel
# for pause/start press Space
# for exit press Esc or window cross

# parametrs
res = wid, hei = 1920, 1080
fps = 70
col_point = 200

brown = pygame.Color('#914626')
white = pygame.Color('#ffffff')

# creating window
win = pygame.display.set_mode(res, 0)
clock = pygame.time.Clock()

points = []
big_points = []


class Point: # creating class for points

    def __init__(self, x, y, r, color=brown):
        self.x = x
        self.y = y
        self.r = r
        self.near = False
        self.dist_near = 5000
        self.color = color

    def update(self):
        if not self.near in big_points: # unconnect
            self.near = False
            self.dist_near = 5000

        if not self in big_points: # find near big point and connection
            for b in big_points:
                dist = math.sqrt((b.x - self.x)**2 + (b.y - self.y)**2)
                if dist < self.dist_near:
                    self.near = b
                    self.dist_near = dist
                    break

        if self.near: # drawing connection
            pygame.draw.aaline(win, self.near.color, (self.x, self.y), (self.near.x, self.near.y), blend=1)

        if self.near: # drawing point
            pygame.draw.circle(win, self.near.color, (self.x, self.y), self.r)
        else:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.r)


def delete_point(x, y): # delete point
    for i in points:
        if math.sqrt((i.x - x)**2 + (i.y - y)**2) < 11:
            points.remove(i)
            if i in big_points:
                big_points.remove(i)


# creating points on window
for i in range(col_point):
    points.append(
        Point(randint(10, wid - 10), randint(10, hei - 10), 5))

# initiation text
pygame.font.init()
font1 = pygame.font.Font(None, 30)

# main cycle
go = True
while True:
    pressed = pygame.mouse.get_pressed()
    xt, yt = pygame.mouse.get_pos()  # find coordinate cursor
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
                p = Point(xt, yt, 10, (randint(0, 255), randint(0, 255), randint(0, 255)))
                points.append(p)
                big_points.append(p)
            if i.button == 2:  # mouse wheel
                delete_point(xt, yt)
            if i.button == 3: # RMB
                points.append(Point(xt, yt, 5))

    if go: # updating points
        win.fill(white)
        [p.update() for p in points]

    # itself text
    colm = font1.render('Количество точек: ' + str(len(points)), 1, (0, 0, 0))
    win.blit(colm, (3, 3))

    # updating window
    pygame.display.flip()
    pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
    clock.tick(fps)