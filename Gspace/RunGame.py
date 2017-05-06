#encoding: utf-8

import pygame
from WorldInterface import *
from Graphics import *
from Keyboard import *

def run_game( world, game_state = {}, fps = 24 ):

    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    back_colour = ( 255, 0, 0 )
    background = pygame.Surface( screen.get_size() )
    background.fill( back_colour )
    background = background.convert()
    owl = (0,0)
    screen.blit( background, owl )

    timer = pygame.time.Clock()
    #world.reset()

    game_state["screen"] = screen
    game_state["clock"] = timer
    game_state["running"] = True
    game_state["keyboard"] = Keyboard(pygame)
    
    while game_state["running"]:
        game_state["running"] = game_state["keyboard"].update(pygame)
        ret = world.update(game_state)
        if isinstance( ret, WorldInterface ):
            world = ret
            ret = None
            world.reset( game_state )
            continue

        # draw to buffer
        draw_world( world, game_state )
        # show buffer
        pygame.display.flip()
        # sync
        timer.tick( fps )


