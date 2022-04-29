from math import floor
from typing import Tuple
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer, QDir, QUrl
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QComboBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont, QMovie
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from ChessAI import AIFunctions
from ChessGame import Game as chess_game

game_over = False
# pdf_path = "FL-Chess__DistAI_V5d.pdf"

def corp_to_color(corp_num):
    colors = ['', 'rd', 'bl', 'gr']
    return colors[corp_num]

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

class PieceVis(QLabel):
    def __init__(self, visual, x_pos, y_pos, parent=None):
        super(PieceVis, self).__init__(parent)
        # Set up some properties
        self.labelPos = QPoint()
        self.vis = visual
        self.onBoarder = False
        self._h_mode = False
        self.moves = []                    # is only accurate between picking up and placing a piece
        self.start = [x_pos ,y_pos ]
        self.end = [0, 0]       # pieces will ask chessgame if they can move
        self.default_vis = QPixmap('./picture/' + visual)
        self.set_img()

    def set_h_mode(self, val):
        self._h_mode = val

    def get_h_mode(self):
        return self._h_mode

    def set_img(self):
        self.setPixmap(self.default_vis)


    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if game_over == True:
            return
        #If user clicks on a piece, it will be moved to the starting position
        #self.start =  screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        #print("start x: ", self.start[0], " y: ", self.start[1])
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
        drag_move = False
        click_end = False
        if game_over == True:
            return
        self.onBoarder = False
        print(self)
        self.end = screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)      # set new end pos
                   # set movement val on board object
        print(self.start, self.end)
        if self.same_loc(self.start, self.end):
            # we did not move, just clicked the piece, store it on the board object as start of click to move
            self.set_h_mode(not self._h_mode)   # highlighting logic
            if self.parent().moving_piece and self.parent().controller.is_enemy(self.end[0], self.end[1]):
                # this is the piece getting attacked
                click_end = True
            # board needs reference to this piece to make changes to it
            else:
                self.parent().moving_piece = self
                self.parent().setMoveStart(self.start)
            # we still might have moved the piece some amount so set it back to the center of its start tile
            move_spot = board_to_screen(self.start[0], self.start[1], self.parent().tileSize)
            self.move(move_spot[0], move_spot[1])
        else:
            drag_move = True
            self.set_h_mode(False)
        self.parent().remove_all_h()
        if self._h_mode:
            self.parent().add_group_h(self.moves)

        if drag_move:
            self.parent().setMoveStart(self.start)
            self.parent().move_end = self.end
            self.parent().do_piece_move(self)

        if click_end:
            self.parent().move_end = self.end
            self.parent().do_piece_move(None)
        """ isAttack = (self.end[0], self.end[1], True) in self.moves
        moveSuccessful = self.parent().controller.move_piece(from_x=self.start[0], from_y=self.start[1],
                                                             to_x=self.end[0], to_y=self.end[1])        # or whatever the show dice roll function is
        self.parent().diceRollResult = self.parent().controller.get_result_of_dice_roll()
        self.parent().make_AI_move()
        if moveSuccessful:
            self.parent()._update_pieces()
            new_spot = board_to_screen(self.end[0], self.end[1],
                                       self.parent().tileSize)  # create pixel position of new piece
            self.start[0] = self.end[0]
            self.start[1] = self.end[1]
        else:
            new_spot = board_to_screen(self.start[0], self.start[1], self.parent().tileSize)
        self.move(new_spot[0], new_spot[1])

        if isAttack:
            self.parent().rollDiceScreen(moveSuccessful)
        self.parent().update_labels() """


        #self.parent().movePieceRelease(self.start, self.end)
    def same_loc(self, s_loc, f_loc):
        return (s_loc[0] == f_loc[0]) and (s_loc[1] == f_loc[1])



