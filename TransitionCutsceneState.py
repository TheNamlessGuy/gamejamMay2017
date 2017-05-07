#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class TransitionCutsceneState(WorldInterface):
    def __init__(self, flying_direction):
        WorldInterface.__init__(self)

        self.background_images = {}
        self.background_images["speedlines_vertical"] = load_image("res/speedlines_vertical.png")
        
        self.player_image = load_image("res/player_falling.png")

        self.whatever_idontcare = Sprite(self.background_images["speedlines_vertical"], Vec2(320, 240), (640, 480))
        self.local_sprites = {"speedlines_vertical": [Sprite(self.background_images["speedlines_vertical"], Vec2(320, 240), (640, 480)), \
                                                      Sprite(self.background_images["speedlines_vertical"], Vec2(320, 720), (640, 480))],\
                              "flyer": Sprite(self.player_image, Vec2(320, 240), (40, 62))}

        self.current_background = self.local_sprites["speedlines_vertical"]
        self.current_flyer = self.local_sprites["flyer"]

        # speed and rotation constants
        if flying_direction == "down":
            self.background_speed = -100
            self.flyer_speed = Vec2(0, 8)
            self.flyer_rotationspeed = 11
            self.flyer_rotationdirection = -1   # 1: counter-clockwise, -1: clockwise
            self.flyer_defaultpos = Vec2(320, -31)
            self.termination_check = lambda ypos: ypos > 480 + 31
        elif flying_direction == "up":
            self.background_speed = 100
            self.flyer_speed = Vec2(0, -20)
            self.flyer_rotationspeed = 100
            self.flyer_rotationdirection = 1   # 1: counter-clockwise, -1: clockwise
            self.flyer_defaultpos = Vec2(320, 480 + 31)
            self.termination_check = lambda ypos: ypos < -31

        self.flying_direction = flying_direction

        # positions
        self.flyer_pos = Vec2(0, 0)
        self.flyer_pos.x = self.flyer_defaultpos.x
        self.flyer_pos.y = self.flyer_defaultpos.y
    
    def update(self, game_state):
        self.sprites = []

        if game_state["keyboard"]["ctrl-debug"]:
            if self.flying_direction == "down":
                return game_state["world-planet"]
            elif self.flying_direction == "up":
                return game_state["world-space"]

        def update_back_falling_and_draw(spr, minpos):
            spr.pos.y += self.background_speed
            if spr.pos.y < minpos:
                spr.pos.y = minpos + 480
            self.sprites.append(spr)

        def update_back_rising_and_draw(spr, maxpos):
            spr.pos.y += self.background_speed
            if spr.pos.y > maxpos:
                spr.pos.y = maxpos - 480
            self.sprites.append(spr)

        def update_and_draw_flyer(spr):
            spr.angle += self.flyer_rotationspeed * self.flyer_rotationdirection
            self.flyer_pos = self.flyer_pos + self.flyer_speed
            spr.pos = self.flyer_pos
            if self.termination_check(self.flyer_pos.y):
                if self.flying_direction == "down":
                    return game_state["world-planet"]
                elif self.flying_direction == "up":
                    return game_state["world-space"]
            self.sprites.append(spr)

        if self.flying_direction == "down":
            update_back_falling_and_draw(self.current_background[0], -240)
            update_back_falling_and_draw(self.current_background[1], 240)
        elif self.flying_direction == "up":
            self.sprites.append(self.whatever_idontcare)
            update_back_rising_and_draw(self.current_background[0], 720)
            update_back_rising_and_draw(self.current_background[1], 240)
        state = update_and_draw_flyer(self.current_flyer)
        if state is not None:
            return state
            

    def reset(self, game_state):
        game_state["camera"].x = 0
        game_state["camera"].y = 0
        self.flyer_pos.x = self.flyer_defaultpos.x
        self.flyer_pos.y = self.flyer_defaultpos.y