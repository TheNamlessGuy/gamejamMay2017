#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, collides_with, Vec2
from random import randint
from math import sin, cos, radians

class SpaceState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        self.world_size = (1920, 1080)

        self.bg = Sprite(load_image('res/space.png'), Vec2(self.world_size[0] // 2, self.world_size[1] // 2), (self.world_size[0], self.world_size[1]))
        self.enter_planet = Sprite(load_image("res/press_space_to_continue1.png"), Vec2(0, 0), (250, 50))
        self.player = [Sprite(load_image("res/spaceship2.png"), Vec2(self.world_size[0] // 2, self.world_size[1] // 2), (80, 80)), 48] # Sprite, invincibility timer

        self.planets = []
        self.meteors = []
        self.spawn_planets(5)
        self.spawn_meteors(8)

        self.player_speed = 10
        self.player_rot_speed = 5

        self.meteor_speed = self.player_speed + 0.5
        self.planet_rot_speed = 0.3

        self.current_planet = None
        self.collided_meteor = False

    def update(self, game_state):
        if len(self.sprites) == 0:
            self.set_sprites()
            self.set_camera(game_state)

        # Update player
        if game_state['keyboard']['ctrl-up']:
            self.player[0].pos[0] -= self.player_speed * sin(radians(self.player[0].angle))
            self.player[0].pos[1] -= self.player_speed * cos(radians(self.player[0].angle))

            hw = self.player[0].size[0] // 2
            hh = self.player[0].size[1] // 2

            if self.player[0].pos[0] - hw < 0: self.player[0].pos[0] = hw
            if self.player[0].pos[1] - hh < 0: self.player[0].pos[1] = hh
            if self.player[0].pos[0] + hw > self.world_size[0]: self.player[0].pos[0] = self.world_size[0] - hw
            if self.player[0].pos[1] + hh > self.world_size[1]: self.player[0].pos[1] = self.world_size[1] - hh

            self.set_camera(game_state)

        self.player[1] -= 1 if self.player[1] != 0 else 0 # invincibility timer
        if self.player[1] != 0 and self.player[1] % 3 == 0:
            self.player[0].image = None
        elif self.player[0].image == None:
            self.player[0].image = load_image('res/spaceship2.png')

        if game_state['keyboard']['ctrl-left']:
            self.player[0].angle += self.player_rot_speed
        if game_state['keyboard']['ctrl-right']:
            self.player[0].angle -= self.player_rot_speed

        # Update meteors + collision
        for meteor in self.meteors:
            if collides_with(self.player[0].pos, self.player[0].size, meteor[0].pos, meteor[0].size) and self.player[1] == 0:
                self.collided_meteor = True
            meteor[0].pos = meteor[0].pos - (meteor[1] * self.meteor_speed)
            meteor[2] -= 1
            if meteor[2] == 0:
                meteor[1].x = randint(-1, 1)
                meteor[1].y = randint(-1, 1)
                meteor[2] = randint(5, 10)

        if self.collided_meteor: return game_state['world-meteor']

        # Update planets, detect if close to landable planet
        can_land_on = None
        for index, planet in enumerate(self.planets):
            planet[0].angle += self.planet_rot_speed
            if collides_with(self.player[0].pos, self.player[0].size, planet[0].pos, planet[0].size) and planet[1]:
                can_land_on = index

        # Detect if landing on planet
        if can_land_on is not None and game_state['keyboard']['ctrl-action']:
            self.current_planet = can_land_on
            game_state['identifier'] = self.planets[can_land_on][2]
            return game_state['world-cutscene']['falling']
        
        # Set "Enter planet" prompt to render
        if can_land_on is not None:
            if self.enter_planet.image is None: self.enter_planet.image = load_image('res/press_space_to_continue1.png')
            self.enter_planet.pos[0] = self.player[0].pos[0]
            self.enter_planet.pos[1] = self.player[0].pos[1] - self.player[0].size[1]
        else:
            self.enter_planet.image = None

    def reset(self, game_state):
        if 'hard-reset' in game_state and game_state['hard-reset']:
            self.__init__()
            game_state['hard-reset'] = False
            return

        if self.current_planet is not None:
            if 'went-well' in game_state and game_state['went-well']:
                self.planets[self.current_planet][1] = False
            else:
                self.player[1] = 48
            self.current_planet = None

        if self.collided_meteor:
            self.player[1] = 48
            self.collided_meteor = False

        self.set_sprites()
        self.set_camera(game_state)

    def set_camera(self, game_state):
        game_state['camera'].x = self.player[0].pos[0] - 320
        game_state['camera'].y = self.player[0].pos[1] - 240

        if game_state['camera'].x < 0: game_state['camera'].x = 0
        if game_state['camera'].y < 0: game_state['camera'].y = 0
        if game_state['camera'].x + 640 > self.world_size[0]: game_state['camera'].x = self.world_size[0] - 640
        if game_state['camera'].y + 480 > self.world_size[1]: game_state['camera'].y = self.world_size[1] - 480

    def set_sprites(self):
        self.sprites[:] = []
        self.sprites.append(self.bg)
        for planet in self.planets:
            self.sprites.append(planet[0])
        for meteor in self.meteors:
            self.sprites.append(meteor[0])
        self.sprites.append(self.player[0])
        self.sprites.append(self.enter_planet)

    def spawn_planets(self, amount):
        self.planets[:] = [] # Clear planets (just in case)
        size = (50, 50)
        for i in range(amount):
            rand = randint(1, 5)
            sprite = Sprite(load_image("res/planet" + str(rand) + ".png"), self.random_pos(size), size)
            self.planets.append([sprite, True, rand]) # Sprite, isEnterable, type

    def spawn_meteors(self, amount):
        self.meteors[:] = [] # Clear meteors (just in case)
        size = (25, 25)
        for i in range(amount):
            sprite = Sprite(load_image('res/asteroid' + str(randint(1, 4)) +'.png'), self.random_pos(size), size)
            self.meteors.append([sprite, Vec2(randint(-1, 1), randint(-1, 1)), randint(5, 10)]) # Sprite, move direction, time to move

    def random_pos(self, size):
        loop = True
        pos = None
        while loop:
            pos = Vec2(randint(0, self.world_size[0]), randint(0, self.world_size[1]))
            loop = False

            if collides_with(pos, size, self.player[0].pos, self.player[0].size):
                loop = True
                continue

            for planet in self.planets:
                if collides_with(pos, size, planet[0].pos, planet[0].size):
                    loop = True
                    break

            if loop: continue

            for meteor in self.meteors:
                if collides_with(pos, size, meteor[0].pos, meteor[0].size):
                    loop = True
                    break
        return pos
