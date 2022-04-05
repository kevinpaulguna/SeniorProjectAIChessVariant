import random
from ChessGameHelpers import Piece, Spot
from turnManager import MedievalTurnManager, CorpCommandTurnManager
from ThreeCorp import Corp

class Game:
    def __init__(self, game_type = "Corp"):
        self.__gameOver = False

        gametypes = ['Corp', 'Medieval']
        if game_type not in gametypes:
            raise ValueError("Invalid game type. Expected one of: ", gametypes)
        else:
            self.__is_corp_command_game = (game_type == "Corp")

        self.tracker = CorpCommandTurnManager() if self.__is_corp_command_game else MedievalTurnManager()

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
        self.__last_move_knight = None

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

        if self.__is_corp_command_game:
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

            self.tracker.set_corps(w1=self.corpW1, w2=self.corpW2, w3=self.corpW3,
                                b1=self.corpB1, b2=self.corpB2, b3=self.corpB3)

        self.__move_path = []

        # assign pieces to board
        for p in pieces:
            self.__board[p.y_loc][p.x_loc].set_piece(p)

    def get_possible_moves_for_piece_at(self, *, x: int, y: int, attack_only: bool = False, ai_backdoor: bool = False):
        # returns array of tuples containing co-ords of possible move spots
        if self.__gameOver:
            print('game over')
            return
        self.__reset_move_vars()
        possibles = []
        piece = self.__board[y][x].piece
        if not piece:
            return possibles
        piece_type = piece.get_type()

        if not ai_backdoor and (self.tracker.current_player != int(piece.is_white())):
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
            if piece_type == "Rook":
                limit+=1
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
        if self.__gameOver:
            print('game over')
            return False

        self.__reset_move_vars()

        rook_attack = False

        useOne = False
        from_spot = self.__board[from_y][from_x]
        to_spot = self.__board[to_y][to_x]

        if not (((to_x, to_y, True) in self.get_possible_moves_for_piece_at(x=from_x, y=from_y)) or
            ((to_x, to_y, False) in self.get_possible_moves_for_piece_at(x=from_x, y=from_y))):
            return False

        # check for piece at spot

        # The spot is empty
        if not from_spot.has_piece():
            self.__move_message = "This is an empty spot. No piece to move!"
            print(self.__move_message)
            return False

        # checks for same piece
        if from_x == to_x and from_y == to_y:
            return False

        # checks if last moved piece was the same knight, handles if not
        if self.__last_move_knight and self.__last_move_knight[0].get_name() != from_spot.piece.get_name():
            if self.__is_corp_command_game:
                self.tracker.use_action(piece_used=self.__last_move_knight[0], small_move=useOne)
            else:
                self.tracker.use_action(piece_used=self.__last_move_knight[0])
            self.__last_move_knight = None

        # Checks what team the piece is on
        if self.tracker.current_player != int(from_spot.piece.is_white()):
            self.__move_message = "This piece is not on your team!"
            print(self.__move_message)
            return False

        if self.__is_corp_command_game and (abs(from_spot.x_loc - to_spot.x_loc) <= 1 and
                abs(from_spot.y_loc - to_spot.y_loc) <= 1 and
                (from_spot.piece.get_type() == 'Bishop' or from_spot.piece.get_type() == 'King') and
                not to_spot.has_piece() and
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
                        piece_color = "white" if from_spot.piece.is_white() else "black"
                        self.__captured_by[piece_color].append(
                            (to_spot.piece.get_name(),
                             to_spot.piece.corp.get_name() if self.__is_corp_command_game else ""
                            )
                        )
                        self.__move_message += "Success! Captured piece! "
                        if to_spot.piece.get_type() == 'King':
                            self.__move_message += "You Win! "
                            self.__gameOver = True
                            #return True
                        elif self.__is_corp_command_game and to_spot.piece.get_type() == 'Bishop':
                            if to_spot.piece.is_white():
                                to_spot.piece.corp.captured(self.corpW2)
                            else:
                                to_spot.piece.corp.captured(self.corpB2)
                        elif self.__is_corp_command_game:
                            to_spot.piece.corp.removeFromCorp(to_spot.piece)

                        rook_attack = (from_spot.piece.get_type() == 'Rook')

                        to_spot.piece.set_killed()
                    else:
                        self.__move_message += "Attack failed! Move unsuccessful! "
                        # we still technicly used an action so we must progress turnManager
                        if self.__is_corp_command_game:
                            self.tracker.use_action(piece_used=from_spot.piece, small_move=useOne)
                        else:
                            self.tracker.use_action(piece_used=from_spot.piece)
                        print(self.__move_message)
                        self.__last_move_knight = None
                        return False
            # empty spot
            else:
                self.__move_message += "Targeted spot is empty... "

            # doesn't count move for knight if not attacking
            if self.__last_dice_roll==-1 and from_spot.piece.get_type() == 'Knight':
                self.__last_move_knight = (from_spot.piece, self.tracker.get_turn_count())
                print('using command authority')
            else:
                self.__last_move_knight = None

                if self.__is_corp_command_game:
                    self.tracker.use_action(piece_used=from_spot.piece, small_move=useOne)
                else:
                    self.tracker.use_action(piece_used=from_spot.piece)

            if rook_attack:
                 to_spot.piece = None
            else:
                if not self.__gameOver: self.__move_message += "Moving to spot. "
                print(self.__move_message)

                to_spot.piece = from_spot.piece
                from_spot.piece = None
                to_spot.piece.x_loc = to_x
                to_spot.piece.y_loc = to_y

                temp = self.__move_path
                if self.__last_move_knight and len(self.get_possible_moves_for_piece_at(x=to_x, y=to_y))==0:
                    if self.__is_corp_command_game:
                        self.tracker.use_action(piece_used=self.__last_move_knight[0], small_move=useOne)
                    else:
                        self.tracker.use_action(piece_used=self.__last_move_knight[0])
                    self.__last_move_knight = None
                self.__move_path = temp
        print('Path:', self.__move_path)
        print("~~~~~")
        self.print_board()
        return True

    def __is_valid_move(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.__move_list = []

        piece = self.__board[from_y][from_x].piece

        if self.__last_move_knight and self.__last_move_knight[1] != self.tracker.get_turn_count():
            self.__last_move_knight = None

        if piece.get_name() in self.tracker._get_pieces_used():
            return False

        # Checks to see if this piece's corp has already used its command authority
        if self.__is_corp_command_game and piece and piece.has_moved() and self.__board[to_y][to_x].has_piece():
            print('This corp has already used its authority')
            return False

        if self.__is_corp_command_game:
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


        if self.__last_move_knight:
            # valid moves for knight attacking after move
            if self.__last_move_knight[0].get_name() == piece.get_name():
                if ((abs(to_x-from_x)==1 and abs(to_y-from_y)==1 or
                        abs(to_x-from_x)==0 and abs(to_y-from_y)==1 or
                        abs(to_x-from_x)==1 and abs(to_y-from_y)==0) and
                        self.__board[to_y][to_x].has_piece()):
                        self.__move_path = [(to_x, to_y)]
                        return True
                else: return False
            if self.__last_move_knight[0].corp == piece.corp:
                return False

        if piece_type == 'Pawn':
            in_range = (
                        (((to_y - from_y) == -1 and (to_x - from_x) == 0) or
                        ((to_y - from_y) == -1 and abs(to_x - from_x) == 1))
                        if piece.is_white() else
                        (((to_y - from_y) == 1 and (to_x - from_x) == 0) or
                        ((to_y - from_y) == 1 and abs(to_x - from_x) == 1))
                    )
            if in_range:
                self.__move_path = [(to_x, to_y)]
            else:
                self.__move_message += "Chosen move is too far away. "
            return in_range
        if piece_type == 'Bishop':
            if (abs(to_x - from_x) > 1 or abs(to_y - from_y) > 1) and self.__board[to_y][to_x].piece is not None:
                return False
            if ((abs(to_x - from_x) == 2 or abs(to_y - from_y) == 2) and
                not self.__is_clear_path(from_x, from_y, to_x, to_y)):
                self.__move_message += f"No clear path to ({str(to_x)}, {str(to_y)}). "
                return False
            else:
                in_range = ((abs(to_x - from_x) <= 2 and (to_y - from_y) == 0) or
                          (abs(to_y - from_y) <= 2 and (to_x - from_x) == 0) or
                          (abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1) or
                          (abs(to_x - from_x) == 2 and abs(to_y - from_y) == 2))
                if in_range:
                    self.__move_path = []
                    x_diff, y_diff = to_x - from_x, to_y - from_y  # distance of move
                    check_x, check_y = 0, 0  # distance of spot to be checked
                    # horizontal movement
                    if abs(x_diff) == 2:
                        check_x = int(x_diff / 2)
                    # vertical movement
                    if abs(y_diff) == 2:
                        check_y = int(y_diff / 2)
                    if (middle := (from_x+check_x, from_y+check_y)) != (from_x, from_y):
                        self.__move_path.append(middle)
                    self.__move_path.append((to_x, to_y))
                else:
                    self.__move_message += "Chosen move is too far away."
                return in_range

        if piece_type in ('Rook', 'Knight', 'King', 'Queen'):
            if self.__is_rook_attack(from_x, from_y, to_x, to_y):
                return True
            if (abs(to_x - from_x) > 1 or abs(to_y - from_y) > 1) and self.__board[to_y][to_x].piece is not None:
                return False
            else:
                if (abs(to_x - from_x) > self.__VALID_MOVE_DICT[piece_type] and
                        abs(to_y - from_y) > self.__VALID_MOVE_DICT[piece_type]):
                    self.__move_message += "Chosen move is too far away. "
                    return False
                elif not self.__is_clear_path(from_x, from_y, to_x, to_y):
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
                        self.__move_path = [(spot.x_loc, spot.y_loc) for spot in reversed(self.__move_list)]
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
                            self.__move_path = [(spot.x_loc, spot.y_loc) for spot in reversed(self.__move_list)]
                            return True
            return False
        else:
            return False

    def __is_rook_attack(self, from_x:int, from_y:int, to_x:int, to_y:int)->bool:
        self.__move_path = []
        return (self.__board[from_y][from_x].piece.get_type() == 'Rook' and
            self.is_enemy(to_x, to_y) and
            (
                abs(to_x - from_x) <= self.__VALID_MOVE_DICT["Rook"]+1 and
                abs(to_y - from_y) <= self.__VALID_MOVE_DICT["Rook"]+1
            )
            )

    def __is_attack_successful(self, current_piece: Piece, target_piece: Piece):
        self.__last_dice_roll = random.randint(1, 6)
        # add +1 if knight is attackiing after a move
        if (self.__last_move_knight and self.__last_move_knight[0].get_name() == current_piece.get_name()
            and self.__last_dice_roll<6):
            self.__last_dice_roll += 1

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

    def __reset_move_vars(self):
        # clear out prev var data
        self.__last_dice_roll = -1
        self.__move_message = ""
        self.__move_path = []

    def delegate_or_recall(self, *, piece: str, from_corp: str, to_corp: str):
        if self.__is_corp_command_game and not self.tracker.delegation_move_has_been_used():
            # locates piece and corps based on string names and calls the request_piece func from Corp
            # returns false if failed to find corp or piece, returns true if found and delegation happens
            corps = [self.corpW1, self.corpW2, self.corpW3, self.corpB1, self.corpB2, self.corpB3]

            from_c = None
            to_c = None
            pc = None
            for c in corps:
                if c.get_name()==from_corp:
                    from_c = c
                if c.get_name()==to_corp:
                    to_c = c
                if from_c and to_c:
                    break

            if not from_c or not to_c:
                return False

            for p in from_c.commanding:
                if p.get_name()==piece:
                    pc = p

            if not p:
                return False

            if not to_c.checkLeng():
                print("corp exceeds max length")
                return False

            to_c.request_piece(pc)
            self.tracker.use_delegation_move()
            return True
        else:
            return False

    def get_pieces_captured_by(self, color:str):
        if color in ("white", "black"):
            return self.__captured_by[color]
        else: return

    def get_corp_info(self, *, white:bool):
        if self.__is_corp_command_game:
            if white:
                return {
                    1: {
                        'name': self.corpW1.get_name(),
                        'commander': self.corpW1.commander.get_name() if self.corpW1.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpW1.commanding]
                    },
                    2: {
                        'name': self.corpW2.get_name(),
                        'commander': self.corpW2.commander.get_name() if self.corpW2.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpW2.commanding]
                    },
                    3: {
                        'name': self.corpW3.get_name(),
                        'commander': self.corpW3.commander.get_name() if self.corpW3.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpW3.commanding]
                    },
                }
            else:
                return {
                    1: {
                        'name': self.corpB1.get_name(),
                        'commander': self.corpB1.commander.get_name() if self.corpB1.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpB1.commanding]
                    },
                    2: {
                        'name': self.corpB2.get_name(),
                        'commander': self.corpB2.commander.get_name() if self.corpB2.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpB2.commanding]
                    },
                    3: {
                        'name': self.corpB3.get_name(),
                        'commander': self.corpB3.commander.get_name() if self.corpB3.commander else "",
                        'commanding': [piece.get_name() for piece in self.corpB3.commanding]
                    },
                }

    def get_result_of_dice_roll(self):
        return self.__last_dice_roll

    def get_move_message(self):
        return self.__move_message

    def get_move_path(self):
        return self.__move_path

    def get_board(self):
        # returns 2d list of tuples (piece name, corp of piece)
        return [[(
            (spot.piece.get_name(), (spot.piece.corp.get_name() if self.__is_corp_command_game else 0))
            if spot.has_piece() else ("___", None)) for spot in row]
            for row in self.__board]

    def is_enemy(self, x_pos, y_pos) -> bool:
        piece = self.__board[y_pos][x_pos].piece
        return piece and piece.is_white() != bool(self.tracker.current_player)

    def _get_board(self):
        return self.__board

    def is_game_over(self):
        return self.__gameOver

    def print_board(self):
        print()
        for row in self.__board:
            for spot in row:
                if spot.has_piece():
                    print(spot.piece.get_name(), end=" ")
                else:
                    print("___", end=" ")
            print('\n')
        print("---------------------------------\n")
