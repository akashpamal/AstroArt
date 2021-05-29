import pygame as pg
import sys
import random
import math
import numpy as np
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from PIL import Image
from kmeansIdentifier import kMeans_quantization


pg.init()
clock = pg.time.Clock()
pg.display.set_caption("Orbital Simulator")

running = True
FPS = 120
WINDOW_SIZE = (1920, 1080)
screen = pg.display.set_mode(WINDOW_SIZE)
screen_rect = screen.get_rect()
display = pg.Surface(WINDOW_SIZE)
display_rect = display.get_rect()

G = 6.67408 * (10 ** -11)  # Gravitational Constant
MASS_AREA_RATIO = 2 * (10 ** 9)  # mass in kilograms to area in pixels

planet_list = []
planet_id = 0 

NUM_PLANETS = 30
IMAGE = "./images/DABABY CAR LESSS GOOOOOO.jpeg"
img = Image.open(IMAGE)
colors = kMeans_quantization(img, NUM_PLANETS)
#colors = ((100, 100, 0), (255, 0, 255), (100, 255, 255), (0, 255, 0))

class Planet:
    def __init__(self, x, y, radius, id, color=[255, 0, 0]):
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
        # self.last_pos = (x, y)
        self.velocity = [0, 0]
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
        

for num, item in enumerate(colors):
    planet_list.append(Planet(random.random() * WINDOW_SIZE[0], random.random() * WINDOW_SIZE[1], random.random() * 10, num, color=item))
    
frame_num = 0
while running:
    # screen.fill([0, 0, 0])q
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
    
    for planet in planet_list:
        if planet.x > 50000 or planet.x < -50000:
            planet_list.remove(planet)
        if planet.y > 50000 or planet.y < -50000:
            planet_list.remove(planet)
        if planet.velocity[0] > 100 or planet.velocity[0] < -100:
            planet_list.remove(planet)
        if planet.velocity[1] > 100 or planet.velocity[1] < -100:
            planet_list.remove(planet)
            
    for planet in planet_list:
        planet.update()
    for planet in planet_list:
        planet.draw()
    
    # if frame_num % 10 > 5:
    #     demo_planet.draw()

    pg.display.flip()
    # print('Flipped screen')
    clock.tick(FPS)
    frame_num += 1