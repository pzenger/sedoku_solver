Solver 1:
    Very little information is stored.  Just a 2D list of ints to represent the board
    Need to compute all possible values for all unfilled squares each time.

Solver 2:
    Each square has an object which keeps track of it's value and what it's possible values are.
    Much faster than Solver 1, especially if there is backtracking

Solver 3:
    Additionally stores which cells of the board still need a value.
    Saves an O(n) scan of the board each time a value is added.
    About 10% faster than solver 2
