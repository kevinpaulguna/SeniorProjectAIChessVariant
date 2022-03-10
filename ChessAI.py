import copy
import random

from ChessGame import Game

BestMove = []



game = Game()


# game.move_piece(from_x=0, from_y=6, to_x=1, to_y=5)


# game.print_board()

# print(game.get_possible_moves_for_piece_at(x=3,y=6))


# demo()

# ------------------

# game.print_board()

# g=game.get_board()
# for line in g:
#     print(line)

# ------------------

class AIFunctions:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.board = game.get__board()

    def updateBoard(self, board):
        self.board = game.get__board()

    def testCopy(self):
        gamecopy = copy.deepcopy(self.game)
        self.game.move_piece(from_x=0, from_y=6, to_x=1, to_y=5)
        self.game.print_board()
        gamecopy.print_board()

        gamecopy.move_piece(from_x=1, from_y=6, to_x=0, to_y=5)
        self.game.print_board()
        gamecopy.print_board()

    # weights attack areas based on friendly piece power
    def attackRef(self, x, y, piece):
        a = 0
        b = 0
        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if a == x and b == y:
                        defpiece = item2.piece
                a = a + 1
            b = b + 1
            a = 0
        type = defpiece.get_type()

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
            elif type == 'Bishop':
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
            elif type == 'Pawn':
                return 5
            else:
                return 3
        else:
            if type == 'Rook':
                return 2
            elif type == 'Pawn':
                return 6
            else:
                return 3

    # returns piece object and its potential movement areas
    def moveMap(self):
        moveData = []
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

        for item in self.board:
            for item2 in item:
                if item2.piece:
                    if self.color == item2.piece.is_white():
                        moveList = game.get_possible_moves_for_piece_at(x=y, y=x)

                        if (item2.piece.get_type() == 'Pawn'):
                            spotVal = 1
                        elif (item2.piece.get_type() == 'Bishop' or item2.piece.get_type() == 'King'):
                            spotVal = 2
                        else:
                            spotVal = 4
                        for l, m, p in moveList:
                            if (p):
                                heatmap[m][l] += self.attackRef(self, x, y, item2.piece)
                            heatmap[m][l] += spotVal
                        dataChunk = [item2.piece, heatmap]

                        #
                        heatmap = [[0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0]]

                        moveData.append(dataChunk)
                y = y + 1
            x = x + 1
            y = 0
            print('\n')

        self.displayMoveData(moveData)

        self.AI_move(moveData)
        return moveData

    def displayMoveData(self, moveData):

        for element, array in moveData:
            print(element.get_name())
            for row in array:
                print(row)

            # print(SameScore)
            # for id2 in array:
            # print(id2)

    def best_move(self, moveData):

        global BestMove
        # BestPieceName = []
        max_weight = None
        BestSameScore = []

        for element, array in moveData:

            SameScore = []
            moves = []
            max_weight_piece = None
            equal_weight = False
            for y, row in enumerate(array):
                for x, weight in enumerate(row):
                    if weight != 0:
                        if not max_weight:
                            # sets up a max weight if there is not one already set
                            max_weight = (x, y, weight)
                            # print(element.get_name())
                            # BestPieceName = element.get_name()
                            # print("Original Max Weight: ", max_weight)
                            SameScore.append((x, y, weight, element.get_name(), element.x_loc, element.y_loc))
                            moves = [(x, y, weight)]

                        else:
                            if weight > max_weight[2]:
                                max_weight_piece = (x, y, weight)
                                BestSameScore = (x, y, weight, element.get_name(), element.x_loc, element.y_loc)
                                # BestPieceName.append(element.get_name())
                                # The next two lines reset the move list and same score
                                # list if a higher max_weight is found
                                moves = [(x, y, weight)]
                                SameScore = [(x, y, weight, element.get_name(), element.x_loc, element.y_loc)]
                                BestMove = max_weight_piece
                                # print("Max Weight if Changed to a higher weight: ", max_weight)
                            elif weight == max_weight[2]:
                                equal_weight = True
                                # Next 2 lines add to the corresponding information to the array
                                moves.append((x, y, weight))
                                SameScore.append((x, y, weight, element.get_name(), element.x_loc, element.y_loc))
                                # print("Same Score Testing: ", SameScore)
                                # Randomly Shuffles the SameScore Array twice to pull a random move
                                random.shuffle(SameScore)
                                # print("Before Max Weight is changed", max_weight)
                                # This changes the max weight after everything has been shuffled to make
                                # sure that the moves is random and not always going to choose the most left
                                # hand sided move
                                max_weight = SameScore[0]
            if equal_weight == True:
                BestSameScore.append(SameScore[0])
                # just shuffle based off the length of the array giving it an index to choose from
                random.shuffle(BestSameScore)
                BestMove = BestSameScore[0]

        # Checklist
        # Done getting weights for all moves
        # Able to get all the different moves if multiple pieces have the same weight for movement

        # Have to implement movement

        # Make sure that the Black side is working on the HeatMap information

        # print("Shuffled Same Score: ", SameScore)
        # print("Prints All available moves: ", moves)
        # print("Testing Piece Name:============================================")
        # print(BestPieceName)
        # print("Prints Final Max Weight After being shuffled: ", max_weight)
        # print("Prints All best of the same weights" , BestSameScore)
        # print("Best Move section: ", BestMove[3])
        print("Best Move after everything: ", BestMove, "\n\n")

        return BestMove

    def AI_move(self, moveData):

        self.best_move(moveData)

        print("Moving to x: ", BestMove[0], " y: ", BestMove[1])
        print("Moving from x: ", BestMove[4], " y: ", BestMove[5])

        game.move_piece(from_x=BestMove[4], from_y=BestMove[5], to_x=BestMove[0], to_y=BestMove[1])

        self.best_move(moveData)

        print("Moving to x: ", BestMove[0], " y: ", BestMove[1])
        print("Moving from x: ", BestMove[4], " y: ", BestMove[5])

        game.move_piece(from_x=BestMove[4], from_y=BestMove[5], to_x=BestMove[0], to_y=BestMove[1])

        self.best_move(moveData)

        print("Moving to x: ", BestMove[0], " y: ", BestMove[1])
        print("Moving from x: ", BestMove[4], " y: ", BestMove[5])

        game.move_piece(from_x=BestMove[4], from_y=BestMove[5], to_x=BestMove[0], to_y=BestMove[1])



    # def for reading the heatmap and choose the highest weighted score
    # convolutions or decision tree

    # another if statement if weights are the same randomize and pick
    # if statement making sure that the pieces dont go back and forth in the same spots,"looping"

    # def if being attacked move piece or sacrifice

    # def if King is being attacked move the king or run the risk if the chances are low

    # def if Enemy King is being attack calculate if that weight is worth to run the chance of attack


aiAssist = AIFunctions(game, True)
# aiAssist2 = AIFunctions(game, False)
aiAssist.moveMap()

# aiAssist2.moveMap()

# aiAssist.testCopy()
