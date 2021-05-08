import unittest


def solution(src, dest):
    """
    Solve a movement puzzle in order to cross the floor.

    The function returns an integer representing the smallest number of moves it will take for you to travel from
    the source square to the destination square using a chess knight's moves (that is, two squares in any direction
    immediately followed by one square perpendicular to that direction, or vice versa, in an "L" shape).

    Both the source and destination squares will be an integer between 0 and 63, inclusive.

    :param src: the source square, on which you start
    :param dest: the destination square, which is where you need to land to solve the puzzle
    :return: an integer representing the smallest number of moves it will take to travel from the source square to the destination square using a chess knight's moves
    """
    if src < 0 or src > 63:
        return 0

    if dest < 0 or dest > 63:
        return 0

    board = []
    row_size = 8
    col_size = 8

    # initialise the board
    for move in range(row_size):
        row = []
        for j in range(col_size):
            row.append(None)
        board.append(row)

    # Get the x and y coordinates of the src and dest, respectively
    source_x = src / row_size
    source_y = src % col_size
    destination_x = dest / row_size
    destination_y = dest % col_size

    # initialize 'board' with the coordinates of the src square
    board[source_x][source_y] = 0

    # Define the legal moves for a chess knight
    knight_moves = [
        [1, 2], [1, -2],
        [-1, 2], [-1, -2],
        [2, 1], [2, -1],
        [-2, 1], [-2, -1]
    ]

    # Number of reachable_squares_coords from source_x to source_y is 0
    reachable_squares_coords = [(source_x, source_y)]

    while reachable_squares_coords:
        # get the coords of the top square
        x, y = reachable_squares_coords.pop(0)

        # for each legal move
        for move in knight_moves:
            row, col = x + move[0], y + move[1]

            # if row and col are both within the defined boundaries of the board
            if 0 <= row < row_size and 0 <= col < col_size:

                # if we have not yet visited this square
                if board[row][col] is None:
                    # set the value of the square
                    board[row][col] = board[x][y] + 1

                    # record the coordinate of this square, which is reachable from the src square
                    reachable_squares_coords.append((row, col))

    # the number of moves is the value stored in the destination square
    num_moves = board[destination_x][destination_y]

    return num_moves


class ChessMoveTests(unittest.TestCase):

    def test_from_0_to_1(self):
        source_square = 0
        destination_square = 1
        expected_moves = 3

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_19_to_36(self):
        source_square = 19
        destination_square = 36
        expected_moves = 1

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_63_to_53(self):
        source_square = 63
        destination_square = 53
        expected_moves = 1

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_63_to_36(self):
        source_square = 63
        destination_square = 36
        expected_moves = 2

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_7_to_55(self):
        source_square = 7
        destination_square = 55
        expected_moves = 4

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_12_to_22(self):
        source_square = 12
        destination_square = 22
        expected_moves = 1

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_13_to_23(self):
        source_square = 13
        destination_square = 23
        expected_moves = 1

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_from_14_to_24(self):
        source_square = 14
        destination_square = 24
        expected_moves = 4

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_negative_src(self):
        source_square = -7
        destination_square = 55
        expected_moves = 0

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_negative_dest(self):
        source_square = 7
        destination_square = -55
        expected_moves = 0

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_src_too_large(self):
        source_square = 75
        destination_square = 55
        expected_moves = 0

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)

    def test_dest_too_large(self):
        source_square = 7
        destination_square = 65
        expected_moves = 0

        moves = solution(source_square, destination_square)
        self.assertEqual(expected_moves, moves)
