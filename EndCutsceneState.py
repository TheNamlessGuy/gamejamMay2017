#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

from math import *

class EndCutsceneState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)

        self.local_backgrounds = {}
        self.local_backgrounds["space"] = Sprite(load_image("res/space.png"), Vec2(320, 240), (640, 480))
        self.local_backgrounds["onplanet"] = Sprite(load_image("res/onplanet_final.png"), Vec2(320, 240), (640, 480))

        self.local_sprites = {}
        self.local_sprites["player_falling"] = Sprite(load_image("res/player_falling.png"), Vec2(100, -31), (40, 62))

        self.walker_pos = Vec2(80, 380)
        self.eater_pos = Vec2(510, 380)
        self.planet_pos = Vec2(320, 240)
        self.planet_current = 0
        self.spaceship_pos = Vec2(320, 240)
        self.spaceship_speed = Vec2(12, -12)
        self.local_sprites["player_walking_body"] = []
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_walk2.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_walk1.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_eat1.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_eat2.png"), self.walker_pos, (100, 62)))

        self.local_sprites["player_walking_legs"] = []
        self.local_sprites["player_walking_legs"].append(Sprite(load_image("res/player_legs1.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_legs"].append(Sprite(load_image("res/player_legs2.png"), self.walker_pos, (100, 62)))

        self.local_sprites["planet"] = []
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten1.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten2.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten3.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten4.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten5.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten6.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten7.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten8.png"), self.planet_pos, (110, 110)))
        self.local_sprites["planet"].append(Sprite(load_image("res/planet_final_eaten9.png"), self.planet_pos, (110, 110)))

        self.local_sprites["spaceship"] = []
        self.local_sprites["spaceship"].append(Sprite(load_image("res/spaceship1.png"), self.spaceship_pos, (80, 80), -45))
        self.local_sprites["spaceship"].append(Sprite(load_image("res/spaceship2.png"), self.spaceship_pos, (80, 80), -45))

        self.spaceship_speed_start = Vec2(12, 12)
        self.spaceship_pos_start = Vec2(-100, -160)
        self.local_sprites["spaceship_1"] = []
        self.local_sprites["spaceship_1"].append(Sprite(load_image("res/spaceship1.png"), self.spaceship_pos_start, (80, 80), -135))
        self.local_sprites["spaceship_1"].append(Sprite(load_image("res/spaceship2.png"), self.spaceship_pos_start, (80, 80), -135))

        self.states = {}
        self.states[0] = self.cutscene_approaching
        self.states[1] = self.cutscene_falling
        self.states[2] = self.cutscene_walking
        self.states[3] = self.cutscene_eating
        self.states[4] = self.cutscene_planeteating
        self.states[5] = self.cutscene_eating
        self.states[6] = self.cutscene_planeteating
        self.states[7] = self.cutscene_eating
        self.states[8] = self.cutscene_planeteating
        self.states[9] = self.cutscene_thefinalbite

        self.current_state = 0
        self.current_frame = 0
    
    def update(self, game_state):
        self.sprites = []

        next_state = self.states[self.current_state](game_state)
        if next_state is not None:
            return next_state

        self.current_frame += 1

    def reset(self, game_state):
        game_state["camera"].x = 0
        game_state["camera"].y = 0
        self.current_frame = 0
        self.current_state = 0

        self.walker_pos = Vec2(80, 380)
        self.eater_pos = Vec2(510, 380)
        self.planet_pos = Vec2(320, 240)
        self.planet_current = 0
        self.spaceship_pos = Vec2(320, 240)
        self.spaceship_speed = Vec2(12, -12)
        self.spaceship_speed_start = Vec2(12, 12)
        self.spaceship_pos_start = Vec2(-100, -160)

    def goto_next(self, game_state):
        self.current_state += 1
        if self.current_state not in self.states:
            return game_state["world-splash"]       
        self.current_frame = 0
        
    def cutscene_approaching(self, game_state):
        self.sprites.append(self.local_backgrounds["space"])

        self.sprites.append(self.local_sprites["planet"][0])

        self.spaceship_pos_start.x += self.spaceship_speed_start.x
        self.spaceship_pos_start.y += self.spaceship_speed_start.y
        self.sprites.append(self.local_sprites["spaceship_1"][self.current_frame % 2])

        if self.spaceship_pos_start.x > 280:
            return self.goto_next(game_state)

    def cutscene_falling(self, game_state):
        self.sprites.append(self.local_backgrounds["onplanet"])

        faller = self.local_sprites["player_falling"]
        faller.pos.y += 11
        faller.angle += 101

        self.sprites.append(faller)

        if faller.pos.y > 380:
            return self.goto_next(game_state)

    def cutscene_walking(self, game_state):
        self.sprites.append(self.local_backgrounds["onplanet"])

        walker_body = self.local_sprites["player_walking_body"][self.current_frame % 2]
        walker_legs = self.local_sprites["player_walking_legs"][self.current_frame % 2]

        self.walker_pos.x += 10

        self.sprites.append(walker_legs)
        self.sprites.append(walker_body)

        if self.walker_pos.x > 510:
            return self.goto_next(game_state)

    def cutscene_eating(self, game_state):
        self.sprites.append(self.local_backgrounds["onplanet"])

        eater_body = self.local_sprites["player_walking_body"][1 + (int(floor(self.current_frame / 3)) % 3)]
        eater_legs = self.local_sprites["player_walking_legs"][0]

        eater_body.pos = self.eater_pos
        eater_legs.pos = self.eater_pos

        self.sprites.append(eater_legs)
        self.sprites.append(eater_body)

        if self.current_frame > 48:
            return self.goto_next(game_state)

    def cutscene_planeteating(self, game_state):
        self.sprites.append(self.local_backgrounds["space"])

        if self.current_frame % 13 == 0:
            self.planet_current += 1

        current_planet = self.local_sprites["planet"][self.planet_current]

        self.sprites.append(current_planet)

        if self.current_frame > 48:
            return self.goto_next(game_state)

    def cutscene_thefinalbite(self, game_state):
        self.sprites.append(self.local_backgrounds["space"])

        if self.current_frame < 15:
            self.sprites.append(self.local_sprites["planet"][9])
        else:
            self.spaceship_pos.x += self.spaceship_speed.x
            self.spaceship_pos.y += self.spaceship_speed.y
            self.sprites.append(self.local_sprites["spaceship"][self.current_frame % 2])
            if self.current_frame > 72:
                return self.goto_next(game_state)