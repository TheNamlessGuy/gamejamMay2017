#encoding: utf-8

from Gspace import WorldInterface, Sprite, load_image, Vec2
from random import randint
from math import sin, cos, radians


class Animator():
    def __init__(self, anims, start_anim, sprite):
        self.anims = anims 
        self.target = sprite
        self.set_anim(start_anim)
        
    def anim_update(self):
        self.next -= 1
        
        if self.next <= 0:
            if self.cur_index == len(self.cur_anim[0]) - 1:
                self.set_anim(self.cur_anim[2])
            else:
                self.set_frame(self.cur_index + 1)
    
    def set_frame(self, index=0):
        self.cur_index = index
        self.next = self.cur_anim[1]
        self.target.image = self.cur_anim[0][self.cur_index]
        
    def set_anim(self, new_anim):
        self.cur_anim = self.anims[new_anim]
        self.set_frame()


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
                               load_image("res/icecreamboat3.png"), \
                               load_image("res/icecreamsmallboat1.png"), \
                               load_image("res/icecreamsmallboat2.png")]
                              
       
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
        self.anims['enemy_boat']['walk'] = (self.res['enemies'][6:9] + [self.res['enemies'][7]], 6, 'walk')
        self.anims['mini_boat'] = {} 
        self.anims['mini_boat']['walk'] = (self.res['enemies'][9:11], 4, 'walk')
               
        #Ticks
        self.ticks = {}
        self.ticks['player_attack'] = 0
        self.ticks['enemy_attack'] = 0
        self.ticks['enemy_move'] = 0       
                                            
        #BG
        self.bg = (Sprite(None, Vec2(320, 240), (640, 480)))
        
        #Player
        self.player = (Sprite(None, Vec2(150, 320), (100, 62)))
        self.player_legs = (Sprite(None, Vec2(200, 360), (100, 62)))
        self.player_speed = 7.0
        self.player_can_attack = True
        self.player_next_attack = 0
        self.player_flipped = False
        self.player_dmg = 1
        self.player_targets = 1
        
        #Enemy
        self.enemies = []

    def update(self, game_state):
        #Clear sprites
        self.sprites[:] = []
        
        #Do ticks
        for key in self.ticks:
            self.ticks[key] -= 1
        
        #Draw BG
        self.sprites.append(self.bg)
        
        #Check Enemy collision TODO
        #for enemy in self.enemies:
            
        
                
        #Do input
        if game_state['keyboard']['ctrl-up']:
            self.player.pos.y -= self.player_speed;
        if game_state['keyboard']['ctrl-left']:
            self.player.pos.x -= self.player_speed;
            self.player_flipped = True         
        if game_state['keyboard']['ctrl-right']:
            self.player.pos.x += self.player_speed;
            self.player_flipped = False
        if game_state['keyboard']['ctrl-down']:
            self.player.pos.y += self.player_speed;
        if game_state['keyboard']['ctrl-action']:
            if self.player_can_attack and self.ticks['player_attack'] <= 0:  
                self.player_can_attack = False
                self.ticks['player_attack'] = 19
                if game_state['spoon-pwr'] == 0:
                    self.player_animator.set_anim('small_eat')
                elif game_state['spoon-pwr'] == 1:
                    self.player_animator.set_anim('medium_eat')
                elif game_state['spoon-pwr'] >= 2:
                    self.player_animator.set_anim('large_eat')
                #Check collision with ENEMIES
                
        else:
            self.player_can_attack = True    
        
        #Debug win    
        if game_state['keyboard']['ctrl-debug'] and game_state['keyboard']['ctrl-right']:
            game_state['went-well'] = True
            game_state['spoon-pwr'] += 1
            if game_state['spoon-pwr'] == 3 or game_state['spoon-pwr'] == 4:
                return game_state['world-cutscene']['rising']
            return game_state['world-cutscene']['spoon-expansion']
                    
        #Enemy think
        for enemy in self.enemies:
            #Direction
            enemy['next_dir'] -= 1
            if enemy['next_dir'] <= 0:
                enemy['next_dir'] = 16
                enemy['direction'] = randint(0,360)
            
            #Movement
            enemy['enemy'].pos.x -= enemy['speed'] * sin(radians(enemy['direction']))
            enemy['enemy'].pos.y -= enemy['speed'] * cos(radians(enemy['direction']))

            #Level bounds
            if enemy['enemy'].pos.x < 60:
                enemy['enemy'].pos.x = 60
                enemy['next_dir'] = 0
            if enemy['enemy'].pos.x > 600:
                enemy['enemy'].pos.x = 600
                enemy['next_dir'] = 0
            if enemy['enemy'].pos.y < 60:
                enemy['enemy'].pos.y = 60
                enemy['next_dir'] = 0
            if enemy['enemy'].pos.y > 420:
                enemy['enemy'].pos.y = 420
                enemy['next_dir'] = 0   
                
            #Spawn miniboat
            if enemy['type'] == 3:
                enemy['next_boat'] -= 1
                if enemy['next_boat'] <= 0:
                    self.spawn_enemy(4, enemy['enemy'].pos)
                    enemy['next_boat'] = 40
        
        #Animate and draw enemy
        for enemy in self.enemies:
            enemy['animator'].anim_update()
            self.sprites.append(enemy['enemy'])
            
        #Position legs, animate and draw player  
        self.player.flip = self.player_flipped 
        self.player_legs.flip = self.player_flipped
        self.player_legs.pos = self.player.pos
        
        self.player_animator.anim_update()
        self.plegs_animator.anim_update()
              
        self.sprites.append(self.player)
        self.sprites.append(self.player_legs)
        
        
    def reset(self, game_state):
        #Reset camera
        game_state['camera'].x = 0
        game_state['camera'].y = 0
    
        #Reset enemies
        self.enemies = []
    
        #Set up player based on SPOON PWR
        if game_state['spoon-pwr'] == 0:
            self.player_animator = Animator(self.anims['player'], 'small_walk', self.player)
            self.player_dmg = 1
        elif game_state['spoon-pwr'] == 1:
            self.player_animator = Animator(self.anims['player'], 'medium_walk', self.player)
            self.player_dmg = 3
        elif game_state['spoon-pwr'] >= 2:
            self.player_animator = Animator(self.anims['player'], 'large_walk', self.player)
            self.player_dmg = 6
            
        self.plegs_animator = Animator(self.anims['player_legs'], 'legs_walk', self.player_legs)
        
        #Set up enemy based on planet
        planet = game_state['identifier']
        self.planet_spawn(planet) 
        
        #set correct BG 
        self.bg.image = self.res['bgs'][planet-1]
        
    def planet_spawn(self, planet):
        print(planet)
        if planet == 1:
            self.spawn_enemy(1, Vec2(460, 320))
        elif planet == 2:
            self.spawn_enemy(2, Vec2(460, 320))
        elif planet == 3:
            self.spawn_enemy(3, Vec2(460, 320))
        elif planet == 4:
            self.spawn_enemy(1, Vec2(350, 120))
            self.spawn_enemy(1, Vec2(300, 260))
            self.spawn_enemy(1, Vec2(320, 380))
        elif planet == 5:    
            self.spawn_enemy(2, Vec2(320, 360))        
            self.spawn_enemy(3, Vec2(350, 120))

    def spawn_enemy(self, enemy_type, pos):
        print("SHOULD SPAWN",enemy_type,pos.x,pos.y)
        if enemy_type == 1:
            enemy = {} #STICK
            enemy['enemy'] = (Sprite(None, Vec2(pos.x, pos.y), (80, 100))) 
            enemy['animator'] = Animator(self.anims['enemy_stick'], 'walk', enemy['enemy'])
            enemy['direction'] = 0
            enemy['next_dir'] = 0
            enemy['speed'] = 7.0
            enemy['type'] = 1 
            enemy['hp'] = 5
            enemy['important'] = True
            self.enemies.append(enemy)
        elif enemy_type == 2:
            enemy = {} #CONE
            enemy['enemy'] = (Sprite(None, Vec2(pos.x, pos.y), (80, 100)))  
            enemy['animator'] = Animator(self.anims['enemy_cone'], 'walk', enemy['enemy'])
            enemy['direction'] = 0
            enemy['next_dir'] = 0
            enemy['speed'] = 6.0
            enemy['type'] = 2
            enemy['hp'] = 5
            enemy['important'] = True
            self.enemies.append(enemy)
        elif enemy_type == 3:
            enemy = {} #BOAT
            enemy['enemy'] = (Sprite(None, Vec2(pos.x, pos.y), (80, 58))) 
            enemy['animator'] = Animator(self.anims['enemy_boat'], 'walk', enemy['enemy'])
            enemy['direction'] = 0
            enemy['next_dir'] = 0
            enemy['next_boat'] = 40
            enemy['speed'] = 2.0
            enemy['type'] = 3
            enemy['hp'] = 5
            enemy['important'] = True
            self.enemies.append(enemy)
        elif enemy_type == 4:
            enemy = {}
            enemy['enemy'] = (Sprite(None, Vec2(pos.x,pos.y), (60, 43))) 
            enemy['animator'] = Animator(self.anims['mini_boat'], 'walk', enemy['enemy'])
            enemy['direction'] = 0
            enemy['next_dir'] = 0
            enemy['speed'] = 6.0
            enemy['type'] = 4
            enemy['hp'] = 5
            enemy['important'] = False
            self.enemies.append(enemy)
        
