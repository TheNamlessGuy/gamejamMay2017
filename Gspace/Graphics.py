#encoding: utf-8

import pygame

from WorldInterface import *

def draw_world( world, game_state ):
    
    screen = game_state["screen"]
    screen.fill( (0,0,0) )
    
    for sprite in world.sprites:
        screen.blit( sprite.image, sprite.pos )
