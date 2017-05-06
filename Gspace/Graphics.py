#encoding: utf-8

import pygame

from WorldInterface import *
from Vec2 import *

def draw_world( world, game_state ):
    
    screen = game_state["screen"]
    screen.fill( (0,0,0) )
    
    for sprite in world.sprites:
        rotated = pygame.transform.rotate( sprite.image, sprite.angle )
        half = rotated.get_rect()
        pos = sprite.pos - Vec2( half.width, half.height ) * 0.5
        screen.blit( rotated, pos.to_tuple() )
