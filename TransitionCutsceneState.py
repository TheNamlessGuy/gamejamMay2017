#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class TransitionCutsceneState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)

        self.background_images = {}
        self.background_images["speedlines_horizontal"] = load_image("res/speedlines_horizontal.png")
        self.background_images["speedlines_vertical"] = load_image("res/speedlines_vertical.png")
        
        self.player_image = load_image("res/player_falling.png")

        self.local_sprites = {"speedlines_vertical": [Sprite(self.background_images["speedlines_vertical"], Vec2(320, 240), (640, 480)), \
                                                      Sprite(self.background_images["speedlines_vertical"], Vec2(320, 720), (640, 480))],\
                              "speedlines_horizontal": [Sprite(self.background_images["speedlines_horizontal"], Vec2(320, 240), (640, 480)), \
                                                      Sprite(self.background_images["speedlines_horizontal"], Vec2(960, 240), (640, 480))], \
                              "flyer": Sprite(self.player_image, Vec2(320, 240), (40, 62))}

        self.current_background = self.local_sprites["speedlines_vertical"]
        self.current_flyer = self.local_sprites["flyer"]

        # speed and rotation constants
        self.background_speed = -100
        self.flyer_speed = Vec2(0, 8)
        self.flyer_rotationspeed = 11
        self.flyer_rotationdirection = -1   # 1: counter-clockwise, -1: clockwise

        # positions
        self.flyer_pos = Vec2(320, -31)
    
    def update(self, game_state):
        self.sprites = []

        if game_state["keyboard"]["ctrl-debug"]:
            return game_state["world-planet"]

        def update_back_y_and_draw(spr, minpos):
            spr.pos.y += self.background_speed
            if spr.pos.y < minpos:
                spr.pos.y = minpos + 480
            self.sprites.append(spr)

        def update_and_draw_flyer(spr):
            spr.angle += self.flyer_rotationspeed * self.flyer_rotationdirection
            self.flyer_pos = self.flyer_pos + self.flyer_speed
            spr.pos = self.flyer_pos
            if self.flyer_pos.y > 480 + 31:
                return game_state["world-planet"]
            self.sprites.append(spr)

        update_back_y_and_draw(self.current_background[0], -240)
        update_back_y_and_draw(self.current_background[1], 240)
        state = update_and_draw_flyer(self.current_flyer)
        if state is not None:
            return state
            

    def reset(self, game_state):
        game_state["camera"].x = 0
        game_state["camera"].y = 0
        self.flyer_pos.x = 320
        self.flyer_pos.y = -31