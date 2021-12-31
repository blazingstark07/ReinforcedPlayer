import pygame as pg
import random
import math
import neat
import pickle
from constants import *
from func import *
from bike import Bike
pg.init()

run = True

def redrawgamewindow(bikes):
    win.fill((0, 0, 0))
    for i, bike in enumerate(bikes):
        if i < 5:
            bike.draw()

    pg.display.update()

def start_test(config_path):        
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    p = neat.Population(config)


    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    winner = p.run(game_loop, 100)

    print('\nBest genome:\n{!s}'.format(winner))
    with open('step1.pkl', 'wb') as output:
        pickle.dump(winner, output)

    pg.quit()
    quit()

def game_loop(genomes, config):
    global run
    bikes = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        bikes.append(Bike(cell_size * 30, cell_size * 20, cell_size, cell_size, (255, 255, 255), white_bike))
        g.fitness = 0
        ge.append(g)


    while run and len(bikes) > 0:
        clock.tick(clock_speed)

    # To check the events done in the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        for ind, bike in enumerate(bikes):
            move = (0, 0)
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            inputs = []
            tl_crds = []
            # print(i)
            for dr in dirs:
                dst = -1
                x, y = bike.x, bike.y
                for tx, ty in zip(bike.tail_x, bike.tail_y):
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

            output = nets[ind].activate(inputs)

            for i, val in enumerate(output):
                move = max((val, i), move)

            if move[1]==0 and bike.dir != "down":
                bike.dir = "up"
            elif move[1]==1 and bike.dir != "up":
                bike.dir = "down"
            elif move[1]==2 and bike.dir != "right":
                bike.dir = "left"
            elif move[1]==3 and bike.dir != "left":
                bike.dir = "right"

        for bike in bikes:
            bike.move()

        if run:
            redrawgamewindow(bikes)
        
        for i, bike in enumerate(bikes):
            is_die, pen = bike.die()
            if is_die and run:
                ge[i].fitness += pen
                bikes.pop(i)
                nets.pop(i)
                ge.pop(i)

        for i, bike in enumerate(bikes):
            ge[i].fitness += 1




if __name__ == "__main__":      
    config_path = 'config-feedforward.txt'
    start_test(config_path)