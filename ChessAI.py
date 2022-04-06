import random

from ChessGame import Game


# game = Game()

class AIFunctions:
    def __init__(self, game: Game, color):
        self.game = game
        self.color = color
        self.board = self.game._get_board()
        self.total_success_moves = 0
        self.total_moves_attempted = 0
        self.last_turn = 0
        self.kingmod = 1
        self.hostilemap = \
            [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

        self.kingOrderGrid = \
            [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    def updateBoard(self):
        self.board = self.game._get_board()

    def __get_position_of_piece(self, piece_name: str):
        if len(piece_name) == 0 or piece_name[0] not in ('w', 'b'):
            print('empty or not w or not b')
            return (-1, -1)

        some_pieces = {
            'Kt': ["1", "2"],
            'R': ["1", "2"],
            'B': ["1", "2"],
            'P': ["1", "2", "3", "4", "5", "6", "7", "8"]
        }

        if "Kg" in piece_name or "Q" in piece_name:
            if len(piece_name) != 3:
                print('invalid royalty piece name')
                return (-1, -1)
        elif not (piece_name[1:-1] in some_pieces and piece_name[-1] in some_pieces[piece_name[1:-1]]):
            print('invalid non royalty piece name')
            return (-1, -1)

        for y, row in enumerate(self.game.get_board()):
            for x, spot in enumerate(row):
                pc, corp = spot
                if pc == piece_name:
                    return (x, y)
        print('piece not on board')
        return (-1, -1)

    #feed x,y of moved king corp piece for orders
    def kingOrders(self, x, y):
        self.resetKingOrders()

        #determine piece advantage
        white = 0
        black = 0

        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if item2.piece.is_white():
                        white = white+1
                    else:
                        black = black+1

        korder = True
        if(white > black and self.color == True or black > white and self.color == False):
            korder = False

        #if the AI does not have piece advantage, make more defensive moves
        if(korder):
            list = self.game.get_possible_moves_for_piece_at(x = y, y = x, ai_backdoor=True)
            for l,m,p in list:
                #sets spot values near the moved king piece to be higher, therefore more defensive
                if(l-x == 1 or x-l == 1 and m-y == 1 or y-m == 1):
                    self.kingOrderGrid[m][l] = 2
        #else the AI has piece advantage, make more aggressive moves
        else:
            #applies to the hostilemap, reducing the impact of dangerous spots,
            #therefore permitting more aggressive movement
            self.kingmod = .2
            self.genHostileMap()

    def resetKingOrders(self):
        self.kingmod = 1
        self.kingOrderGrid = \
            [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

    # weights attack areas based on friendly piece power
    def attackRef(self, x, y, piece):
        a = 0
        b = 0
        defpiece = None
        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if a == x and b == y:
                        defpiece = item2.piece
                a = a + 1
            b = b + 1
            a = 0

        # TODO: case needs to be handled where defpiece isn't assigned or determine why it isn't
        if defpiece:
            type = defpiece.get_type()
        else:
            return 0

        if piece.get_type() == 'Pawn':
            if type == 'Pawn':
                return 3
            elif type == 'Bishop':
                return 2
            else:
                return 1
        elif piece.get_type() == 'Rook':
            if type == 'Pawn' or type == 'Bishop' or type == 'Rook':
                return 2
            else:
                return 3
        elif piece.get_type() == 'Bishop':
            if type == 'Pawn':
                return 4
            if type == 'Bishop':
                return 3
            else:
                return 2
        elif piece.get_type() == 'Knight':
            if type == 'Pawn':
                return 5
            else:
                return 2
        elif piece.get_type() == 'Queen':
            if type == 'Rook':
                return 2
            if type == 'Pawn':
                return 5
            else:
                return 3
        elif piece.get_type() == 'King':
            if type == 'Rook':
                return 2
            if type == 'Pawn':
                return 6
            else:
                return 3

    def genHostileMap(self):
        x = 0
        y = 0
        self.hostilemap = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if self.color != item2.piece.is_white():
                        moveList = self.game.get_possible_moves_for_piece_at(x=y, y=x, ai_backdoor=True)

                        if (item2.piece.get_type() == 'Pawn'):
                            spotVal = .2
                        elif (item2.piece.get_type() == 'Bishop' or item2.piece.get_type() == 'King'):
                            spotVal = .3
                        else:
                            spotVal = .4
                        for a, b, c in moveList:
                            self.hostilemap[b][a] += spotVal * self.kingmod
                y = y + 1
            x = x + 1
            y = 0

    # returns piece object and its potential movement areas
    def moveMap(self):
        self.updateBoard()
        self.genHostileMap()
        kCore = []
        xCore = []
        yCore = []

        heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

        x = 0
        y = 0

        player = "white" if self.game.tracker.get_current_player() else "black"

        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if self.color == item2.piece.is_white():
                        moveList = self.game.get_possible_moves_for_piece_at(x=y, y=x)

                        if (item2.piece.get_type() == 'Pawn'):
                            spotVal = 2
                        elif (item2.piece.get_type() == 'Bishop' or item2.piece.get_type() == 'King'):
                            # originally 2, changed to 1 as weights for movement effect choices
                            spotVal = 1
                        else:
                            spotVal = 4
                        for l, m, p in moveList:
                            if (p):
                                heatmap[m][l] += self.attackRef(x, y, item2.piece)

                            # weighting longer moves higher
                            if (m - x == 2 or x - m == 2 or y - l == 2 or l - y == 2):
                                heatmap[m][l] += 1
                                if player == "white":
                                    if (m - x == 2 or x - m == 2 or y - l == 2):
                                        heatmap[m][l] += 1
                                if player == "black":
                                    if (m - x == 2 or x - m == 2 or l - y == 2):
                                        heatmap[m][l] += 1
                            elif (m - x == 3 or x - m == 3 or y - l == 3 or l - y == 3):
                                heatmap[m][l] += 2
                                if player == "white":
                                    if (m - x == 3 or x - m == 3 or y - l == 3):
                                        heatmap[m][l] += 1
                                if player == "black":
                                    if (m - x == 3 or x - m == 3 or l - y == 3):
                                        heatmap[m][l] += 1
                            elif (m - x == 4 or x - m == 4 or y - l == 4 or l - y == 4):
                                heatmap[m][l] += 2
                                if player == "white":
                                    if (m - x == 4 or x - m == 4 or y - l == 4):
                                        heatmap[m][l] += 1
                                if player == "black":
                                    if (m - x == 2 or x - m == 2 or l - y == 2):
                                        heatmap[m][l] += 1
                            elif (m - x == 5 or x - m == 5 or y - l == 5 or l - y == 5):
                                heatmap[m][l] += 3
                                if player == "white":
                                    if (m - x == 5 or x - m == 5 or y - l == 5):
                                        heatmap[m][l] += 1
                                if player == "black":
                                    if (m - x == 5 or x - m == 5 or l - y == 5):
                                        heatmap[m][l] += 1
                            heatmap[m][l] += spotVal - self.hostilemap[m][l] + self.kingOrderGrid[m][l]

                        dataChunk = [item2.piece, heatmap]
                        if (item2.piece.get_corp() == 'corpW1' or item2.piece.get_corp() == 'corpB1'):
                            kCore.append(dataChunk)
                        elif (item2.piece.get_corp() == 'corpW2' or item2.piece.get_corp() == 'corpB2'):
                            xCore.append(dataChunk)
                        else:
                            yCore.append(dataChunk)

                        heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]]



                y = y + 1
            x = x + 1
            y = 0
            print('\n')
        #self.corpSplitData(moveData)
        return kCore, xCore, yCore

    def displayMoveData(self, moveData):

        for element, array in moveData:
            print(element.get_name())
            for row in array:
                print(row)

    def best_move(self, moveData):
        max_weight = None
        BKingLocation = self.__get_position_of_piece('bKg')
        WKingLocation = self.__get_position_of_piece('wKg')
        BestSameScore = []
        # print('start check')
        for element, array in moveData:
            SameScore = []
            max_weight_piece = None

            self.__get_position_of_piece('bKg')
            self.__get_position_of_piece('wKg')

            for y, row in enumerate(array):
                if max(row) > 0:
                    for x, weight in enumerate(row):
                        if weight != 0:
                            if ((x == WKingLocation[0] and y == WKingLocation[1])
                                    or (x == BKingLocation[0] and y == BKingLocation[1])):
                                print("Testing1========================================")
                                max_weight_piece = (x, y, weight + 20, element.get_name(), element.x_loc, element.y_loc)
                                SameScore = [max_weight_piece]
                            if not max_weight_piece:
                                if ((x == WKingLocation[0] and y == WKingLocation[1])
                                        or (x == BKingLocation[0] and y == BKingLocation[1])):
                                    max_weight_piece = (
                                    x, y, weight + 20, element.get_name(), element.x_loc, element.y_loc)
                                    SameScore = [max_weight_piece]
                                    print("Testing2========================================")
                                else:
                                    max_weight_piece = (x, y, weight, element.get_name(), element.x_loc, element.y_loc)
                                    SameScore = [max_weight_piece]
                                # sets up a max weight if there is not one already set
                                # max_weight_piece = (x, y, weight, element.get_name() , element.x_loc, element.y_loc)
                                # SameScore = [max_weight_piece]
                            else:
                                if weight > max_weight_piece[2]:
                                    if ((x == WKingLocation[0] and y == WKingLocation[1])
                                            or (x == BKingLocation[0] and y == BKingLocation[1])):
                                        max_weight_piece = (
                                        x, y, weight, element.get_name(), element.x_loc, element.y_loc)
                                        SameScore = [max_weight_piece]
                                        print("Testing3========================================")
                                    else:
                                        max_weight_piece = (
                                        x, y, weight, element.get_name(), element.x_loc, element.y_loc)
                                        SameScore = [max_weight_piece]

                                    # max_weight_piece = (x, y, weight, element.get_name() , element.x_loc, element.y_loc)
                                    # SameScore = [max_weight_piece]

                                elif weight == max_weight_piece[2]:
                                    SameScore.append((x, y, weight, element.get_name(), element.x_loc, element.y_loc))

            # # to check max weight piece after every from piece is checked
            # if max_weight_piece:
            #     print('max pc', max_weight_piece)

            if len(SameScore) > 0:
                # Shuffles the SameScore Array twice to pull a random move
                random.shuffle(SameScore)
                max_weight_piece = SameScore[0]

                if not max_weight:
                    max_weight = max_weight_piece[2]
                elif max_weight < max_weight_piece[2]:
                    BestSameScore = []
                    max_weight = max_weight_piece[2]

                if max_weight == max_weight_piece[2]:
                    BestSameScore.append(max_weight_piece)

        if len(BestSameScore) == 0:
            self.game.tracker.end_turn()
            BestMove = (element.x_loc, element.x_loc, 0, element.get_name(), element.x_loc, element.y_loc)
        else:
            random.shuffle(BestSameScore)
            BestMove = BestSameScore[0]

        # print('end check, result', BestMove)

        print("Best Move after everything: ", BestMove, "\n\n")

        return BestMove

    def AI_move(self, BestMove):

        # self.displayMoveData(moveData)
        # self.best_move(moveData)
        print(BestMove)
        print("Moving ", BestMove[3], " from x: ", BestMove[4], " y: ", BestMove[5], "Moving to x: ", BestMove[0],
              " y: ", BestMove[1])

        if self.game.move_piece(from_x=BestMove[4], from_y=BestMove[5], to_x=BestMove[0], to_y=BestMove[1]):
            self.total_success_moves += 1
        self.total_moves_attempted += 1
        # self.displayMoveData(moveData)

    def make_move(self):
        if not self.game.game_status():
            if self.last_turn != self.game.tracker.get_turn_count():
                self.total_success_moves = 0
                self.total_moves_attempted = 0
            print("starting new move:")
            player = "white" if self.game.tracker.get_current_player() else "black"
            print('current player:', player)
            x = self.moveMap()
            y = self.best_move(x)
            self.AI_move(y)
            self.last_turn = self.game.tracker.get_turn_count()
            colour = "white" if self.color else "black"
            print(colour, "team had", self.total_success_moves, 'successful moves out of', self.total_moves_attempted,
                  'this turn')

# aiAssistWhite = AIFunctions(game, True)
# aiAssistBlack = AIFunctions(game, False)


# for num in range (100):
#    if not game.game_status():
#        if game.tracker.get_current_player():
#            aiAssistWhite.make_move()
#        else:
#            aiAssistBlack.make_move()
#    else:
#        print("Game Over!")
#        break