class TileVis(QLabel):
    def __init__(self, visual, move, attack, parent=None):
        super(TileVis, self).__init__(parent)
        # Set up some properties
        self.is_active = False
        self.move_highlight = QLabel(parent=self)
        self.move_highlight.setStyleSheet("background-color: rgba(255,255,0,150)")
        self.move_highlight.resize(75, 75)
        self.atk_highlight = QLabel(parent=self)
        self.atk_highlight.setStyleSheet("background-color: rgba(255,69,0,150)")
        self.atk_highlight.resize(75, 75)
        self.default_vis = QPixmap('./picture/' + visual)
        self.set_img(False)

    def set_active(self, val, atk=False):
        self.is_active = val
        self.set_img(atk)

    def set_img(self, atk):
        if self.is_active:
            self.atk_highlight.show() if atk else self.move_highlight.show()
        else:
            self.move_highlight.hide()
            self.atk_highlight.hide()
            self.setPixmap(self.default_vis)

    def get_active(self):
        return self.is_active

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.start_click = screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)


    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.end_click = screen_to_board(ev.windowPos().x(), ev.windowPos().y(), self.parent().tileSize)
        if self.same_loc(self.start_click, self.end_click):
            if self.parent().moving_piece:
                self.parent().move_end = self.end_click
                self.parent().do_piece_move(self.parent().moving_piece)

    def same_loc(self, s_loc, f_loc):
        return (s_loc[0] == f_loc[0]) and (s_loc[1] == f_loc[1])


