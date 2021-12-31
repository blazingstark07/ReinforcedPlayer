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

winner = pickle.load(open("step2.pkl", 'rb'))
config_path = 'config-feedforward.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    config_path)
model = neat.nn.FeedForwardNetwork.create(winner, config)

def redrawgamewindow(bikes, bikes_comp):
    win.fill((0, 0, 0))
    for i, bike in enumerate(bikes):
        bike_comp = bikes_comp[i]
        if i < 5:
            bike.draw()
            bike_comp.draw()

    pg.display.update()

def start_test(config_path):        
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    winner = p.run(game_loop, 400)

    print('\nBest genome:\n{!s}'.format(winner))
    with open('step3.pkl', 'wb') as output:
        pickle.dump(winner, output)

    pg.quit()
    quit()

def game_loop(genomes, config):
    global run
    bikes = []
    bikes_comp = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        bikes.append(Bike(cell_size * 30, cell_size * 20, cell_size, cell_size, (255, 255, 255), white_bike))
        bikes_comp.append((Bike(cell_size * 20, cell_size * 20, cell_size, cell_size, (255, 255, 0), yellow_bike)))
        g.fitness = 0
        ge.append(g)


    while run and len(bikes) > 0:
        clock.tick(clock_speed)

    # To check the events done in the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        for ind in range(len(bikes)):
            bike, bike_comp = bikes[ind], bikes_comp[ind]
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
            if (bike_comp.x, bike_comp.y) in window:
                window[(bike_comp.x, bike_comp.y)] = 3

            for tx, ty in zip(bike.tail_x, bike.tail_y):
                if (tx, ty) in window:
                    window[(tx, ty)] = 4

            for tx, ty in zip(bike_comp.tail_x, bike_comp.tail_y):
                if (tx, ty) in window:
                    window[(tx, ty)] = 5
            
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

        for ind, bike in enumerate(bikes_comp):
            bike_comp = bikes[ind]
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
            if (bike_comp.x, bike_comp.y) in window:
                window[(bike_comp.x, bike_comp.y)] = 3

            for tx, ty in zip(bike.tail_x, bike.tail_y):
                if (tx, ty) in window:
                    window[(tx, ty)] = 4

            for tx, ty in zip(bike_comp.tail_x, bike_comp.tail_y):
                if (tx, ty) in window:
                    window[(tx, ty)] = 5
            
            inputs = list(window.values())

            output = model.activate(inputs)

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

        for bike in bikes_comp:
            bike.move()

        if run:
            redrawgamewindow(bikes, bikes_comp)
        
        for ind, bike in enumerate(bikes):
            is_die, pen = False, 0
            bike_comp = bikes_comp[ind]
            is_die, pen = bike.die()
            if not is_die: is_die, pen = bike_comp.die(); pen = 0
            if not is_die:
                for i in range(bike_comp.tail_size):
                    if distance(bike.x, bike.y, bike_comp.tail_x[i], bike_comp.tail_y[i]) < cell_size and run:
                        is_die = True
                        pen = -400

                # check if the white bike crushed with yellow bike's tail
                for i in range(bike.tail_size):
                    if distance(bike_comp.x, bike_comp.y, bike.tail_x[i], bike.tail_y[i]) < cell_size and run:
                        is_die = True
                        pen = 400

            if is_die and run:
                ge[ind].fitness += pen
                bikes.pop(ind)
                bikes_comp.pop(ind)
                nets.pop(ind)
                ge.pop(ind)

        for i, bike in enumerate(bikes):
            ge[i].fitness += 1




if __name__ == "__main__":      
    start_test(config_path)