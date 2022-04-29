import os
import sys
from PyQt5.QtWidgets import QApplication
from visuals import BoardVis

# for pyinstaller to package and link images correctly
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def main():
    app = QApplication(sys.argv)
    window = BoardVis()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()