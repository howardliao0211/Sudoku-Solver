from PyQt6 import QtWidgets, QtCore
from dataclasses import dataclass
from typing import List, Tuple, Dict
import numpy as np
import random

try:
    from Sudoku.board_widget import BoardWidget
    from Sudoku.view_model import BoardViewModel
    from Sudoku.update_info import BoardUpdateInfo
except ModuleNotFoundError:
    from board_widget import BoardWidget
    from view_model import BoardViewModel
    from update_info import BoardUpdateInfo

class BoardMainWindow(QtWidgets.QMainWindow):
    def __init__(self, viewModel: BoardViewModel, parent = None):
        super().__init__(parent)
        self.viewModel = viewModel
    
    def setup(self):
        self.board = BoardWidget()

        gl = QtWidgets.QGridLayout()
        self.emptyPercentSpinbox = QtWidgets.QDoubleSpinBox()
        self.emptyPercentSpinbox.setRange(0, 0.9)
        self.emptyPercentSpinbox.setSingleStep(0.1)
        self.emptyPercentSpinbox.setValue(0.3)
        self.genButton = QtWidgets.QPushButton('Generate')

        self.solvePeriodSpinbox = QtWidgets.QSpinBox()
        self.solvePeriodSpinbox.setRange(0, 1000)
        self.solvePeriodSpinbox.setSingleStep(10)
        self.solvePeriodSpinbox.setValue(100)
        self.solveButton = QtWidgets.QPushButton('Solve')

        gl.addWidget(QtWidgets.QLabel('Empty percent:'), 0, 0)
        gl.addWidget(self.emptyPercentSpinbox, 0, 1)
        gl.addWidget(self.genButton, 0, 2)

        gl.addWidget(QtWidgets.QLabel('Solve period (ms):'), 1, 0)
        gl.addWidget(self.solvePeriodSpinbox, 1, 1)
        gl.addWidget(self.solveButton, 1, 2)

        self.clearButton = QtWidgets.QPushButton('Clear Board')
        self.editButton = QtWidgets.QPushButton('Edit Board')
        self.stopButton = QtWidgets.QPushButton('Stop Solver')

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.board)
        mainLayout.addLayout(gl)
        mainLayout.addWidget(self.clearButton)
        mainLayout.addWidget(self.editButton)
        mainLayout.addWidget(self.stopButton)

        wg = QtWidgets.QWidget()
        wg.setLayout(mainLayout)
        self.setCentralWidget(wg)

        self.clearButton.clicked.connect(self.clearButtonEvent)
        self.genButton.clicked.connect(self.genButtonEvent)
        self.solveButton.clicked.connect(self.solveButtonEvent)
        self.editButton.clicked.connect(self.editButtonEvent)
        self.viewModel.updateBoardSignal.connect(self.updateBoardEvent)

    def stopSolverButtonEvent(self) -> None:
        self.viewModel.stopSolver()

    def clearButtonEvent(self) -> None:
        self.viewModel.clearBoard()

    def editButtonEvent(self) -> None:
        if self.editButton.text() == 'Edit Board':
            self.editButton.setText('Stop Edit')

            for i in range(9):
                for j in range(9):
                    self.board.cells[i][j].setEnabled(True)
            
            self.genButton.setEnabled(False)
            self.solveButton.setEnabled(False)
        else:
            self.editButton.setText('Edit Board')

            for i in range(9):
                for j in range(9):
                    if self.board.cells[i][j].text() != '':
                        self.viewModel.editBoard(self.viewModel.board, i, j, int(self.board.cells[i][j].text()), False)

            self.genButton.setEnabled(True)
            self.solveButton.setEnabled(True)

    def genButtonEvent(self) -> None:
        emptyPercent = self.emptyPercentSpinbox.value()
        self.viewModel.gen(emptyPercent)

    def solveButtonEvent(self) -> None:
        stepPeriodMs = self.solvePeriodSpinbox.value()
        self.viewModel.solve(stepPeriodMs=stepPeriodMs)
    
    @QtCore.pyqtSlot(BoardUpdateInfo)
    def updateBoardEvent(self, info: BoardUpdateInfo) -> None:
        self.board.cells[info.row][info.col].setText(str(info.val) if info.val != 0 else '')
        self.board.cells[info.row][info.col].setEnabled(info.isEnable)

        if info.isEnable:
            self.board.cells[info.row][info.col].setStyleSheet("color: red;")
        else:
            self.board.cells[info.row][info.col].setStyleSheet("color: white;")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([])
    vm = BoardViewModel()
    win = BoardMainWindow(vm)
    win.setup()
    win.show()
    sys.exit(app.exec())
    
