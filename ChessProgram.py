import random


class Spot:
    x_loc = None
    y_loc = None
    piece = None
    value = 0

    def __init__(self, x, y, piece):
        self.x_loc = x
        self.y_loc = y
        self.piece = piece

    def set_spot(self, x, y, piece):
        self.x_loc = x
        self.y_loc = y
        self.piece = piece

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_piece(self, piece):
        self.piece = piece


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
    hasAttacked = 0

    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

    def move(self, target):
        if self.hasAttacked == 1:
            print("This piece has already attacked you can no longer make actions with this piece")
            return
        # eventually bP1 will be changed to an actual piece name or something of the sort
        # if the pawn is white you would just increase by 1
        if self.name == 'bP1':
            print("Available moves are \n",
                  self.x_loc, self.y_loc - 1, "\n",
                  self.x_loc + 1, self.y_loc - 1, "\n",
                  self.x_loc - 1, self.y_loc - 1, "\n")
        if self.name == 'wP1':
            print("Available moves are \n",
                  self.x_loc, self.y_loc + 1, "\n",
                  self.x_loc + 1, self.y_loc + 1, "\n",
                  self.x_loc - 1, self.y_loc + 1, "\n")
        if abs(target.x_loc - self.x_loc) > 1:
            print("can't target too far sideways")
            return
        elif self.y_loc - target.y_loc != 1:
            print("can't target not in next row")
            return
        elif target.piece == None:
            print("moving")
            target.piece = self
            board[self.y_loc][self.x_loc].piece = None
            self.x_loc = target.x_loc
            self.y_loc = target.y_loc
            self.hasMoved = 1
            return
        elif target.piece.is_white == self.is_white:
            print("cant target contains ally piece")
            return
        elif target.piece.is_white != self.is_white:
            Dice = random.randint(1, 6)
            print("The roll on the dice is", Dice)
            # for this part you would check the piece type, such as pawn, king, queen,
            # and what not to know how much you would have to roll
            if Dice > 3:
                print("capturing piece at target")
                target.piece.set_killed()
                target.piece = self
                board[self.y_loc][self.x_loc].piece = None
                self.x_loc = target.x_loc
                self.y_loc = target.y_loc
                self.hasMoved = 1
                self.hasAttacked = 1
                return
            else:
                print("The odds were not in your favor, you will retain the position you were at")
                self.hasAttacked = 1
                return
        else:
            print("something went wrong")
            return


# Function to print the current board state
def print_Board(board):
    for item in board:
        for item2 in item:
            if item2.piece:
                print(item2.piece.name, end=" ")
            else:
                print(item2.piece, end=" ")
        print('\n')


# Function to move the piece in one spot tho another target spot
def movePiece(Spot1, Spot2):
    target = Spot2
    current = Spot1
    if current.piece == None:
        print("no piece to move")
        return
    current.piece.move(target)


# Creation of the board
board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

# for loop fills the board with spot objects
value = 0
for item in range(0, 8):
    for item2 in range(0, 8):
        value += 1
        s = Spot(item2, item, None)
        s.set_value(value)
        board[item][item2] = s

# Creation of the piece objects
#
# White
#
#
# creating white pawns
wP1 = Pawn(0, 1, 'wP1', white=True)
wP2 = Pawn(1, 1, 'wP2', white=True)
wP3 = Pawn(2, 1, 'wP3', white=True)
wP4 = Pawn(3, 1, 'wP4', white=True)
wP5 = Pawn(4, 1, 'wP5', white=True)
wP6 = Pawn(5, 1, 'wP6', white=True)
wP7 = Pawn(6, 1, 'wP7', white=True)
wP8 = Pawn(7, 1, 'wP8', white=True)

# setting the pawn location on the board
board[wP1.y_loc][wP1.x_loc].set_piece(wP1)
board[wP2.y_loc][wP2.x_loc].set_piece(wP2)
board[wP3.y_loc][wP3.x_loc].set_piece(wP3)
board[wP4.y_loc][wP4.x_loc].set_piece(wP4)
board[wP5.y_loc][wP5.x_loc].set_piece(wP5)
board[wP6.y_loc][wP6.x_loc].set_piece(wP6)
board[wP7.y_loc][wP7.x_loc].set_piece(wP7)
board[wP8.y_loc][wP8.x_loc].set_piece(wP8)

#
# Black
#
# Creating black pawns
bP1 = Pawn(0, 6, 'bP1', white=False)
bP2 = Pawn(1, 6, 'bP2', white=False)
bP3 = Pawn(2, 6, 'bP3', white=False)
bP4 = Pawn(3, 6, 'bP4', white=False)
bP5 = Pawn(4, 6, 'bP5', white=False)
bP6 = Pawn(5, 6, 'bP6', white=False)
bP7 = Pawn(6, 6, 'bP7', white=False)
bP8 = Pawn(7, 6, 'bP8', white=False)

# setting the pawn location on the board
board[bP1.y_loc][bP1.x_loc].set_piece(bP1)
board[bP2.y_loc][bP2.x_loc].set_piece(bP2)
board[bP3.y_loc][bP3.x_loc].set_piece(bP3)
board[bP4.y_loc][bP4.x_loc].set_piece(bP4)
board[bP5.y_loc][bP5.x_loc].set_piece(bP5)
board[bP6.y_loc][bP6.x_loc].set_piece(bP6)
board[bP7.y_loc][bP7.x_loc].set_piece(bP7)
board[bP8.y_loc][bP8.x_loc].set_piece(bP8)

# print_Board(board)
movePiece(board[6][0], board[5][0])
movePiece(board[5][0], board[4][0])
movePiece(board[4][0], board[3][0])
movePiece(board[3][0], board[2][0])
movePiece(board[2][0], board[1][0])
movePiece(board[2][0], board[1][0])

# print_Board(board)