class BoardVis(QMainWindow):
    def __init__(self):
        super(BoardVis,self).__init__()
        self.controller = chess_game()
        self.__game_type = ""
        self.h_mode = True
        self.white_pov = True
        self.move_start = None
        self.move_end = None
        self.moving_piece = None
        #This block sets up the window properties
        #self.setGeometry(500, 200, 300, 300)
        self.setFixedSize(925, 675)
        self.setWindowTitle("Chess Board")
        self.highlighted = []
        self.corp_menu = CorpMenu(self)
        self.ai_delay = QTimer(self)
        self.ai_delay.timeout.connect(self.ai_single_move)
        # buttons:
        # This button allow you can stop your turn
        self.stopButton = QPushButton("End Turn", self)
        # This button allow you can reset the game when you want to start new game
        self.newGameButton = QPushButton("Restart", self)

        # This button can display the rules
        self.helperButton = QPushButton("i", self)
        self.show_the_rules = displayRules()

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
        self.corpCommanderButton = QRadioButton("Corp Command", self)

        # Set up the roll dice screen
        self.pauseBackground = QLabel(self)
        self.rollText = QLabel(self)
        self.rollDiceAnimation = QLabel(self)
        self.resultCaptureText = QLabel(self)
        self.okayButton = QPushButton("Return to Board", self)
        self.attackSuccess = None
        self.diceRollResult = -1

        self.ai_player = None

        self.showBoard()


    def do_piece_move(self, mvd_piece: PieceVis):
        print("was called")
        piece = mvd_piece
        if not piece:
            piece = self.moving_piece
        piece.set_h_mode(False)
        self.remove_all_h()
        isAttack = (self.move_end[0], self.move_end[1], True) in piece.moves
        moveSuccessful = self.controller.move_piece(from_x=self.move_start[0], from_y=self.move_start[1],
                                                    to_x=self.move_end[0], to_y=self.move_end[1])
        self.diceRollResult = self.controller.get_result_of_dice_roll()
        new_spots = []
        if moveSuccessful:
            for x, y in self.controller.get_move_path():
                new_spot = board_to_screen(x, y, self.tileSize)  # create pixel position of new piece
                new_spots.append(new_spot)
            piece.start[0] = self.move_end[0]
            piece.start[1] = self.move_end[1]
        else:
            new_spot = board_to_screen(self.move_start[0], self.move_start[1], self.tileSize)
        print("moved piece: ", piece)
        # piece.move(new_spot[0], new_spot[1])
        if len(new_spots)>1:
            new_spots.reverse()

            mv_delay = QTimer(self)

            def spot_by_spot():
                if len(new_spots)==0:
                    mv_delay.stop()
                    return
                x, y = new_spots.pop()
                print(x,y)
                piece.move(x, y)

            mv_delay.timeout.connect(spot_by_spot)
            mv_delay.start(500)
        else:
            piece.move(new_spot[0], new_spot[1])

        if isAttack:
            self._update_pieces()
            self.rollDiceScreen(moveSuccessful)
        else:
            self.make_AI_move() #TODO: find place for this after update pieces is fixed

        self.update_labels()

        self.reset_movement_data()

    def reset_movement_data(self):
        self.moving_piece = None
        self.move_start = None
        self.move_end = None

    def closeEvent(self,event):
        self.show_the_rules.close()
        # displayRules.close()
        self.corp_menu.close()
        event.accept()

    def set_h_mode(self, val: bool):
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

    def setMoveStart(self, position):
        self.move_start = position

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

    #Create table option properties
        self.tableOption.setText("Current Turn: White")
        self.tableOption.setAlignment(Qt.AlignCenter)
        self.tableOption.resize(200, 25)
        font = QFont()
        font.setFamily("Impact")
        font.setPixelSize(self.tableOption.height() * 0.8)
        self.tableOption.setFont(font)
        self.tableOption.move(int(self.boardSize) - 10,
                              int(self.boardSize /2 -75) - (self.tableOption.height()) * 0.5 +20)
        self.tableOption.hide()

    #Create show information of move indicator
        self.moveIndicator.setText("Remaining Move:")
        self.moveIndicator.setAlignment(Qt.AlignCenter)
        self.moveIndicator.resize(200, 25)
        font = QFont()
        font.setFamily("impact")
        font.setPixelSize(self.moveIndicator.height() * 0.8)
        self.moveIndicator.setFont(font)
        self.moveIndicator.move(int(self.boardSize) - 10,
                                int(self.boardSize /2)- (self.moveIndicator.height()) * 0.5 - 20)
        self.moveIndicator.hide()

    #manage corp button setup:
        self.__set_button(self.corpButton, 0.7)
        self.corpButton.setCheckable(True)
        self.corpButton.clicked.connect(self.corpBClicked)
        self.corpButton.resize(180,40)
        self.corpButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 50,
                             25)

        self.wCapturedText = QLabel(self)
        self.wCapturedFrame = QFrame(self)

        self.bCapturedText = QLabel(self)
        self.bCapturedFrame = QFrame(self)

        # Create white pieces captured
        self.wCapturedText.setText("CAPTURED BY WHITE")
        self.wCapturedText.setAlignment(Qt.AlignCenter)
        self.wCapturedText.resize(200, 25)
        font = QFont()
        font.setBold(True)
        font.setFamily("Castellar, Baskerville")
        font.setPixelSize(self.moveIndicator.height() * 0.6)
        self.wCapturedText.setFont(font)
        self.wCapturedText.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 60,
                             390)

        #set frame for wCapturedPic:
        self.wCapturedFrame.setFrameShape(QFrame.Box)
        self.wCapturedFrame.setLineWidth(2)
        self.wCapturedFrame.setGeometry(int(self.boardSize) - 10,
                                      420,
                                      200, 140)



        # Create black pieces captured
        self.bCapturedText.setText("CAPTURED BY BLACK")
        self.bCapturedText.setAlignment(Qt.AlignCenter)
        self.bCapturedText.resize(200, 25)
        font = QFont()
        font.setBold(True)
        font.setFamily("Castellar, Baskerville")
        font.setPixelSize(self.moveIndicator.height() * 0.6)
        self.bCapturedText.setFont(font)
        self.bCapturedText.move(
            int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 60,
            95)

        # set frame for bCapturedPic:
        self.bCapturedFrame.setFrameShape(QFrame.Box)
        self.bCapturedFrame.setLineWidth(2)
        self.bCapturedFrame.setGeometry(int(self.boardSize) - 10,
                                        125,
                                        200, 140)

        if self.__game_type != "Corp":
            self.corpButton.hide()

    #Create stop button properties
        self.__set_button(self.stopButton, 0.7)
        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.stopButton.move(int(self.boardSize - ((self.stopButton.width() - self.tableOption.width()) / 2))-50,
                              int(self.boardSize / 2 + 250) - (self.stopButton.height() * 0.5)-20)

        self.stopButton.resize(180,40)
        self.stopButton.hide()

    #Create restart button properties

        self.__set_button(self.newGameButton, 0.7)
        self.newGameButton.move(int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2))-50,
                             int(self.boardSize / 2 + 300) - (self.newGameButton.height() * 0.5)-20)

        self.newGameButton.resize(180,40)
        self.newGameButton.clicked.connect(self.returnToStartScreen)
        self.newGameButton.hide()

        # create properties for the helper button
        self.__set_button(self.helperButton, 2.0)
        self.helperButton.clicked.connect(lambda: self.show_the_rules.show())
        self.helperButton.move(25/2, 25/2)
        self.helperButton.resize(50, 50)
        self.helperButton.setStyleSheet('''
            QPushButton {
                font-family: "Times New Roman";
                font-size: 25px;
                background-color: rgb(0, 204, 204);
                color: black;
                border: 0.1em solid #000000;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: black;
                color: rgb(0, 204, 204);
                border-color: rgb(0, 204, 204);
            }
            ''')
        self.helperButton.show()
        self.helperButton.raise_()



       # Create StartScreen properties
        self.startScreen.setAlignment(Qt.AlignCenter)
        self.startScreen.resize(925, 675)
        self.startScreen.setStyleSheet("background-image: url(./picture/fullstartscreen.png);")
        self.startScreen.move(0, 0)

        moveIntoSidePanel = ((925-self.boardSize)/2)

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
        self.chooseSideText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + moveIntoSidePanel,
                                 int((self.boardSize / 2) - 300))
        self.chooseSideText.hide()


        # Create start screen properties
        self.pauseBackground.setAlignment(Qt.AlignCenter)
        self.pauseBackground.resize(925, 675)
        self.pauseBackground.setStyleSheet('background-color: black')
        self.pauseBackground.setStyleSheet("background-image: url(./picture/fullstartscreen.png);")
        self.pauseBackground.move(0, 0)
        self.pauseBackground.hide()

        mainAreaButtonCSS = '''
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
            '''

        # Set up for okay button properties
        self.okayButton.clicked.connect(self.okayButtonClicked)
        self.okayButton.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.okayButton.height() * 0.4)
        self.okayButton.setFont(font)
        self.okayButton.setStyleSheet(mainAreaButtonCSS)
        self.okayButton.move(int((self.boardSize / 2) - (self.okayButton.width() / 2)) + moveIntoSidePanel
                             , int((self.boardSize / 2) + 250))
        self.okayButton.hide()

        #set up the option screen properties
        self.optionScreen.setAlignment(Qt.AlignCenter)
        self.optionScreen.resize(self.boardSize / 1.5, self.boardSize / 2)
        self.optionScreen.setStyleSheet('background-color: rgba(0, 0, 0, .8)')
        self.optionScreen.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2)) - 180 + moveIntoSidePanel
                               , int((self.boardSize / 2) - 150))
        self.optionScreen.hide()

        # Set up for start game button properties
        self.startGame.clicked.connect(self.startGameClicked)
        self.startGame.resize(150, 40)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.startGame.height() * 0.4)
        self.startGame.setFont(font)
        self.startGame.setStyleSheet(mainAreaButtonCSS)
        self.startGame.move(int((self.boardSize / 2) - (self.startGame.width() / 2)) + moveIntoSidePanel
                            , int((self.boardSize / 2) + 250))
        self.startGame.hide()

        optionsTitlesCSS = 'font-weight: bold; color: rgb(0, 204, 204)'

        #set up team text properties
        self.teamText.setAlignment(Qt.AlignCenter)
        self.teamText.setText("Team:")
        self.teamText.resize(200, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.teamText.height() * 0.2)
        self.teamText.setFont(font)
        self.teamText.setStyleSheet(optionsTitlesCSS)
        self.teamText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200 + moveIntoSidePanel,
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
        self.opponentText.setStyleSheet(optionsTitlesCSS)
        self.opponentText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200 + moveIntoSidePanel,
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
        self.highlightText.setStyleSheet(optionsTitlesCSS)
        self.highlightText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200 + moveIntoSidePanel,
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
        self.gameTypeText.setStyleSheet(optionsTitlesCSS)
        self.gameTypeText.move(int((self.boardSize / 2) - (self.chooseSideText.width() / 2)) + 200 + moveIntoSidePanel,
                               int((self.boardSize / 2) + 85))
        self.gameTypeText.hide()

        radioButtonTextCSS = 'color: white; font-size: 15px'

        #set up white/black button properties
        self.team_group = QButtonGroup()

        self.team_group.addButton(self.whiteButton)
        self.__set_button(self.whiteButton, 0.4)
        self.whiteButton.move(int((self.boardSize / 2) - (self.whiteButton.width() / 2)) + moveIntoSidePanel
                              , int((self.boardSize / 2) - 130))


        # Set up for black button properties
        self.team_group.addButton(self.blackButton)
        self.__set_button(self.blackButton, 0.4)
        self.blackButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2)) + moveIntoSidePanel
                              , int((self.boardSize / 2) - 100))
        self.whiteButton.setChecked(True)

        self.whiteButton.setStyleSheet(radioButtonTextCSS)
        self.blackButton.setStyleSheet(radioButtonTextCSS)
        self.whiteButton.adjustSize()
        self.blackButton.adjustSize()

        #set up human/computer button properties
        self.opponent_group = QButtonGroup(self)

        self.opponent_group.addButton(self.humanButton, 1)
        self.__set_button(self.humanButton, 0.4)
        self.humanButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2)) + moveIntoSidePanel
                              , int((self.boardSize / 2) - 40))

        self.opponent_group.addButton(self.computerButton, 2)
        self.__set_button(self.computerButton, 0.4)
        self.computerButton.move(int((self.boardSize / 2) - (self.blackButton.width() / 2)) + moveIntoSidePanel
                                 , int((self.boardSize / 2) - 10))
        self.humanButton.setChecked(True)

        self.humanButton.setStyleSheet(radioButtonTextCSS)
        self.computerButton.setStyleSheet(radioButtonTextCSS)
        self.humanButton.adjustSize()
        self.computerButton.adjustSize()

        #set up highlight on/off button properties
        self.highlight_group = QButtonGroup(self)

        self.highlight_group.addButton(self.onhighlight, 1)
        self.__set_button(self.onhighlight, 0.4)
        self.onhighlight.move(int((self.boardSize / 2) - (self.onhighlight.width() / 2)) + moveIntoSidePanel
                              , int((self.boardSize / 2) + 50))

        self.highlight_group.addButton(self.offhighlight, 2)
        self.__set_button(self.offhighlight, 0.4)
        self.offhighlight.move(int((self.boardSize / 2) - (self.offhighlight.width() / 2)) + moveIntoSidePanel
                               , int((self.boardSize / 2) + 80))
        self.onhighlight.setChecked(True)

        self.onhighlight.setStyleSheet(radioButtonTextCSS)
        self.offhighlight.setStyleSheet(radioButtonTextCSS)
        self.onhighlight.adjustSize()
        self.offhighlight.adjustSize()

        #set up medieval/corp button properties
        self.gameType_group = QButtonGroup(self)

        self.gameType_group.addButton(self.medievalButton, 1)
        self.__set_button(self.medievalButton, 0.4)
        self.medievalButton.move(int((self.boardSize / 2) - (self.medievalButton.width() / 2)) + moveIntoSidePanel
                                 , int((self.boardSize / 2) + 140))

        self.gameType_group.addButton(self.corpCommanderButton, 2)
        self.__set_button(self.corpCommanderButton, 0.4)
        self.corpCommanderButton.move(int((self.boardSize / 2) - (self.corpCommanderButton.width() / 2)) + moveIntoSidePanel
                                      , int((self.boardSize / 2) + 170))
        self.corpCommanderButton.setChecked(True)

        self.medievalButton.setStyleSheet(radioButtonTextCSS)
        self.corpCommanderButton.setStyleSheet(radioButtonTextCSS)
        self.medievalButton.adjustSize()
        self.corpCommanderButton.adjustSize()

        self.captured_by = {
            "white": [],
            "black": []
        }

    def update_captured_pieces(self):
        self.delete_captured_pieces()
        self.updated_captured_by('black')
        self.updated_captured_by('white')
        self.show_captured_pieces()

    def updated_captured_by(self, color:str):
        if color == 'white':
            starting = 425
        elif color == 'black':
            starting = 130
        else:
            return

        captured = [piece_to_img_name(piece[0]).lower()+".png" for piece in self.controller.get_pieces_captured_by(color)]

        self.captured_by[color] = []

        img_size = 35
        offset = 40
        for i, pc in enumerate(captured):

            captured_pc = QLabel(self)
            captured_pc.setAlignment(Qt.AlignCenter)
            cap = QPixmap('./picture/' + pc)
            cap = cap.scaled(img_size, img_size)
            captured_pc.setPixmap(cap)
            captured_pc.resize(img_size, img_size)
            captured_pc.move(
                int(self.boardSize - ((self.newGameButton.width() - self.tableOption.width()) / 2)) - 10 + (img_size*(i%5)),
                    starting + (offset*int(i/5))
            )
            self.captured_by[color].append(captured_pc)
            # setattr(self, "wCapturedPic{}".format(i), self.wCapturedPic)

    def show_captured_pieces(self):
        for team in self.captured_by.values():
            for captured in team:
                captured.show()

    def delete_captured_pieces(self):
        for team in self.captured_by.values():
            for captured in team:
                captured.setParent(None)

    def make_AI_move(self):
        if not self.computerButton.isChecked() or self.ai_turn_over():
            return      # ai not selected, bail out of function
        self.ai_delay.start(1500)

    def ai_single_move(self):
        self.ai_player.make_move()
        self._update_pieces()
        self.update_labels()
        self.update_captured_pieces()
        if self.ai_turn_over():
            self.ai_delay.stop()

    def ai_turn_over(self):
        whites_turn = (self.controller.tracker.get_current_player()==1)
        if self.controller.is_game_over():  # special case for gameover
            self.handle_gameover()
            return True
        return self.whiteButton.isChecked() == whites_turn    # the active color is the color the human chose, no longer computer's turn

    def handle_gameover(self):
        global game_over
        game_over = True
        self.stopButton.hide()
        self.moveIndicator.hide()
        self.tableOption.setText("Winner: " +
                                ("White" if self.controller.tracker.get_current_player() else "Black") +
                                " Team!")
        return

    def startGameClicked(self):
        if self.medievalButton.isChecked():
            self.__game_type = "Medieval"
            self.corpButton.hide()
        elif self.corpCommanderButton.isChecked():
            self.__game_type = "Corp"
            self.corpButton.show()
        self.controller = chess_game(game_type=self.__game_type)
        if self.__game_type == "Corp":
            self.corp_menu = CorpMenu(self)

        self._update_pieces()
        self.update_labels()
        self.update_captured_pieces()

        if self.blackButton.isChecked():
            self.blackButtonClicked()
        elif self.whiteButton.isChecked():
            self.whiteButtonClicked()

        if self.computerButton.isChecked():
            self.ai_player = AIFunctions(self.controller, self.blackButton.isChecked())

        # TODO: Handle once AI is enabled
        # if self.humanButton.isChecked():
        #     self.humanButtonClicked()
        # elif self.computerButton.isChecked():
        #     self.computerButtonClicked()

        if self.onhighlight.isChecked():
            self.h_mode = True
        elif self.offhighlight.isChecked():
            self.h_mode = False

        self.hideStartScreen()
        self.tableOption.show()
        self.moveIndicator.show()
        self.newGameButton.show()
        self.stopButton.show()
        self.helperButton.show()

        if self.blackButton.isChecked():
            self.make_AI_move()

    def __rolldiceWork(self):
        moveIntoSidePanel = ((925-self.boardSize)/2)
        # Set up roll dice text properties
        self.rollText.setAlignment(Qt.AlignCenter)
        self.rollText.setText("Rolling Dice...")
        self.rollText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.rollText.height() * 0.4)
        self.rollText.setFont(font)
        self.rollText.setStyleSheet('font-weight: bold; color: rgb(0, 204, 204)')
        self.rollText.move(int((self.boardSize / 2) - (self.rollText.width() / 2)) + moveIntoSidePanel,
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
        self.rollDiceAnimation.move(300+moveIntoSidePanel, 200)
        self.rollDiceAnimation.hide()

    def __roll_dice(self):
        moveIntoSidePanel = ((925-self.boardSize)/2)
        # Set up capture result text properties
        self.rollText.hide()
        self.resultCaptureText.setAlignment(Qt.AlignCenter)
        self.resultCaptureText.resize(900, 100)
        font = QFont()
        font.setFamily('Arial')
        font.setPixelSize(self.resultCaptureText.height() * 0.4)
        self.resultCaptureText.setFont(font)
        self.resultCaptureText.setStyleSheet('font-weight: bold; color: rgb(0, 204, 204)')
        self.resultCaptureText.move(int((self.boardSize / 2) - (self.rollText.width() / 2)) + moveIntoSidePanel,
                           int((self.boardSize / 2) - 300))

        pixmap1 = QPixmap('./picture/die' + str(self.diceRollResult))
        pixmap1 = pixmap1.scaled(128, 128)
        self.rollDiceAnimation.setPixmap(pixmap1)
        self.rollDiceAnimation.move(300 + moveIntoSidePanel, 200)
        # update when after roll
        self.resultCaptureText.clear()
        if self.controller.is_game_over():
            self.resultCaptureText.setText("Capture Successful! \n Game Over!!")
            global game_over
            game_over = True
            self.stopButton.hide()
            self.moveIndicator.hide()
            self.tableOption.setText("Winner: " +
                                    ("White" if self.controller.tracker.get_current_player() else "Black") +
                                    " Team!")
        else:
            self.resultCaptureText.setText("Capture " + ("Successful!" if self.attackSuccess else "Failed!"))
        self.okayButton.raise_()

        #clear attack var
        self.attackSuccess = None

    def okayButtonClicked(self):
        self.hidepauseBackground()
        self.update_captured_pieces()
        self.make_AI_move() #TODO: find place for this after update pieces is fixed

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
        self.remove_all_h()
        self.update_labels()
        self.reset_movement_data()
        self.make_AI_move()

    def corpBClicked(self):
        for i in range(1,4):
            self.corp_menu.update_leader(i)
            self.corp_menu.update_group(i)
        print("corp button clicked")
        self.corp_menu.show()

    def update_labels(self):
        self.tableOption.setText("Current Player: " + ("White" if self.controller.tracker.get_current_player() else "Black"))
        self.moveIndicator.setText("Remaining Moves: " + str(self.controller.tracker.get_number_of_available_moves() ))


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

    def returnToStartScreen(self):
        global game_over
        game_over = False
        self.newGameButton.hide()
        self.stopButton.hide()
        self.moveIndicator.hide()
        self.tableOption.hide()
        self.corpButton.hide()
        self.hidepauseBackground()
        self.showSideChoice()
        self.remove_all_h()
        self.reset_movement_data()
        self.helperButton.hide()

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
        self.mk_basic_label("yt").move(0, 0)
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
            # i = 1
            name1, name2 = combo[i]
            l1 = self.mk_basic_label(name1)
            l2 = self.mk_basic_label(name2)
            l1.move(int( (i + 1) * self.tileSize), 0)
            l2.move(0, int((i + 1) * self.tileSize))
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

    def _update_pieces(self):
        print("updating pieces")
        pieces_array = self.controller.get_board()
        for y in range(8):
            for x in range(8):
                cur_p = self.piecePos[y][x]
                if cur_p and cur_p != "0":
                        cur_p.setParent(None)
                piece, corp_name = pieces_array[y][x]
                color_name = ""
                if corp_name:
                    corp_num = corp_name[-1]
                    color_name = corp_to_color(int(corp_num))
                piece = piece_to_img_name(piece)
                if not piece:
                    continue
                label = PieceVis(piece + color_name, x, y, parent=self)
                    # Set the image based on the array element.
                label.resize(75, 75)
                label.setScaledContents(True)
                label.move(int((x+1) * self.tileSize), int((y+1) * self.tileSize))
                label.show()
                self.piecePos[y][x] = label

    def update_flipped(self):
        pass

class PieceGroup(QWidget):
    def __init__(self, labels, corp_num):
        super(PieceGroup, self).__init__()
        self.corp_color = corp_to_color(corp_num)
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
                label = corpVis(label_name + self.corp_color, piece_name, 50)
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

    def get_swap_data(self):
        if self.left_opt.currentIndex():
            from_corp = self.corp_opt.currentText()
            to_corp = self.get_king_corp()
        else:
            from_corp = self.get_king_corp()
            to_corp = self.corp_opt.currentText()
        piece = self.piece_opt.currentText()
        return [piece, from_corp, to_corp]

    def set_corp_data(self, new_data):
        self.corp_data = new_data

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
    def __init__(self, leader, corp):

        super(LeaderBox, self).__init__()
        self.leader = leader
        self.commander = self.create_leader_icon(corp)

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

    def create_leader_icon(self, corp):
        size = 75
        color = corp_to_color(corp)
        leader_img = piece_to_img_name(self.leader)
        return corpVis(leader_img + color, self.leader, size)



class KingBox(LeaderBox):
    def __init__(self, leader, corp, corps):
        super().__init__(leader, corp)
        self.corps_ref = corps

        self.swap_line = Deleg_Label(self.get_corp_options())
        self.top.addWidget(self.swap_line)
        self.confirm_button = QPushButton("Confirm")
        self.top.addWidget(self.confirm_button)


    # could probably use the original data but this works out more nicely
    def get_corp_options(self):
        options = {}
        for i in range(1,4):
            options[self.corps_ref[i]['name']] = self.corps_ref[i]['commanding']
        return options

    def update_deleg_line(self):
        data = self.get_corp_options()
        self.swap_line.set_corp_data(data)

    def disable_button(self, val):
        self.confirm_button.setDisabled(val)

class CorpMenu(QWidget):
    def __init__(self, main_window):
        super(CorpMenu, self).__init__()
        self.setGeometry(0,0, 1, 1)
        self.setWindowTitle("Corp Delegation")
        self.main_window = main_window
        self.controller : chess_game = main_window.controller
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
        swap_data = self.king_box.swap_line.get_swap_data()
        self.controller.delegate_or_recall(piece=swap_data[0], from_corp=swap_data[1], to_corp=swap_data[2])
        self.update_data()
        self.king_box.corps_ref = self.corps_ref
        self.king_box.update_deleg_line()
        self.king_box.disable_button(self.controller.tracker.delegation_move_has_been_used())
        self.update_all_groups()
        self.main_window._update_pieces()

    def update_data(self):
        is_white = self.controller.tracker.get_current_player()
        self.corps_ref = self.controller.get_corp_info(white=is_white)

    def create_col(self, outer_layout, leader, group, num):
        leader_box = LeaderBox(leader, num)
        col = QVBoxLayout()
        self.col_layouts.append(col)
        col.addWidget(leader_box)
        col.addWidget(PieceGroup(group, num))
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
            new_leader = KingBox(leader, i, self.corps_ref)
            new_leader.disable_button(self.controller.tracker.delegation_move_has_been_used())
            new_leader.confirm_button.clicked.connect(self.confirm_clicked)
            self.king_box = new_leader
        else:
            new_leader = LeaderBox(leader, i)
        current_leader = self.col_layouts[i-1].itemAt(0).widget()
        self.col_layouts[i-1].replaceWidget(current_leader, new_leader)
        current_leader.setParent(None)

    def update_all_groups(self):
        for i in range(1,4):
            self.update_group(i)

    def update_group(self, i):
        self.update_data()
        group = self.corps_ref[i]['commanding']
        new_piece_group = PieceGroup(group, i)
        current_group = self.col_layouts[i-1].itemAt(self.col_layouts[i-1].count() - 1).widget()
        self.col_layouts[i-1].replaceWidget(current_group, new_piece_group)
        current_group.setParent(None)

class displayRules(QWebEngineView):
# class displayRules(QWidget):
    def __init__(self):
        super(displayRules, self).__init__()
        self.resize(600, 600)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.load(QUrl.fromLocalFile(QDir.current().filePath('FL-Chess__DistAI_V5d.pdf')))
