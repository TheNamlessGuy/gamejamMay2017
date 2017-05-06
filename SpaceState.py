#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, collides_with
from random import randint
from math import sin, cos

class SpaceState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)

        self.enter_planet = Sprite(load_image("res/enterplanet.png"), (0, 0), (100, 50))
        self.player = (Sprite(load_image("res/spaceship2.png"), (320, 240), (50, 50)), 10) # Sprite, invincibility timer

        self.planets = []
        self.spawn_planets(5)

        self.meteors = []
        self.spawn_meteors(8)

        self.player_speed = 1
        self.player_rot_speed = 0.5

        self.meteor_speed = self.player_speed + 0.5
        self.planet_rot_speed = 0.5

        self.current_planet = None
        self.collided_meteor = False

    def update(self, game_state):
        self.sprites[:] = [] # Clear sprites
        new_state = None

        # Update player
        if game_state['keyboard']['ctrl-up']:
            self.player.pos[0] += self.player_speed * sin(self.player.angle)
            self.player.pos[1] += self.player_speed * cos(self.player.angle)

        if game_state['keyboard']['ctrl-left']:
            self.player.angle -= self.player_rot_speed
        if game_state['keyboard']['ctrl-right']:
            self.player.angle += self.player_rot_speed

        # Update meteors + collision
        for meteor in self.meteors:
            if collides_with(self.player[0].pos, self.player[0].size, meteor.pos, meteor.size):
                self.collided_meteor = True
                new_state = game_state['world-meteor']
            # TODO: if collides with camera
            self.sprites.append(meteor)

        if new_state is not None: return new_state

        # Update planets, detect if close to landable planet
        can_land_on = None
        for index, planet in enumerate(self.planets):
            planet[0].angle += self.planet_rot_speed
            if collides_with(self.player[0].pos, self.player[0].size, planet[0].pos, planet[0].size):
                can_land_on = index

            # TODO: if collides with camera
            self.sprites.append(planet[0])


        # Detect if landing on planet
        if can_land_on is not None and game_state['keyboard']['ctrl-action']:
            self.current_planet = can_land_on
            return game_state['world-planet']

        # Set player to render
        self.sprites.append(self.player[0])
        # Set "Enter planet" prompt to render
        if can_land_on is not None:
            self.enter_planet.pos = (self.player[0].pos[0], self.player[0].pos[1] - self.player[0].size[1])
            self.sprites.append(self.enter_planet)

    def reset(self, game_state):
        if self.current_planet is not None:
            if game_state['went-well']:
                self.planets[self.current_planet][1] = False
            else:
                self.player[1] = 10
            self.current_planet = None

        if self.collided_meteor:
            self.player[1] = 10
            self.collided_meteor = False

    def spawn_planets(self, amount):
        return
        self.planets[:] = [] # Clear planets (just in case)
        size = (50, 50)
        for i in range(amount):
            sprite = Sprite(load_image("res/planet" + str(randint(0, 3)) + ".png"), self.random_pos(size), size)
            self.planets.append((sprite, True)) # Sprite, isEnterable

    def spawn_meteors(self, amount):
        return
        self.meteors[:] = [] # Clear meteors (just in case)
        size = (25, 25)
        for i in range(amount):
            self.meteors.append(Sprite(load_image('res/meteor.png'), self.random_pos(size), size))

    def random_pos(self, size):
        loop = True
        while loop:
            pos = (randint(0, 1920), randint(0, 1080))
            loop = False

            if collides_with(pos, size, self.player.pos, self.player.size):
                loop = True
                continue

            for planet in self.planets:
                if collides_with(pos, size, planet[0].pos, planet[0].size):
                    loop = True
                    break

            if loop: continue

            for meteor in self.meteors:
                if collides_with(pos, size, planet.pos, planet.size):
                    loop = True
                    break