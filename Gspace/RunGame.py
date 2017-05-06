#encoding: utf-8

import pygame
import WorldInterface

#import graphics

#dummy until graphics is implemented

def draw_world( world ):
    print "no draw implementation yet"

def run_game( world, game_state = {}, fps = 24 ):
    
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    back_colour = ( 255, 0, 0 )
    background = pygame.Surface( screen.get_size() ).fill( back_colour ).convert()
    owl = (0,0)
    screen.blit( background, owl )
    
    timer = pygame.time.Clock()
    world.reset()
    
    game_state["screen"] = screen
    game_state["clock"] = timer
    game_state["running"] = True
    
    while game_state["running"]:
        ret = WorldInterface.update( world, game_state )
        if isinstance( ret, WorldInterface ):
            world = ret
            ret = None
            world.reset( game_state )
            continue
        
        # draw to buffer
        draw_world( world )
        # show buffer
        pygame.display.flip()
        # sync
        timer.tick( fps )


