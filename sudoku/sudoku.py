#!/usr/bin/env python
#coding:utf-8


import time
import numpy as np
from solver import Solver

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solve = Solver(board)
    solve.solve()
    solved_board = solve.to_dict()
    return solved_board


if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    times = []

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        # print_board(board)

        start_time = time.time()
        # Solve with backtracking
        solved_board = backtracking(board)
        end_time = time.time()

        # Print solved board. TODO: Comment this out when timing runs.
        # print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

        times.append(end_time-start_time)

    print("Finishing all boards in file.")
    print("running time statistics:")
    print("min: ",min(times))
    print("max: ",max(times))
    print("mean: ",np.mean(times))
    print("standard deviation: ",np.std(times))