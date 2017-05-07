#encoding: utf-8

import pygame

from WorldInterface import *
from Vec2 import *

def draw_world( world, game_state ):
    
    screen = game_state["screen"]
    screen.fill( (0,0,0) )
    
    for sprite in world.sprites:
        if sprite.image == None: continue

        image = sprite.image
        if sprite.flip:
            image = pygame.transform.flip(image, True, False)

        transformed = pygame.transform.rotate( pygame.transform.scale( image, sprite.size ), sprite.angle )
        rect        = transformed.get_rect()
        pos         = sprite.pos - Vec2( rect.width, rect.height ) * 0.5 - game_state['camera']
        # TODO: particles...
        screen.blit( transformed, pos.to_tuple() )
        
    # TODO: post process
    if game_state["blur"]:
        screen_rect = screen.get_rect()
        blur_rect   = ( screen_rect.w // 2, screen_rect.h // 2 )
        small = pygame.transform.smoothscale( screen, blur_rect )
        pygame.transform.smoothscale( small, ( screen_rect.w, screen_rect.h ), screen )
        
