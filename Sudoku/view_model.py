from PyQt6 import QtWidgets, QtCore
from typing import List, Tuple, Dict
import numpy as np
import random


try:
    from Sudoku.update_info import BoardUpdateInfo
    from Sudoku.worker import Worker
except ModuleNotFoundError:
    from update_info import BoardUpdateInfo
    from worker import Worker

class BoardViewModel(QtWidgets.QWidget):
    updateBoardSignal = QtCore.pyqtSignal(BoardUpdateInfo)

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.rows = 9
        self.cols = 9
        self.board = np.zeros((self.rows, self.cols))
    
    def startWorker(self, fn, *args, **kwargs) -> None:
        worker = Worker()
        worker.setFunction(fn, *args, **kwargs)
        thread = QtCore.QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        self.worker = worker
        self.thread = thread

    def solve(self, board: np.ndarray = None, stepPeriodMs: int = 0, runInThread:bool = True) -> None:
        if runInThread:
            self.startWorker(self.solveFunc, board, stepPeriodMs)
        else:
            self.solveFunc(board=board, stepPeriodMs=stepPeriodMs)
    
    def solveFunc(self, board: np.ndarray, stepPeriodMs: int):
        if board != None:
            self.board = board

        newBoard = self.board.copy()
        coordToSolve = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    coordToSolve.append((i, j))

        res = self.solveStep(newBoard, coordToSolve, 0, stepPeriodMs)
        if not res:
            print('Unable to solve Sudoku')

    def solveStep(self, newBoard: np.ndarray, coordToSolve: List[Tuple[int, int]], i, stepPeriodMs: int) -> bool:
        '''
        Solve Sudoku board with backtracking.
        1. Loop through every empty sell.
        2. Find possible choice for that cell.
        '''
        if i > len(coordToSolve) - 1:
            res = self.__isValid(newBoard)

            if res:
                self.board = newBoard
                return True
            else:
                return False
        
        row, col = coordToSolve[i]
        choices = self.__findPossibleChoice(newBoard, row, col)

        for choice in choices:
            if stepPeriodMs > 0:
                QtCore.QThread.msleep(stepPeriodMs)

            info = BoardUpdateInfo(row, col, choice, True)
            self.updateBoardSignal.emit(info)

            newBoard[row][col] = choice
            res = self.solveStep(newBoard, coordToSolve, i + 1, stepPeriodMs)
            if res:
                return True

            if stepPeriodMs > 0:
                QtCore.QThread.msleep(stepPeriodMs)

            newBoard[row][col] = self.board[row][col]
            info.val = self.board[row][col]
            self.updateBoardSignal.emit(info)
        
        return False

    def gen(self, emptyPercent: float, runInThread: bool = True) -> None:
        if runInThread:
            self.startWorker(self.genFunc, emptyPercent)
        else:
            self.genFunc(emptyPercent)
    
    def genFunc(self, emptyPercent: float) -> None:
        if emptyPercent < 0 or emptyPercent > 1:
            raise ValueError('Invalid empty percent value.')

        self.clearBoard()

        allCoordinate = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        newBoard = self.board.copy()
        self.genStep(newBoard, allCoordinate, 0)

        shuffleSudoku(self.board, 20)

        emptyCoordinate = random.sample(allCoordinate, int(emptyPercent * self.rows * self.cols))
        for row, col in emptyCoordinate:
            self.board[row][col] = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                info = BoardUpdateInfo(row, col, self.board[row][col], True if self.board[row][col] == 0 else False)
                self.updateBoardSignal.emit(info)


    def genStep(self, newBoard: np.ndarray, validCoordinate: List[int], i: int) -> bool:
        if i >= len(validCoordinate):
            self.board = newBoard
            return True
        
        row, col = validCoordinate[i]
        choices = self.__findPossibleChoice(newBoard, row, col)

        for choice in choices:
            newBoard[row][col] = choice
            res = self.genStep(newBoard, validCoordinate, i + 1)

            if res:
                return True
            
            newBoard[row][col] = self.board[row][col]
        
        return False
    
    def clearBoard(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.updateBoardSignal.emit(BoardUpdateInfo(i, j, 0, True))
                self.board[i][j] = 0

    def printBoard(self, name: str = '') -> None:
        self.printAnyBoard(self.board, name)
    
    def printAnyBoard(self, board: np.ndarray, name: str = ''):
        if name != '':
            print(f'[{name}]')
        print("-" * (self.cols * 2 + 3))
        for i in range(self.rows):
            if i % 3 == 0 and i != 0:
                print("-" * (self.cols * 2 + 3))
            for j in range(self.cols):
                if j % 3 == 0 and j != 0:
                    print("|", end=' ')
                if board[i][j] == 0:
                    print(".", end=' ')
                else:
                    print(int(board[i][j]), end=' ')
            print('')
        print("-" * (self.cols * 2 + 3))

    def __findPossibleChoice(self, board: np.ndarray, row: int, col: int) -> List[int]:
        possibleChoice = []
        originalValue = board[row][col]
        for num in range(1, 10):
            board[row][col] = num
            if self.__isValid(board):
                possibleChoice.append(num)
        board[row][col] = originalValue
        return possibleChoice

    def __isValid(self, board: np.ndarray) -> bool:
        # Reference from https://www.geeksforgeeks.org/check-if-given-sudoku-board-configuration-is-valid-or-not/.
        # Arrays to track seen numbers in rows,
        # columns, and sub-matrix
        rows = [0] * 9
        cols = [0] * 9
        subMat = [0] * 9

        for i in range(9):
            for j in range(9):
                # Skip empty cells
                num = int(board[i][j])
                if num == 0:
                    continue

                val = num
                pos = 1 << (val - 1)

                # Check for duplicates in the current row
                if (rows[i] & pos) > 0:
                    return False
                rows[i] |= pos

                # Check for duplicates in the current column
                if (cols[j] & pos) > 0:
                    return False
                cols[j] |= pos

                # Calculate the index for the 3x3 sub-matrix
                idx = (i // 3) * 3 + j // 3

                # Check for duplicates in the current sub-matrix
                if (subMat[idx] & pos) > 0:
                    return False
                subMat[idx] |= pos

        return True

def shuffleSudoku(board, numOperations):
    """
    Shuffle a NumPy-based Sudoku board by performing a specified number of random valid operations.

    :param board: The Sudoku board as a 9x9 NumPy array.
    :param numOperations: Number of random operations to perform.
    """
    # Swap rows within a block
    def swapRowsWithinBlock(board):
        block = random.choice([0, 1, 2])
        row1 = random.randint(block * 3, block * 3 + 2)
        row2 = random.randint(block * 3, block * 3 + 2)
        board[[row1, row2]] = board[[row2, row1]]  # Swap rows safely

    # Swap columns within a block
    def swapColumnsWithinBlock(board):
        block = random.choice([0, 1, 2])
        col1 = random.randint(block * 3, block * 3 + 2)
        col2 = random.randint(block * 3, block * 3 + 2)
        board[:, [col1, col2]] = board[:, [col2, col1]]  # Swap columns safely

    # Swap row blocks
    def swapRowBlocks(board):
        block1, block2 = random.sample([0, 1, 2], 2)
        rows1 = slice(block1 * 3, block1 * 3 + 3)
        rows2 = slice(block2 * 3, block2 * 3 + 3)
        board[rows1], board[rows2] = board[rows2].copy(), board[rows1].copy()  # Swap row blocks safely

    # Swap column blocks
    def swapColumnBlocks(board):
        block1, block2 = random.sample([0, 1, 2], 2)
        cols1 = slice(block1 * 3, block1 * 3 + 3)
        cols2 = slice(block2 * 3, block2 * 3 + 3)
        board[:, cols1], board[:, cols2] = board[:, cols2].copy(), board[:, cols1].copy()  # Swap column blocks safely

    # List of valid operations
    operations = [swapRowsWithinBlock, swapColumnsWithinBlock, swapRowBlocks, swapColumnBlocks]

    # Perform the specified number of random operations
    for _ in range(numOperations):
        random.choice(operations)(board)

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    vm = BoardViewModel()
    vm.gen(0.1, runInThread=False)
    vm.printBoard()

    vm.solve(runInThread=False)
    vm.printBoard()

