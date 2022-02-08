import random
from ChessPieces import *

class Spot:
    x_loc = None
    y_loc = None
    piece = None

    def __init__(self, x, y, piece):
        self.x_loc = x
        self.y_loc = y
        self.piece = piece

    def set_piece(self, piece):
        self.piece = piece

class Game:
    def __init__(self):
        #Creation of the board
        self.__board = [[Spot(x,y,None) for x in range(0,8)] for y in range(0,8)]
        
        #game helpers
        self.__move_list = []
        self.__valid_move_dict = {
            "Pawn": 1,
            "Bishop": 2,
            "Rook": 2,
            "King": 3,
            "Queen": 3,
            "Knight": 4
        }
        
        #create pieces
        pieces = ([Pawn(s, 6, 'wP'+str(s+1), white=True) for s in range(0,8)] +
                  [Pawn(s, 1, 'bP'+str(s+1), white=False) for s in range(0,8)] +
                  [Bishop(2, 7, 'wB1', white=True), Bishop(5, 7, 'wB2', white=True),
                   Bishop(2, 0, 'bB1', white=False), Bishop(5, 0, 'bB2', white=False),
                   Rook(0, 7, 'wR1', white=True), Rook(7, 7, 'wR2', white=True),
                   Rook(0, 0, 'bR1', white=False), Rook(7, 0, 'bR2', white=False),
                   Knight(1, 7, 'wKt1', white=True), Knight(6, 7, 'wKt2', white=True),
                   Knight(1, 0, 'bKt1', white=False), Knight(6, 0, 'bKt2', white=False),
                   Queen(3, 7, 'wQ', white=True), Queen(3, 0, 'bQ', white=False),
                   King(4, 7, 'wKg', white=True), King(4, 0, 'bKg', white=False)])

        #assign pieces to board
        for p in pieces:
            self.__board[p.y_loc][p.x_loc].set_piece(p)
    
    def move_piece(self, *, from_x, from_y, to_x, to_y):
        from_spot=self.__board[from_y][from_x]
        to_spot=self.__board[to_y][to_x]

        self.__move_list = []

        #check for piece at spot
        if from_spot.piece == None:
            print("Error! no piece to move")
            return
        #move
        print(from_spot.piece.name, end=": ")
        if not self.__is_valid_move(from_x, from_y, to_x, to_y):
            print("invalid move")
        else:
            from_spot=self.__board[from_y][from_x]
            to_spot=self.__board[to_y][to_x]
            #non empty spot
            if to_spot.piece:
                #ally spot
                if to_spot.piece.is_white == from_spot.piece.is_white:
                    print("cant target ally piece")
                    return
                #enemy spot
                else:
                    print("attempting capture of piece at target", end=". ")
                    if self.__is_attack_successful(from_spot.piece, to_spot.piece):
                        print("attack successful!", end=" ")
                        to_spot.piece.set_killed()
                    else:
                        print("attack failed. move unsuccesful.")
                        return
            #empty spot
            else:
                print("no piece to attack", end=". ")
            print("moving")
            to_spot.piece = from_spot.piece
            from_spot.piece = None
            to_spot.piece.x_loc = to_x
            to_spot.piece.y_loc = to_y
        return
    
    def __is_valid_move(self, from_x, from_y, to_x, to_y):
        #check for bounds
        if to_x>7 or to_y>7 or to_x<0 or to_y<0: 
            print("target out of bounds", end=". ")
            return False
        p = self.__board[from_y][from_x].piece
        piece_type = type(p).__name__
        if piece_type=='Pawn':
            if p.is_white:
                return (((to_y-from_y)==-1 and (to_x-from_x)==0) or
                        ((to_y-from_y)==-1 and abs(to_x-from_x)==1))
            else:
                return (((to_y-from_y)==1 and (to_x-from_x)==0) or
                        ((to_y-from_y)==1 and abs(to_x-from_x)==1))
        if piece_type=='Bishop':
            return ((abs(to_x-from_x)<=2 and (to_y-from_y)==0) or
                    (abs(to_y-from_y)<=2 and (to_x-from_x)==0) or
                    (abs(to_x-from_x)==1 and abs(to_y-from_y)==1) or
                    (abs(to_x-from_x)==2 and abs(to_y-from_y)==2))
        if piece_type=='Knight' or piece_type=='King' or piece_type=='Queen' or piece_type=='Rook':
            if (abs(to_x - from_x) > self.__valid_move_dict[piece_type] and 
                abs(to_y - from_y) > self.__valid_move_dict[piece_type]):
                print("too far away", end=". ")
                return False
            elif not self.__is_clear_path(from_x,from_y,to_x,to_y):
                print('Path is blocked', end=". ")
                return False
        return True

    def __is_clear_path(self, from_x, from_y, to_x, to_y):
        current_piece = self.__board[from_y][from_x].piece
        target = self.__board[to_y][to_x]
        piece_type = type(current_piece).__name__
        if piece_type=='Bishop':
            if (to_x-from_x==2 and (to_y-from_y)==0):
                return (self.__board[from_y][from_x+1] == None)
            if (to_x-from_x==-2 and (to_y-from_y)==0):
                return (self.__board[from_y][from_x-1] == None)
            if (to_x-from_x==2 and (to_y-from_y)==2):
                return (self.__board[from_y+1][from_x+1] == None)
            if (to_x-from_x==-2 and (to_y-from_y)==-2):
                return (self.__board[from_y-1][from_x-1] == None)
        if piece_type=='Knight' or piece_type=='King' or piece_type=='Queen' or piece_type=='Rook':
            if len(self.__move_list)==0:
                self.__move_list.append(target)

            x_range = current_piece.x_loc - target.x_loc
            y_range = current_piece.y_loc - target.y_loc
            x_steps = [-1, 0, 1]
            y_steps = [-1, 0, 1]

            if x_range == 0 and y_range > 0:
                x_steps = [-1, 0, 1]
                y_steps = [0, 1, -1]
            elif x_range == 0 and y_range < 0:
                x_steps = [-1, 0, 1]
                y_steps = [0, -1, 1]
            elif x_range > 0 and y_range == 0:
                x_steps = [0, 1, -1]
                y_steps = [-1, 0, 1]
            elif x_range < 0 and y_range == 0:
                x_steps = [0, -1, 1]
                y_steps = [-1, 0, 1]
            elif x_range > 0 and y_range > 0:
                x_steps = [0, 1, -1]
                y_steps = [0, 1, -1]
            elif x_range > 0 and y_range < 0:
                x_steps = [0, 1, -1]
                y_steps = [0, -1, 1]
            elif x_range < 0 and y_range > 0:
                x_steps = [0, -1, 1]
                y_steps = [0, 1, -1]
            elif x_range < 0 and y_range < 0:
                x_steps = [0, -1, 1]
                y_steps = [0, -1, 1]

            if target.x_loc == 0:
                x_steps = [0, 1]
            elif target.x_loc == 7:
                x_steps = [-1, 0]
            if target.y_loc == 0:
                y_steps = [0, 1]
            elif target.y_loc == 7:
                y_steps = [-1, 0]

            #move len +1 i.e. 5 Kt, 4 Kg & Q, 3 R
            if len(self.__move_list) == self.__valid_move_dict[piece_type]+1: 
                return False

            for item in x_steps:
                for item2 in y_steps:
                    if item2 == 0 and item == 0:
                        continue
                    if self.__board[target.y_loc + item2][target.x_loc + item].piece == current_piece:
                        return True
                    if self.__board[target.y_loc + item2][target.x_loc + item].piece == None:
                        if self.__board[target.y_loc + item2][target.x_loc + item] in self.__move_list:
                            continue
                        self.__move_list.append(self.__board[target.y_loc + item2][target.x_loc + item])
                        if not self.__is_clear_path(from_x, from_y, self.__move_list[-1].x_loc, self.__move_list[-1].y_loc):
                            self.__move_list.pop()
                            continue
                        else:
                            return True
            return False
        else: return True
        
    def __is_attack_successful(self, current_piece, target_piece):
        dice = random.randint(1, 6)
        print("The roll on the dice is", dice, end=". ")

        capture_table_mins = {
            "Pawn": {
                "Pawn": 4,
                "Rook": 6,
                "Bishop": 5,
                "Knight": 6,
                "Queen": 6,
                "King": 6
            },
            "Rook": {
                "Pawn": 5,
                "Rook": 5,
                "Bishop": 5,
                "Knight": 4,
                "Queen": 4,
                "King": 4
            },
            "Bishop": {
                "Pawn": 3,
                "Rook": 5,
                "Bishop": 4,
                "Knight": 5,
                "Queen": 5,
                "King": 5
            },
            "Knight": {
                "Pawn": 2,
                "Rook": 5,
                "Bishop": 5,
                "Knight": 5,
                "Queen": 5,
                "King": 5
            },
            "Queen": {
                "Pawn": 2,
                "Rook": 5,
                "Bishop": 5,
                "Knight": 4,
                "Queen": 4,
                "King": 4
            },
            "King": {
                "Pawn": 0,
                "Rook": 5,
                "Bishop": 4,
                "Knight": 4,
                "Queen": 4,
                "King": 4
            }
        }
        attack_piece_type=type(current_piece).__name__
        defend_piece_type=type(target_piece).__name__
        return dice>=capture_table_mins[attack_piece_type][defend_piece_type]

    def get_board(self):
        # return self.__board.copy()
        return [[(item2.piece.name if item2.piece else "___") for item2 in item]for item in self.__board]

    def print_board(self):
        print()
        for item in self.__board:
            for item2 in item:
                if item2.piece:
                    print(item2.piece.name, end =" ")
                else:
                    print("___", end =" ")
            print('\n')

