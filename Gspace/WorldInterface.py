#encoding: utf-8

# methods that contain this function are considered pure virtual (c++ style)
def override_this_method_plz():
    raise "the bar"

class WorldInterface:
    def __init__( self ):
        self.background = None
        self.sprites = []
        self.render_settings = {}

    # game logic:
    def update( self, game_state={} ):
        override_this_method_plz()

    # when the manager switches to the world: 
    def onLoad( self, game_state={} ):
        override_this_method_plz()

    def onUnload( self, game_state={} ):
        override_this_method_plz()
