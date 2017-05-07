#encoding: utf-8

import pygame

__sprite_db = {}

def load_image( path ):
    global sprite_db

    if not path in __sprite_db.keys():
        # crashes if the path is invalid
        sprite = pygame.image.load( path )
        # otherwise, it will be inserted to db here
        __sprite_db[ path ] = sprite
        return sprite
    else:
        return __sprite_db[ path ]

# override this class to add features
class Sprite:
    def __init__( self, image, pos, size, angle=0.0, z=0, flip=False ):
        self.image          = image
        self.pos            = pos
        self.size           = size
        self.angle          = angle
        self.z              = z
        self.special_fx_id  = 0 # ugly hack that works <3
        self.flip           = flip

