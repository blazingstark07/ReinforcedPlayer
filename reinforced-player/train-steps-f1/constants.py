import pygame as pg

cell_size = 16
scl = 40
win_size = (scl*cell_size, scl*cell_size)
config_path = 'config-feedforward.txt'
clock_speed = 800

win = pg.display.set_mode(win_size)
pg.display.set_caption("SNAKE GAME")
clock = pg.time.Clock()
white_bike = pg.image.load('white_bike.png')
yellow_bike = pg.image.load('yellow_bike.png')