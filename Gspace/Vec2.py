#encoding: utf-8

class Vec2:
    def __init__( self, x, y ):
        self.x = x
        self.y = y
    
    # indexing operators:
    def __getitem__( self, index ):
        return [ self.x, self.y ][ index ]
        
    def __setitem__( self, index, value ):
        # can we make this prettier???
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise "index must be 0 or 1"
    
    # add, sub, mul, rmul operators:
    def __add__( self, other ):
        return Vec2( self.x + other.x, self.y + other.y )
    
    def __sub__( self, other ):
        return Vec2( self.x - other.x, self.y - other.y )

    def __mul__( self, other ):
        return Vec2( self.x * other, self.y * other )

    def __rmul__( self, other ):
        return __mul__( self, other )
    
    # x= operators here:
    def __iadd__( self, other ):
        self = __add__( self, other )
        
    def __isub__( self, other ):
        self = __sub__( self, other )

    def __imul__( self, other ):
        self = __mul__( self, other )

    def to_tuple( self ):
        return ( self.x, self.y )
