# Sedoku Puzzle Solver
# By Peter Zenger
# January 10, 2013

numbers = [1,2,3,4,5,6,7,8,9]

def load_board(name):
    """Loads a board which is defined by a 9x9 grid in a file"""
    f = open(name)
    return [[f.read(1) for i in xrange(10)] for i in xrange(9)]


def row(board, x):
    """Returns all integers of a row"""
    return [int(board[x][i]) for i in xrange(9)]

def col(board, x):
    """returns all integers of a column"""
    return [int(board[i][x]) for i in xrange(9)]

def square(b, x, y = -1):
    """Returns the integer values in a 3x3 square
    Top left is 0, top right is 2, bottom left is 6 etc"""
    if y >= 0:
        if x < 3:
            x = int(y/3)
        elif x < 6:
            x = 3 + int(y/3)
        else:
            x = int(y/3)+ 6
    row = int(x/3)*3
    col = (x % 3)*3
    return [int(b[row+i][col+j]) for i in xrange(3) for j in xrange(3)]

def candidates(board, r, c):
    """Returns all of the possible numbers for a specific cell"""
    if int(board[r][c]) == 0:
        return [i for i in numbers if i not in row(board, r) and i not in col(board, c) and i not in square(board, r, c)]
    else:
        return []

def all_candidates(board):
    """Returned all the candidate numbers for every spot which does not yet have a value"""
    possible = [(candidates(board, x, y), x, y) for x in xrange(9) for y in xrange(9)]
    filtered = [x for x in possible if len(x[0]) > 0]
    sorted_possible = sorted(filtered, lambda x,y: 1 if len(x[0]) > len(y[0]) else -1 if len(y[0]) > len(x[0]) else 0)
    return sorted_possible

def stringify_board(board):
    """ Turn the board into a string for outputting """
    return ''.join(str(item) for line in board for item in line)
    
if __name__ == "__main__":
    file_name = "board1.board"
    board = load_board(file_name)
    c_list = all_candidates(board)
    while len(c_list) > 0:
        r = c_list[0][1]
        c = c_list[0][2]
        value = c_list[0][0][0]
        board[r][c] = value
        c_list = all_candidates(board)
   
    output_board = stringify_board(board)

    print "Completed board: "
    print output_board
    with open(file_name+".sol", 'w') as f:
        f.write(output_board)

