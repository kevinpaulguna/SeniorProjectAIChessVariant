from typing import Tuple
from xmlrpc.client import Boolean
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont,QMovie


from ChessGame import Game as chess_game

def board_to_screen(x, y, size):
    new_x = (x+1) * size
    new_y = (y+1) * size
    return (new_x, new_y)

def screen_to_board(x, y, size):
    b_x = int(x / size) -1
    b_y = int(y / size) -1
    return (b_x, b_y)

class PieceVis(QLabel):
    def __init__(self, visual, visual_h, parent=None):
        super(PieceVis, self).__init__(parent)

        # Set up some properties
        self.labelPos = QPoint()

        self.onBoarder = False
        self._h_mode = False
        self.moves = []                    # is only accurate between picking up and placing a piece
        self.start = [0, 0]     # and boardvis will no longer be in charge of whether a piece can move. 
        self.end = [0, 0]       # pieces will ask chessgame if they can move
        self.default_vis = QPixmap('./picture/' + visual)
        self.active_vis = QPixmap('./picture/' + visual_h)
        self.is_active = False
        self.set_img()

    def get_active(self):
        return self.is_active

    def set_active(self, val):
        self.is_active = val
        self.set_img()

    def set_h_mode(self, val):
        self._h_mode = val

    def get_h_mode(self):
        return self._h_mode

    def set_img(self):
        if self.is_active:
            self.setPixmap(self.active_vis)
        else:
            self.setPixmap(self.default_vis)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        #If user clicks on a piece, it will be moved to the starting position
        self.start =  screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        self.moves = self.parent().controller.get_possible_moves_for_piece_at(x=self.start[0], y=self.start[1])
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
            self.labelPos = ((ev.globalPos() - self.parent().pos()) - QPoint(0, 30))
        self.move(self.labelPos - QPoint(self.parent().tileSize / 2, (self.parent().tileSize / 2)))
        self.onBoarder = False


    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.onBoarder = False
        
        self.end = screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        if self.start == self.end:
            # we did not move, just clicked the piece
            self.set_h_mode(not self._h_mode)
        else:
            self.set_h_mode(False)
        self.parent().remove_all_h()
        if self._h_mode:
            self.parent().add_group_h(self.moves)


        isAttack = (self.end[0], self.end[1], True) in self.moves
        moveSuccessful = self.parent().controller.move_piece(from_x=self.start[0], from_y=self.start[1],
                                                             to_x=self.end[0], to_y=self.end[1])        # or whatever the show dice roll function is

        if moveSuccessful:
            self.parent()._update_pieces(self.parent().controller.get_board())
            new_spot = board_to_screen(self.end[0], self.end[1],
                                       self.parent().tileSize)  # create pixel position of new piece

        else:
            new_spot = board_to_screen(self.start[0], self.start[1], self.parent().tileSize)
        self.move(new_spot[0], new_spot[1])

        if isAttack:
            self.parent().rollDiceScreen(moveSuccessful)
        #self.parent().movePieceRelease(self.start, self.end)
    def loc_changed(self, s_loc, f_loc):
        return s_loc != f_loc

class TileVis(QLabel):
    def __init__(self, visual, move, attack, parent=None):
        super(TileVis, self).__init__(parent)
        # Set up some properties
        self.is_active = False
        self.move_vis = QPixmap('./picture/' + move)
        self.atk_vis = QPixmap('./picture/' + attack)
        self.default_vis = QPixmap('./picture/' + visual)
        self.set_img(False)

    def set_active(self, val, atk=False): 
        self.is_active = val
        self.set_img(atk)

    def set_img(self, atk):
        if self.is_active:
            self.setPixmap(self.atk_vis) if atk else self.setPixmap(self.move_vis) 
        else:
            self.setPixmap(self.default_vis)

    def get_active(self):
        return self.is_active


