from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QPoint


class Piece(QLabel):
    def __init__(self, pieceColor, pieceType, pieceCommander, parent=None):
        super(Piece, self).__init__(parent)

        # Set up some properties
        self.labelPos = QPoint()

        self.onBoarder = False
        self.startingPosition = [0, 0]
        self.endingPosition = [0, 0]


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
