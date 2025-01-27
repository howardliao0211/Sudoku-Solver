from PyQt6 import QtWidgets, QtCore, QtGui
from typing import List

class BoardWidget(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(None)
        self.initUI()

    def initUI(self):
        main_grid = QtWidgets.QGridLayout()
        main_grid.setSpacing(10)  # Set spacing between sub-boxes
        self.cells: List[List[QtWidgets.QLineEdit]] = [[None for _ in range(9)] for _ in range(9)]

        for row in range(9):
            for col in range(9):
                cell = QtWidgets.QLineEdit()
                cell.setFixedSize(40, 40)
                cell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                cell.setFont(QtGui.QFont('Arial', 20))
                cell.setMaxLength(1)
                cell.setValidator(QtGui.QIntValidator(1, 9, self))
                self.cells[row][col] = cell

        # Create frames for 3x3 sub-boxes
        for row in range(3):
            for col in range(3):
                frame = QtWidgets.QFrame()
                frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
                frame.setLineWidth(3)
                sub_grid = QtWidgets.QGridLayout()
                sub_grid.setSpacing(5)  # Set spacing between cells within sub-boxes
                for i in range(3):
                    for j in range(3):
                        sub_grid.addWidget(self.cells[row * 3 + i][col * 3 + j], i, j)
                frame.setLayout(sub_grid)
                main_grid.addWidget(frame, row, col)

        self.setLayout(main_grid)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([])
    win = BoardWidget()
    win.show()
    sys.exit(app.exec())
    
