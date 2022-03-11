from ast import Del
from math import floor
from turtle import color
from typing import Tuple
from xmlrpc.client import Boolean
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QGridLayout,QComboBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont,QMovie


from ChessGame import Game as chess_game, Piece

game_over = False

def corp_to_color(corp_num):
    colors = ['rd', 'bl', 'gr']
    return colors[corp_num - 1]

def board_to_screen(x, y, size):
    new_x = (x+1) * size
    new_y = (y+1) * size
    return (new_x, new_y)

def screen_to_board(x, y, size):
    b_x = int(x / size) -1
    b_y = int(y / size) -1
    return (b_x, b_y)

def piece_to_img_name(piece):
    k_pieces = {
            "wKt": "wk",
            "bKt": "bk",
            "wKg": "wki",
            "bKg": "bki"
        }
    if piece == "___":
        return None
    if piece[:3] in k_pieces.keys():
        piece_name = k_pieces[piece[:3]]
    else:
        piece_name = piece[:2]
    return piece_name

def deleteItemsOfLayout(layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
                 widget.remove()
             else:
                 deleteItemsOfLayout(item.layout())

#pieceVis  is a representation of the pieces in the game
#movableVis is the movable pieces

class corpVis(QLabel):
    def __init__(self, vis, name, size, parent=None):
        super(corpVis, self).__init__()
        self.default_vis = QPixmap('./picture/' + vis).scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.set_img()
        self.piece_name = name

    def set_img(self):
        self.setPixmap(self.default_vis)
    #This function is snap the piece back to it place when the person releases wrong place
    #obsoleted

class LeaderVis(QLabel):
    def __init__(self, vis, parent=None):
        super(LeaderVis, self).__init__()



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
        if game_over == True:
            return
        #If user clicks on a piece, it will be moved to the starting position
        self.start =  screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        self.moves = self.parent().controller.get_possible_moves_for_piece_at(x=self.start[0], y=self.start[1])
        self.raise_()
    # Set the region limits of the board that the piece can move to
    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if game_over == True:
            return
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
        if game_over == True:
            return
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
        self.parent().update_labels()
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
        self.h_mode = True
        self.white_pov = True
        #This block sets up the window properties
        #self.setGeometry(500, 200, 300, 300)
        self.setFixedSize(925, 700)
        self.setWindowTitle("Chess Board")
        self.highlighted = []
        self.corp_menu = CorpMenu(self.controller)
        # buttons:
        # This button allow you can stop your turn
        self.stopButton = QPushButton("End Turn", self)

        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)


        # choose highlight mode on/off
        self.corpButton = QPushButton("Manage Corps", self)

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
        self.optionScreen = QLabel(self)
        self.teamText = QLabel(self)
        self.opponentText = QLabel(self)
        self.highlightText = QLabel(self)
        self.gameTypeText = QLabel(self)

        #set up the buttons
        self.startGame= QPushButton("Start game",self)
        self.whiteButton = QRadioButton("White side", self)
        self.blackButton = QRadioButton("Black side", self)
        self.humanButton = QRadioButton("Human", self)
        self.computerButton = QRadioButton("Computer", self)
        self.offhighlight = QRadioButton("Off", self)
        self.onhighlight = QRadioButton("On", self)
        self.medievalButton = QRadioButton("Medieval", self)
        self.corpCommanderButton = QRadioButton("Corp Commander", self)

        # Set up the roll dice screen
        self.pauseBackground = QLabel(self)
        self.rollText = QLabel(self)
        self.rollDiceAnimation = QLabel(self)
        self.resultCaptureText = QLabel(self)
        self.okayButton = QPushButton("Okay", self)
        self.attackSuccess = None



        self.showBoard()

    def closeEvent(self,event):
        self.corp_menu.close()
        event.accept()

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
        self.__set_button(self.corpButton, 0.7)
        self.corpButton.setCheckable(True)
        self.corpButton.clicked.connect(self.corpBClicked)
        self.corpButton.resize(155,40)
        self.corpButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 25,
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
        self.chooseSideText.setText("Welcome to Fuzzy Logic Chess!"
                                    "\nGame Setup:")
        self.chooseSideText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.chooseSideText.height() * 0.4)
        self.chooseSideText.setFont(font)
        self.chooseSideText.setStyleSheet('font-weight: bold; color: rgba(0, 204, 204, 255)')
        self.chooseSideText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)),
                                 int((self.boardSize / 2) - 300))
        self.chooseSideText.hide()


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
        self.okayButton.setStyleSheet( '''
            QPushButton {
                background-color: rgb(0, 204, 204);
                color: black;
                border: 0.1em solid #000000;
            }
            QPushButton:hover {
                background-color: black;
                color: rgb(0, 204, 204);
                border-color: rgb(0, 204, 204);
            }
            ''')
        self.okayButton.move(int((self.boardSize / 2) - (self.okayButton.width() / 2))
                             , int((self.boardSize / 2) + 250))
        self.okayButton.hide()

        #set up the option screen properties
        self.optionScreen.setAlignment(Qt.AlignCenter)
        self.optionScreen.resize(self.boardSize / 1.5, self.boardSize / 2)
        self.optionScreen.setStyleSheet('background-color: rgba(0, 0, 0, .8)')
        self.optionScreen.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2)) - 180
                               , int((self.boardSize / 2) - 150))
        self.optionScreen.hide()

        # Set up for start game button properties
        self.startGame.clicked.connect(self.startGameClicked)
        self.startGame.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.startGame.height() * 0.4)
        self.startGame.setFont(font)
        self.startGame.setStyleSheet(
            '''
            QPushButton {
                background-color: rgb(0, 204, 204);
                color: black;
                border: 0.1em solid #000000;
                box-shadow:
            }
            QPushButton:hover {
                background-color: black;
                color: rgb(0, 204, 204);
                border-color: rgb(0, 204, 204);
            }
            '''
            )
        self.startGame.move(int((self.boardSize / 2) - (self.startGame.width() / 2))
                            , int((self.boardSize / 2) + 250))
        self.startGame.hide()

        #set up team text properties
        self.teamText.setAlignment(Qt.AlignCenter)
        self.teamText.setText("Team:")
        self.teamText.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.teamText.height() * 0.2)
        self.teamText.setFont(font)
        self.teamText.setStyleSheet('font-weight: bold; color: rgba(0, 204, 204, 255)')
        self.teamText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200,
                                  int((self.boardSize / 2) - 175))
        self.teamText.hide()

        #set up opponent text properties
        self.opponentText.setAlignment(Qt.AlignCenter)
        self.opponentText.setText("Opponent: ")
        self.opponentText.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.teamText.height() * 0.2)
        self.opponentText.setFont(font)
        self.opponentText.setStyleSheet('font-weight: bold; color: rgba(0, 204, 204, 255)')
        self.opponentText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200,
                               int((self.boardSize / 2) - 95))
        self.opponentText.hide()

        #set up highlight text properties
        self.highlightText.setAlignment(Qt.AlignCenter)
        self.highlightText.setText("Highlight: ")
        self.highlightText.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.teamText.height() * 0.2)
        self.highlightText.setFont(font)
        self.highlightText.setStyleSheet('font-weight: bold; color: rgba(0, 204, 204, 255)')
        self.highlightText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200,
                                int((self.boardSize / 2) - 5))
        self.highlightText.hide()

        #set up game type text properties
        self.gameTypeText.setAlignment(Qt.AlignCenter)
        self.gameTypeText.setText("Game Type: ")
        self.gameTypeText.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.teamText.height() * 0.2)
        self.gameTypeText.setFont(font)
        self.gameTypeText.setStyleSheet('font-weight: bold; color: rgba(0, 204, 204, 255)')
        self.gameTypeText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200,
                               int((self.boardSize / 2) + 85))
        self.gameTypeText.hide()

        #set up white/black button properties
        self.team_group = QButtonGroup()

        self.team_group.addButton(self.whiteButton)
        self.__set_button(self.whiteButton, 0.4)
        self.whiteButton.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2))
                              , int((self.boardSize / 2) - 130))

        # Set up for black button properties
        self.team_group.addButton(self.blackButton)
        self.__set_button(self.blackButton, 0.4)
        self.blackButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2))
                              , int((self.boardSize / 2) - 100))

        #set up human/computer button properties
        self.opponent_group = QButtonGroup(self)
        self.opponent_group.addButton(self.humanButton, 1)
        self.__set_button(self.humanButton, 0.4)
        self.humanButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2))
                              , int((self.boardSize / 2) - 40))

        self.opponent_group.addButton(self.computerButton, 2)
        self.__set_button(self.computerButton, 0.4)
        self.computerButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2))
                                 , int((self.boardSize / 2) - 10))

        #set up highlight on/off button properties
        self.highlight_group = QButtonGroup(self)
        self.highlight_group.addButton(self.onhighlight, 1)
        self.__set_button(self.onhighlight, 0.4)
        self.onhighlight.move(int((self.boardSize / 2) - (self.onhighlight.width() / 2))
                              , int((self.boardSize / 2) + 50))

        self.highlight_group.addButton(self.offhighlight, 2)
        self.__set_button(self.offhighlight, 0.4)
        self.offhighlight.move(int((self.boardSize / 2) - (self.offhighlight.width() / 2))
                               , int((self.boardSize / 2) + 80))

        #set up medieval/corp button properties
        self.gameType_group = QButtonGroup(self)
        self.gameType_group.addButton(self.medievalButton, 1)
        self.__set_button(self.medievalButton, 0.4)
        self.medievalButton.move(int((self.boardSize / 2) - (self.medievalButton.width() / 2))
                                 , int((self.boardSize / 2) + 140))

        self.gameType_group.addButton(self.corpCommanderButton, 2)
        self.__set_button(self.corpCommanderButton, 0.4)
        self.corpCommanderButton.move(int((self.boardSize / 2) - (self.corpCommanderButton.width() / 2))
                                      , int((self.boardSize / 2) + 170))


    def startGameClicked(self):
        if self.blackButton.isChecked():
            self.blackButtonClicked()
        if self.whiteButton.isChecked():
            self.whiteButtonClicked()
        """
        if self.humanButton.isChecked():
            self.humanButtonClicked()
        if self.computerButton.isChecked():
            self.computerButtonClicked()
        """

        if self.onhighlight.isChecked():
            self.h_mode = True
        if self.offhighlight.isChecked():
            self.h_mode = False

        """
        if self.medievalButton.isChecked():
            self.medievalButtonClicked()
        if self.corpCommanderButton.isChecked():
            self.corpCommanderButtonClicked()
        """
        self.hideStartScreen()

    def __rolldiceWork(self):
        # Set up roll dice text properties
        self.rollText.hide()
        self.rollText.setAlignment(Qt.AlignCenter)
        self.rollText.setText("Rolling Dice...")
        self.rollText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.rollText.height() * 0.4)
        self.rollText.setFont(font)
        self.rollText.setStyleSheet('font-weight: bold; color: rgba(0, 255, 255, 255); dip')
        self.rollText.move(int((self.boardSize / 2) - (self.rollText.width() / 2)),
                           int((self.boardSize / 2) - 300))
        # self.rollText.hide()

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
        if self.controller.game_status() == True:
            self.resultCaptureText.setText("Capture Successful! \n Game Over!!")
            global game_over
            game_over = True
        else:
            self.resultCaptureText.setText("Capture " + ("Successful!" if self.attackSuccess else "Failed!"))

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
        self.update_labels()

    def corpBClicked(self):
        for i in range(1,4):
            self.corp_menu.update_leader(i)
            self.corp_menu.update_group(i)
        self.corp_menu.show()

    def update_labels(self):
        if self.controller.tracker.get_current_player():
            self.tableOption.setText("Current Turn: White")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")
        else:
            self.tableOption.setText("Current Turn: Black")
            self.moveIndicator.setText("Remaining Move:"
                                       "\nLeft Side  :  " +
                                       "\nRight Side: " +
                                       "\n Center     : ")


    def showSideChoice(self):
        self.startScreen.show()
        self.startScreen.raise_()
        self.chooseSideText.show()
        self.chooseSideText.raise_()

        self.optionScreen.show()
        self.optionScreen.raise_()
        self.teamText.show()
        self.teamText.raise_()
        self.opponentText.show()
        self.opponentText.raise_()
        self.highlightText.show()
        self.highlightText.raise_()
        self.gameTypeText.show()
        self.gameTypeText.raise_()

        self.whiteButton.show()
        self.whiteButton.raise_()
        self.blackButton.show()
        self.blackButton.raise_()
        self.computerButton.show()
        self.computerButton.raise_()
        self.humanButton.show()
        self.humanButton.raise_()
        self.offhighlight.show()
        self.offhighlight.raise_()
        self.onhighlight.show()
        self.onhighlight.raise_()
        self.medievalButton.show()
        self.corpCommanderButton.show()
        self.medievalButton.raise_()
        self.corpCommanderButton.raise_()

        self.startGame.show()
        self.startGame.raise_()

    def hideStartScreen(self):
        self.startScreen.hide()
        self.chooseSideText.hide()
        self.whiteButton.hide()
        self.blackButton.hide()
        self.teamText.hide()
        self.optionScreen.hide()
        self.opponentText.hide()
        self.computerButton.hide()
        self.humanButton.hide()
        self.offhighlight.hide()
        self.onhighlight.hide()
        self.medievalButton.hide()
        self.corpCommanderButton.hide()
        self.highlightText.hide()
        self.gameTypeText.hide()
        self.startGame.hide()

    def whiteButtonClicked(self):
        self.controller.tracker.current_player = 1
        #self.player = 0
        self.hideStartScreen()


    def blackButtonClicked(self):
        self.controller.tracker.current_player = 1
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
        for y in range(8):
            for x in range(8):
                cur_p = self.piecePos[y][x]
                if cur_p and cur_p != "0":
                        cur_p.clear()
                piece, corp_name = pieces_array[y][x]
                if corp_name:
                    corp_num = corp_name[-1]
                    color_name = corp_to_color(int(corp_num))
                piece = piece_to_img_name(piece)
                if not piece:
                    continue
                label = PieceVis(piece + color_name, piece + 'bl', parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int((x+1) * self.tileSize), int((y+1) * self.tileSize))
                label.show()
                self.piecePos[y][x] = label

    def update_flipped(self):
        pass

