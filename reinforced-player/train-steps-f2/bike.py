from constants import *
from func import *
import pygame as pg
import random
import math

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
            self.max_loop = 500 
            self.max_till_now = 0
            self.prev_cords = []

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

            if (self.x, self.y) in self.prev_cords:
                self.max_till_now += 1
            else: self.max_till_now = 0

            self.prev_cords.append((self.x, self.y))
            if len(self.prev_cords) > self.max_loop:
                self.prev_cords.pop(0)

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
               return True, -200

            for i in range(self.tail_size):
                if distance(self.x, self.y, self.tail_x[i], self.tail_y[i]) < cell_size and self.dir!="stop":
                    return True, -350

            if self.max_till_now > self.max_loop:
                return True, -500

            return False, 0