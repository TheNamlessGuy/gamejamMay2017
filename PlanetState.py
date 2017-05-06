#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2


class PlanetState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.res = {}
        self.res['planets'] = [load_image("res/onplanet1.png"), \
                               load_image("res/onplanet2.png"), \
                               load_image("res/onplanet3.png"), \
                               load_image("res/onplanet4.png")]


        self.bg = (Sprite(load_image("res/onplanet1.png"), Vec2(320, 240), (640, 480)))
        #self.player = (Sprite(load_image("res/player
        self.enemy = (Sprite(load_image("res/icecreamstick1.png"), Vec2(360, 360), (80, 100)))
        

    def update(self, game_state):
        #Clear sprites
        self.sprites[:] = []
        
        #Draw BG
        self.sprites.append(self.bg)
        
        #self.sprites.append(self.enemy)
        
        #Do input
        if game_state['keyboard']['ctrl-up']:
            pass
        if game_state['keyboard']['ctrl-left']:
            pass
        if game_state['keyboard']['ctrl-right']:
            pass
        if game_state['keyboard']['ctrl-down']:
            pass
        
        
    def reset(self, game_state):
        #reset camera
        game_state['camera'].x = 0
        game_state['camera'].y = 0
    
        planet = game_state['identifier']
        self.bg.image = self.res['planets'][planet-1]
        
        
        
        
    
