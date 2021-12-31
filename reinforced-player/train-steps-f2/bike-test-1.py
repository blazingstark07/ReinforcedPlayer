import pygame as pg
import random
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
            window = {}
            move = (0, 0)
            for i in range(-5, 6, 1):
                for j in range(-5, 6, 1):
                    tmp_x, tmp_y = (bike.x - i*cell_size, bike.y - j*cell_size)
                    if tmp_y < 0 or tmp_y > scl*cell_size-bike.height or tmp_x < 0 or tmp_x > scl*cell_size-bike.width:
                        window[(tmp_x, tmp_y)] = 1
                    else: 
                        window[(tmp_x, tmp_y)] = 0

            window[(bike.x, bike.y)] = 2
            for tx, ty in zip(bike.tail_x, bike.tail_y):
                if (tx, ty) in window:
                    window[(tx, ty)] = 4

            inputs = list(window.values())
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