from __future__ import print_function
import sys, os, math


def get_boards(directory):
    # Return the names of the boards within a directory

    return [f for f in os.listdir(directory) if f[-2:] == '.b']


def translate(board):
    #Translate the board to Enfragmo specification

    n = len(board[0])
    numbers = range(1, n + 1)
    m = math.sqrt(n)
    enfragmo_board = ""
    enfragmo_board += "TYPE INT [ %d.. %d]\n" % (numbers[0], numbers[-1])
    enfragmo_board += "PREDICATE Filled\n"
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                enfragmo_board += "(%d,%d,%d)\n" % (i+1, j+1, board[i][j])
        enfragmo_board += "\n"

    enfragmo_board += "\n"
    enfragmo_board += "FUNCTION N\n"
    enfragmo_board += "( : %d )" % m

    return enfragmo_board


def load_board(directory, board):
    # Load the board into a list of lists

    try:
        with open(os.path.normpath('%s/%s' % (directory, board)), 'r') as f:
            data = f.readlines()
        board_2d = []
        formatting = True
        if ' ' in data[0]:
            formatting = False
        for line in data:
            new_row = []
            if formatting:
                for x in line.strip():
                    new_row.append(int(x))
            else:
                for x in line.strip().split(' '):
                    new_row.append(int(x))
            board_2d.append(new_row)
        return board_2d
    except IOError:
        print("Error opening '%s', check spelling and try again" % board)
        sys.exit(-1)

def save_boards(directory, boards):
    # Save the enfragmo boards into an enfragmo directory

    if not os.path.exists(os.path.normpath('%s/enfragmo' % directory)):
        print('Creating Enfragmo folder')
        os.makedirs(os.path.normpath('%s/enfragmo' % directory))

    for board in boards:
        with open(os.path.normpath('%s/enfragmo/%s' %(directory, board[1][:-2]+'.I')), 'w') as f:
            f.write(board[0])


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Peter Zenger's Enfragmo board translator")
        print("Usage: %s [Family directory within boards folder]" % sys.argv[0])
        print("Output: In the folder an enfragmo folder with all translated boards")
        sys.exit(-1)

    directory = os.path.normpath('./boards/%s' % sys.argv[1])

    #load each board and translate it
    board_list = get_boards(directory)
    translated_boards = [translate(load_board(directory, board)) for board in board_list]

    save_boards(directory, zip(translated_boards, board_list))
    print("SUCCESS")


if __name__ == '__main__':
    main()

