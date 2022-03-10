import sys
from PyQt5.QtWidgets import QApplication
from visuals import BoardVis
from ChessGame import Game as chess_game

def main():
    #game = chess_game()
    app = QApplication(sys.argv)
    window = BoardVis()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()