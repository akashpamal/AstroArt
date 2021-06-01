#TODO: make sun-sun interaction only
#TODO: make mass and size not interdependent

import pygame as pg
import sys
import random
import math
import copy
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from PIL import Image
import json
import multiprocessing

from kmeansIdentifier import kMeans_quantization
from saving import Saver

FPS = 240
WINDOW_TOLERANCE = 25
G = 6.67408 * (10 ** -11)  # Gravitational Constant
MASS_AREA_RATIO = 2 * (10 ** 9)  # mass in kilograms to area in pixels


class Planet:
    #Planet Class provided by https://github.com/000Nobody/Orbit-Simulator 
    def __init__(self, vel_x, vel_y, x, y, radius, id, color = (255, 0, 0)):
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
        self.planet_list = planet_list
        self.screen = screen
        
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
        for planet in self.planet_list:
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
        for planet in self.planet_list:
            if (
                self.id != planet.id
                and self.rect.colliderect(planet.rect)
                and self.mass > planet.mass
            ):
                self.planet_list.remove(planet)
                if self.radius <= 200:
                    self.volume += planet.volume
                    self.radius = self.volume ** (1. /3.)

    def draw(self):
        pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.radius))
        
def run_simulation(number):
    pg.init()
    CLOCK = pg.time.Clock()
    pg.display.set_caption("Astro-Art Animator")

    global screen, display, max_planets, planet_list
    WINDOW_SIZE = (1440, 800)
    BG_COLOR = [0, 0, 0]
    screen = pg.display.set_mode(WINDOW_SIZE)
    # screen_rect = screen.get_rect()
    # display = pg.Surface(WINDOW_SIZE)
    # display_rect = display.get_rect()
    planet_list = []
    max_planets = 64
    screen.fill(BG_COLOR)

    kmeans = False
    image = None
    if kmeans:
        # IMAGE = "./input_images/DABABY CAR LESSS GOOOOOO.jpeg"
        img = Image.open(image)
        colors = kMeans_quantization(img, max_planets)
    else:
        colors = [(random.random() * 255, random.random() * 255, random.random() * 255) for i in range(max_planets)]

    # # LOADING A JSON FILE
    # with open('./training_data/69696420.json', 'r') as data: 
    #     init_conds = json.load(data)

    # for num, planet in enumerate(init_conds.values()):
    #     planet_list.append(Planet(vel_x = planet[0], vel_y = planet[1], x = planet[2], y = planet[3], radius = planet[4], id = num, color = planet[5]))

    # RANDOM GENERATION
    # for num, item in enumerate(colors):
    #     planet_list.append(Planet(random.random()-0.5, random.random()-0.5, random.random() * WINDOW_SIZE[0], random.random() * WINDOW_SIZE[1], random.random() * 5, num, color=item))
    
    # # SOLAR SYSTEM 3 BODY - NO INTERACTION
    # planet_list.append(Planet(0, 0, 750, 400, 55, 1, (255, 255, 0))) #sun
    # planet_list.append(Planet(0, 2, 950, 400, 4, 2, (0, 255, 0))) #green
    # planet_list.append(Planet(0, -2, 420, 400, 3, 3, (0, 0, 255))) #blue
    # planet_list.append(Planet(0, -2, 1030, 400, 1, 4)) #red

    # # BINARY STAR SYSTEM
    planet_list.append(Planet(0.2, -0.8, 900, 400, 20, 1, (255, 255, 255))) #sun - yellow
    planet_list.append(Planet(-0.2, 0.8, 740, 400, 20, 2, (255, 255, 0))) #sun - yellow
    planet_list.append(Planet(0.4, -0.3, 1240, 730, 2, 3)) #planet - red
    planet_list.append(Planet(0.4, -0.5, 240, 230, 1, 4)) #planet - red 
    
    planet_info = [(item.velocity[0], item.velocity[1], item.x, item.y, item.radius, (item.color[0], item.color[1], item.color[2])) for item in planet_list] #pg.Surface pickle problem avoided
    saver = Saver(number, screen, planet_info)

    running = True
    while running:
        screen.fill(BG_COLOR) #NOTE: comment out to add orbits
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        for planet in planet_list:
            if planet.x > WINDOW_SIZE[0] + WINDOW_TOLERANCE or planet.x < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                print(number, len(planet_list))
            elif planet.y > WINDOW_SIZE[1] + WINDOW_TOLERANCE or planet.y < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                print(number, len(planet_list))
            elif planet.velocity[0] > 100 or planet.velocity[0] < -100:
                planet_list.remove(planet)
                print(number, len(planet_list))
            elif planet.velocity[1] > 100 or planet.velocity[1] < -100:
                planet_list.remove(planet)
                print(number, len(planet_list))
            # elif (planet.velocity[0] ** 2 + planet.velocity[1] ** 2) ** 0.5 < 0.001:
            #     planet_list.remove(planet)
            #     print(number, len(planet_list))
                
        if len(planet_list) == 0:
            saver.save_data()
            screen.fill(BG_COLOR)
            return
            
        for planet in planet_list:
            planet.update()
        for planet in planet_list:
            planet.draw()

        pg.display.flip()
        CLOCK.tick(FPS)

if __name__ == '__main__':
    # NUM_PROCESSES = 6
    # save_file_numbers = [(elem, ) for elem in range(100)]
    # if NUM_PROCESSES is None:
    #     with multiprocessing.Pool() as pool:
    #         pool.starmap(run_simulation, save_file_numbers)
    # else:
    #     with multiprocessing.Pool(NUM_PROCESSES) as pool:
    #         pool.starmap(run_simulation, save_file_numbers)
    run_simulation("test_file")
    # run_simulation(2)