class PieceGroup(QWidget):
    def __init__(self, labels):
        super(PieceGroup, self).__init__()
        self.labels = labels
        self.create_group()
    # Changed layout mode to grid
    def create_group(self):
        layout = QGridLayout()
        items_per_row = 3
        num_rows = len(self.labels) / items_per_row
        for i in range(floor(num_rows) + 1):
            if len(self.labels) <= 0:
                self.setLayout(layout)
                return
            elif len(self.labels) >= items_per_row:
                cur_row_items = items_per_row
            else:
                cur_row_items = len(self.labels)
            for j in range(cur_row_items):
                piece_name = self.labels.pop()
                label_name = piece_to_img_name(piece_name)
                label = corpVis(label_name, piece_name, 50)
                layout.addWidget(label, i, j)
        self.setLayout(layout)

class Deleg_Label(QWidget):
    def __init__(self, corp_data):
        super(Deleg_Label, self).__init__()
        layout = QHBoxLayout()
        self.corp_data = corp_data
        self.left_opt = QComboBox()
        self.left_opt.addItems(["Delegate","Recall"])
        self.left_opt.currentTextChanged.connect(self.on_left_changed)
        self.corp_opt = QComboBox()
        self.set_corp_options()
        self.corp_opt.currentTextChanged.connect(self.on_corp_changed)
        self.piece_opt = QComboBox()
        self.set_piece_options()
        self.label = QLabel()
        self.set_label_txt()

        layout.addWidget(self.left_opt)
        layout.addWidget(self.piece_opt)
        layout.addWidget(self.label)
        layout.addWidget(self.corp_opt)
        self.setLayout(layout)

    def get_data(self):
        if self.left_opt.currentIndex():
            from_corp = self.corp_opt.currentText()
            to_corp = self.get_king_corp()
        else:
            from_corp = self.get_king_corp()
            to_corp = self.corp_opt.currentText()
        piece = self.piece_opt.currentText()
        return [piece, from_corp, to_corp]


    def on_left_changed(self):
        self.set_label_txt()
        self.set_piece_options()

    def on_corp_changed(self):
        self.set_piece_options()

    def set_label_txt(self):
        text = 'to' if self.left_opt.currentIndex() == 0 else 'from'
        self.label.setText(text)

    def set_corp_options(self):
        swappable = [corp_name for i, corp_name in enumerate(self.corp_data.keys()) if i in [0,2]]
        self.corp_opt.addItems(swappable)

    def get_king_corp(self):
        king_corp = list(self.corp_data.keys())
        return king_corp[1]

    def set_piece_options(self):
        self.piece_opt.clear()
        if self.left_opt.currentIndex():
            self.piece_opt.addItems(self.corp_data[self.corp_opt.currentText()])    # true is Recall
        else:
            self.piece_opt.addItems(self.corp_data[self.get_king_corp()])


