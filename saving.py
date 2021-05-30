import pygame as pg
import json

class Saver:
    def __init__(self, number, screen, planets):
        self.number = number
        self.screen = screen
        self.planets = planets
    
    def save_data(self):
        pg.image.save(self.screen, "./training_data/" + str(self.number) + ".png")
        
        modified_planets = dict()
        for num, item in enumerate(self.planets):
            modified_planets[num] = (item.velocity[0], item.velocity[1], item.x, item.y, item.radius, (item.color[0], item.color[1], item.color[2]))
        
        with open("./training_data/" + str(self.number) + ".json", 'w') as out:  
            json.dump(modified_planets, out)