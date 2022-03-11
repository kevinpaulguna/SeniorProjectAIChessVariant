import sys
from PyQt5.QtWidgets import QApplication
from visuals import BoardVis

def main():
    app = QApplication(sys.argv)
    window = BoardVis()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()