class LeaderBox(QWidget):
    def __init__(self, leader):

        super(LeaderBox, self).__init__()
        self.leader = leader
        self.commander = self.create_leader_icon()

        commander_row = QHBoxLayout()
        commander_row.addStretch(1)
        commander_row.addWidget(self.commander)
        commander_row.addStretch(1)

        self.top = QVBoxLayout()
        self.top.addLayout(commander_row)
        self.top.setContentsMargins(0, 10, 0, 10)


        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.StyledPanel)
        top_frame.setLayout(self.top)
        layout = QVBoxLayout()
        layout.addWidget(top_frame)
        self.setLayout(layout)

    def create_leader_icon(self):
        size = 75
        leader_img = piece_to_img_name(self.leader)
        return corpVis(leader_img, self.leader, size)



class KingBox(LeaderBox):
    def __init__(self, leader, corps):
        super().__init__(leader)
        self.corps_ref = self.get_corp_options(corps)

        self.swap_line = Deleg_Label(self.corps_ref)
        self.top.addWidget(self.swap_line)
        self.confirm_button = QPushButton("Confirm")
        self.top.addWidget(self.confirm_button)


    # could probably use the original data but this works out more nicely
    def get_corp_options(self, data):
        options = {}
        for i in range(1,4):
            options[data[i]['name']] = data[i]['commanding']
        return options

