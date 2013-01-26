# Sedoku Puzzle Solver
# By Peter Zenger
# January 10, 2013

from __future__ import print_function
import sys

#numbers = [1,2,3,4,5,6,7,8,9]

def load_board(name):
    """Loads a board which is defined by a 9x9 grid in a file"""
    try:
        f = open(name, 'r')
        data = f.readlines()
        #If the board is inputed with spaces between numbers (for general form)
        if ' ' in data[0]:
            print("Format 2")
            board_2d = [[int(x) for x in line.split(' ')] for line in data]
        else:
            print("Format 1")
            board_2d = [[int(x) for x in line.strip()] for line in data] 
        f.close()
        return board_2d
    except IOError:
        print("Error opening '%s', check spelling and try again" % name)
        sys.exit(-1)


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


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku 2 SAT program")
        print("Usage: %s [INPUT FILE] [OUTPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]
    output_board = sys.argv[2]

    board = load_board(input_board)
    m = len(board[0]) / 3
    n = pow(m, 6)
    print(board, m, n)

    #Generate Formulas for Each square has value (C111 or C112 or ... or C11N)
    #Number % sqr(m) == n value
    #Generate Forumulas for each row
    #Generate forumulas for each column
    #Generate formulas for each square
    #Parse board to add unit clauses
    #Joing it all together

    """c_list = all_candidates(board)
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
        f.write(output_board)"""

    
if __name__ == "__main__":
    main()
    

