import io
from PIL import Image
import random
import math
import sys

def kMeans_quantization(image, colors = 8):
    pixels = image.load()
    mean_keys = random_pixels(pixels, image, colors)
    prev_population = [0 for _ in range(colors)]
    gen = 0
    
    while True:
        means = dict()
        groups = dict()
        for key in mean_keys:
            means[key] = set()
            
        for x in range(image.width):
            for y in range(image.height):
                min_group = None
                min_ammount = math.inf
                
                color = pixels[x, y]
                if color in groups:
                    means[groups[color]].add(color)
                else:
                    another_min = min(mean_keys, key= lambda item: squared_error(item, pixels[x, y]))
                    groups[pixels[x, y]] = another_min
                    means[another_min].add(pixels[x, y])
    
        population = [len(means[given_mean]) for given_mean in mean_keys]
        difference = [a[0]-a[1] for a in zip(population, prev_population)]
        print("Generation", gen, "-->", difference)
        prev_population = population
        
        #4
        new_means = []
        for mean in means:
            red = 0
            green = 0
            blue = 0
            
            for another_pixel in means[mean]:
                red += another_pixel[0]
                green += another_pixel[1]
                blue += another_pixel[2]
            
            new_means.append((int(red/len(means[mean])), int(green/len(means[mean])), int(blue/len(means[mean]))))
            
        if all(group == 0 for group in difference):
            break
        mean_keys = new_means
        print(new_means)
        gen += 1
    
    print("Final Means:", new_means)
    print("Saving...")
    for x in range(image.width):
        for y in range(image.height):
            min_group = None
            min_ammount = math.inf
            
            for key in new_means:
                value = squared_error(key, pixels[x, y])
                if value <= min_ammount:
                    min_ammount = value
                    min_group = key
            
            pixels[x, y] = min_group
            
    return new_means

def random_pixels(pixels, image, count):
    output = []
    while len(output) != count:
        yes = pixels[random.randrange(0, image.width), random.randrange(0, image.height)]
        if yes not in output:
            output.append(yes)
    return output
    
def squared_error(pixel1, pixel2):
    return sum((p[0]-p[1]) ** 2 for p in zip(pixel1, pixel2))
