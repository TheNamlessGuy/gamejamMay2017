#encoding: utf-8

# methods that contain this function are considered pure virtual (c++ style)
def needs_implementation():
    raise "the bar"

class WorldInterface:
    def __init__( self ):
        pass

    # graphics:
    def draw( self, render_settings={} ):
        needs_implementation()

    # game logic:
    def update( self, game_state ):
        needs_implementation()

    # when the manager switches to the world: 
    def onLoad( self, game_state ):
        needs_implementation()
