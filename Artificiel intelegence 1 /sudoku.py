"""Sudoku backtracking"""
import time

with open('Assignment 2 sudoku.txt', 'r') as f:
    lines = f.readlines()

# read all sudokus and ID from file
puzzles = []
current_puzzle = []
labels = []

# read all sudokus from the file
for line in lines:
    line = line.strip()
    if line.startswith("SUDOKU"):
        labels.append(line)
        if current_puzzle:
            puzzles.append(current_puzzle)
        current_puzzle = []
    elif line.isdigit() and len(line) == 9:
        current_puzzle.append([int(char) for char in line])
if current_puzzle:
    puzzles.append(current_puzzle)

def safe_opt(mat, row, col, num): # function for finding safe options
    
    for i in range(9): # 1-9 is available numbers to use
        if mat[row][i] == num: # check if the number already exists in row
            return False # no optional solution
    for i in range(9):
        if mat[i][col] == num: # check if number already exists in column
            return False
        
    startRow = row - row % 3  # starting row index of the box 
    startCol = col - col % 3  # starting column index of the box 
    for j in range(3):  # loop over rows of the 3x3 box
        for k in range(3):  # loop over columns of the 3x3 box
            if mat[j + startRow][k + startCol] == num:  # check if the number already exists in the 3x3 box
                return False
    return True
def insert_num(mat, row, col, num): # insert valid number at row and col
    
    if mat[row][col] != 0: # checks if matrix row and col isn't equal to 0
        return [] # returns empty list
    valid_numbers = [] # valid numbers
    for num in range(1, 10): # 1-9 numbers 
        if safe_opt(mat, row, col, num): # safe_opt 
            valid_numbers.append(num) # append valid numbers to num variable
        return valid_numbers # return valid numbers

# Recursive backtracking function that attempts to fill the Sudoku board
def solve_sudoku(mat, row=0, col=0):
    if row == 9:  # if we have filled all rows, the puzzle is solved
        return True
    if col == 9:  # if we reach the end of a row, move to the next row
        return solve_sudoku(mat, row + 1, 0)
    if mat[row][col] != 0:  # skip cells that already have a number
        return solve_sudoku(mat, row, col + 1)
    for num in range(1, 10):  # try placing numbers 1 through 
        if safe_opt(mat, row, col, num):  # check if number is valid at this position
            mat[row][col] = num  # tentatively place the number
            if solve_sudoku(mat, row, col + 1):  # continue solving for the next cell
                return True
            mat[row][col] = 0  # backtrack if placing the number didn’t lead to a solution
    return False

start_time = time.time()
# Solve each sudoku and print result
for idx, (label, mat) in enumerate(zip(labels, puzzles), 1):
    
    print(f"\n{label} - Original:")
    for row in mat:
        print(row)
    
    if solve_sudoku(mat):
        print(f"{label} - Solved:")
        for row in mat:
    
            print(row)
    else:
        print(f"{label} - No solution")

end_time = time.time()
print(f"Executed time {end_time - start_time:.4f} seconds")