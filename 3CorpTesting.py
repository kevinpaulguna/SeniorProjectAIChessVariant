import random

class Piece:
    def __init__(self, x: int, y: int, name: str, white: bool, type: str):
        self.killed = False
        self.x_loc  = x
        self.y_loc= y
        self.__name = name
        self.__white = white
        self.__type = type
        #NEWCODE Start
        self.corp = None
        #NEWCODE End

    def set_killed(self):
        self.killed = True

    def is_white(self):
        return self.__white
    
    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    #NEWCODE Start
    def set_corp(self, corp):
        self.corp = corp

    def has_moved(self):
        return self.corp.hasCommanded()

    def set_moved(self):
        self.corp.command()
    #NEWCODE End

    

class Spot:
    def __init__(self, x: int, y: int, piece: Piece):
        self.x_loc = x
        self.y_loc = y
        self.piece = piece

    def set_piece(self, piece: Piece):
        self.piece = piece

#NEWCODE Start
class corp:
    def __init__(self, name, commander):
        self.commandAuthUsed = False    #checks whether this corp has used its command
        self.commander = commander      #commander piece, will either be a bishop or a king
        self.commanding = []            #pieces that are in the corp, nnot including the commander
        self.defeated = False 
        self.__name = name
        self.smallMove = False

    #sets the whether the commander has used its one spot move to true
    def movedOne(self):
        self.smallMove = True

    #returns whether the commander has taken the one spot move
    def commanderMoved(self):
        return self.smallMove

    #checks if this corp is white side or black side
    def isWhite(self):
        if self.defeated == True:
            return
        return self.commander.is_white()

    #checks if this corp is commanded by an king or a bishop
    def checkKing(self):
        if self.commander.get_type() == 'King':
            return True
        return False

    #checks to see if the max corp size has been reached if this corp is commanded by a bishop
    def checkLeng(self):
        if self.checkKing() == False and len(self.commanding) == 6:
            print('Max core length exceeded')
            return False
        return True

    #checks to see if a piece is already in this corp
    def hasPiece(self, piece):
        if piece not in self.commanding:
            #print('Piece not in corp')
            return False
        return True

    #checks to see whether this corp has used its command authority
    def hasCommanded(self):
        if self.commandAuthUsed == True:
            return True
        return False

    #adds a specific piece to this corp
    #this is only used by other functions of when initializing the corps
    #do not call directly within the code
    def addToCorp(self, piece):
        if piece.is_white() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if not self.checkLeng():
            return
        if self.hasPiece(piece):
            print('piece already in corp')
            return
        self.commanding.append(piece)
        piece.set_corp(self)
        return

    #removes a piece from this corp
    def removeFromCorp(self, piece):
        if not self.hasPiece(piece):
            print('piece not in corp')
            return
        self.commanding.remove(piece)

    #resets the command authority
    def resetCommand(self):
        self.commandAuthUsed = False
        self.smallMove = False
    
    #sets the command authority to used if it has been
    def command(self):
        if self.hasCommanded():
            print("command authority is already used")
            return
        self.commandAuthUsed = True

    #This corp requests a piece from another corp
    #If the piece can be moved, it is added to this corp and removed from its previous corp
    def request_piece(self, piece):
        if self.hasCommanded():
            print("command authority is already used")
            return
        if piece.corp.isWhite() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if self.hasPiece(piece):
            print('piece already in corp')
            return
        if self.checkKing() == piece.corp.checkKing():
            print('Bishop cant take from bishop')
            return
        if not self.checkLeng():
            return
        self.command()
        print('moving ', piece.get_name(), ' to ', self.__name )
        piece.corp.removeFromCorp(piece)
        self.addToCorp(piece)

    #This method is called when a bishop is defeated
    #All the pieces in that bishop's corp are added to the king's corp
    #This method is not required to be called when the king dies because the game will end.
    def captured(self, corp):
        if corp.isWhite() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if not corp.checkKing():
            print('must return to king')
            return
        self.defeated = True
        self.commander = None
        #print(self.commanding)
        print('Moving pieces from defeated ', self.__name, ' to ', corp.__name)
        for piece in self.commanding:
            #print(piece.get_name())
            corp.addToCorp(piece)
        self.commanding.clear()

    #Prints the commander and all the pieces commanded in this corp
    def printCorp(self):
        if self.defeated == True:
            print("this corp no longer exists")
            return
        print('\n', self.__name, ':\n', self.commander.get_name())
        for piece in self.commanding:
            print(piece.get_name())
        print('\n')
#NEWCODE End


