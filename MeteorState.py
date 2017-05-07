#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2, collides_with
from random import randint
from math import sin, cos, radians

class MeteorState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.bg = Sprite(load_image('res/space.png'), Vec2(320, 240), (640, 480))
        self.player = Sprite(load_image('res/spaceship2.png'), Vec2(320, 400), (60, 60))
        self.meteorites = []

        self.generate_meteorite_waves(randint(5, 10))
        self.meteor_speed = 5
        self.player_speed = 15
        self.player_rot_speed = 10

    def update(self, game_state):
        if game_state['keyboard']['ctrl-debug']:
            self.meteorites[:] = []

        if game_state['keyboard']['ctrl-up']:
            self.player.pos[0] -= self.player_speed * sin(radians(self.player.angle))
            self.player.pos[1] -= self.player_speed * cos(radians(self.player.angle))

            hw = self.player.size[0] // 2
            hh = self.player.size[1] // 2

            if self.player.pos[0] - hw < 0: self.player.pos[0] = hw
            if self.player.pos[1] - hh < 0: self.player.pos[1] = hh
            if self.player.pos[0] + hw > 640: self.player.pos[0] = 640 - hw
            if self.player.pos[1] + hh > 480: self.player.pos[1] = 480 - hh

        if game_state['keyboard']['ctrl-left']:
            self.player.angle += self.player_rot_speed
        if game_state['keyboard']['ctrl-right']:
            self.player.angle -= self.player_rot_speed

        hitbox_offset = 15
        player_pos = self.player.pos - Vec2(self.player.size[0] // 2, self.player.size[1] // 2) + hitbox_offset
        player_size = (self.player.size[0] - hitbox_offset, self.player.size[1] - hitbox_offset)
        for meteor in reversed(self.meteorites):
            meteor_pos = meteor[0].pos - Vec2(meteor[0].size[0] // 2, meteor[0].size[1] // 2) + hitbox_offset
            meteor_size = (meteor[0].size[0] - hitbox_offset, meteor[0].size[1] - hitbox_offset)
            if collides_with(player_pos, player_size, meteor_pos, meteor_size):
                game_state['went-well'] = False
                return game_state['world-gameover']

            meteor[0].pos[1] += self.meteor_speed
            meteor[0].angle += meteor[1]
            if meteor[0].pos[1] > 500:
                self.meteorites.pop(self.meteorites.index(meteor))
                self.sprites.pop(self.sprites.index(meteor[0]))

        if len(self.meteorites) == 0:
            game_state['went-well'] = True
            return game_state['world-space']

    def reset(self, game_state):
        self.generate_meteorite_waves(randint(5, 10))
        self.player.pos[0] = 320
        self.player.pos[1] = 400
        self.player.angle = 0

        self.sprites[:] = []
        self.sprites.append(self.bg)
        for meteor in self.meteorites:
            self.sprites.append(meteor[0])
        self.sprites.append(self.player)

        game_state['camera'].x = 0
        game_state['camera'].y = 0

    def generate_meteorite_waves(self, amount):
        self.meteorites[:] = []

        for i in range(amount):
            last_x = 0
            y = (-i * 250)
            free_space = self.generate_free_space(y)
            while True:
                meteor = Sprite(load_image('res/asteroid2.png'), Vec2(last_x + 50, y), (50, 50))
                if collides_with(meteor.pos, meteor.size, free_space[0], free_space[1]):
                    meteor.pos[0] += free_space[1][0]
                last_x = meteor.pos[0]
                self.meteorites.append((meteor, randint(1, 5))) # Sprite, rot speed

                if meteor.pos[0] + meteor.size[0] > 640: break

    def generate_free_space(self, y):
        return ((randint(0, 430), y), (100, 100))