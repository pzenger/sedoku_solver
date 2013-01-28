# Sedoku Puzzle to SAT converter
# By Peter Zenger
# January 25, 2013

from __future__ import print_function
import sys, math

def load_board(name):
    """Loads a board which is defined by a 9x9 grid in a file"""
    try:
        f = open(name, 'r')
        data = f.readlines()

        #If the board is inputed with spaces between numbers (for general form)
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

def stringify_board(board):
    """ Turn the board into a string for outputting """
    return ''.join(str(item) for line in board for item in line)

def generate_row_pairs(n):
    """Generates a list of lists, 
    Where each of the inner lists is a clause which restricts the values within a row.
    The overall list contains all the clauses which allow a value to
    only appear once in any row."""
    res = []

    for r in xrange(n): #Row
        for c in xrange(n): #Column
            for v in xrange(n): #Value
                for o in range(c+1,n): #Other cell
                    lhs = (r*n**2)+c*n+v+1
                    rhs = (r*n**2)+o*n+v+1

                    clause = [lhs*-1, rhs*-1]
                    res.append(clause)

    return res

def generate_column_pairs(n):
    """Generates a list of lists, 
    Where each of the inner lists is a clause which restricts the values within a column.
    The overall list contains all the clauses which allow a value to
    only appear once in any column."""
    res = []

    for c in xrange(n): #Column
        for r in xrange(n): #Row
            for v in xrange(n): #Value
                for o in range(r+1, n): #Other cell
                    lhs = (r*n**2)+c*n+v+1
                    rhs = o*n**2+c*n+v+1

                    clause = [lhs*-1, rhs*-1]
                    res.append(clause)
    return res

def generate_square_pairs(n):
    """ Generates a list of lists,
    Where the inner lists are the atoms for the clauses which restrict
    values within the subsquares"""

    s = int(math.sqrt(n))

    res = []

    for x in xrange(s): #for each square in a row
        for k in xrange(s): #for each square in a column
            for i in xrange(s): #row within square
                for j in xrange(s): #column within square
                    for v in xrange(n): #value of cell
                        for oi in xrange(s): #other cells row
                            for oj in xrange(s): #other cells column
                                if oi <= i and oj <= j:
                                    pass
                                else:
                                    square_value = (x*n*n*s) + (n*s*k)
                                    lhs = square_value + (i*n*n) + (j*n) + v + 1
                                    rhs = square_value + (oi*n*n) + (oj*n) + v + 1

                                    clause = [lhs*-1, rhs*-1]
                                    res.append(clause)
    return res

def generate_unit_clauses(board):
    """Find the initial unit clauses
    Based on what is already filled in on the input board"""

    res = []

    n = len(board)
    for i in xrange(n):
        for j in xrange(n):
            if board[i][j].isdigit():
                print ("b",board[i][j])
    return res

def format_clauses(clauses):
    """ Format clauses for desired output
    In this case, add a 0 to the end of each one"""

    fixed_clauses = [x+[0] for x in clauses]
    return fixed_clauses

def create_report(clauses, out_filename):
    pass

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print("Peter Zenger's Sedoku 2 SAT program")
        print("Usage: %s [INPUT FILE] [OUTPUT FILE]" % sys.argv[0])
        sys.exit(-1)

    input_board = sys.argv[1]
    output_filename = sys.argv[2]

    board = load_board(input_board)
    m = int(math.sqrt(len(board[0])))   #Size of each subsquare
    n = pow(m, 2)                   #Max number used [1...n]
    cells = pow(m, 4)               #Total number of cells
    total = pow(m, 6)               #Total number of variables
    print(board, m, n)

    #List of lists for all holds all the atoms for each cell
    #eg. [[1,2...9],[10,11...18], ... [721,722...729]]
    ensure_colour_clauses = [[x+(y*n)+1 for x in xrange(n)] for y in xrange(cells)]
    row_clauses = generate_row_pairs(n)
    column_clauses = generate_column_pairs(n)
    square_clauses = generate_square_pairs(n)
    unit_clauses = generate_unit_clauses(board)

    all_clauses = ensure_colour_clauses + row_clauses + column_clauses + square_clauses


    #print(ensure_colour_clauses)
    #print(square_clauses)
    #print(len(all_clauses))
    print("%s" % "--"*50)
    

    all_clauses = format_clauses(all_clauses)
    #print(all_clauses)

    create_report(all_clauses, output_filename)


    #Parse board to add unit clauses
    #report

   
    
if __name__ == "__main__":
    main()
    

