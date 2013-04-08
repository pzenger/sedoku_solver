# General Sedoku Direct Solver
# By Peter Zenger
# April 1, 20

from __future__ import print_function
from copy import deepcopy
import os, sys, math

m = 0
n = 0
numbers = []


class Value():
    """
    A Value in a square
    Stores its value, possible values location,
    and whether it has been propagted or not
    """

    def __init__(self, value):
        self.possible_values = []
        self.value = int(value)

    def remove_value(self, value):
        """ Removes a value from the set of possible_values """
        if int(value) in self.possible_values:
            self.possible_values.remove(int(value))
            return True
        return False

    def set_value(self, value=-1):
        """ Sets the value and flags Value to have been propagated """
        if value == -1:
            self.value = self.possible_values[0]
        else:
            self.value = int(value)
            self.possible_values = [self.value]  # added

    def setup(self, row, column):
        """
        Compute location of this Value
        Update the possible_values
        """
        self.row = row
        self.column = column
        self.square = compute_square(row, column)
        if self.value > 0:
            self.possible_values = [self.value]
            return True
        else:
            self.possible_values = numbers[:]
            return False


def init_board(name):
    """
    Loads a board which is defined by an NxN grid in a file
    The board can be formated 'DDDD' or 'D D D D D'
    The board must be of the size M^2 by M^2
    """
    try:
        f = open(os.path.normpath('../boards/' + name), 'r')
        data = f.readlines()
        f.close()

        board_2d = []
        formatting = True
        if ' ' in data[0]:
            formatting = False

        for line in data:
            new_row = []

            if formatting:
                for x in line.strip():
                    new_row.append(Value(x))
            else:
                for x in line.strip().split(' '):
                    new_row.append(Value(x))

            board_2d.append(new_row)

        global numbers, m, n

        n = len(board_2d[0])        # Size of each side of the square
        m = int(math.sqrt(n))       # Size of each subsquare
        numbers = range(1, n + 1)   # Possible values for a square to have

        # Setup each square of the board
        for row in range(n):
            for col in range(n):
                if board_2d[row][col].setup(row, col):
                    to_visit.append(board_2d[row][col])

        return board_2d

    except IOError:
        print("Error opening '%s', check spelling and try again" % name)
        sys.exit(-1)


def compute_square(row, column):
    """Computes which sub-square number the square resides in"""

    square_number = int(row / m) * (n / m) + int(column / m)
    return square_number


def stringify_board(board):
    """ Turn the board into a string for outputting """

    output = []
    for line in board:
        tmp = []
        for item in line:
            tmp.append(str(item.value))
            tmp.append(' ')
        tmp.append('\n')
        output.append(tmp)

    return ''.join(str(item) for line in output for item in line)


def propagate(value):
    """ Removes possible values from each intersecting square """
    # Value is object

    remove_rows(value.value, value.row)
    remove_columns(value.value, value.column)
    remove_square(value.value, value.square)

    return

# Do something to only grab unfilled values
def remove_rows(value, row):
    return [board[row][col].remove_value(value) for col in xrange(n)]


def remove_columns(value, col):
    return [board[row][col].remove_value(value) for row in xrange(n)]


def remove_square(value, square):
    row = int(square / m) * m
    col = (square % m) * m
    if n <= 2:
        return
    return [board[row + i][col + j].remove_value(value) for i in range(0, m) for j in range(0, m)]


def get_lowest_possibility():
    """ Returns the square that has the least number of possibilities"""
    low = 10000
    low_item = None
    for row in board:
        for item in row:
            if int(item.value) == 0:
                if len(item.possible_values) < low:
                    low = len(item.possible_values)
                    low_item = item

    if low_item:
        return [low_item]
    else:
        return None


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku solver program")
        print("Usage: %s [INPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]

    global board, to_visit
    contradiction = False
    to_visit = []   # List of nodes to propagate

    board = init_board(input_board)

    filled_count = 0
    total_count = m ** 4

    branch_boards = []

    solved = False
    while (not contradiction and not solved):
        if to_visit:
            for item in to_visit:
                if len(item.possible_values) == 0:
                    contradiction = True
                elif len(item.possible_values) == 1:
                    item.set_value()
                    propagate(item)
                    filled_count += 1
                else:

                    # Save each branch except the first
                    for v in item.possible_values[1:]:
                        branch_boards.append(
                            (deepcopy(board),
                             filled_count,
                             deepcopy(item),
                             v)
                        )

                    # Explore first branch
                    item.set_value(item.possible_values[0])
                    propagate(item)
                    filled_count += 1

        to_visit = get_lowest_possibility()

        if contradiction and len(branch_boards) > 0:
            # If there are unexplored branches, explore them
            board, filled_count, next_value, value = branch_boards.pop()

           # print("Branching: %d unexplored" % len(branch_boards))

            board[next_value.row][next_value.column].set_value(value)
            to_visit = [board[next_value.row][next_value.column]]

            contradiction = False

        # If the # of filled squares equals the total squares, the puzzle is solved
        if filled_count >= total_count:
            solved = True

    if contradiction:
        print("!!! UNSATISFIABLE !!!")
    else:
        print("Completed board: ")
        output_board = stringify_board(board)

        print(output_board)


if __name__ == "__main__":
    import time
    time1 = time.time()
    main()
    time2 = time.time()
    print(time2 - time1)
