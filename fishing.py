## IMPORT ALL THE THINGS---------------------
import os
import sys
import math
import random
import time

import pygame
from pygame.locals import *

#initialize pygame-------------------------
pygame.init()

## FUNCTIONS---------------------------------
def load_image(path):
    image = pygame.image.load(path).convert()
    image.set_colorkey((0, 0, 0), RLEACCEL)
    return image

## CLOCK-------------------------------------
clock = pygame.time.Clock()

## MAP---------------------------------------
f = open('./data/map.txt')
map_data = [[int(c) for c in row] for row in f.read().split('\n')]
f.close()

## SCREEN STUFF------------------------------
DISPLAY_SIZE = (300, 200)

pygame.display.set_caption('Cat Fishing')

#surfaces
screen = pygame.display.set_mode(size=(DISPLAY_SIZE[0]*3, DISPLAY_SIZE[1]*3))

background_surf = pygame.Surface(DISPLAY_SIZE)
player_surf = background_surf.copy()
instructions_surf = background_surf.copy()

## SOUNDS------------------------------------
#Background music set on repeat
#pygame.mixer.music.load('data/music.wav')
#pygame.mixer.music.play(-1)

#Sound effects
#for sound in os.listdir('data/sfx'):   

# IMAGES-------------------------------------
cat_path = 'data/images/cat/'
boat_path = 'data/images/boat/'
water_path = 'data/images/water_tile/'
instructions_path = 'data/images/instructions/'

boat_tiles = os.listdir(boat_path)    
water_tiles = os.listdir(water_path)
instructions_imgs = os.listdir(instructions_path)

f = open('./data/map.txt')
map_data = [[int(c) for c in row] for row in f.read().split('\n')]
f.close()

## CLASSES-----------------------------------
class Cat(pygame.sprite.Sprite):
    """
    Represents the cat controlled by the player. 
    Press and hold spacebar to increase throwing distance. 
    Alternate pressing left and right arrow keys to reel in the line. 
    """
    def __init__(self):
        super(Cat, self).__init__()
        self.color = ['white/', 'siamese/', 'tabby/']
        self.index = 0
        self.images = [load_image(cat_path + self.color[0] + img) for img in os.listdir(cat_path + self.color[0])]
        self.image = self.images[1]
        
        self.rect = pygame.Rect(24,26,24,26)
        self.rect.center = (180, 80)
        
    def change_color(self, num):
        self.images = [load_image(cat_path + self.color[num] + img) for img in os.listdir(cat_path + self.color[num])]
        self.image = self.images[0]

    def update(self, pressed_keys, event):
        '''
        This method iterates through the elements inside self.images and 
        displays the next one each tick. 
        Change the sprite color by pressing 1, 2, or 3.
        '''
        self.index += 1
        if self.index != 0:
            if self.index > 14:
                self.index = 1
            if self.index < 7:
                self.image = self.images[0]
            else:
                self.image = self.images[1]

        if pressed_keys[K_1]:
            self.change_color(1)

        if pressed_keys[K_2]:
            self.change_color(0)
        
        if pressed_keys[K_3]:
            self.change_color(2)

class Catchable(pygame.sprite.Sprite):
    """ 
    Represents the items that can be fished up
    """
    def __init__(self, type, spawn_rate, pull_strength, points, catch_path):
        super(Catch, self).__init__()
        self.type = type
        self.spawn_rate = spawn_rate
        self.pull_strength = pull_strength
        self.points = points
        self.image = load_image(catch_path)
        self.time = None

    def update(self):
        if self.time is not None:  # If the timer has been started...
            # and 500 ms have elapsed, kill the sprite.
            if pygame.time.get_ticks() - self.time >= 750:
                self.kill()


class Throwable(pygame.sprite.Sprite):
    """
    Represents the bobber
    """
    def __init__(self):
        super(Throwable, self).__init__()
        self.index = 0
        self.images = [load_image('data/images/bobber/' + img) for img in os.listdir('data/images/bobber')]
        self.image = self.images[1]
        self.rect = pygame.Rect(15,15,15,15)
        self.rect.center = (169, 106)

    def update(self, pressed_keys, event):
        '''
        This method iterates through the elements inside self.images and 
        displays the next one each tick. 
        '''
        self.index += 1
        if self.index != 0:
            if self.index > 24:
                self.index = 1
            if self.index < 12:
                self.image = self.images[0]
            else:
                self.image = self.images[1]