class BoardVis(QMainWindow):
    def __init__(self):
        super(BoardVis,self).__init__()
        self.controller = chess_game()
        self.h_mode = False
        self.white_pov = True
        #This block sets up the window properties
        #self.setGeometry(500, 200, 300, 300)
        self.setFixedSize(925, 700)
        self.setWindowTitle("Chess Board")
        self.highlighted = []
        
        # buttons:
        # This button allow you can stop your turn
        self.stopButton = QPushButton("End Turn", self)

        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)
        # Choose side button on start screen
        self.whiteButton = QPushButton("White side", self)
        self.blackButton = QPushButton("Black side", self)

        # choose highlight mode on/off
        self.highlightButton = QPushButton("Highlight Moves", self)

        self.tableOption = QLabel(self)
        
        #Show remaining moves
        self.moveIndicator = QLabel(self)
        # Holds labels for the tiles on the board.
        self.tilePos = [["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"]]

        # Holds labels for the pieces on the board.
        self.piecePos = [["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"],
                        ["0", "0", "0", "0", "0", "0", "0", "0"]]

        self.chooseSideText = QLabel(self)
        self.startScreen = QLabel(self)

        # Set up the roll dice screen
        self.pauseBackground = QLabel(self)
        self.rollText = QLabel(self)
        self.rollDiceAnimation = QLabel(self)
        self.resultCaptureText = QLabel(self)
        self.okayButton = QPushButton("Okay", self)
        self.attackSuccess = None

        

        self.showBoard()


    def set_h_mode(self, val: Boolean):
        self.h_mode = val

    def add_to_h(self, tile: TileVis):
        if not self.h_mode:
            return
        if tile not in self.highlighted:
            tile.set_active(True)
            self.highlighted.append(tile)

    def add_group_h(self, squares: Tuple):
        if not self.h_mode:
            return
        for pos in squares:
            tile = self.tilePos[pos[1]][pos[0]]
            tile.set_active(True, pos[2])
            self.highlighted.append(tile)

    def remove_all_h(self):
        if not self.highlighted:
            return
        for row in self.tilePos:
            for tile in row:
                if type(tile) is TileVis:
                    tile.set_active(False, False)
        for tile in self.highlighted:
            self.list_remove(tile)

    def list_remove(self, tile:TileVis):
        tile.set_active(False, False)
        self.highlighted.remove(tile)

    def showBoard(self):
        # Initialize the board.
        self.setBoard()
        self.showSideChoice()
        self.resize(self.boardSize + self.tableOption.width(), self.boardSize )

    def setBoard(self):
        self.tileSize = 75
        self.boardSize = self.tileSize * 9.5
        #add the tile images
        self.set_non_playables()

        #get data from controller and display it
        board = self.controller.get_board()
        self._update_pieces(board)
    
    #Create table option properties
        self.tableOption.setText("Current Turn: White")
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

    #highlight button setup:
        self.__set_button(self.highlightButton, 0.7)
        self.highlightButton.setCheckable(True)
        self.highlightButton.clicked.connect(self.highlightBClicked)
        self.highlightButton.resize(155,40)
        self.highlightButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 25,
                             25)

    #Create stop button properties
        self.__set_button(self.stopButton, 0.7)
        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.stopButton.move(int(self.boardSize - ((self.stopButton.width() - self.tableOption.width()) / 2)),
                              int(self.boardSize / 2 + 250) - (self.stopButton.height() * 0.5))

    #Create restart button properties
        
        self.__set_button(self.newGameButton, 0.7)
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



        # Create start screen properties
        self.pauseBackground.setAlignment(Qt.AlignCenter)
        self.pauseBackground.resize(self.boardSize, self.boardSize)
        self.pauseBackground.setStyleSheet('background-color: rgba(180,180,180,1)')
        self.pauseBackground.move(0, 0)
        self.pauseBackground.hide()

        # Set up for okay button properties
        self.okayButton.clicked.connect(self.okayButtonClicked)
        self.okayButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.okayButton.height() * 0.4)
        self.okayButton.setFont(font)
        self.okayButton.move(int((self.boardSize / 2) - (self.okayButton.width() / 2))
                             , int((self.boardSize / 2) + 300))
        self.okayButton.hide()


    def __rolldiceWork(self):
        # Set up roll dice text properties
        self.rollText.setAlignment(Qt.AlignCenter)
        self.rollText.setText("Roll Dice active")
        self.rollText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.rollText.height() * 0.4)
        self.rollText.setFont(font)
        self.rollText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.rollText.move(int((self.boardSize / 2) - (self.rollText.width() / 2)),
                           int((self.boardSize / 2) - 300))
        self.rollText.hide()

        # roll dice animation
        self.rollDiceAnimation.setAlignment(Qt.AlignCenter)
        self.rollDiceAnimation = QLabel(self)
        size = QSize(128, 128)
        pixmap = QMovie('./picture/dice.gif')
        self.rollDiceAnimation.setMovie(pixmap)
        pixmap.setScaledSize(size)
        self.rollDiceAnimation.resize(300, 300)
        pixmap.start()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.__roll_dice)
        self.timer.start()
        self.rollDiceAnimation.move(300, 200)
        self.rollDiceAnimation.hide()

    def __roll_dice(self):
        # Set up capture result text properties
        self.rollText.hide()
        self.resultCaptureText.setAlignment(Qt.AlignCenter)
        self.resultCaptureText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.resultCaptureText.height() * 0.4)
        self.resultCaptureText.setFont(font)
        self.resultCaptureText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255)')
        self.resultCaptureText.move(int((self.boardSize / 2) - (self.rollText.width() / 2)),
                           int((self.boardSize / 2) - 300))
        
        dice = self.controller.get_result_of_dice_roll()
        pixmap1 = QPixmap('./picture/die' + str(dice))
        pixmap1 = pixmap1.scaled(128, 128)
        self.rollDiceAnimation.setPixmap(pixmap1)
        self.rollDiceAnimation.move(300, 200)

        # update when after roll
        self.resultCaptureText.clear()
        self.resultCaptureText.setText("Capture result: " + ("Success!" if self.attackSuccess else "Failed!"))

        self.okayButton.show()
        self.okayButton.raise_()

        #clear attack var
        self.attackSuccess = None


    def okayButtonClicked(self):
        self.hidepauseBackground()

    def __set_button(self, button: QPushButton, scale):
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(button.height() * scale)
        button.setFont(font)

    def __set_facing_mode(self, val):
        self.white_pov = val
        self.set_non_playables()
        self._update_pieces()

    def stopButtonClicked(self):
        self.controller.tracker.end_turn()

    def highlightBClicked(self):
        self.set_h_mode(self.highlightButton.isChecked())

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
        self.controller.tracker.current_player = 1
        #self.player = 0
        self.hideStartScreen()


    def blackButtonClicked(self):
        self.controller.tracker.current_player = 0
        #the AI runsnings
        self.hideStartScreen()

    def rollDiceScreen(self, attackSuccess:bool):

        self.attackSuccess = attackSuccess
        self.pauseBackground.show()
        self.pauseBackground.raise_()
        self.__rolldiceWork()
        self.rollDiceAnimation.show()
        self.rollDiceAnimation.raise_()
        self.rollText.show()
        self.rollText.raise_()
        self.resultCaptureText.show()
        self.resultCaptureText.raise_()

    def hidepauseBackground(self):
        self.pauseBackground.hide()
        self.rollText.hide()
        self.rollDiceAnimation.hide()
        self.resultCaptureText.hide()
        self.resultCaptureText.clear()
        self.okayButton.hide()

    def set_non_playables(self):
        label = self.mk_basic_label("yt")
        label.move(0, 0)
        self.set_emptys("wt", "bt", "gt", "ot")
        self.set_lets_and_nums()
    
    def set_lets_and_nums(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        nums = ["8", "7", "6", "5", "4", "3", "2", "1"]
            
        if not self.white_pov:
            letters.reverse()
            nums.reverse()
        combo = [(letters[i], nums[i]) for i in range(8)]
        for i in range(8):
            name1, name2 = combo[i]
            l1 = self.mk_basic_label(name1)
            l2 = self.mk_basic_label(name2)
            l1.move(int( (i + 1) * self.tileSize), 0)
            l2.move(0, int( (i + 1) * self.tileSize))
            l1.show()
            l2.show()

    def set_emptys(self, white, black, move_h, atk_h):
        is_white = True
        for j in range(8):
            for i in range(8):
                name = white if is_white else black
                label = TileVis(name,  move_h, atk_h, parent=self)            
                label.setPixmap(QPixmap('./picture/' + name))  
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int((i+1) * self.tileSize), int((j+1) * self.tileSize))
                self.tilePos[j][i] = label
                is_white = not is_white
            is_white = not is_white

    def mk_basic_label(self, name):
        label = QLabel(parent=self)            
        label.setPixmap(QPixmap('./picture/' + name))  
        label.resize(75, 75)
        label.setScaledContents(True)
        return label
    #def update_pieces(self, ):
    def _update_pieces(self, pieces_array):
        k_pieces = {
            "wKt": "wk",
            "bKt": "bk",
            "wKg": "wki",
            "bKg": "bki"
        }

        for y in range(8):
            for x in range(8):
                cur_p = self.piecePos[y][x]
                if cur_p and cur_p != "0":
                        cur_p.clear()
                piece = pieces_array[y][x]
                if piece == "___":
                    continue
                if piece[:3] in k_pieces.keys():
                     piece = k_pieces[piece[:3]]
                else:
                    piece = piece[:2]
                label = PieceVis(piece, piece + 'bl', parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int((x+1) * self.tileSize), int((y+1) * self.tileSize))
                label.show()
                self.piecePos[y][x] = label

    def update_flipped(self):
        pass

    #This function is snap the piece back to it place when the person releases wrong place
    #obsoleted
