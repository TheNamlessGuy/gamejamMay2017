#encoding: utf-8

import pygame

sprite_db = {}

def load_image( path ):
    global sprite_db

    if not path in sprite_db.keys():
        # crashes if the path is invalid
        sprite = pygame.image.load( path )
        # otherwise, it will be inserted to db here
        sprite_db[ path ] = sprite
        return sprite
    else:
        return sprite[ path ]

# override this class to add features
class Sprite:
    def __init__( self, image, pos, size, angle ):
        self.image  = image
        self.pos    = pos
        self.size   = size
        self.angle  = angle
