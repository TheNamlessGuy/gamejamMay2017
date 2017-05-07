#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class SplashState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.gamejam = Sprite(load_image('res/gamejam.png'), Vec2(320, 200), (300, 300))
        #self.load_bar = Sprite(load_image('res/load_bar.png'), Vec2())

    def update(self, game_state):
        if len(self.sprites) == 0: self.sprites.append(self.gamejam)

        if game_state['keyboard']['ctrl-action']:
            return game_state['world-space']

    def reset(self, game_state):
        self.sprites.append(self.gamejam)