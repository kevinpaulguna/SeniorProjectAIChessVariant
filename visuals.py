from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton 
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont
import sys

from ChessGame import Game

def board_to_screen(x, y, size):
    new_x = x * size
    new_y = y * size
    return (new_x, new_y)

def screen_to_board(x, y, size):
    return ((x - (size/2)) / size, (y - (size/2)) / size)


class PieceVis(QLabel):
    def __init__(self, visual, visual_h, parent=None):
        super(PieceVis, self).__init__(parent)

        # Set up some properties
        self.labelPos = QPoint()

        self.onBoarder = False
        self.startingPosition = [0, 0]
        self.endingPosition = [0, 0]
        self.default_vis = QPixmap('./picture/' + visual)
        self.active_vis = QPixmap('./picture/' + visual_h)
        self.is_active = False
        self.set_img()

    def get_active(self):
        return self.is_active

    def set_active(self, val):
        self.is_active = val
        self.set_img()

    def set_img(self):
        if self.is_active:
            self.setPixmap(self.active_vis)
        else:
            self.setPixmap(self.default_vis)

    def mousePressEvent(self, ev: QMouseEvent) -> None:

                #If user clicks on a piece, it will be moved to the starting position
                self.labelPos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
                self.startingPosition = [int(self.labelPos.x() / self.parent().tileSize),
                                         int(self.labelPos.y() / self.parent().tileSize)]
                self.raise_()
    # Set the region limits of the board that the piece can move to
    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
            if ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                    and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < \
                    (0 + (self.parent().tileSize / 2)):
                self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                       0 + (self.parent().tileSize / 2))
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)) \
                    and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
                self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                       0 + (self.parent().tileSize / 2))
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)) and \
                    ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
                self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                       self.parent().tileSize * 9.25 - (self.parent().tileSize / 2))
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)) \
                    and ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
                self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                       self.parent().tileSize * 9.25 - (self.parent().tileSize / 2))
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() < (0 + (self.parent().tileSize / 2)):
                self.labelPos = QPoint(0 + (self.parent().tileSize / 2),
                                       (ev.globalPos().y() - self.parent().pos().y()) - 30)
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() < (0 + (self.parent().tileSize / 2)):
                self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                       0 + (self.parent().tileSize / 2))
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).x() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
                self.labelPos = QPoint(self.parent().tileSize * 9.25 - (self.parent().tileSize / 2),
                                       (ev.globalPos().y() - self.parent().pos().y()) - 30)
                self.onBoarder = True
            elif ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30)).y() > \
                    (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)):
                self.labelPos = QPoint((ev.globalPos().x() - self.parent().pos().x()) - 0,
                                       (self.parent().tileSize * 9.25 - (self.parent().tileSize / 2)))
                self.onBoarder = True

            if not self.onBoarder:
                self.lablePos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
            self.move(self.lablePos - QPoint(self.parent().tileSize / 2, (self.parent().tileSize / 2)))
            self.onBoarder = False


    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        # Make sure it is the right turn for the piece and that the commander has command points.
            self.onBoarder = False
            self.endingPosition = [int(self.labelPos.x() / self.parent().tileSize),
                                   int(self.labelPos.y() / self.parent().tileSize)]
            self.parent().movePieceRelease(self.startingPosition, self.endingPosition)


class TileVis(QLabel):
    def __init__(self, visual, parent=None):
        super(TileVis, self).__init__(parent)
        # Set up some properties
        self.is_active = False
        self.active_vis = QPixmap('./picture/yt')
        self.default_vis = QPixmap('./picture/' + visual)
        self.set_img()

    def set_active(self, val):
        self.is_active = val
        self.set_img()

    def set_img(self):
        if self.is_active:
            self.setPixmap(self.active_vis)
        else:
            self.setPixmap(self.default_vis)

    def get_active(self):
        return self.is_active

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.set_active(not self.is_active)


