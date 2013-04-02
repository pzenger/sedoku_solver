# Sedoku Direct Solver
# By Peter Zenger
# April 1, 20

from __future__ import print_function
import os
import sys
import math

m = 0
n = 0
cells = 0
nvar = 0
numbers = []


def load_board(name):
    """
    Loads a board which is defined by an NxN grid in a file
    The board can be formated 'DDDD' or 'D D D D D'
    The board must be of the size M^2 by M^2
    """
    try:
        f = open(os.path.normpath('../boards/'+name), 'r')
        data = f.readlines()

        # If the board is inputed with spaces between numbers (for general
        # form)
        if ' ' in data[0]:
            print("Format 2")
            board_2d = [[x for x in line.split(' ')] for line in data]
        else:
            print("Format 1")
            board_2d = [[x for x in line.strip()] for line in data]
        f.close()
        return board_2d
    except IOError:
        print("Error opening '%s', check spelling and try again" % name)
        sys.exit(-1)


def row(board, x):
    """Returns all integers of a row"""
    return [int(board[x][i]) for i in xrange(n)]


def col(board, x):
    """returns all integers of a column"""
    return [int(board[i][x]) for i in xrange(n)]


def square(board, x):
    """Returns the integer values in a 3x3 square
    Top left is 0, top right is 2, bottom left is 6 etc"""

    row = int(x/m)*m
    col = (x % m)*m
    return [int(board[row+i][col+j]) for i in xrange(m) for j in xrange(m)]


def compute_square(row, column):
    """Computes a squares number"""

    square_number = int(row/m)*m + int(column/m)
    return square_number


def candidates(board, r, c):
    """Returns all of the possible numbers for a specific cell"""

    if int(board[r][c]) <= 0:
        return [i for i in numbers
                if i not in row(board, r)
                and i not in col(board, c)
                and i not in square(board, compute_square(r, c))]
    else:
        return []


def get_candidates(board):
    """Returned all the candidate numbers for every spot which does not yet have a value"""

    #Merge possible and filtered into 1 call
    possible = [(candidates(board, x, y), x, y)
                for x in xrange(n)
                for y in xrange(n)]

    print(possible)

    filtered = [x for x in possible if len(x[0]) > 0]

    print(filtered)

    sorted_possible = sorted(filtered,
                             lambda x, y: 1 if len(x[0]) > len(y[0])
                             else -1 if len(y[0]) > len(x[0])
                             else 0)
    return sorted_possible


def stringify_board(board):
    """ Turn the board into a string for outputting """

    for line in board:
        line.append('\n')
    return ''.join(str(item) for line in board for item in line)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku solver program")
        print("Usage: %s [INPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]
    board = load_board(input_board)

    global numbers
    global m
    global n

    m = int(math.sqrt(len(board[0])))  # Size of each subsquare
    n = pow(m, 2)  # Max number used [1...n]
    numbers = range(1, n+1)

    candidate_list = get_candidates(board)
    while len(candidate_list) > 0:
        r = candidate_list[0][1]
        c = candidate_list[0][2]

        # Takes first value. Todo: If more than 1 option, save board state and try.
        # If it fails, go back to last board state
        # fail if impossible, => No candidates left to try
        value = candidate_list[0][0][0]
        board[r][c] = value
        candidate_list = get_candidates(board)

    output_board = stringify_board(board)

    print("Completed board: ")
    print(output_board)
    with open(os.path.normpath('./output/'+input_board+'.sol'), 'w') as f:
        f.write(output_board)

if __name__ == "__main__":
    main()