class CorpMenu(QWidget):
    def __init__(self, game):
        super(CorpMenu, self).__init__()
        self.setGeometry(0,0, 1, 1)
        self.setWindowTitle("Corp Delegation")
        self.controller : chess_game = game
        self.col_layouts = []
        self.leaders = []
        self.set_corps()    #used the first time to create all layouts and attach them appropriately
        self.corps_ref = {}
        self.king_box = None

    def set_corps(self):
        self.update_data()
        layout = QHBoxLayout()
        for i in (range(1,4)):
            self.create_col(layout, self.corps_ref[i]['commander'], self.corps_ref[i]['commanding'], i)
        self.setLayout(layout)

    def confirm_clicked(self):
        swap_data = self.king_box.swap_line.get_data()
        self.controller.delegate_or_recall(piece=swap_data[0], from_corp=swap_data[1], to_corp=swap_data[2])
        self.update_all_groups()

    def update_data(self):
        is_white = self.controller.tracker.get_current_player()
        self.corps_ref = self.controller.get_corp_info(white=is_white)

    def create_col(self, outer_layout, leader, group, num):
        leader_box = LeaderBox(leader)
        col = QVBoxLayout()
        self.col_layouts.append(col)
        col.addWidget(leader_box)
        col.addWidget(PieceGroup(group))
        col.setSpacing(0)
        col.setContentsMargins(10,0,10,0)
        col_frame = QFrame()
        col_frame.setFrameShape(QFrame.StyledPanel)
        col_frame.setLayout(col)
        outer_layout.addWidget(col_frame)

    # I split these up since there are situations that we want one without the other
    # namely, when corps switch pieces
    def update_leader(self, i):
        self.update_data()
        leader = self.corps_ref[i]['commander']
        if i == 2:
            new_leader = KingBox(leader, self.corps_ref)
            new_leader.confirm_button.clicked.connect(self.confirm_clicked)
            self.king_box = new_leader
        else:
            new_leader = LeaderBox(leader)
        current_leader = self.col_layouts[i-1].itemAt(0).widget()
        self.col_layouts[i-1].replaceWidget(current_leader, new_leader)
        current_leader.setParent(None)

    def update_all_groups(self):
        for i in range(1,4):
            self.update_group(i)

    def update_group(self, i):
        self.update_data()
        group = self.corps_ref[i]['commanding']
        new_piece_group = PieceGroup(group)
        current_group = self.col_layouts[i-1].itemAt(self.col_layouts[i-1].count() - 1).widget()
        self.col_layouts[i-1].replaceWidget(current_group, new_piece_group)
        current_group.setParent(None)





    """
    def create_group(self, labels, outer_layout):
        items_per_row = 3
        num_rows = len(labels) / items_per_row
        for i in range(round(num_rows) + 1):
            piece_row = QHBoxLayout()
            if len(labels) <= 0:
                return
            elif len(labels) >= items_per_row:
                cur_row_items = items_per_row
            else:
                cur_row_items = len(labels)
            for i in range(cur_row_items):
                    label_name = piece_to_img_name(labels.pop())
                    label = corpVis(label_name, 50)
                    piece_row.addWidget(label)
                    if not len(labels):
                        piece_row.addStretch()
            piece_row.addSpacing(0)
            outer_layout.addLayout(piece_row)

    """





