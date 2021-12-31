import pygame as pg
import random
import random
import math
import pickle
import neat
pg.init()

winner = pickle.load(open("step3.pkl", 'rb'))
config_path = 'config-feedforward.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)
model = neat.nn.FeedForwardNetwork.create(winner, config)

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


def redrawgamewindow(bike_white, bike_yellow):
    win.fill((0, 0, 0))
    pg.draw.line(win, (255, 0, 0), (0, 0), (0, scl*cell_size), width=1)
    pg.draw.line(win, (255, 0, 0), (0, 1), (scl*cell_size, 1), width=1)
    pg.draw.line(win, (255, 0, 0), (scl*cell_size-1, scl*cell_size), (scl*cell_size-1, 0), width=1)
    pg.draw.line(win, (255, 0, 0), (scl*cell_size, scl*cell_size-1), (0, scl*cell_size-1), width=1)
    bike_white.draw()
    bike_yellow.draw()


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

    winner = p.run(game_loop,100)
    print('\nBest genome:\n{!s}'.format(winner))

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

        if keys[pg.K_UP] and bike_white.dir != "down":
            bike_white.dir = "up"
        elif keys[pg.K_DOWN] and bike_white.dir != "up":
            bike_white.dir = "down"
        elif keys[pg.K_LEFT] and bike_white.dir != "right":
            bike_white.dir = "left"
        elif keys[pg.K_RIGHT] and bike_white.dir != "left":
            bike_white.dir = "right"


        window = {}
        move = (0, 0)
        for i in range(-5, 6, 1):
            for j in range(-5, 6, 1):
                tmp_x, tmp_y = (bike_yellow.x - i*cell_size, bike_yellow.y - j*cell_size)
                if tmp_y < 0 or tmp_y > scl*cell_size-bike_yellow.height or tmp_x < 0 or tmp_x > scl*cell_size-bike_yellow.width:
                    window[(tmp_x, tmp_y)] = 1
                else: 
                    window[(tmp_x, tmp_y)] = 0

        window[(bike_yellow.x, bike_yellow.y)] = 2
        if (bike_white.x, bike_white.y) in window:
                window[(bike_white.x, bike_white.y)] = 3

        for tx, ty in zip(bike_yellow.tail_x, bike_yellow.tail_y):
            if (tx, ty) in window:
                window[(tx, ty)] = 4

        for tx, ty in zip(bike_white.tail_x, bike_white.tail_y):
            if (tx, ty) in window:
                window[(tx, ty)] = 5
        
        inputs = list(window.values())

        output = model.activate(inputs)

        for i, val in enumerate(output):
            move = max((val, i), move)

        if move[1]==0 and bike_yellow.dir != "down":
            bike_yellow.dir = "up"
        elif move[1]==1 and bike_yellow.dir != "up":
            bike_yellow.dir = "down"
        elif move[1]==2 and bike_yellow.dir != "right":
            bike_yellow.dir = "left"
        elif move[1]==3 and bike_yellow.dir != "left":
            bike_yellow.dir = "right"


        bike_white.move()
        bike_yellow.move()

        if run:
            redrawgamewindow(bike_white, bike_yellow)

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