## VARIABLES TO BE USED IN GAME LOOP --------------------------------
running = True

j = 1 #counter for the boat animation
instructions = 1 #counter for the instructions animation

player = Cat()
bobber = Throwable()
group = pygame.sprite.Group([player, bobber])

#these variables are for the power bar
power_level = 5
bar_x = 25
bar_y = 25
bar_height = 10
x_change = 0

#fish 
#fish_types = [{type: salmon, }]
## GAME LOOP --------------------------------
while running:
    background_surf.fill((240, 255, 255))
    instructions_surf.fill((0,0,0))
    instructions_surf.set_colorkey((0,0,0))


    #instructions ---------------------------
    instructions_img = load_image('data/images/instructions/instructions_1.png')
    if instructions != 0:
        if instructions < 20:
            instructions_surf.blit(instructions_img,(30,23))
        else:
            instructions_surf.blit(instructions_img,(30,25))
        if instructions > 40:
            instructions = 1
        instructions += 1

    #visualize the power bar after instructions disappear
    if instructions == 0:
        pygame.draw.rect(instructions_surf, power_color, (bar_x, bar_y, power_level, bar_height), 0, 3)
        instructions_surf.blit(power_bar_outline,(24,16))

    #power bar --------------------------------------
    power_bar_outline = load_image('data/images/power_bar.png')
    if power_level < 20:
        power_color = (255,0,0)
    elif power_level < 50:
        power_color = (255, 165, 0)
    elif power_level < 75:
        power_color = (234, 255, 0)
    else: 
        power_color = (50,205,50)
    
    #fishing pole ------------------------------------
    fishing_pole = load_image('data/images/fishing_pole/normal/normal_pole.png')
    instructions_surf.blit(fishing_pole, (164,59))
    
    #boat------------------------------------
    if j != 0:
        if j < 10:
            boat_tile = load_image(boat_path + boat_tiles[0])
        elif j < 20:
            boat_tile = load_image(boat_path + boat_tiles[1])
        elif j < 30:
            boat_tile = load_image(boat_path + boat_tiles[2])
        elif j < 40:
            boat_tile = load_image(boat_path + boat_tiles[3])
        else:
            boat_tile = load_image(boat_path + boat_tiles[4])

    if j > 50:
        j = 1
    j+=1

    #water------------------------------------
    water_tile = load_image(water_path + water_tiles[0])

    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == 1:
                background_surf.blit(water_tile,(140 + x * 10 - y * 10, 35 + x * 5 + y * 5))  
            if tile == 2:
                background_surf.blit(water_tile,(140 + x * 10 - y * 10, 35 + x * 5 + y * 5))  
                background_surf.blit(boat_tile, (140 + x * 10 - y * 10, 35 + x * 5 + y * 5 -44))   
            if tile == 3:
                background_surf.blit(water_tile,(140 + x * 10 - y * 10, 35 + x * 5 + y * 5))   
      
    #key presses--------------------------------
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:
                instructions = 0
                power_level = 7

  
        if pressed_keys[pygame.K_SPACE]:         
            x_change = 3
            power_level += x_change

        if event.type == KEYUP:
            if event.key == K_SPACE:
                #enemy.time = pygame.time.get_ticks()
                if power_level <= 20:
                    bobber.rect.center = (169, 106)
                elif power_level <= 30:
                    bobber.rect.center = (160, 110)
                elif power_level <= 40:
                    bobber.rect.center = (150, 115)
                elif power_level <= 50:
                    bobber.rect.center = (140, 120)
                elif power_level <= 60:
                    bobber.rect.center = (130, 125)
                elif power_level <= 70:
                    bobber.rect.center = (120, 130)
                elif power_level <= 80:
                    bobber.rect.center = (110, 135)
                elif power_level <= 90:
                    bobber.rect.center = (100, 140)
                elif power_level < 106:
                    bobber.rect.center = (90, 145)
                elif 108 > power_level  >= 106:
                    bobber.rect.center = (80, 150)
                
        if power_level >= 108:
            power_level = 5

        




    #display images
    group.update(pressed_keys, event)
    group.draw(background_surf)
    
    screen.blit(pygame.transform.scale(background_surf, screen.get_size()), (0,0))
    screen.blit(pygame.transform.scale(instructions_surf, screen.get_size()), (0,0))

    pygame.display.flip()

    # keeps the game at 30 frames per second
    clock.tick(30)
