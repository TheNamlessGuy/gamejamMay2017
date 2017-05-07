#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class SpoonCutsceneState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)

        self.local_sprites = []
        self.local_sprites.append(Sprite(load_image("res/spoon_expansion_cutscene1.png"), Vec2(320, 240), (640, 480)))
        self.local_sprites.append(Sprite(load_image("res/spoon_expansion_cutscene2.png"), Vec2(320, 240), (640, 480)))
        self.local_sprites.append(Sprite(load_image("res/spoon_expansion_cutscene3.png"), Vec2(320, 240), (640, 480)))
        self.local_sprites.append(Sprite(load_image("res/spoon_expansion_cutscene4.png"), Vec2(320, 240), (640, 480)))
        self.local_sprites.append(Sprite(load_image("res/spoon_expansion_cutscene5.png"), Vec2(320, 240), (640, 480)))

        self.states = {}
        self.states[0] = self.cutscene_begin
        self.states[1] = self.cutscene_startexpansion
        self.states[2] = self.cutscene_finalexpansion
        self.states[3] = self.cutscene_standstill
        self.states[4] = self.cutscene_party

        self.current_state = 0
        self.current_frame = 0
    
    def update(self, game_state):
        self.sprites = []

        if game_state["keyboard"]["ctrl-debug"]:
            return game_state["world-cutscene"]["rising"]

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
            return game_state["world-cutscene"]["rising"]        
        self.current_frame = 0

    def cutscene_begin(self, game_state):
        self.sprites.append(self.local_sprites[0])
        if self.current_frame > 2:
            return self.goto_next(game_state)

    def cutscene_startexpansion(self, game_state):
        timelimit = 50

        if self.current_frame == timelimit:
            self.sprites.append(self.local_sprites[0])
            return self.goto_next(game_state)

        if self.current_frame % (timelimit - self.current_frame) == 0:
            self.sprites.append(self.local_sprites[1])
        else:
            self.sprites.append(self.local_sprites[0])

    def cutscene_finalexpansion(self, game_state):
        if self.current_frame > 15:
            self.sprites.append(self.local_sprites[1])
            return self.goto_next(game_state)

        if self.current_frame % 2 == 0:
            self.sprites.append(self.local_sprites[2])
        else:
            self.sprites.append(self.local_sprites[1])

    def cutscene_standstill(self, game_state):
        self.sprites.append(self.local_sprites[2])

        if self.current_frame > 16:
            return self.goto_next(game_state)

    def cutscene_party(self, game_state):
        if self.current_frame % 2 == 0:
            self.sprites.append(self.local_sprites[3])
        else:
            self.sprites.append(self.local_sprites[4])

        if self.current_frame > 48:
            return self.goto_next(game_state)