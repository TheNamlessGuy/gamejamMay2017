#encoding: utf-8

from Gspace import *
from SpaceState import SpaceState
#from PlanetState import PlanetState
#from MeteorState import MeteorState

if __name__ == '__main__':
    game_state = {}
    game_state['world-space'] = SpaceState()
    #game_state['world-planet'] = PlanetState()
    #game_state['world-meteor'] = MeteorState()
    world = game_state['world-space']
    run_game( world, game_state, 24 )

"""
# gammal kod! använd denna event-loop vid override av WorldInterface i update-metoden!!!
# TODO: ta bort kommentaren efter att ni har implementerat detta
while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    
    pygame.display.flip()
"""
