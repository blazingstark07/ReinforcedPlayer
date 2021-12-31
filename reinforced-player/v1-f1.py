import pygame as pg
import random
import random
import math
pg.init()

cell_size = 16
scl = 40
win_size = (scl*cell_size, scl*cell_size)

win = pg.display.set_mode(win_size)
pg.display.set_caption("SNAKE GAME")
clock = pg.time.Clock()
white_bike = pg.image.load('white_bike.png')
yellow_bike = pg.image.load('yellow_bike.png')

def distance(x, y, x1, y1):
    ret = math.sqrt((x-x1)**2+(y-y1)**2)
    return ret

class Bike(object):
        def __init__(self, x, y, height, width, colour, head):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.vel = cell_size
            self.dir = "stop"
            self.tail_size = 20
            self.tail_x = [self.x]*self.tail_size
            self.tail_y = [self.y]*self.tail_size
            self.colour = colour
            self.head = head

# To draw the snake and the fruit
        def move(self):
            self.tail_x.pop(0)
            self.tail_y.pop(0)
            self.tail_x.append(self.x)
            self.tail_y.append(self.y)
            if self.dir == "up":
                self.y -= self.vel
            elif self.dir == "down":
                self.y += self.vel
            elif self.dir == "left":
                self.x -= self.vel
            elif self.dir == "right":
                self.x += self.vel

        def draw(self):
            for i in range(self.tail_size):
                pg.draw.rect(
                    win, (self.colour[0], self.colour[1], self.colour[2]), (self.tail_x[i], self.tail_y[i], self.width, self.height))

                dir_head = self.head

                if self.dir == "up":
                    dir_head = pg.transform.rotate(self.head, 180)
                elif self.dir == "down":
                    dir_head = pg.transform.rotate(self.head, 0)
                elif self.dir == "left":
                    dir_head = pg.transform.rotate(self.head, -90)
                elif self.dir == "right":
                    dir_head = pg.transform.rotate(self.head, 90)

                win.blit(dir_head, (self.x, self.y, self.width, self.height))

        def die(self):
            if self.y < 0 or self.y > scl*cell_size-self.height or self.x < 0 or self.x > scl*cell_size-self.width:
               return True

            for i in range(self.tail_size):
                if distance(self.x, self.y, self.tail_x[i], self.tail_y[i]) < cell_size and self.dir!="stop":
                    return True


def redrawgamewindow(bike_white, bike_yellow, tl_crds):
    win.fill((0, 0, 0))
    pg.draw.line(win, (255, 0, 0), (0, 0), (0, scl*cell_size), width=1)
    pg.draw.line(win, (255, 0, 0), (0, 1), (scl*cell_size, 1), width=1)
    pg.draw.line(win, (255, 0, 0), (scl*cell_size-1, scl*cell_size), (scl*cell_size-1, 0), width=1)
    pg.draw.line(win, (255, 0, 0), (scl*cell_size, scl*cell_size-1), (0, scl*cell_size-1), width=1)
    bike_white.draw()
    bike_yellow.draw()
    for x, y in tl_crds:
        pg.draw.line(win, (255, 0, 0), (bike_white.x, bike_white.y), (x, y), width=1)


    pg.display.update()


def end_game(end_colour):
    pg.time.delay(500)
    win.fill((end_colour))
    pg.display.update()
    pg.time.delay(1000)

    return False


def start_test(config_path):        
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(game_loop,50)
    print('\nBest genome:\n{!s}'.format(winner))

def sign(x):
    if x == 0: return 0
    return x/abs(x)

def is_tch(crd, tail, dr):
    x, y = crd
    tx, ty = tail
    dx = tx - x
    dy = ty - y

    if sign(dx) != dr[0] or sign(dy) != dr[1]: return False
    
    if dr[1]==0: a, b, c = 0, 1, -y
    elif dr[0] == 0: a, b, c = 1, 0, -x
    else: a, b, c = -dr[1], dr[0], -dr[0]*y + dr[1]*x

    dst = abs(a*tx + b*ty + c)/(a**2 + b**2)**0.5
    if dst <= 1: return True

def game_loop():
    

    run = True
    bike_white = Bike(cell_size * 30, cell_size * 20, cell_size, cell_size, (255, 255, 255), white_bike)
    bike_yellow = Bike(cell_size * 20, cell_size * 20, cell_size, cell_size, (255, 255, 0), yellow_bike)

    while run:
        clock.tick(10)

    # To check the events done in the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    # To take the inputs of keys pressed
        keys = pg.key.get_pressed()

        move = (0, 0)
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        inputs = []
        tl_crds = []
        # print(i)
        for dr in dirs:
            dst = -1
            x, y = bike_white.x, bike_white.y
            for tx, ty in zip(bike_white.tail_x, bike_white.tail_y):
                if is_tch((x, y), (tx, ty), dr):
                    tl_crds.append((tx, ty))
                    dst = distance(x, y, tx, ty)
                    break
            if dst == -1:
                height, width = win_size
                if dr == (0, 1):
                    dst = height - y
                    tl_crds.append((x, height))
                elif dr == (0, -1):
                    dst = y
                    tl_crds.append((x, 0))
                elif dr == (1, 0):
                    dst = width - x
                    tl_crds.append((width, y))
                elif dr == (-1, 0):
                    dst = x
                    tl_crds.append((0, y))
                else: 
                    check = True
                    tmp_x, tmp_y = x, y
                    while check:
                        tmp_x += dr[0]
                        tmp_y += dr[1]

                        if tmp_x <= 0 or tmp_x > width or tmp_y <= 0 or tmp_y > height:
                            check = False
                            dst = distance(x, y, tmp_x, tmp_y)
                            tl_crds.append((tmp_x, tmp_y))
                             


            inputs.append(dst)
        print(inputs)
        if keys[pg.K_UP] and bike_white.dir != "down":
            bike_white.dir = "up"
        elif keys[pg.K_DOWN] and bike_white.dir != "up":
            bike_white.dir = "down"
        elif keys[pg.K_LEFT] and bike_white.dir != "right":
            bike_white.dir = "left"
        elif keys[pg.K_RIGHT] and bike_white.dir != "left":
            bike_white.dir = "right"

        if keys[pg.K_w] and bike_yellow.dir != "down":
            bike_yellow.dir = "up"
        elif keys[pg.K_s] and bike_yellow.dir != "up":
            bike_yellow.dir = "down"
        elif keys[pg.K_a] and bike_yellow.dir != "right":
            bike_yellow.dir = "left"
        elif keys[pg.K_d] and bike_yellow.dir != "left":
            bike_yellow.dir = "right"

        bike_white.move()
        bike_yellow.move()

        if run:
            redrawgamewindow(bike_white, bike_yellow, tl_crds)

        #gameover conditions
        if distance(bike_white.x, bike_white.y, bike_yellow.x, bike_yellow.y) <= cell_size and run:
            run = end_game((255, 0, 0))

        if bike_white.die() and run:
            run = end_game(bike_yellow.colour)
        if bike_yellow.die() and run:
            run = end_game(bike_white.colour)

        # check if the yellow bike crushed with white bike's tail
        for i in range(bike_white.tail_size):
            if distance(bike_yellow.x, bike_yellow.y, bike_white.tail_x[i], bike_white.tail_y[i]) < cell_size and run:
                run = end_game(bike_white.colour)

        # check if the white bike crushed with yellow bike's tail
        for i in range(bike_yellow.tail_size):
            if distance(bike_white.x, bike_white.y, bike_yellow.tail_x[i], bike_yellow.tail_y[i]) < cell_size and run:
                run = end_game(bike_yellow.colour)



game_loop()