from Sudoku import Board

def main() -> None:
    board = Board()
    board.gen(0.5)
    board.printBoard()

if __name__ == '__main__':
    main()