class Game:
    def __init__(self):
        #TODO: this is only for demo
        self.move_failed = False


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
        pieces = ([Piece(s, 6, 'wP'+str(s+1), white=True, type="Pawn") for s in range(0,8)] +
                  [Piece(s, 1, 'bP'+str(s+1), white=False, type="Pawn") for s in range(0,8)] +
                  [Piece(2, 7, 'wB1', white=True, type="Bishop"), Piece(5, 7, 'wB2', white=True, type="Bishop"),
                   Piece(2, 0, 'bB1', white=False, type="Bishop"), Piece(5, 0, 'bB2', white=False, type="Bishop"),
                   Piece(0, 7, 'wR1', white=True, type="Rook"), Piece(7, 7, 'wR2', white=True, type="Rook"),
                   Piece(0, 0, 'bR1', white=False, type="Rook"), Piece(7, 0, 'bR2', white=False, type="Rook"),
                   Piece(1, 7, 'wKt1', white=True, type="Knight"), Piece(6, 7, 'wKt2', white=True, type="Knight"),
                   Piece(1, 0, 'bKt1', white=False, type="Knight"), Piece(6, 0, 'bKt2', white=False, type="Knight"),
                   Piece(3, 7, 'wQ', white=True, type="Queen"), Piece(3, 0, 'bQ', white=False, type="Queen"),
                   Piece(4, 7, 'wKg', white=True, type="King"), Piece(4, 0, 'bKg', white=False, type="King")])

        #NEWCODE Start
        #creating the three corps for each color and adding the pieces to them
        print('\n')
        self.corpW1 = corp('corpW1', pieces[16])
        pieces[16].corp = self.corpW1
        self.corpW1.addToCorp(pieces[0])
        self.corpW1.addToCorp(pieces[1])
        self.corpW1.addToCorp(pieces[2])
        self.corpW1.addToCorp(pieces[24])
        #corpW1.printCorp()

        self.corpW2 = corp('corpW2', pieces[30])
        pieces[30].corp = self.corpW2
        self.corpW2.addToCorp(pieces[3])
        self.corpW2.addToCorp(pieces[4])
        self.corpW2.addToCorp(pieces[20])
        self.corpW2.addToCorp(pieces[21])
        self.corpW2.addToCorp(pieces[28])
        #corpW2.printCorp()

        self.corpW3 = corp('corpW3', pieces[17])
        pieces[17].corp = self.corpW3
        self.corpW3.addToCorp(pieces[5])
        self.corpW3.addToCorp(pieces[6])
        self.corpW3.addToCorp(pieces[7])
        self.corpW3.addToCorp(pieces[25])
        #corpW3.printCorp()

        self.corpB1 = corp('corpB1', pieces[18])
        pieces[18].corp = self.corpB1
        self.corpB1.addToCorp(pieces[8])
        self.corpB1.addToCorp(pieces[9])
        self.corpB1.addToCorp(pieces[10])
        self.corpB1.addToCorp(pieces[26])
        #corpB1.printCorp()


        self.corpB2 = corp('corpB2', pieces[31])
        pieces[31].corp = self.corpB2
        self.corpB2.addToCorp(pieces[11])
        self.corpB2.addToCorp(pieces[12])
        self.corpB2.addToCorp(pieces[22])
        self.corpB2.addToCorp(pieces[23])
        self.corpB2.addToCorp(pieces[29])
        #corpB2.printCorp()


        self.corpB3 = corp('corpB3', pieces[19])
        pieces[19].corp = self.corpB3
        self.corpB3.addToCorp(pieces[13])
        self.corpB3.addToCorp(pieces[14])
        self.corpB3.addToCorp(pieces[15])
        self.corpB3.addToCorp(pieces[27])
        #corpB3.printCorp()

        #NEWCODE End

        #assign pieces to board
        for p in pieces:
            self.__board[p.y_loc][p.x_loc].set_piece(p)
    
    #NEWCODE Start
    def resetTurn(self):
        self.corpW1.resetCommand()
        self.corpW2.resetCommand()
        self.corpW3.resetCommand()
        self.corpB1.resetCommand()
        self.corpB2.resetCommand()
        self.corpB3.resetCommand()
    #NEWCODE End

    #returns array of tuples containing co-ords of possible move spots
    def get_possible_moves_for_piece_at(self, *, x:int, y:int):
        possibles = []

        piece = self.__board[y][x].piece
        piece_type = piece.get_type()

        #gets possible moves
        if piece_type=='Pawn':
            potential_y_coord = y-1 if piece.is_white() else y+1
            possibles=[(x, potential_y_coord), (x-1,potential_y_coord), (x+1, potential_y_coord)]
        elif piece_type=='Bishop':
            possibles=[(x,y+1), (x,y-1), (x,y+2), (x,y-2),
                    (x+1,y+1), (x+1,y-1), (x-1,y+1), (x-1,y-1),
                    (x+2,y+2), (x+2,y-2), (x-2,y+2), (x-2,y-2)]
        elif piece_type in ('Rook', 'Knight', 'King', 'Queen'):
            limit = self.__valid_move_dict[piece_type]+1
            for i in range(limit):
                for j in range(limit):
                    if (i,j)!=(0,0):
                        for candidate in [(x+i,y+j),(x+i,y-j),(x-i,y+j),(x-i,y-j)]:
                            if candidate not in possibles:
                                possibles.append(candidate)

        #removes any out of bounds or ally spots
        for coord in possibles.copy():
            potential_x, potential_y = coord
            if (potential_x>7 or potential_y>7 or potential_x<0 or potential_y<0 or
                (self.__board[potential_y][potential_x].piece and 
                self.__board[potential_y][potential_x].piece.is_white()==piece.is_white()) or
                not self.__is_clear_path(x,y, potential_x, potential_y)):
                possibles.remove(coord)

        return possibles

    def move_piece(self, *, from_x: int, from_y: int, to_x: int, to_y: int):
        from_spot=self.__board[from_y][from_x]
        to_spot=self.__board[to_y][to_x]

        self.__move_list = []

        #check for piece at spot
        if from_spot.piece == None:
            print("Error! no piece to move")
            return

        #NEWCODE Start
        useOne = False
        if from_spot.piece.has_moved() == True and from_spot.piece.get_type() != 'Bishop' and from_spot.piece.get_type() != 'King':
            print('This corp has already used its authority')
            return
        elif abs(from_spot.x_loc - to_spot.x_loc) <= 1 and abs(from_spot.y_loc - to_spot.y_loc) <= 1 and (from_spot.piece.get_type() == 'Bishop' or from_spot.piece.get_type())== 'King':
            #print(from_spot.x_loc, from_spot.y_loc)
            if from_spot.piece.corp.commanderMoved():
                if from_spot.piece.has_moved():
                    print('has used all moves')
                    return
                print('using command authority')
            useOne = True
        
        #NEWCODE End

        #move
        print(from_spot.piece.get_name(), end=": ")
        if not self.__is_valid_move(from_x, from_y, to_x, to_y):
            print("invalid move")
            return
        else:
            from_spot=self.__board[from_y][from_x]
            to_spot=self.__board[to_y][to_x]
            #non empty spot
            if to_spot.piece:
                #ally spot
                if to_spot.piece.is_white() == from_spot.piece.is_white():
                    print("cant target ally piece")
                    return
                #enemy spot
                else:
                    print("attempting capture of piece at target", end=". ")
                    if self.__is_attack_successful(from_spot.piece, to_spot.piece):
                        print("attack successful!", end=" ")
                        
                        #TODO: this is only for demo
                        self.move_failed=False

                        #NEWCODE Start
                        if to_spot.piece.get_type() == 'King':
                            print('you win')
                            return
                        elif to_spot.piece.get_type() == 'Bishop':
                            if to_spot.piece.is_white():
                                to_spot.piece.corp.captured(self.corpW2)
                            else:
                                to_spot.piece.corp.captured(self.corpB2)
                        else:
                            to_spot.piece.corp.removeFromCorp(to_spot.piece)
                        #NEWCODE End

                        to_spot.piece.set_killed()
                    else:
                        print("attack failed. move unsuccesful.")
                        
                        #TODO: this is only for demo
                        self.move_failed=True

                        return
            #empty spot
            else:
                print("no piece to attack", end=". ")
            print("moving")

            #NEWCODE Start
            if useOne == True:
                print('using commander single space move')
                from_spot.piece.corp.movedOne()
            else:
                print('using command authority')
                from_spot.piece.set_moved()

            #NEWCODE End

            to_spot.piece = from_spot.piece
            from_spot.piece = None
            to_spot.piece.x_loc = to_x
            to_spot.piece.y_loc = to_y
            to_spot.piece.hasMoved = 1
        print("~~~~~")
        self.print_board()
        return
    
    def __is_valid_move(self, from_x: int, from_y: int, to_x: int, to_y: int):
        #check for bounds
        if to_x>7 or to_y>7 or to_x<0 or to_y<0: 
            print("target out of bounds", end=". ")
            return False
        p = self.__board[from_y][from_x].piece
        piece_type = p.get_type()
        if piece_type=='Pawn':
            if p.is_white():
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
                print('No clear path', end=". ")
                return False
        return True

    def __is_clear_path(self, from_x: int, from_y:int, to_x: int, to_y: int):
        current_piece = self.__board[from_y][from_x].piece
        target = self.__board[to_y][to_x]
        piece_type = current_piece.get_type()
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

    def __is_attack_successful(self, current_piece: Piece, target_piece: Piece):
        dice = random.randint(1, 6)
        print("The roll on the dice is", dice, end=". ")

        #format: capture_table_mins[attacking piece][defending piece] = min reqd for successful attack
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
        attack_piece_type=current_piece.get_type()
        defend_piece_type=target_piece.get_type()
        return dice>=capture_table_mins[attack_piece_type][defend_piece_type]

    def get_board(self):
        return [[(item2.piece.get_name() if item2.piece else "___") for item2 in item]for item in self.__board]

    def print_board(self):
        print()
        for item in self.__board:
            for item2 in item:
                if item2.piece:
                    print(item2.piece.get_name(), end =" ")
                else:
                    print("___", end =" ")
            print('\n')
        print("---------------------------------\n")


game = Game()

game.move_piece(from_x=4,from_y=6,to_x=3,to_y=5)
game.move_piece(from_x=4,from_y=7,to_x=4,to_y=6)
game.move_piece(from_x=4,from_y=6,to_x=4,to_y=5)
game.resetTurn()
game.move_piece(from_x=4,from_y=6,to_x=4,to_y=5)
