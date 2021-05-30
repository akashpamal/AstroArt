import pygame as pg
import sys
import random
import math
import copy
import numpy as np
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from PIL import Image
import json
import multiprocessing

from kmeansIdentifier import kMeans_quantization
from saving import Saver

FPS = 120
WINDOW_TOLERANCE = 25
WINDOW_SIZE = (1440, 800)

G = 6.67408 * (10 ** -11)  # Gravitational Constant
MASS_AREA_RATIO = 2 * (10 ** 9)  # mass in kilograms to area in pixels
NUM_PLANETS = 60


class Planet:
    def __init__(self, vel_x, vel_y, x, y, radius, id, color=[255, 0, 0]):
        self.x = x
        self.y = y
        self.radius = radius
        self.volume = self.radius ** 3
        self.rect = pg.Rect(
            self.x - self.radius / 1.5,
            self.y - self.radius / 1.5,
            self.radius * 1.5,
            self.radius * 1.5,
        )
        self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO
        self.id = id
        self.velocity = [vel_x, vel_y]
        self.color = color
        
    def update(self):
        self.getVelocity()
        self.collision()
        self.rect = pg.Rect(
            self.x - self.radius / 1.5,
            self.y - self.radius / 1.5,
            self.radius * 1.5,
            self.radius * 1.5,
        )
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
    def getVelocity(self):
        for planet in planet_list:
            if self.id != planet.id:
                dx = planet.x - self.x
                dy = planet.y - self.y
                angle = math.atan2(dy, dx)  # Calculate angle between planets
                d = math.sqrt((dx ** 2) + (dy ** 2))  # Calculate distance
                if d == 0:
                    d = 0.00000000000000000001  # Prevent division by zero error
                f = (
                    G * self.mass * planet.mass / (d ** 2)
                )  # Calculate gravitational force
                
                self.velocity[0] += (math.cos(angle) * f) / self.mass
                self.velocity[1] += (math.sin(angle) * f) / self.mass
                
    def collision(self):
        for planet in planet_list:
            if (
                self.id != planet.id
                and self.rect.colliderect(planet.rect)
                and self.mass > planet.mass
            ):
                planet_list.remove(planet)
                if self.radius <= 200:
                    self.volume += planet.volume
                    self.radius = self.volume ** (1. /3.)

    def draw(self):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))
        

def run_simulation(number):
    pg.init()
    CLOCK = pg.time.Clock()
    pg.display.set_caption("Astro-Art Animator")
    kmeans = False
    image = None
    if kmeans:
        # IMAGE = "./input_images/DABABY CAR LESSS GOOOOOO.jpeg"
        img = Image.open(image)
        colors = kMeans_quantization(img, NUM_PLANETS)
    else:
        colors = [(random.random() * 255, random.random() * 255, random.random() * 255) for i in range(NUM_PLANETS)]

    # with open('./training_data/69696420.json', 'r') as data:
    #     init_conds = json.load(data)

    # for num, planet in enumerate(init_conds.values()):
    #     planet_list.append(Planet(vel_x = planet[0], vel_y = planet[1], x = planet[2], y = planet[3], radius = planet[4], id = num, color = planet[5]))

    global screen, display, num_planets, planet_list
    screen = pg.display.set_mode(WINDOW_SIZE)
    screen_rect = screen.get_rect()
    display = pg.Surface(WINDOW_SIZE)
    display_rect = display.get_rect()

    planet_list = []


    for num, item in enumerate(colors):
        planet_list.append(Planet(random.random()-0.5, random.random()-0.5, random.random() * WINDOW_SIZE[0], random.random() * WINDOW_SIZE[1], random.random() * 5, num, color=item))
        
    saver = Saver(number, screen, copy.deepcopy(planet_list))
        
    running = True
    while running:
        # screen.fill([0, 0, 0])
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    running = False
        
        for planet in planet_list:
            if planet.x > WINDOW_SIZE[0] + WINDOW_TOLERANCE or planet.x < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                print(len(planet_list))
            elif planet.y > WINDOW_SIZE[1] + WINDOW_TOLERANCE or planet.y < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                print(len(planet_list))
            elif planet.velocity[0] > 100 or planet.velocity[0] < -100:
                planet_list.remove(planet)
                print(len(planet_list))
            elif planet.velocity[1] > 100 or planet.velocity[1] < -100:
                planet_list.remove(planet)
                print(len(planet_list))
            # elif (planet.velocity[0] ** 2 + planet.velocity[1] ** 2) ** 0.5 < 0.001:
            #     planet_list.remove(planet)
            #     print(len(planet_list))
                
        if len(planet_list) == 0:
            saver.save_data()
            quit()
            
        for planet in planet_list:
            planet.update()
        for planet in planet_list:
            planet.draw()

        pg.display.flip()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    NUM_PROCESSES = None
    save_file_numbers = [(elem, ) for elem in range(100)]
    if NUM_PROCESSES is None:
        with multiprocessing.Pool() as pool:
            pool.starmap(run_simulation, save_file_numbers)
    else:
        with multiprocessing.Pool(NUM_PROCESSES) as pool:
            pool.starmap(run_simulation, save_file_numbers)
    # run_simulation(1)
    # run_simulation(2)