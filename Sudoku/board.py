from typing import Dict
import numpy as np
import random
import timeit

class Board:
    def __init__(self) -> None:
        self.rows = 9
        self.cols = 9
        self.board = np.zeros((self.rows, self.cols))
    
    def solve(self) -> None:
        pass

    def solveStep(self) -> None:
        pass

    def gen(self, validPercent: float) -> None:
        if validPercent < 0 or validPercent > 1:
            raise ValueError('Invalid empty percent value.')

        validNumber = int(self.rows * self.cols * validPercent)
        allCoordinate = [(row, col) for row in range(self.rows) for col in range(self.cols)]
        validCoordiate = random.sample(allCoordinate, validNumber)

        for row, col in validCoordiate:
            self.board[row][col] = random.randint(1, 9)

            while not self.__isValid(row, col):
                self.board[row][col] = random.randint(1, 9)

    def printBoard(self) -> None:
        print("-" * (self.cols * 2 + 3))
        for i in range(self.rows):
            if i % 3 == 0 and i != 0:
                print("-" * (self.cols * 2 + 3))
            for j in range(self.cols):
                if j % 3 == 0 and j != 0:
                    print("|", end=' ')
                if self.board[i][j] == 0:
                    print(".", end=' ')
                else:
                    print(int(self.board[i][j]), end=' ')
            print('')
        print("-" * (self.cols * 2 + 3))
    

    def __isValid(self, row: int, col: int) -> bool:
        '''
        Sudoku is valid if:
        1. No repeating number in every row.
        2. No repeating number in every col.
        3. No repeating number in every block.
        '''

        occur: Dict[int, int] = {}
        for i in range(self.rows):
            num = self.board[i][col]

            if num == 0:
                continue
            if num in occur:
                return False
            occur[num] = 1
        
        occur.clear()
        for j in range(self.cols):
            num = self.board[row][j]

            if num == 0:
                continue
            if num in occur:
                return False
            occur[num] = 1
        
        occur.clear()
        rowStart = (row // 3) * 3
        colStart = (col // 3) * 3

        for i in range(rowStart, rowStart + 3, 1):
            for j in range(colStart, colStart + 3, 1):
                num = self.board[i][j]

                if num == 0:
                    continue
                if num in occur:
                    return False
                occur[num] = 1

        return True

if __name__ == '__main__':
    board = Board()
    board.gen(0.5)
    board.printBoard()
