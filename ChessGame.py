import random
from turnManager import TurnManager
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


class Game:
    def __init__(self):
        self.tracker = TurnManager()

        # board
        self.__board = [[Spot(x, y) for x in range(0, 8)] for y in range(0, 8)]

        # captured pieces dict, each list is named for the team which captured the pieces in it
        self.__captured_by = {
            "white": [],
            "black": []
        }

        # game helpers
        self.__move_list = []
        self.__VALID_MOVE_DICT = {
            "Pawn": 1,
            "Bishop": 2,
            "Rook": 2,
            "King": 3,
            "Queen": 3,
            "Knight": 4
        }

        self.__last_dice_roll = -1
        self.__move_message = ""

        # create pieces
        pieces = ([Piece(s, 6, 'wP' + str(s + 1), white=True, type="Pawn") for s in range(0, 8)] +
                  [Piece(s, 1, 'bP' + str(s + 1), white=False, type="Pawn") for s in range(0, 8)] +
                  [Piece(2, 7, 'wB1', white=True, type="Bishop"), Piece(5, 7, 'wB2', white=True, type="Bishop"),
                   Piece(2, 0, 'bB1', white=False, type="Bishop"), Piece(5, 0, 'bB2', white=False, type="Bishop"),
                   Piece(0, 7, 'wR1', white=True, type="Rook"), Piece(7, 7, 'wR2', white=True, type="Rook"),
                   Piece(0, 0, 'bR1', white=False, type="Rook"), Piece(7, 0, 'bR2', white=False, type="Rook"),
                   Piece(1, 7, 'wKt1', white=True, type="Knight"), Piece(6, 7, 'wKt2', white=True, type="Knight"),
                   Piece(1, 0, 'bKt1', white=False, type="Knight"), Piece(6, 0, 'bKt2', white=False, type="Knight"),
                   Piece(3, 7, 'wQ', white=True, type="Queen"), Piece(3, 0, 'bQ', white=False, type="Queen"),
                   Piece(4, 7, 'wKg', white=True, type="King"), Piece(4, 0, 'bKg', white=False, type="King")])

        # creating the three corps for each color and adding the pieces to them
        print('\n')
        self.corpW1 = Corp('corpW1', pieces[16])
        pieces[16].corp = self.corpW1
        self.corpW1.addToCorp(pieces[0])
        self.corpW1.addToCorp(pieces[1])
        self.corpW1.addToCorp(pieces[2])
        self.corpW1.addToCorp(pieces[24])
        # corpW1.printCorp()

        self.corpW2 = Corp('corpW2', pieces[30])
        pieces[30].corp = self.corpW2
        self.corpW2.addToCorp(pieces[3])
        self.corpW2.addToCorp(pieces[4])
        self.corpW2.addToCorp(pieces[20])
        self.corpW2.addToCorp(pieces[21])
        self.corpW2.addToCorp(pieces[28])
        # corpW2.printCorp()

        self.corpW3 = Corp('corpW3', pieces[17])
        pieces[17].corp = self.corpW3
        self.corpW3.addToCorp(pieces[5])
        self.corpW3.addToCorp(pieces[6])
        self.corpW3.addToCorp(pieces[7])
        self.corpW3.addToCorp(pieces[25])
        # corpW3.printCorp()

        self.corpB1 = Corp('corpB1', pieces[18])
        pieces[18].corp = self.corpB1
        self.corpB1.addToCorp(pieces[8])
        self.corpB1.addToCorp(pieces[9])
        self.corpB1.addToCorp(pieces[10])
        self.corpB1.addToCorp(pieces[26])
        # corpB1.printCorp()

        self.corpB2 = Corp('corpB2', pieces[31])
        pieces[31].corp = self.corpB2
        self.corpB2.addToCorp(pieces[11])
        self.corpB2.addToCorp(pieces[12])
        self.corpB2.addToCorp(pieces[22])
        self.corpB2.addToCorp(pieces[23])
        self.corpB2.addToCorp(pieces[29])
        # corpB2.printCorp()

        self.corpB3 = Corp('corpB3', pieces[19])
        pieces[19].corp = self.corpB3
        self.corpB3.addToCorp(pieces[13])
        self.corpB3.addToCorp(pieces[14])
        self.corpB3.addToCorp(pieces[15])
        self.corpB3.addToCorp(pieces[27])
        # corpB3.printCorp()

        # assign pieces to board
        for p in pieces:
            self.__board[p.y_loc][p.x_loc].set_piece(p)

    def resetTurn(self):  # Used to reset corp command count for each corp
        self.corpW1.resetCommand()
        self.corpW2.resetCommand()
        self.corpW3.resetCommand()
        self.corpB1.resetCommand()
        self.corpB2.resetCommand()
        self.corpB3.resetCommand()

    # returns array of tuples containing co-ords of possible move spots
    def get_possible_moves_for_piece_at(self, *, x: int, y: int, attack_only: bool = False):
        self.__reset_move_vars()
        possibles = []
        piece = self.__board[y][x].piece
        if not piece:
            return possibles
        piece_type = piece.get_type()

        if self.tracker.current_player != int(piece.is_white()):
            # the piece selected is not in the active turn so it has no moves
            return possibles

        # gets possible moves, making sure to not include out of bounds moves
        if piece_type == 'Pawn':
            new_y_coord = y - 1 if piece.is_white() else y + 1
            for new_x_coord in [x, x - 1, x + 1]:
                if not (new_x_coord > 7 or new_y_coord > 7 or new_x_coord < 0 or new_y_coord < 0):
                    possibles.append((new_x_coord, new_y_coord, self.__board[new_y_coord][new_x_coord].has_piece()))


        elif piece_type in ('Bishop', 'Rook', 'Knight', 'King', 'Queen'):
            limit = self.__VALID_MOVE_DICT[piece_type] + 1
            for i in range(limit):
                for j in range(limit):
                    if (i, j) != (0, 0):
                        # checks for duplicates
                        for c_x, c_y in [(x + i, y + j), (x + i, y - j), (x - i, y + j), (x - i, y - j)]:
                            if ((c_x, c_y, True) not in possibles and
                                    (c_x, c_y, False) not in possibles and
                                    not (c_x > 7 or c_y > 7 or c_x < 0 or c_y < 0)):
                                if piece_type == "Bishop" and not (
                                        i == j or i == 0 or j == 0):  # checks if invalid move for Bishop
                                    continue
                                possibles.append((c_x, c_y, self.__board[c_y][c_x].has_piece()))

        else:
            return possibles

        # removes any blocked paths or ally spots
        for potential_spot in possibles.copy():
            potential_x, potential_y, has_piece = potential_spot

            # 1. checks for ally
            # 2. validates move, i.e. checks for blocked path. 
            # (must use is_valid_move instead of is_clear_path to prevent issues with linked list)
            if ((has_piece and self.__board[potential_y][potential_x].piece.is_white() == piece.is_white()) or
                (attack_only and not has_piece) or not self.__is_valid_move(x, y, potential_x, potential_y)):
                possibles.remove(potential_spot)

        # returns tuple containing (x coord:int, y coord:int, attack possible: boolean)
        return possibles

    def move_piece(self, *, from_x: int, from_y: int, to_x: int, to_y: int):
        self.__reset_move_vars()

        rook_attack = False
        from_spot = self.__board[from_y][from_x]
        to_spot = self.__board[to_y][to_x]

        # check for piece at spot

        # The spot is empty
        if not from_spot.has_piece():
            self.__move_message = "This is an empty spot. No piece to move!"
            print(self.__move_message)
            return False

        # Checks what team the piece is on
        if self.tracker.current_player != int(from_spot.piece.is_white()):
            self.__move_message = "This piece is not on your team!"
            print(self.__move_message)
            return False
        if from_x == to_x and from_y == to_y:
            return

        useOne = False
        if (abs(from_spot.x_loc - to_spot.x_loc) <= 1 and
                abs(from_spot.y_loc - to_spot.y_loc) <= 1 and
                (from_spot.piece.get_type() == 'Bishop' or from_spot.piece.get_type() == 'King') and
                not from_spot.piece.corp.commanderMoved()):
                    useOne = True

        # movement message
        self.__move_message = f"{from_spot.piece.get_name()} to ({str(to_x)}, {str(to_y)}): "

        if not self.__is_valid_move(from_x, from_y, to_x, to_y):
            self.__move_message += "Invalid move! "
            print(self.__move_message)
            return False
        else:
            # non empty spot
            if to_spot.piece:
                # ally spot
                if to_spot.piece.is_white() == from_spot.piece.is_white():
                    self.__move_message += "You can't attack your own team! "
                    print(self.__move_message)
                    return False
                # enemy spot
                else:
                    self.__move_message += "Attempting capture... "
                    if self.__is_attack_successful(from_spot.piece, to_spot.piece):
                        self.__move_message += "Success! Captured piece! "
                        if to_spot.piece.get_type() == 'King':
                            print('you win')
                            return
                        elif to_spot.piece.get_type() == 'Bishop':
                            if to_spot.piece.is_white():
                                to_spot.piece.corp.captured(self.corpW2)
                            else:
                                to_spot.piece.corp.captured(self.corpB2)
                        ##############################################################
                        elif from_spot.piece.get_type() == 'Rook':

                            rook_attack = True
                            to_spot.piece.corp.removeFromCorp(to_spot.piece)
                            to_spot.piece.set_killed()
                            piece_color = "white" if from_spot.piece.is_white else "black"
                            self.__captured_by[piece_color].append(to_spot.piece)



                        else:
                            to_spot.piece.corp.removeFromCorp(to_spot.piece)
                        to_spot.piece.set_killed()
                        piece_color = "white" if from_spot.piece.is_white else "black"
                        self.__captured_by[piece_color].append(to_spot.piece)
                    else:
                        self.__move_message += "Attack failed! Move unsuccessful! "
                        # we still technicly used an action so we must progress turnManager
                        from_spot.piece.set_moved()
                        temp = self.tracker.current_player
                        self.tracker.use_action()
                        if temp is not self.tracker.current_player:
                            self.resetTurn()
                        print(self.__move_message)
                        return False
            # empty spot
            else:
                self.__move_message += "Targeted spot is empty... "
            if useOne == True:
                print('using commander single space move')
                from_spot.piece.corp.movedOne()
            else:
                print('using command authority')
                from_spot.piece.set_moved()

            self.__move_message += "Moving to spot. "
            print(self.__move_message)

            temp = self.tracker.current_player
            self.tracker.use_action()
            if temp is not self.tracker.current_player:
                self.resetTurn()

            if rook_attack:
                to_spot.piece = None

            else:
                to_spot.piece = from_spot.piece
                from_spot.piece = None
                to_spot.piece.x_loc = to_x
                to_spot.piece.y_loc = to_y
        print("~~~~~")
        self.print_board()
        return True

    def __is_valid_move(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.__move_list = []

        piece = self.__board[from_y][from_x].piece
        # Checks to see if this piece's corp has already used its command authority
        if piece and piece.has_moved() and self.__board[to_y][to_x].piece is not None:
            print('This corp has already used its authority')
            return False

        if abs(from_x - to_x) <= 1 and abs(from_y - to_y) <= 1 and (
                piece.get_type() == 'Bishop' or piece.get_type() == 'King'):
            # print(from_spot.x_loc, from_spot.y_loc)
            if piece.corp.commanderMoved():
                if piece.has_moved():
                    print('has used all moves')
                    return False
                # print('using command authority')
        elif piece.has_moved() == True:
            print('This corp has already used its authority')
            return False

        # check for bounds
        if to_x > 7 or to_y > 7 or to_x < 0 or to_y < 0:
            self.__move_message += "You are outside the board! "
            return False
        piece_type = piece.get_type()
        if piece_type == 'Pawn':
            result = ((((to_y - from_y) == -1 and (to_x - from_x) == 0) or (
                    (to_y - from_y) == -1 and abs(to_x - from_x) == 1))
                      if piece.is_white() else
                      (((to_y - from_y) == 1 and (to_x - from_x) == 0) or (
                              (to_y - from_y) == 1 and abs(to_x - from_x) == 1)))
            if not result:
                self.__move_message += "Chosen move is too far away. "
            return result
        if piece_type == 'Bishop':
            if ((abs(to_x - from_x) == 2 or abs(to_y - from_y) == 2) and 
                not self.__is_clear_path(from_x, from_y, to_x, to_y)):
                self.__move_message += f"No clear path to ({str(to_x)}, {str(to_y)}). "
                return False
            else:
                result = ((abs(to_x - from_x) <= 2 and (to_y - from_y) == 0) or
                          (abs(to_y - from_y) <= 2 and (to_x - from_x) == 0) or
                          (abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1) or
                          (abs(to_x - from_x) == 2 and abs(to_y - from_y) == 2))
                if not result:
                    self.__move_message += "Chosen move is too far away."
                return result

        if piece_type in ('Rook', 'Knight', 'King', 'Queen'):
            if (abs(to_x - from_x) > self.__VALID_MOVE_DICT[piece_type] and
                    abs(to_y - from_y) > self.__VALID_MOVE_DICT[piece_type]):
                self.__move_message += "Chosen move is too far away. "
                return False
            elif not self.__is_clear_path(from_x, from_y, to_x, to_y):
                # allows for archer attack even when there is not a clear path to move to target
                if piece_type=='Rook' and (self.__board[to_y][to_x].has_piece() and self.__board[to_y][to_x].piece != piece.is_white()):
                    return True
                self.__move_message += f"No clear path to ({str(to_x)}, {str(to_y)}). "
                return False

        return True

    def __is_clear_path(self, from_x: int, from_y: int, to_x: int, to_y: int):
        current_piece = self.__board[from_y][from_x].piece
        target = self.__board[to_y][to_x]
        piece_type = current_piece.get_type()
        if piece_type == 'Bishop':
            x_diff, y_diff = to_x - from_x, to_y - from_y  # distance of move
            check_x, check_y = 0, 0  # distance of spot to be checked
            # horizontal movement
            if abs(x_diff) == 2:
                check_x = int(x_diff / 2)
            # vertical movement
            if abs(y_diff) == 2:
                check_y = int(y_diff / 2)
            return (not self.__board[from_y + check_y][from_x + check_x].has_piece())
        if piece_type in ('Rook', 'Knight', 'King', 'Queen'):
            if len(self.__move_list) == 0:
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

            # move len +1 i.e. 5 Kt, 4 Kg & Q, 3 R
            if len(self.__move_list) == self.__VALID_MOVE_DICT[piece_type] + 1:
                return False

            for item in x_steps:
                for item2 in y_steps:
                    if item2 == 0 and item == 0:
                        continue
                    if self.__board[target.y_loc + item2][target.x_loc + item].piece == current_piece:
                        return True
                    if not self.__board[target.y_loc + item2][target.x_loc + item].has_piece():
                        if self.__board[target.y_loc + item2][target.x_loc + item] in self.__move_list:
                            continue
                        self.__move_list.append(self.__board[target.y_loc + item2][target.x_loc + item])
                        if not self.__is_clear_path(from_x, from_y, self.__move_list[-1].x_loc,
                                                    self.__move_list[-1].y_loc):
                            self.__move_list.pop()
                            continue
                        else:
                            return True
            return False
        else:
            return False

    def __is_attack_successful(self, current_piece: Piece, target_piece: Piece):
        self.__last_dice_roll = random.randint(1, 6)

        self.__move_message += f"The roll on the dice is {self.__last_dice_roll}... "

        # format: capture_table_mins[attacking piece][defending piece] = min reqd for successful attack
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
        attack_piece_type = current_piece.get_type()
        defend_piece_type = target_piece.get_type()
        return self.__last_dice_roll >= capture_table_mins[attack_piece_type][defend_piece_type]

    def get_board(self):
        return [[(item2.piece.get_name() if item2.piece else "___") for item2 in item] for item in self.__board]

    def get_pieces_captured_by(self):
        return self.__captured_by

    def get_result_of_dice_roll(self):
        return self.__last_dice_roll

    def get_move_message(self):
        return self.__move_message

    def __reset_move_vars(self):
        # clear out prev var data
        self.__last_dice_roll = -1
        self.__move_message = ""

    def print_board(self):
        print()
        for item in self.__board:
            for item2 in item:
                if item2.piece:
                    print(item2.piece.get_name(), end=" ")
                else:
                    print("___", end=" ")
            print('\n')
        print("---------------------------------\n")
        
       
