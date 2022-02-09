import imp
import sys
from PyQt5.QtWidgets import QApplication
from visuals import BoardVis, PieceVis
from ChessGame import Game







def main():
    game = Game()
    app = QApplication(sys.argv)
    window = BoardVis(game)
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()