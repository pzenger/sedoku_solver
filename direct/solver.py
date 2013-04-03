# Sedoku Direct Solver
# By Peter Zenger
# April 1, 20

from __future__ import print_function
from copy import deepcopy
import os
import sys
import math

# http://magictour.free.fr/top95
# http://norvig.com/easy50.txt


m = 0
n = 0
numbers = []
to_propagate = []


class Value():
    def __init__(self, value):
        self.possible_values = []
        self.value = int(value)
        self.row = 0
        self.square = 0
        self.column = 0
        self.propagated = False

    def __str__(self):
        return self.value

    def remove_value(self, value):
        if int(value) in self.possible_values:
            self.possible_values.remove(int(value))
        #if not self.propagated and len(self.possible_values) == 1:
        #    self.set_value(self.possible_values[0])
        if not self.propagated and len(self.possible_values) == 0:
            global contradiction
            contradiction = True
            print("CONTRADICTION")

    def set_value(self, value):
        if not self.propagated:
            print("ADING TO PROPOGATE, value: ", value)
            self.value = int(value)
            self.possible_values = [self.value] #added
            to_propagate.append(self)
            self.propagated = True

    def setup(self, row, column):
        self.row = row
        self.column = column
        self.square = compute_square(row, column)
        if self.value > 0:
            self.possible_values = [self.value]
            to_propagate.append(self)
            self.propagated = True
        else:
            self.possible_values = numbers[:]


def init_board(name):
    """
    Loads a board which is defined by an NxN grid in a file
    The board can be formated 'DDDD' or 'D D D D D'
    The board must be of the size M^2 by M^2
    """
    try:
        f = open(os.path.normpath('../boards/' + name), 'r')
        data = f.readlines()

        # If the board is inputed with spaces between numbers (for general
        # form)
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

        f.close()

        global numbers
        global m
        global n

        #m = int(math.sqrt(len(board_2d[0])))  # Size of each subsquare
        n = len(board_2d[0])
        m = int(math.sqrt(n))
        print(len(board_2d[0]))
        #n = pow(m, 2)  # Max number used [1...n]
        numbers = range(1,n+1)

        print(m)
        print(n)
        print(numbers)

        setup_values(board_2d)

        return board_2d
    except IOError:
        print("Error opening '%s', check spelling and try again" % name)
        sys.exit(-1)


def setup_values(board):
    for x in range(n):
        for y in range(n):
            board[x][y].setup(x, y)


def compute_square(row, column):
    """Computes a squares number"""

    square_number = int(row / m) * (n/m) + int(column / m)
    print("s",square_number)
    return square_number


def stringify_board(board):
    """ Turn the board into a string for outputting """

    output = []
    for line in board:
        tmp = []
        for item in line:
            tmp.append(str(item.value))
        tmp.append('\n')
        output.append(tmp)

    return ''.join(str(item) for line in output for item in line)


def propagate(value):
    remove_rows(value.value, value.row)
    remove_columns(value.value, value.column)
    remove_square(value.value, value.square)

    return


def remove_rows(value, row):
    [board[row][col].remove_value(value) for col in xrange(n)]
    return


def remove_columns(value, col):
    [board[row][col].remove_value(value) for row in xrange(n)]
    return


def remove_square(value, square):
    row = int(square / m) * m
    col = (square % m) * m
    if n <= 2:
        return
    [board[row + i][col + j].remove_value(value) for i in range(0,m) for j in range(0,m)]
    return

def add_definite():
    for row in board:
        for item in row:
            if len(item.possible_values) == 1:
               item.set_value(item.possible_values[0])



def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku solver program")
        print("Usage: %s [INPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]

    global contradiction
    contradiction = False

    global board
    board = init_board(input_board)

    propagate_count = 1
    square_count = m ** 4

    branch_boards = []
    #To store, all current values, value of each branch

    solved = False
    while (not contradiction and not solved):
        rounds = 0
        while(rounds < 2 ):
            while (len(to_propagate) > 0):
                propagate(to_propagate.pop())
                propagate_count += 1
                rounds=0
            rounds += 1
            add_definite()


        if propagate_count >= square_count:
            solved = True

        if not solved:
            print("BRANCHING")
            if not contradiction:
                #find lowest # branches not done, add to list
                #to_propagate.extend(get_lowest_possibilities(board))

                saved_board = deepcopy(board)
                to_visit = get_lowest_possibilities()
                for branch in to_visit:
                    branch_boards.append(
                        (saved_board,
                         propagate_count,
                         deepcopy(branch[0]),
                        branch[1])
                    )
                    #make_branches(board)
                    #save_board(board)
            if branch_boards:
                print (branch_boards.pop())
                board, propagate_count, next_value, value = branch_boards.pop()
                contradiction = False

                board[next_value.row][next_value.column].set_value(value)

                #board[next_value.row][next_value.column].set



    if (contradiction):
        print("UNSATISFIABLE")
        print("Partially completed board: ")
    else:
        print("Completed board: ")
    output_board = stringify_board(board)

    print(output_board)
    with open(os.path.normpath('./output/' + input_board + '.sol'), 'w') as f:
        f.write(output_board)


def get_lowest_possibilities():
    low = 1000
    items = []
    for row in board:
        for item in row:
            if item.propagated == False:
                if len(item.possible_values) < low:
                    print("low values: ", low)
                    low = item.value
                    items = [item]
                elif len(item.possible_values) == low:
                    print("second value:", low)
                    items.append(item)

    branches = []
    for item in items:
        for val in item.possible_values:
            branches.append((item, val))
    print("branches: ", branches)
    return branches

if __name__ == "__main__":
    main()
