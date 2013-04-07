from __future__ import print_function
import random
import sys, os


def row_values(board, row, n):
    return [int(board[row][i]) for i in range(n)]


def column_values(board, col, n):
    return [int(board[i][col]) for i in range(n)]


def subsquare_values(board, row, col, m):
    square = int(row / m) * ((m ** 2) / m) + int(col / m)
    s_row = int(square / m) * m
    s_col = (square % m) * m

    return [int(board[s_row + i][s_col + j]) for i in range(0, m) for j in range(0, m)]


def stringify_board(board):
    """ Format the board for outputting """

    output = []
    for line in board:
        tmp = []
        for item in line:
            tmp.append(item)
            tmp.append(' ')
        tmp.append('\n')
        output.append(tmp)

    return ''.join(str(item) for line in output for item in line)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Peter Zenger's Generalized Sedoku board generator")
        print("Usage: %s [num boards] [size of subsquare] [percentage filled]" % sys.argv[0])
        sys.exit(-1)

    boards_total = int(sys.argv[1])
    created = 0
    m = int(sys.argv[2])
    n = m ** 2
    p = float(sys.argv[3]) / 100
    p_int = int(p * 100)

    total_size = m ** 4

    while created < boards_total:
        board = [[0 for _ in range(n)] for _ in range(n)]
        filled = 0.0

        while filled / total_size < p:
            tmp = random.randrange(n) + 1
            tmp_row = random.randrange(n)
            tmp_col = random.randrange(n)
            if tmp not in (
                        row_values(board, tmp_row, n) + column_values(board, tmp_col, n) + subsquare_values(board,
                                                                                                            tmp_row,
                                                                                                            tmp_col,
                                                                                                            m)):
                board[tmp_row][tmp_col] = tmp
                filled += 1

        with open(os.path.join('./boards/generated/', '%db%d.%d.b' % (n, p_int, created)), 'w') as file1:
            file1.write(stringify_board(board))

        created += 1

        #print(stringify_board(board))


if __name__ == "__main__":
    main()