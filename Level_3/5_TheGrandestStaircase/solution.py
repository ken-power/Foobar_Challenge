import unittest


def staircase_combinations(height, bricks, memo):
    """
    Recursively check different staircase combinations starting with the specified number of bricks. We can take
    advantage of the memoization optimization technique - https://en.wikipedia.org/wiki/Memoization.

    Note there is a space-time tradeoff here. We know our budget is max 200 bricks, so we can take advantage of that
    upper bound to optimize for execution time and use more memory to cache intermediate results. I would revisit
    this design if the problem constraints changed.

    :param height: height of the staircase
    :param bricks: number of bricks
    :param memo: the memoized cache
    :return: the value stored at [height][bricks]
    """
    if memo[height][bricks] != 0:
        return memo[height][bricks]
    if bricks == 0:
        return 1
    if bricks < height:
        return 0

    memo[height][bricks] = staircase_combinations(height + 1, bricks - height, memo) + \
                           staircase_combinations(height + 1, bricks, memo)

    return memo[height][bricks]


def solution(n):
    """
    Return the number of staircases that can be built from bricks. The value of n will always be at least 3 (so you
    can have a staircase at all), but no more than 200, because Commander Lambda's not made of money!

    :param n: the number of bricks
    :return: returns the number of different staircases that can be built from exactly n bricks; return 0 if 3<n<200.
    """
    # n will always be at least 3 (so we can have a staircase at all), but no more than 200 (because of budget)
    min_bricks = 3
    max_bricks = 200

    # if we have too few bricks, or too many are requested, then we can't build a staircase
    if min_bricks < n > max_bricks:
        return 0

    # create a grid to store the combinations, and initialize the elements to 0
    combinations = [[0 for column in range(n + 2)] for row in range(n + 2)]

    starting_height = 1
    combinations = staircase_combinations(starting_height, n, combinations) - 1

    return combinations


class StaircaseTests(unittest.TestCase):

    def test_200_bricks(self):
        num_bricks = 200
        expected_staircase_combos = 487067745

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_3_bricks(self):
        num_bricks = 3
        expected_staircase_combos = 1

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_4_bricks(self):
        num_bricks = 4
        expected_staircase_combos = 1

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_5_bricks(self):
        num_bricks = 5
        expected_staircase_combos = 2

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_6_bricks(self):
        num_bricks = 6
        expected_staircase_combos = 3

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_15_bricks(self):
        num_bricks = 15
        expected_staircase_combos = 26

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_too_few_bricks(self):
        num_bricks = 2
        expected_staircase_combos = 0

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)

    def test_too_many_bricks(self):
        num_bricks = 201
        expected_staircase_combos = 0

        staircases = solution(num_bricks)
        self.assertEqual(expected_staircase_combos, staircases)
