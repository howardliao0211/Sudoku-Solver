from PyQt6 import QtWidgets
from Sudoku import BoardMainWindow, BoardViewModel
import sys
import os

def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    vm = BoardViewModel()
    win = BoardMainWindow(vm)
    win.setup()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
