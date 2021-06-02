#TODO: make sun-sun interaction only -- class based system or no?

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
    #Planet Class basis provided by https://github.com/000Nobody/Orbit-Simulator 
    def __init__(self, vel_x, vel_y, x, y, radius, id, color = (255, 0, 0), disp_size = None, type = "planet"):
        self.x = x
        self.y = y
        self.radius = radius
        self.volume = self.radius ** 3
        self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO
        self.id = id
        self.velocity = [vel_x, vel_y]
        self.color = color
        self.planet_list = planet_list
        self.screen = screen
        self.crashes = 0
        self.type = type
        if disp_size is None:
            self.disp_size = radius
        else:
            self.disp_size = disp_size
        
    def update(self):
        if self.type == "planet":
            self.getVelocity()
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        
    def getVelocity(self):
        for planet in self.planet_list:
            if self.id != planet.id:
                dx = planet.x - self.x
                dy = planet.y - self.y
                angle = math.atan2(dy, dx)  # Calculate angle between planets
                d = math.sqrt((dx ** 2) + (dy ** 2))  # Calculate distance
                if d < (planet.disp_size + self.disp_size):
                    vel_x = ((self.mass * self.velocity[0]) + (planet.mass * planet.velocity[0]))/((self.mass + planet.mass)/1.3)
                    vel_y = ((self.mass * self.velocity[1]) + (planet.mass * planet.velocity[1]))/((self.mass + planet.mass)/1.3)

                    # vel_x = (planet.velocity[0] + self.velocity[0])/5
                    # vel_y = (planet.velocity[1] + self.velocity[1])/5

                    if (planet.disp_size <= self.disp_size):
                        planet_list.remove(planet)
                        self.crashes += 1
                        self.velocity[0] = vel_x
                        self.velocity[1] = vel_y
                    else:
                        planet_list.remove(self)
                        planet.crashes += 1
                        planet.velocity[0] = vel_x
                        planet.velocity[1] = vel_y
                else:
                    f = G * self.mass * planet.mass / (d ** 2) # Calculate gravitational force
                    self.velocity[0] += (math.cos(angle) * f) / self.mass
                    self.velocity[1] += (math.sin(angle) * f) / self.mass
                
                if planet.crashes > 10:
                    planet_list.remove(planet)

    def draw(self):
        pg.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), int(self.disp_size))
        
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
    max_planets = 100
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
    # with open('./training_data/laser.json', 'r') as data: 
    #     init_conds = json.load(data)

    # for num, planet in enumerate(init_conds.values()):
    #     planet_list.append(Planet(vel_x = planet[0], vel_y = planet[1], x = planet[2], y = planet[3], radius = planet[4], id = num, color = planet[5]))

    # # RANDOM GENERATION
    for num, item in enumerate(colors):
        planet_list.append(Planet(random.random()-0.5, random.random()-0.5, random.random() * WINDOW_SIZE[0], random.random() * WINDOW_SIZE[1], random.random() * 10, num, color=item, disp_size = 3))

    # # SOLAR SYSTEM 3 BODY - NO INTERACTION
    # planet_list.append(Planet(0, 0, 750, 400, 55, 1, (255, 255, 0), type="star")) #sun
    # planet_list.append(Planet(0, 2, 950, 400, 4, 2, (0, 255, 0), disp_size=10)) #green
    # planet_list.append(Planet(0, -2, 420, 400, 3, 3, (0, 0, 255), disp_size=5)) #blue
    # planet_list.append(Planet(0, -2, 1030, 400, 1, 4, disp_size=4)) #red
    
    
    # # SOLAR SYSTEM 3 BODY - INTERACTION UNSTABLE
    # planet_list.append(Planet(0, 0, 750, 400, 50, 1, (255, 255, 0), type="star")) #sun
    # planet_list.append(Planet(1.5, 0.1, 750, 50, 15, 2, (0, 255, 0))) #green
    # planet_list.append(Planet(0.2, 2, 550, 400, 20, 3, (0, 0, 255), disp_size=10)) #blue
    # planet_list.append(Planet(0.1, -1, 270, 600, 4, 4)) #red

    # # SOLAR SYSTEM 3 BODY - INTERACTION STABLE
    # planet_list.append(Planet(0, 0, 750, 400, 50, 1, (255, 255, 0), type="star")) #sun
    # planet_list.append(Planet(1.7, 0, 750, 100, 10, 2, (0, 255, 0))) #green
    # planet_list.append(Planet(-2.5, 0, 750, 600, 15, 3, (0, 0, 255), disp_size=10)) #blue
    # planet_list.append(Planet(0.8, -2, 575, 400, 5, 4)) #red

    # # BINARY STAR SYSTEM
    # planet_list.append(Planet(0.2, -0.8, 900, 400, 20, 1, (255, 255, 255), disp_size = 30)) #sun - yellow
    # planet_list.append(Planet(-0.2, 0.8, 740, 400, 20, 2, (255, 255, 0), disp_size = 30)) #sun - yellow
    # planet_list.append(Planet(0.4, -0.3, 1240, 730, 2, 3, disp_size = 10)) #planet - red
    # planet_list.append(Planet(0.4, -0.5, 240, 230, 1, 3, disp_size = 8)) #planet - red 
    
    planet_info = [(item.velocity[0], item.velocity[1], item.x, item.y, item.radius, (item.color[0], item.color[1], item.color[2])) for item in planet_list] #pg.Surface pickle problem avoided
    saver = Saver(number, screen, planet_info)

    running = True
    while running:
        # screen.fill(BG_COLOR) #NOTE: comment out to add orbits
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        for planet in planet_list:
            if planet.x > WINDOW_SIZE[0] + WINDOW_TOLERANCE or planet.x < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                # print(number, len(planet_list))
            elif planet.y > WINDOW_SIZE[1] + WINDOW_TOLERANCE or planet.y < -WINDOW_TOLERANCE:
                planet_list.remove(planet)
                # print(number, len(planet_list))
            elif planet.velocity[0] > 50 or planet.velocity[0] < -50:
                planet_list.remove(planet)
                # print(number, len(planet_list))
            elif planet.velocity[1] > 50 or planet.velocity[1] < -50:
                planet_list.remove(planet)
                # print(number, len(planet_list))
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