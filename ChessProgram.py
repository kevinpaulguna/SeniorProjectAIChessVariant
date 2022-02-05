import random

#this node class is used for linked lists when looking at piecec movement
#it contains a single spot
class Node:
    def __init__(self, spot):
        self.spot = spot
        self.next = None
        self.previous = None

        
#this is the class for the linked list
class LinkedList:
    head = None

    def __init__(self):
        self.head = None
    
    #prints the x and y locations of the spots(nodes) of the list
    def print_list(self):
        printval = self.head
        while printval != None:
            print(printval.spot.x_loc, printval.spot.y_loc)
            printval = printval.next

    #adds a new node to the list based on the spot passed through
    def add_node(self, nextspot):
        newNode = Node(nextspot)
        if self.head is None:
            self.head = newNode
            return
        end = self.head
        while (end.next):
            end = end.next
        end.next = newNode
        end.next.previous = end
    
    #returns the last spot(node) in the list
    def get_last_spot(self):
        end = self.head
        while end.next != None:
            end = end.next
        return end.spot

    #removes the last node from the list
    def pop_node(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head.next = None
            return
        end = self.head
        while(end.next.next):
            end = end.next
        end.next = None

    #checks whether the spot is already in the list
    def contains(self, spot):
        end = self.head
        #print(spot)
        while end != None:
            #print('loop')
            if end.spot.x_loc == spot.x_loc and end.spot.y_loc == spot.y_loc:
                return True
            end = end.next
        return False

    #returns the length of the list
    def length(self):
        count = 0
        end = self.head
        while end != None:
            end = end.next
            count += 1
        return count


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


    #movement for the knight class
class Knight(Piece):
    x_loc = None
    y_loc = None
    name = None
    hasMoved = 0
    type = 'knight'
    move_list = LinkedList()
    
    def __init__(self, x, y, name, white):
        self.x_loc = x
        self.y_loc = y
        self.name = name
        self.is_white = white

        #this method checks if the piece can move and moves it if it can
    def move(self, target):
        if self.canMove(target) == True:
            if target.piece == None:
                target.piece = self
                board[self.y_loc][self.x_loc].piece = None
                self.x_loc = target.x_loc
                self.y_loc = target.y_loc
                self.hasMoved = 1
            elif target.piece.is_white != self.is_white:
                target.piece.set_killed()
                target.piece = self
                board[self.y_loc][self.x_loc].piece = None
                self.x_loc = target.x_loc
                self.y_loc = target.y_loc
                self.hasMoved = 1
        self.move_list = LinkedList()

        
        
    #checks whether the the piece is blocked by other pieces when attempting to move
    #this method uses the linked list class and recursion to check each spot neighboring the target spot
    #and repeats this process until a path to the piece has been found or it runs out of paths
    #returns true if there is a viable path, otherwise, it returns false
    def moveBlocked(self, target):
        if self.move_list.head == None:
            self.move_list.add_node(target)
            
        #Used for testing the function
        #temp = 0
        #while(temp < 30000000):
            #temp += 1

        #print("\n")
        #print(target.x_loc, target.y_loc)
        x_range = self.x_loc - target.x_loc
        y_range = self.y_loc - target.y_loc
        x_steps = [-1, 0, 1]
        y_steps = [-1, 0, 1]
        #print(x_range)


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

        #print("X_range and steps: " , x_range, y_range, x_steps, y_steps)
        #current = target
        #print('recursion ', current.x_loc, current.y_loc)

        #print(self.move_list.length())
        if self.move_list.length() == 5:
            return False

        for item in x_steps:
            #print(item)
            for item2 in y_steps:
                #print('x and y: ', item, item2)
                if item2 == 0 and item == 0:
                    continue
                if board[target.y_loc + item2][target.x_loc + item].piece == self:
                    #print('True')
                    #self.move_list.print_list()
                    return True
                if board[target.y_loc + item2][target.x_loc + item].piece == None:
                    if self.move_list.contains(board[target.y_loc + item2][target.x_loc + item]):
                        #print('test')
                        continue
                    #print(target.y_loc + item2, target.x_loc + item)
                    self.move_list.add_node(board[target.y_loc + item2][target.x_loc + item])
                    #print(item, item2)
                    #self.move_list.print_list()
                    if self.moveBlocked(target=self.move_list.get_last_spot()) is False:            #Recursively calls iteself to check the next spot
                        self.move_list.pop_node()
                        #print('pop')
                        continue
                    else:
                        return True
        return False

    
    #checks whether the piece can move to the target spot
    def canMove(self, target):
        if abs(target.x_loc - self.x_loc) > 4 and abs(target.y_loc - self.y_loc) > 4:
            print("can't too many squares")
            return False
        elif self.moveBlocked(target) == False:
            print('Move blocked')
            return False
        elif target.piece == None:
            print("moving")
            return True
        elif target.piece.is_white != self.is_white:
            print("capturing piece at target")
            return True
        elif target.piece.is_white == self.is_white:
            print("cant target contains ally piece")
            return False
        else:
            print("something went wrong")
            return False
        
        
        
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
wP1 = Pawn(0, 1, 'wP1', white = True)
wP2 = Pawn(1, 1, 'wP2', white = True)
wP3 = Pawn(2, 1, 'wP3', white = True)
wP4 = Pawn(3, 1, 'wP4', white = True)
wP5 = Pawn(4, 1, 'wP5', white = True)
wP6 = Pawn(5, 1, 'wP6', white = True)
wP7 = Pawn(6, 1, 'wP7', white = True)
wP8 = Pawn(7, 1, 'wP8', white = True)

#creating white knights
wk1 = Knight(1, 0, 'wk1', white = True)
wk2 = Knight(6, 0, 'wk1', white = True)

#setting the pawn location on the board
board[wP1.y_loc][wP1.x_loc].set_piece(wP1)
board[wP2.y_loc][wP2.x_loc].set_piece(wP2)
board[wP3.y_loc][wP3.x_loc].set_piece(wP3)
board[wP4.y_loc][wP4.x_loc].set_piece(wP4)
board[wP5.y_loc][wP5.x_loc].set_piece(wP5)
board[wP6.y_loc][wP6.x_loc].set_piece(wP6)
board[wP7.y_loc][wP7.x_loc].set_piece(wP7)
board[wP8.y_loc][wP8.x_loc].set_piece(wP8)

#setting white knight locations
board[wk1.y_loc][wk1.x_loc].set_piece(wk1)
board[wk2.y_loc][wk2.x_loc].set_piece(wk2)


#
#Black
#
#Creating black pawns
bP1 = Pawn(0, 6, 'bP1', white = False)
bP2 = Pawn(1, 6, 'bP2', white = False)
bP3 = Pawn(2, 6, 'bP3', white = False)
bP4 = Pawn(3, 6, 'bP4', white = False)
bP5 = Pawn(4, 6, 'bP5', white = False)
bP6 = Pawn(5, 6, 'bP6', white = False)
bP7 = Pawn(6, 6, 'bP7', white = False)
bP8 = Pawn(7, 6, 'bP8', white = False)

#creating black knights
bk1 = Knight(1, 7, 'bk1', white = False)
bk2 = Knight(6, 7, 'bk1', white = False)

#setting the pawn location on the board
board[bP1.y_loc][bP1.x_loc].set_piece(bP1)
board[bP2.y_loc][bP2.x_loc].set_piece(bP2)
board[bP3.y_loc][bP3.x_loc].set_piece(bP3)
board[bP4.y_loc][bP4.x_loc].set_piece(bP4)
board[bP5.y_loc][bP5.x_loc].set_piece(bP5)
board[bP6.y_loc][bP6.x_loc].set_piece(bP6)
board[bP7.y_loc][bP7.x_loc].set_piece(bP7)
board[bP8.y_loc][bP8.x_loc].set_piece(bP8)

#setting black knight location
board[bk1.y_loc][bk1.x_loc].set_piece(bk1)
board[bk2.y_loc][bk2.x_loc].set_piece(bk2)


print_Board(board)
print('\n')
movePiece(board[6][0], board[5][0])
movePiece(board[7][1], board[5][1])
movePiece(board[5][1], board[2][0])
print('\n')
print_Board(board)
