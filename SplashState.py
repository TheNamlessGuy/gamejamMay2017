#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class SplashState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.gamejam = Sprite(load_image('res/gamejam.png'), Vec2(320, 200), (300, 300))
        self.load_bar = Sprite(load_image('res/load_bar.png'), Vec2(100, 400), [5, 30])

    def update(self, game_state):
        if len(self.sprites) == 0: self.reset(game_state)

        self.load_bar.pos[0] += 13
        self.load_bar.size[0] += 26
        if self.load_bar.size[0] >= 440:
            return game_state['world-space']

    def reset(self, game_state):
        self.sprites.append(self.gamejam)
        self.sprites.append(self.load_bar)
        self.load_bar.pos.x = 100
        self.load_bar.size[0] = 5