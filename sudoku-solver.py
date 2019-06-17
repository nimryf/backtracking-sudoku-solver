import numpy as np


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array of integers
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    if run_algorithm(sudoku):
        return sudoku
    else:
        for i in range(0, 9):
            for j in range(0, 9):
                if sudoku[i][j] == 0:
                    sudoku[i][j] = -1
        return sudoku


def test_solver():
    """
    Tests whether the solver works by comparing its solution with the given solution.
    """
    try:
        sudokus = np.load("resources/data/sudokus.npy")
        solutions = np.load("resources/data/solutions.npy")
    except:
        print("Sudokus not found or invalid.")
        return False

    if np.array_equal(sudoku_solver(sudokus[0]), solutions[0]):
        print("Sample puzzle solved successfully.")
        return True
    else:
        print("Something went wrong...")
        return False


def test_waters():
    """
    Tests that sudokus and their solutions are available.
    It is not used anywhere, but it can be useful to understand this code.
    """
    # Load sudokus
    sudokus = np.load("resources/data/sudokus.npy")
    print("Shape of sudokus array:", sudokus.shape,
          "; Type of array values:", sudokus.dtype)

    # Load solutions
    solutions = np.load("resources/data/solutions.npy")
    print("Shape of solutions array:", solutions.shape,
          "; Type of array values:", solutions.dtype, "\n")

    # Print the first sudoku...
    print("Sudoku #1:")
    print(sudokus[0], "\n")

    # ...and its solution
    print("Solution of Sudoku #1:")
    print(solutions[0])


def locateSquareHelper(x):
    """
    Helps find square units, the nine 3x3 cells in a puzzle, in which a cell is in.

    Input
        x : row or column index of the cell in the puzzle.

    Output
        x : location of square unit, specifically the first cell of the unit.
    """
    if x < 6:
        if x < 3:
            x = 0
        else:
            x = 3
    else:
        x = 6
    return x


def getSquareUnit(sudoku, i, j):
    """
    Finds a cell's peers in the square unit that it is in.
    Peers are the other numbers in the puzzle.

    Input
        sudoku : 9x9 numpy array of integers.
        i, j : row and column indices of cell in the puzzle.

    Output
        temp_square : numpy list of the cell's peers.
    """
    temp_square = []
    i = locateSquareHelper(i)
    j = locateSquareHelper(j)

    for x in range(i, i+3):
        for y in range(j, j+3):
            temp_square.append(sudoku[x][y])
    return temp_square


def getRowUnit(sudoku, i):
    """
    Finds a cell's peers in the row that it is in.
    Peers are the other numbers in the puzzle.

    Input
        sudoku : 9x9 numpy array of integers.
        i: row index of cell in the puzzle.

    Output
        temp_row : numpy list of the cell's peers in the specified row.
    """
    temp_row = []
    for y in range(0, 9):
        temp_row.append(sudoku[i][y])
    return temp_row


def getColumnUnit(sudoku, j):
    """
    Finds a cell's peers in the square unit that it is in.
    Peers are the other numbers in the puzzle.

    Input
        sudoku : 9x9 numpy array of integers.
        j : column index of cell in the puzzle.

    Output
        temp_column : numpy list of the cell's peers in the specified column.
    """
    temp_column = []
    for x in range(0, 9):
        temp_column.append(sudoku[x][j])
    return temp_column


def findBlankCell(sudoku, blank_cell):
    """
    Finds the next blank cell in the puzzle.

    Input
        sudoku : 9x9 numpy array of integers, the puzzle.
        blank_cell : location of the blank cell in the puzzle.

    Output
        True or false, depending on whether a blank cell was found.
        blank_cell is set to the location if True.
    """
    for i in range(0, 9):
        for j in range(0, 9):
            if(sudoku[i][j] == 0):
                blank_cell[0] = i
                blank_cell[1] = j
                return True
    return False


def validateMove(sudoku, i, j, num):
    """
    Validates the placement of a number in the puzzle, according to the game's rules.

    Input
        sudoku : 9x9 numpy array of integers; the puzzle being solved.
        i, j : location of current square in the puzzle.
        num : the number to be placed at the square (1-9).

    Output
        True or false, depending whether the move is valid or not.
    """
    row_peers = getRowUnit(sudoku, i)
    col_peers = getColumnUnit(sudoku, j)
    sqr_peers = getSquareUnit(sudoku, i, j)
    if row_peers.count(num) > 0 or col_peers.count(num) > 0 or sqr_peers.count(num) > 0:
        return False
    else:
        return True


def run_algorithm(sudoku):
    """
    Runs a backtracking algorithm to solve the input puzzle.

    Input
        sudoku : 9x9 numpy array of integers; an unsolved sudoku puzzle.

    Output
        The puzzle is solved and true is returned if there is a solution.

        If there is no solution, false is returned. 
    """
    blank_cell = [0, 0]

    if not findBlankCell(sudoku, blank_cell):
        return True

    i = blank_cell[0]
    j = blank_cell[1]

    for num in range(1, 10):
        if(validateMove(sudoku, i, j, num)):
            sudoku[i][j] = num

            if(run_algorithm(sudoku)):
                return True

            sudoku[i][j] = 0
    return False


# test_solver()
