# Sedoku Puzzle Solver
# By Peter Zenger
# January 10, 2013

import sys, os, math, copy

global m
global n
global numbers

m = 0
n = 0
numbers = []


def load_board(name):
    try:
        with open(os.path.normpath('../boards/' + name), 'r') as f:
            data = f.readlines()

        board_2d = []
        formatting = True
        if ' ' in data[0]:
            formatting = False

        for line in data:
            new_row = []

            if formatting:
                for x in line.strip():
                    new_row.append(x)
            else:
                for x in line.strip().split(' '):
                    new_row.append(x)

            board_2d.append(new_row)

        global numbers, m, n

        n = len(board_2d[0])        # Size of each side of the square
        m = int(math.sqrt(n))       # Size of each subsquare
        numbers = range(1, n + 1)   # Possible values for a square to have

        return board_2d

    except IOError:
        print("Error opening '%s', check spelling and try again" % name)
        sys.exit(-1)


def row(board, row):
    """Returns all integers of a row"""

    return [int(board[row][i]) for i in xrange(n)]


def col(board, col):
    """returns all integers of a column"""

    return [int(board[i][col]) for i in xrange(n)]


def compute_square(row, column):
    """Computes which sub-square number the square resides in"""

    square_number = int(row / m) * (n / m) + int(column / m)
    return square_number


def square(board, square):
    """ Returns all values within a subsquare """

    row = int(square / m) * m
    col = int(square % m) * m
    return [int(board[row + i][col + j]) for i in range(m) for j in range(m)]


def candidates(board, r, c):
    """Returns all of the possible numbers for a specific cell"""

    if int(board[r][c]) == 0:
        return [i for i in numbers if
                i not in row(board, r) and i not in col(board, c) and i not in square(board, compute_square(r, c))]
    else:
        return []


def all_candidates(board):
    """Returned all the candidate numbers for every spot which does not yet have a value"""

    possible = [(candidates(board, row, col), row, col) for row in range(n) for col in range(n) if
                int(board[row][col]) == 0]
    filtered = [x for x in possible if len(x[0]) > 0]

    #Sort such that shorted possible lists first
    sorted_possible = sorted(possible, lambda x, y: 1 if len(x[0]) > len(y[0]) else -1 if len(y[0]) > len(x[0]) else 0)
    return sorted_possible


def solved(board):
    """Check if the board is solved or not"""

    for row in board:
        for item in row:
            if int(item) == 0:
                return False
    return True


def stringify_board(board):
    """ Turn the board into a string for outputting """

    output = []
    for line in board:
        tmp = []
        for item in line:
            tmp.append(str(item))
            tmp.append(' ')
        tmp.append('\n')
        output.append(tmp)

    return ''.join(str(item) for line in output for item in line)

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku solver program")
        print("Usage: %s [INPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]

    board = load_board(input_board)
    branch_boards = []
    contradiction = False

    while not contradiction and not solved(board):

        c_list = all_candidates(board)

        if len(c_list[0][0]) == 0:
            contradiction = True

        elif len(c_list[0][0]) == 1:
            r = c_list[0][1]
            c = c_list[0][2]
            value = c_list[0][0][0]
            board[r][c] = value
            #c_list = all_candidates(board)

        # Or else create a branch for each possibility
        else:
            for v in c_list[0][0][1:]:
                branch_boards.append(
                    (copy.deepcopy(board),
                     c_list[0][1],
                     c_list[0][2],
                     v)
                )

            # Explore first branch
            board[c_list[0][1]][c_list[0][2]] = c_list[0][0][0]
            #c_list = all_candidates(board)

        if contradiction and len(branch_boards) > 0:
            board, next_row, next_col, value = branch_boards.pop()

            #print("Branching: %d unexplored" % len(branch_boards))

            board[next_row][next_col] = value

            contradiction = False



    if contradiction:
        print("UNSATISFIABLE")
    else:
        print("Completed board: ")
        output_board = stringify_board(board)
        print(output_board)
    #with open(input_board + ".sol", 'w') as f:
    #    f.write(output_board)



if __name__ == "__main__":


    import time

    time1 = time.time()
    main()
    time2 = time.time()
    print(time2 - time1)