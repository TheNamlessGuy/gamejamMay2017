#encoding: utf-8

from Gspace import *
from SpaceState import *
from PlanetState import *
from MeteorState import *
from GameOverState import *
from TransitionCutsceneState import *
from SpoonCutsceneState import *

if __name__ == '__main__':
    game_state = {}
    game_state['world-space'] = SpaceState()
    game_state['world-planet'] = PlanetState()
    game_state['world-meteor'] = MeteorState()
    game_state['world-gameover'] = GameOverState()
    game_state['world-cutscene'] = {'falling': TransitionCutsceneState("down"), 'rising': TransitionCutsceneState("up"), 'spoon-expansion': SpoonCutsceneState()}
    game_state['camera'] = Vec2( 0.0, 0.0 )
    game_state['spoon-pwr'] = 0
    run_game( game_state['world-space'], game_state, 24 )
