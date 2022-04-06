from ThreeCorp import Corp

class Piece:
    def __init__(self, x: int, y: int, name: str, white: bool, type: str, corp: Corp = None):
        self.killed = False
        self.x_loc = x
        self.y_loc = y
        self.__name = name
        self.__white = white
        self.__type = type
        self.corp = corp

    def set_killed(self):
        self.killed = True

    def is_white(self):
        return self.__white

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_corp(self):
        return self.corp

    def set_corp(self, corp: Corp):
        self.corp = corp

    def has_moved(self):
        return self.corp.hasCommanded()

    def set_moved(self):
        self.corp.command()

class Spot:
    def __init__(self, x: int, y: int, piece: Piece = None):
        self.x_loc = x
        self.y_loc = y
        self.piece = piece

    def set_piece(self, piece: Piece):
        self.piece = piece

    def has_piece(self):
        return (self.piece != None)