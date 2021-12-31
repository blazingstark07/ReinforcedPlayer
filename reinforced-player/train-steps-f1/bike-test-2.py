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

winner = pickle.load(open("step1.pkl", 'rb'))
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


    winner = p.run(game_loop, 200)

    print('\nBest genome:\n{!s}'.format(winner))
    with open('step2.pkl', 'wb') as output:
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
            move = (0, 0)
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            inputs = []
            tl_crds = []
            # print(i)
            for dr in dirs:
                dst = -1
                x, y = bike.x, bike.y
                for tx, ty in zip(bike.tail_x+bike_comp.tail_x, bike.tail_y + bike_comp.tail_y):
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

        for ind, bike in enumerate(bikes_comp):
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
            bike_comp = bikes_comp[ind]
            is_die, pen = False, 0
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