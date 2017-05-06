#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2

class Animator():
    def __init__(self, anims, start_anim, sprite):
        self.anims = anims 
        self.target = sprite
        self.do_anim(start_anim)
        
    def anim_update(self):
        self.next -= 1
        
        if self.next <= 0:
            if self.cur_index == len(self.cur_anim[0]) - 1:
                self.do_anim(self.cur_anim[2])
            else:
                self.cur_index += 1
                self.target.image = self.cur_anim[0][self.cur_index]
                self.next = self.cur_anim[1]
                self.target.image = self.cur_anim[0][self.cur_index]
                
    def do_anim(self, new_anim, index=0):
        self.cur_anim = self.anims[new_anim]
        self.cur_index = index
        self.next = self.cur_anim[1]
        self.target.image = self.cur_anim[0][self.cur_index]


class PlanetState(WorldInterface):
    def __init__(self):
        WorldInterface.__init__(self)
        #load all res
        self.res = {}
        self.res['bgs'] = [load_image("res/onplanet1.png"), \
                           load_image("res/onplanet2.png"), \
                           load_image("res/onplanet3.png"), \
                           load_image("res/onplanet4.png"),
                           load_image("res/onplanet5.png")]
        
        self.res['player'] = [load_image("res/player_small_body_walk1.png"), \
                              load_image("res/player_small_body_walk2.png"), \
                              load_image("res/player_small_body_eat1.png"), \
                              load_image("res/player_small_body_eat2.png"), \
                              load_image("res/player_medium_body_walk1.png"), \
                              load_image("res/player_medium_body_walk2.png"), \
                              load_image("res/player_medium_body_eat1.png"), \
                              load_image("res/player_medium_body_eat2.png"), \
                              load_image("res/player_large_body_walk1.png"), \
                              load_image("res/player_large_body_walk2.png"), \
                              load_image("res/player_large_body_eat1.png"), \
                              load_image("res/player_large_body_eat2.png"), \
                              load_image("res/player_legs1.png"), \
                              load_image("res/player_legs2.png")]
                              
        self.res['enemies'] = [load_image("res/icecreamstick1.png"), \
                               load_image("res/icecreamstick2.png"), \
                               load_image("res/icecreamcone1.png"), \
                               load_image("res/icecreamcone2.png"), \
                               load_image("res/icecreamcone1_open.png"), \
                               load_image("res/icecreamcone2_open.png"), \
                               load_image("res/icecreamboat1.png"), \
                               load_image("res/icecreamboat2.png"), \
                               load_image("res/icecreamboat3.png")]
                              
       
        #Animation configurations
        self.anims = {}
        self.anims['player'] = {}
        self.anims['player']['small_walk'] = (self.res['player'][0:2], 10, 'small_walk')
        self.anims['player']['medium_walk'] = (self.res['player'][4:6], 10, 'medium_walk')
        self.anims['player']['large_walk'] = (self.res['player'][8:10], 10, 'large_walk')        
        self.anims['player']['small_eat'] = (self.res['player'][2:4], 10, 'small_walk')
        self.anims['player']['medium_eat'] = (self.res['player'][6:8], 10, 'medium_walk')
        self.anims['player']['large_eat'] = (self.res['player'][10:12], 10, 'large_walk')        
        self.anims['player_legs'] = {}
        self.anims['player_legs']['legs_walk'] = (self.res['player'][12:14], 10, 'legs_walk')
        self.anims['enemy_stick'] = {}
        self.anims['enemy_stick']['walk'] = (self.res['enemies'][0:2], 8, 'walk')
        self.anims['enemy_cone'] = {}
        self.anims['enemy_cone']['walk'] = (self.res['enemies'][2:4], 8, 'open')
        self.anims['enemy_cone']['open'] = (self.res['enemies'][4:6], 8, 'walk')
        self.anims['enemy_boat'] = {}   
        self.anims['enemy_boat']['walk'] = (self.res['enemies'][6:9] + [self.res['enemies'][7]], \
                                            6, 'walk')              
                                            
        #BG
        self.bg = (Sprite(None, Vec2(320, 240), (640, 480)))
        
        #Player
        self.player = (Sprite(None, Vec2(150, 320), (100, 62)))
        self.player_legs = (Sprite(None, Vec2(200, 360), (100, 62)))
        self.player_speed = 1
        self.player_can_attack = True
        self.player_next_attack = 0
        
        #Enemy
        self.enemy = (Sprite(None, Vec2(460, 320), (80, 100))) 
        self.enemy_direction = 0
        self.enemy_next_dir = 0
        self.enemy_speed = 1
        
        self.enemytemp = (Sprite(None, Vec2(150, 120), (80, 100))) 
        self.enemytemp2 = (Sprite(None, Vec2(300, 240), (80, 58))) 

    def update(self, game_state):
        #Clear sprites
        self.sprites[:] = []
        
        #Draw BG
        self.sprites.append(self.bg)
                
        #Do input
        if game_state['keyboard']['ctrl-up']:
            pass
        if game_state['keyboard']['ctrl-left']:
            pass
        if game_state['keyboard']['ctrl-right']:
            pass
        if game_state['keyboard']['ctrl-down']:
            pass
        if game_state['keyboard']['ctrl-action']:
            self.player_animator.do_anim('small_eat')
            #if player_can_attack and game_state['clock'] >= self.sprites.append(self.player):
                #DO ATTACK    
                #self.player_can_attack = False
                #self.player_next_attack = game_state['clock'] + 0.8
        if game_state['keyboard']['ctrl-debug'] and game_state['keyboard']['ctrl-right']:
            game_state['went-well'] = True
            return game_state['world-space']
        #else:
            #player_can_attack = True    
            
        
            
        #Position legs and draw player    
        self.player_legs.pos = self.player.pos
        
        self.player_animator.anim_update()
        self.plegs_animator.anim_update()
        self.enemy_animator.anim_update()
        self.enemy2_animator.anim_update()
        self.enemy3_animator.anim_update()
        
        
        self.sprites.append(self.player)
        self.sprites.append(self.player_legs)
        
        #Enemy thinks
        #time for next dir?
            #set new dir
        
        #Move enemy
        #Do anim update
        
        
        #Draw Enemy   
        self.sprites.append(self.enemy)
        self.sprites.append(self.enemytemp)
        self.sprites.append(self.enemytemp2)
        
        
    def reset(self, game_state):
        #Reset camera
        
        game_state['camera'].x = 0
        game_state['camera'].y = 0
    
        #Set up animations
        self.player_animator = Animator(self.anims['player'], 'small_walk', self.player)
        self.plegs_animator = Animator(self.anims['player_legs'], 'legs_walk', self.player_legs)
        
        #stick
        self.enemy_animator = Animator(self.anims['enemy_stick'], 'walk', self.enemy)
        self.enemy2_animator = Animator(self.anims['enemy_cone'], 'walk', self.enemytemp)
        self.enemy3_animator = Animator(self.anims['enemy_boat'], 'walk', self.enemytemp2)
        
        #reset state vars
    
        #set correct BG
        planet = game_state['identifier']
        self.bg.image = self.res['bgs'][planet-1]
        
        
        
        
    
