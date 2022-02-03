import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
import Piece

class chessBoardWindow(QMainWindow):
    def __init__(self):
        super(chessBoardWindow,self).__init__()
        #This block sets up the window properties
        self.setGeometry(500, 200, 300, 300)
        self.setWindowTitle("Chess Board")

        '''
        # This button allow you can stop your turn
        self.stopButton = QPushButton("Stop", self)

        # This button allow you can pause game
        self.pauseButton = QPushButton("Pause", self)

        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)
        '''

        self.tableOption = QLabel(self)

        #Show remaining moves
        self.moveIndicator = QLabel(self)


        self.tileSetup = [["yt", "A", "B", "C", "D", "E", "F", "G", "H"],
                          ["1", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["2", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["3", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["4", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["5", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["6", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"],
                          ["7", "wt", "bt", "wt", "bt", "wt", "bt", "wt", "bt"],
                          ["8", "bt", "wt", "bt", "wt", "bt", "wt", "bt", "wt"]]
        # Holds labels for the tiles on the board.
        self.tilePos = [[" ", "A", "B", "C", "D", "E", "F", "G", "H"],
                        ["1","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["2","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["3","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["4","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["5","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["6","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["7","0", "0", "0", "0", "0", "0", "0", "0"],
                        ["8","0", "0", "0", "0", "0", "0", "0", "0"]]

        # Holds initial setup commands for the pieces.
        self.pieceSet = [[" ", "A", "B", "C", "D", "E", "F", "G", "H"],
                         ["1","br", "bk", "bb", "bq", "bki", "bb", "bk", "br"],
                         ["2","bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                         ["3","0", "0", "0", "0", "0", "0", "0", "0"],
                         ["4","0", "0", "0", "0", "0", "0", "0", "0"],
                         ["5","0", "0", "0", "0", "0", "0", "0", "0"],
                         ["6","0", "0", "0", "0", "0", "0", "0", "0"],
                         ["7","wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                         ["8","wr", "wk", "wb", "wq", "wki", "wb", "wk", "wr"]]
        # Holds labels for the pieces on the board.
        self.piecePos = [[" ", "A", "B", "C", "D", "E", "F", "G", "H"],
                        ["1", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["2", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["3", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["4", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["5", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["6", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["7", "0", "0", "0", "0", "0", "0", "0", "0"],
                        ["8", "0", "0", "0", "0", "0", "0", "0", "0"]]

        self.showBoard()




    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.resize(self.boardSize + self.tableOption.width(), self.boardSize )


    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 9.5
        self.addBoardComponents(self.tileSetup, self.tilePos)
        self.addBoardComponents(self.pieceSet, self.piecePos)
    '''
    #Create table option properties
        self.tableOption.setText("First Turn: White")
        self.tableOption.setAlignment(Qt.AlignCenter)
        self.tableOption.resize(200, 25)
        font = QFont()
        font.setFamily("Impact")
        font.setPixelSize(self.tableOption.height() * 0.8)
        self.tableOption.setFont(font)
        self.tableOption.move(int(self.boardSize), int(self.boardSize /2 -75)
                              - (self.tableOption.height()) * 0.5)

    #Create show information of move indicator
        self.moveIndicator.setText("Remaining Move:"
                                   "\nLeft Side  :  "+
                                   "\nRight Side: "+
                                   "\n Center     : ")
        self.moveIndicator.setAlignment(Qt.AlignCenter)
        self.moveIndicator.resize(200, 100)
        font = QFont()
        font.setFamily("impact")
        font.setPixelSize(self.moveIndicator.height() * 0.2)
        self.moveIndicator.setFont(font)
        self.moveIndicator.move(int(self.boardSize), int(self.boardSize /2)
                                - (self.moveIndicator.height()) * 0.5)

    #Create pause button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.pauseButton.height() * 0.8)
        self.pauseButton.setFont(font)
        self.pauseButton.move(int(self.boardSize - ((self.pauseButton.width()-self.tableOption.width())/2)),
                              int(self.boardSize /2 + 200)- (self.pauseButton.height() * 0.5))

    #Create stop button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.stopButton.height() * 0.8)
        self.stopButton.setFont(font)
        self.stopButton.move(int(self.boardSize - ((self.stopButton.width() - self.tableOption.width()) / 2)),
                              int(self.boardSize / 2 + 250) - (self.stopButton.height() * 0.5))

    #Create restart button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.newGameButton.height() * 0.8)
        self.newGameButton.setFont(font)
        self.newGameButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)),
                             int(self.boardSize / 2 + 300) - (self.newGameButton.height() * 0.5))
    '''
    def addBoardComponents(self, sender, destination):
        # These are used as iterators to move through the arrays.
        xIter = 0
        yIter = 0

        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            for tile in row:
                if not tile == "0":
                    # This assigns special properties to each piece type.
                    if tile == "wp" or tile == "bp":
                        if xIter <= 2:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "pawn", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "pawn", 2, parent=self)
                        elif xIter == 3 or xIter == 4:
                            label = Piece.Piece(tile[0], "pawn", 1, parent=self)
                        elif xIter >= 5:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "pawn", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "pawn", 0, parent=self)
                    elif tile == "wr" or tile == "br":
                        label = Piece.Piece(tile[0], "rook", 1, parent=self)
                    elif tile == "wk" or tile == "bk":
                        if xIter <= 2:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "knight", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "knight", 2, parent=self)
                        elif xIter >= 5:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "knight", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "knight", 0, parent=self)
                    elif tile == "wb" or tile == "bb":
                        if xIter <= 3:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "bishop", 0, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "bishop", 2, parent=self)
                        elif xIter >= 6:
                            if tile[0] == "w":
                                label = Piece.Piece(tile[0], "bishop", 2, parent=self)
                            else:
                                label = Piece.Piece(tile[0], "bishop", 0, parent=self)
                    elif tile == "wq" or tile == "bq":
                        label = Piece.Piece(tile[0], "queen", 1, parent=self)
                    elif tile == "wki" or tile == "bki":
                        label = Piece.Piece(tile[0], "king", 1, parent=self)
                    else:
                        label = QLabel(self)
                    # Set the image based on the array element.
                    label.resize(75, 75)
                    pixmap = QPixmap('./picture/' + tile)
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)
                    label.move(int(xIter * self.tileSize), int(yIter * self.tileSize))
                    label.show()

                    # Move the new label to the label array.
                    destination[yIter][xIter] = label

                xIter += 1
            xIter = 0
            yIter += 1
    #This function is snap the piece back to it place when the person releases wrong place
    def movePieceRelease(self, fromPos, toPos):
        if not fromPos == toPos and not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                       int(fromPos[1] * self.tileSize))

        elif not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize), int(fromPos[1] * self.tileSize))

def chessBoard():
    app = QApplication(sys.argv)
    window = chessBoardWindow()
    window.show()
    sys.exit(app.exec_())

def main():
    chessBoard()

if __name__ == '__main__':
    main()