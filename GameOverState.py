#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class GameOverState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.bg = Sprite(load_image('res/gameover.png'), Vec2(320, 240), (640, 480))

    def update(self, game_state):
        if game_state['keyboard']['ctrl-action']:
            game_state['spoon-pwr'] = 0
            game_state['hard-reset'] = True
            return game_state['world-splash']

    def reset(self, game_state):
        self.sprites.append(self.bg)
