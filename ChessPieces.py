class Piece:
    killed = False
    is_white = False

    def __init__(self):
        self.killed = False

    def set_killed(self):
        self.killed = True

    def get_white(self):
        return self.is_white

class Pawn(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

class Bishop(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

class Rook(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

class Knight(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

class Queen(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

class King(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white