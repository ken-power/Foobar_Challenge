# Don't Get Volunteered: Finding the shortest path for a chess knight

## The problem

As a henchman on Commander Lambda's space station, you're expected to be resourceful, smart, and a quick thinker. It's not easy building a doomsday device and ordering the bunnies around at the same time, after all! In order to make sure that everyone is sufficiently quick-witted, Commander Lambda has installed new flooring outside the henchman dormitories. It looks like a chessboard, and every morning and evening you have to solve a new movement puzzle in order to cross the floor. That would be fine if you got to be the rook or the queen, but instead, you have to be the knight. Worse, if you take too much time solving the puzzle, you get "volunteered" as a test subject for the LAMBCHOP doomsday device!

To help yourself get to and from your bunk every day, write a function called `solution(src, dest)` which takes in two parameters: the source square, on which you start, and the destination square, which is where you need to land to solve the puzzle.  The function should return an integer representing the smallest number of moves it will take for you to travel from the source square to the destination square using a chess knight's moves (that is, two squares in any direction immediately followed by one square perpendicular to that direction, or vice versa, in an "L" shape).  Both the source and destination squares will be an integer between 0 and 63, inclusive, and are numbered like the example chessboard below:

```
-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------
```
## Solution
There are some constraints in this problem:
* We need to move within the boundaries of a chessboard.
* We can only move as a knight.
* We need to make sure to consider the chessboard edges when making a move, and that we stay within the defined boundaries of the board, i.e., an 8x8 grid..

## Implementation


I created a matrix to represent the chess board, and initialized each element to `None`. We can later assign values to the source square, the destination square, and any squares the knight visits while moving from the source to the destination. 

```python
    board = []
    row_size = 8
    col_size = 8

    # initialise the board
    for move in range(row_size):
        row = []
        for j in range(col_size):
            row.append(None)
        board.append(row)
```

I chose to represent the valid moves for a chess knight as an array of arrays:
```python
    # Define the legal moves for a chess knight
    knight_moves = [
        [1, 2],  [1, -2],
        [-1, 2], [-1, -2],
        [2, 1],  [2, -1],
        [-2, 1], [-2, -1]
    ]
```

The full code for the `solution()` function is here. All code is available in [solution.py](solution.py).

```python
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
```

## Unit Tests
Google offers these two test cases. There are also a bunch of hidden tests that the code must pass.
```
Input:
solution.solution(0, 1)
Output:
    3

Input:
solution.solution(19, 36)
Output:
    1
```
I implemented these two test cases as unit tests, and built up some more tests for different moves and conditions. All the tests are available in [solution.py](solution.py).

```python
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
```

## References

* MasterClass. [The Knight in Chess: What a Knight Is and How to Move a Knight Across a Chessboard](https://www.masterclass.com/articles/what-is-the-knight-in-chess)
* Pritam. [How Does The Knight Move In Chess? (Complete Guide!)](https://chessdelta.com/knight-moves-in-chess/). Chess Delta.
* Wikipedia. [Knight (chess)](https://en.wikipedia.org/wiki/Knight_%28chess%29) 
* DeepMind. [AlphaZero: Shedding new light on chess, shogi, and Go](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go)
* Surag. [A Simple Alpha(Go) Zero Tutorial](https://web.stanford.edu/~surag/posts/alphazero.html)
* On AI, 2018. [AlphaZero Explained](https://nikcheerla.github.io/deeplearningschool/2018/01/01/AlphaZero-Explained/)