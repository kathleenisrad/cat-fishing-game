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
pole_path = 'data/images/fishing_pole/'
instructions_path = 'data/images/instructions/'

boat_tiles = os.listdir(boat_path)    
water_tiles = os.listdir(water_path)
instructions_imgs = os.listdir(instructions_path)

## CLASSES-----------------------------------
class Cat(pygame.sprite.Sprite):
    """
    Represents the cat controlled by the player. 
    Press 1, 2 , or 3 to change the cat color.
    Alternate pressing left and right arrow keys to reel in the line. 
    """
    def __init__(self):
        super(Cat, self).__init__()
        self.color = ['white/', 'siamese/', 'tabby/']
        self.index = 0
        self.images = [load_image(cat_path + self.color[0] + img) for img in os.listdir(cat_path + self.color[0])]
        self.image = self.images[1]
        self.throw = False
        
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
        if self.throw == False:
            self.index += 1
            if self.index != 0:
                if self.index > 14:
                    self.index = 1
                if self.index < 7:
                    self.image = self.images[0]
                else:
                    self.image = self.images[1]
        else:
            self.index += 1
            if self.index != 0:
                if self.index > 20:
                    self.throw = False
                    self.index=1
                if 1 < self.index < 13:
                    self.image = self.images[2]
                else:
                    self.image = self.images[3]

        if pressed_keys[K_1]:
            self.change_color(1)
        if pressed_keys[K_2]:
            self.change_color(0)
        if pressed_keys[K_3]:
            self.change_color(2)

class Pole(pygame.sprite.Sprite):
    """
    Represents the cat controlled by the player. 
    Press 1, 2 , or 3 to change the cat color.
    Alternate pressing left and right arrow keys to reel in the line. 
    """
    def __init__(self):
        super(Pole, self).__init__()
        self.index = 0
        self.type = ['normal/']
        self.images = [load_image(pole_path + self.type[0] + img) for img in os.listdir(pole_path + self.type[0])]
        self.image = self.images[0]
        self.throw = False
        self.rect = pygame.Rect(50,50,50,50)
        
    def update(self, pressed_keys, event):
        '''
        This method iterates through the elements inside self.images and 
        displays the next one each tick. 
        Change the sprite color by pressing 1, 2, or 3.
        '''
        if self.throw == False:
            self.image = self.images[0]
            self.rect.center = (189,84)
            
        else:
            self.index += 1
            if self.index != 0:
                if self.index > 20:
                    self.throw = False
                    self.index=1
                if 1 < self.index < 13:
                    self.image = self.images[1]
                    self.rect.center = (202,86)
                else:
                    self.image = self.images[2]
                    self.rect.center = (156,93)

class Catchable(pygame.sprite.Sprite):
    """ 
    Represents the items that can be fished up
    """
    def __init__(self, type, pull_strength, points):
        super(Catchable, self).__init__()
        self.type = type
        self.pull_strength = pull_strength
        self.points = points
        #self.image = load_image(catch_path)
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

#counters
j = 1 #boat animation
instructions = 1 #instructions animation

#class instances
player = Cat()
bobber = Throwable()
pole = Pole()

#sprite groups
group = pygame.sprite.Group([player, bobber, pole])
fish_group = pygame.sprite.Group()

#power bar
power_level = 5
bar_x = 25
bar_y = 25
bar_height = 10
x_change = 0

#fish variables
ADDFISH = pygame.USEREVENT + 1

fish_dictionary = {
    'salmon': {'pull_strength' : 5, 
               'points' : 10,},
    'trout':  {'pull_strength' : 10, 
               'points' : 20,},
    'tuna':  {'pull_strength' : 10, 
               'points' : 20,}        
}


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

    #power bar ---------------------------------
    power_bar_outline = load_image('data/images/power_bar.png')

    if power_level < 20:
        power_color = (255,0,0) #red
    elif power_level < 50:
        power_color = (255, 165, 0) #orange
    elif power_level < 75:
        power_color = (234, 255, 0) #yellow
    else: 
        power_color = (50,205,50) #green

    #visualize the power bar after instructions disappear
    if instructions == 0:
        pygame.draw.rect(instructions_surf, power_color, (bar_x, bar_y, power_level, bar_height), 0, 3)
        instructions_surf.blit(power_bar_outline,(24,16))
    

    #boat--------------------------------------
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
                player.index = 1
                player.throw = True
                pole.throw = True
                
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
                elif 108 >= power_level  >= 106:
                    bobber.rect.center = (80, 150)

                fish_event = pygame.event.Event(ADDFISH)
                pygame.event.post(fish_event)

        elif event.type == ADDFISH:
            if power_level <= 25:
                fish_weights = [50,25,25]
            elif power_level <= 75:
                fish_weights = [34,33,33]
            elif power_level < 106:
                fish_weights = [25,25,50]
            elif 108 > power_level  >= 106:
                fish_weights = [0,0,100]

            fish_spawned = random.choices(['salmon', 'trout', 'tuna'], fish_weights,k=1)[0]

            new_fish = Catchable(type=fish_spawned, pull_strength = fish_dictionary[fish_spawned]['pull_strength'], points = fish_dictionary[fish_spawned]['points'])

            print(f'You caught a {fish_spawned}! It is worth {new_fish.points} points!')

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
