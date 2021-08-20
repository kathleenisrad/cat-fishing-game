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
    """Represents the cat controlled by the player. Press and hold spacebar to increase throwing distance. Alternate pressing A and L keys to reel in the line. """
    NET_PULL = 0

    def __init__(self):
        super(Cat, self).__init__()
        self.color = ['white/', 'black/', 'tabby/']
        self.index = 0
        self.images = [load_image(cat_path + self.color[0] + img) for img in os.listdir(cat_path + self.color[0])]
        self.image = self.images[1]
        
        self.rect = pygame.Rect(24,26,24,26)
        self.rect.center = (160, 80)
        
    def change_color(self, num):
        self.images = [load_image(cat_path + self.color[num] + img) for img in os.listdir(cat_path + self.color[num])]
        self.image = self.images[0]

    def update(self, pressed_keys, event):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        if self.index != 0:
            if self.index > 14:
                self.index = 1
            if self.index < 7:
                self.image = self.images[0]
            else:
                self.image = self.images[1]

        if pressed_keys[K_RIGHT]:
            if pressed_keys[K_LEFT]:
                NET_PULL += 1*REEL_PULL

        if pressed_keys[K_1]:
            self.change_color(1)

        if pressed_keys[K_2]:
            self.change_color(0)
        
        if pressed_keys[K_3]:
            self.change_color(2)

## GAME LOOP --------------------------------
running = True
i = 1
j = 1
instructions = 1
player = Cat()
group = pygame.sprite.Group(player)

decrease_speed = -1
power_level = 0
bar_x = 25
bar_y = 25
bar_height = 10
x_change = 0

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
    #boat------------------------------------
    if j != 0:
        if j < 15:
            boat_tile = load_image(boat_path + boat_tiles[0])
        elif j < 30:
            boat_tile = load_image(boat_path + boat_tiles[1])
        elif j < 45:
            boat_tile = load_image(boat_path + boat_tiles[2])
        elif j < 60:
            boat_tile = load_image(boat_path + boat_tiles[3])
        else:
            boat_tile = load_image(boat_path + boat_tiles[4])

    if j > 75:
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
  
        if pressed_keys[pygame.K_SPACE]:         
            x_change = 5
            power_level += x_change

        if event.type == KEYUP:
            if event.key == K_SPACE:
                distance = power_level
                power_level = 0

        if power_level > 100:
            power_level = 0

    pygame.draw.rect(instructions_surf, (255,0,0), (bar_x, bar_y, power_level, bar_height))

    group.update(pressed_keys, event)
    group.draw(background_surf)
    
    screen.blit(pygame.transform.scale(background_surf, screen.get_size()), (0,0))
    screen.blit(pygame.transform.scale(instructions_surf, screen.get_size()), (0,0))

 
    pygame.display.flip()
    # keeps the game at 30 frames per second
    clock.tick(30)