game = Game()

game.print_board()

game.move_piece(from_x=0,from_y=6,to_x=1,to_y=5)
game.move_piece(from_x=1,from_y=5,to_x=0,to_y=5)
game.move_piece(from_x=2,from_y=7,to_x=2,to_y=6)
game.move_piece(from_x=2,from_y=5,to_x=1,to_y=5)
game.move_piece(from_x=2,from_y=6,to_x=3,to_y=5)
game.move_piece(from_x=2,from_y=7,to_x=2,to_y=6)
game.move_piece(from_x=2,from_y=6,to_x=2,to_y=4)

game.print_board()

game.move_piece(from_x=3,from_y=7,to_x=2,to_y=7)
game.move_piece(from_x=2,from_y=7,to_x=2,to_y=4)
game.move_piece(from_x=2,from_y=7,to_x=2,to_y=3)
game.move_piece(from_x=2,from_y=7,to_x=2,to_y=5)
game.move_piece(from_x=2,from_y=5,to_x=6,to_y=1)
game.move_piece(from_x=2,from_y=5,to_x=3,to_y=4)
game.move_piece(from_x=3,from_y=4,to_x=6,to_y=1)

game.print_board()

game.move_piece(from_x=0,from_y=7,to_x=0,to_y=5)
game.move_piece(from_x=1,from_y=7,to_x=0,to_y=5)
game.move_piece(from_x=0,from_y=5,to_x=0,to_y=3)
game.move_piece(from_x=0,from_y=3,to_x=0,to_y=6)
game.move_piece(from_x=0,from_y=6,to_x=1,to_y=4)
game.move_piece(from_x=1,from_y=4,to_x=4,to_y=1)

game.print_board()

g=game.get_board()
for line in g:
    print(line)
