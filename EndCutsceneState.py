#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

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
        self.local_sprites["player_walking_body"] = []
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_walk1.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_body"].append(Sprite(load_image("res/player_large_body_walk2.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_legs"] = []
        self.local_sprites["player_walking_legs"].append(Sprite(load_image("res/player_legs1.png"), self.walker_pos, (100, 62)))
        self.local_sprites["player_walking_legs"].append(Sprite(load_image("res/player_legs2.png"), self.walker_pos, (100, 62)))

        self.states = {}
        self.states[0] = self.cutscene_falling
        self.states[1] = self.cutscene_walking
        self.states[2] = self.cutscene_eating

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

    def goto_next(self, game_state):
        self.current_state += 1
        if self.current_state not in self.states:
            return game_state["world-gameover"]       
        self.current_frame = 0

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

        eater_body = self.local_sprites["player_walking_body"][0]
        eater_legs = self.local_sprites["player_walking_legs"][0]

        eater_body.pos = self.eater_pos
        eater_legs.pos = self.eater_pos

        self.sprites.append(eater_legs)
        self.sprites.append(eater_body)