class BoardVis(QMainWindow):
    def __init__(self):
        super(BoardVis,self).__init__()
        game = Game()
        self.controller = game
        #This block sets up the window properties
        self.setGeometry(500, 200, 300, 300)
        self.setWindowTitle("Chess Board")

        
        # This button allow you can stop your turn
        self.stopButton = QPushButton("End Turn", self)

        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)
        

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

        self.chooseSideText = QLabel(self)
        self.startScreen = QLabel(self)

        # Choose side button on start screen
        self.whiteButton = QPushButton("White side", self)
        self.blackButton = QPushButton("Black side", self)

        self.showBoard()
        self.showSideChoice()



    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.resize(self.boardSize + self.tableOption.width(), self.boardSize )


    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 9.5
        #add the tile images
        self.addBoardComponents(self.tileSetup, self.tilePos)

        #get data from controller and display it
        board = self.controller.get_board()
        self.addBoardComponents(self.pieceSet, self.piecePos)
    
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


    #Create stop button properties
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(self.stopButton.height() * 0.7)
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
        # Create StartScreen properties
        self.startScreen.setAlignment(Qt.AlignCenter)
        self.startScreen.resize(self.boardSize, self.boardSize)
        self.startScreen.setStyleSheet("background-image: url(./picture/startscreen.jpg);"
                                       "background-repeat: no-repeat;"
                                       "background-position: center;")
        self.startScreen.move(0, 0)
        self.startScreen.hide()

        # Set up choose side text properties
        self.chooseSideText.setAlignment(Qt.AlignCenter)
        self.chooseSideText.setText("Welcome to the chess game!"
                                    "\nPlease Choose Your Side")
        self.chooseSideText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseSideText.height() * 0.4)
        self.chooseSideText.setFont(font)
        self.chooseSideText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.chooseSideText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)),
                                 int((self.boardSize / 2) - 300))
        self.chooseSideText.hide()

        # Set up for white button properties
        self.whiteButton.clicked.connect(self.whiteButtonClicked)
        self.whiteButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.whiteButton.height() * 0.4)
        self.whiteButton.setFont(font)
        self.whiteButton.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2))
                              , int((self.boardSize / 2) - 150))

        # Set up for black button properties
        self.blackButton.clicked.connect(self.blackButtonClicked)
        self.blackButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.blackButton.height() * 0.4)
        self.blackButton.setFont(font)
        self.blackButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2))
                              , int((self.boardSize / 2) - 50))

    def stopButtonClicked(self):
        self.switchTurn()


    def swictchTurn(self):
        if self.turn == "white":
            self.turn = "black"
            self.tableOption.setText("Turn: black")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")
        else:
            self.turn = "white"
            self.tableOption.setText("Turn: White")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")


    def showSideChoice(self):
        self.startScreen.show()
        self.startScreen.raise_()
        self.chooseSideText.show()
        self.chooseSideText.raise_()
        self.whiteButton.show()
        self.whiteButton.raise_()
        self.blackButton.show()
        self.blackButton.raise_()

    def hideStartScreen(self):
        self.startScreen.hide()
        self.chooseSideText.hide()
        self.whiteButton.hide()
        self.blackButton.hide()

    def whiteButtonClicked(self):
        self.player = 0
        self.hideStartScreen()


    def blackButtonClicked(self):
        self.player = 1
        #the AI runsnings
        self.hideStartScreen()

    
    def addBoardComponents(self, sender, destination):
        # These are used as iterators to move through the arrays.
        x_iter = 0
        y_iter = 0
        piece_imgs = {
            "wP": "wp"
        }
        # Iterate through all tiles in the tile set array and create images for them.
        # The images are stored in another array that can be manipulated.
        for row in sender:
            x_iter = 0
            for tile in row:
                if tile == "0":
                    continue
                if len(tile) == 1:
                    #these are the board letters and number 
                     label = QLabel(parent=self)            
                     label.setPixmap(QPixmap('./picture/' + tile))                   
                elif tile[1] == 't':
                    label =TileVis(tile, parent=self)

                else:
                    label = PieceVis(tile, tile + 'bl', parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int(x_iter * self.tileSize), int(y_iter * self.tileSize))
                label.show()

                # Move the new label to the label array.
                destination[y_iter][x_iter] = label

                x_iter += 1
            y_iter += 1

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        x = self.screen_to_board(a0.pos().x())
        y = self.screen_to_board(a0.pos().y())

        return super().mousePressEvent(a0)

    #This function is snap the piece back to it place when the person releases wrong place
    def movePieceRelease(self, fromPos, toPos):
        if not fromPos == toPos and not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize),
                                                       int(fromPos[1] * self.tileSize))

        elif not self.piecePos[fromPos[1]][fromPos[0]] == "0":
            # Snap the piece back to its start position when the person releases it.
            self.piecePos[fromPos[1]][fromPos[0]].move(int(fromPos[0] * self.tileSize), int(fromPos[1] * self.tileSize))

    def screen_to_board(self, screen_val):
        return round( (screen_val - 37.5) / 75 )

def chessBoard():
    app = QApplication(sys.argv)
    window = BoardVis()
    window.show()
    sys.exit(app.exec_())

def main():
    chessBoard()

if __name__ == '__main__':
    main()
