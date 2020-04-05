# Kira DeGraw, CS580 Assignment 3 - solves Sudoku games with backtracking
import time


def main():
    puzzle = readFile() # get the initial sudoku puzzle
    start = 0
    end = 0
    validInput = 0

    # loop while the user does not enter a valid choice (1 or 2)
    while validInput == 0:
        print("\n1. Naive Backtracking")
        print("2. Smart Backtracking")
        alg = input("Enter the algorithm you want to use: ")

        # 1. Naive Backtracking
        if alg == '1':
            validInput = 1
            start = time.time()
            solveNaive(puzzle) # solve based on naive backtracking
            end = time.time()
            print("\n***** Solved Puzzle *****")
            printPuzzle(puzzle)

        # 2. Smart Backtracking - MRV
        elif alg == '2':
            validInput = 1
            start = time.time()
            solveSmart(puzzle) # solve based on smart backtracking
            end = time.time()
            print("\n***** Solved Puzzle *****")
            printPuzzle(puzzle)
        else:
            print("\nInvalid Input. Enter 1 or 2 for algorithm selection.")

    print("Total Time:", end - start)

# read file to get initial sudoku puzzle
def readFile():
    puzzle = []

    # open file
    f = open("sudokuPuzzle.txt", "r")

    # read initial sudoku puzzle
    lines = f.readlines()[1:]  # skip the first line (name of puzzle)

    # loop through lines in file
    for j in range(len(lines)):
        currentLine = lines[j]  # get the current line

        # add sudoku lines to the puzzle, strip the newline character
        puzzle.append([int(i) for i in str(currentLine.strip())])
    f.close()  # close file

    # print initial board
    print("***** Initial Puzzle *****")
    printPuzzle(puzzle)

    return puzzle


# print sudoku puzzle in a pretty format
    # puzzle = current puzzle, 0 represents a blank number
def printPuzzle(puzzle):
    # loop through length of puzzle
    for i in range(len(puzzle)):
        if i != 0 and i % 3 == 0:
            # print border after every third line before the first index is printed
            print("------------------------")

        # loop through columns in each row
        for j in range(len(puzzle[0])):
            if j != 0 and j % 3 == 0:
                print("| ", end="")  # prints divider, but end doesn't print a newline

            if j != 8:  # not last column
                print(str(puzzle[i][j]) + " ", end="")  # end doesn't print a newline
            else:
                print(puzzle[i][j])


# find an empty square in given puzzle
    # puzzle = current sudoku puzzle board
def getEmptySquare(puzzle):
    # loop through puzzle rows
    for i in range(len(puzzle)):
        # loop through puzzle columns per row
        for j in range(len(puzzle[0])):
            # if puzzle square is 0, that means its blank
            if puzzle[i][j] == 0:
                return i, j  # row, col
    return None


# solve given sudoku puzzle with naive backtracking
    # puzzle = current sudoku board
def solveNaive(puzzle):
    # find an empty square
    empty = getEmptySquare(puzzle)

    # found solution if no empty squares
    if not empty:
        return True
    else:
        row, col = empty  # row and cols for current empty square

    # loop through each possible value 1-9
    for i in range(1, 10):
        # check if possible value is valid
        if valid(puzzle, i, (row, col)):
            # set square to valid value
            puzzle[row][col] = i

            # check if solved, loop through until solved
            if solveNaive(puzzle):
                return True

            # if it doesn't work and ends up not being valid, reset this square to blank
            puzzle[row][col] = 0

    return False


# minimum remaining values: find which empty square has MRV
    # puzzle = current sudoku board
def minOptions(puzzle):
    # set initial variables
    minValidOptions = 100
    minRow = 0
    minCol = 0

    # loop through each row
    for j in range(0, 9):
        # loop through each column
        for k in range(0, 9):
            validOptions = 0  # current number of valid moves for square
            if puzzle[j][k] == 0:  # we only care if the square is blank
                # loop through all possible values
                for i in range(1, 10):
                    # check if possible value is valid
                    if valid(puzzle, i, (j, k)):
                        validOptions += 1  # count number of valid options for current square

                # store the best minimum remaining value
                if validOptions < minValidOptions:
                    # save variable info
                    minValidOptions = validOptions
                    minRow = j
                    minCol = k

    return minRow, minCol


# solve given sudoku puzzle with smart backtracking using minimum remaining value
    # puzzle = current sudoku board
def solveSmart(puzzle):
    # check for an empty square in puzzle
    empty = getEmptySquare(puzzle)
    # solved if none are empty since we made valid moves
    if not empty:
        return True

    # find the row and col with minimum remaining values left
    row, col = minOptions(puzzle)

    # loop through possible values (1-9)
    for i in range(1, 10):
        # check if possible value is valid
        if valid(puzzle, i, (row, col)):
            # set square to valid value
            puzzle[row][col] = i

            # check if it can be solved with that value, loop
            if solveSmart(puzzle):
                return True

            # set square back to empty if not solvable from that value
            puzzle[row][col] = 0

    return False


# check if a certain position is valid
    # puzzle = current sudoku board,
    # value = possible value to check if valid in position
    # position = row, col
def valid(puzzle, value, position):
    # loop through columns
    for i in range(len(puzzle)):
        if puzzle[i][position[1]] == value and position[0] != i:
            return False

    # loop through rows
    for i in range(len(puzzle[0])):
        if puzzle[position[0]][i] == value and position[1] != i:
            return False

    # check each 3x3 square
    squareX = position[1] // 3
    squareY = position[0] // 3

    for i in range(squareY*3, squareY*3 + 3):
        for j in range(squareX * 3, squareX*3 + 3):
            if puzzle[i][j] == value and (i, j) != position:
                return False

    return True


if __name__ == "__main__":
    main()
