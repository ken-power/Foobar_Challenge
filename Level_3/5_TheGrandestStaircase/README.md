# The Grandest Staircase Of Them All: Partitioning, Memoization, and Dynamic Programming

## The problem
With the LAMBCHOP doomsday device finished, Commander Lambda is preparing to debut on the galactic stage -- but in order to make a grand entrance, Lambda needs a grand staircase! As the Commander's personal assistant, you've been tasked with figuring out how to build the best staircase EVER.

Lambda has given you an overview of the types of bricks available, plus a budget. You can buy different amounts of the different types of bricks (for example, 3 little pink bricks, or 5 blue lace bricks). Commander Lambda wants to know how many different types of staircases can be built with each amount of bricks, so they can pick the one with the most options.

Each type of staircase should consist of 2 or more steps.  No two steps are allowed to be at the same height - each step must be lower than the previous one. All steps must contain at least one brick. A step's height is classified as the total amount of bricks that make up that step.

For example, when `N = 3`, you have only 1 choice of how to build the staircase, with the first step having a height of 2 and the second step having a height of 1: (`#` indicates a brick)

```
#
##
21
```

When `N = 4`, you still only have 1 staircase choice:

```
#
#
##
31
```

But when `N = 5`, there are two ways you can build a staircase from the given bricks. The two staircases can have heights `(4, 1)` or `(3, 2)`, as shown below:

```
#
#
#
##
41

#
##
##
32
```

Write a function called `solution(n)` that takes a positive integer `n` and returns the number of different staircases that can be built from exactly `n` bricks. `n` will always be at least 3 (so you can have a staircase at all), but no more than 200, because Commander Lambda's not made of money!

## Solution
We are being asked to work out how many staircases can be built from a given number of bricks. The problem statement is asking us to partition the bricks into as many combinations as possible that form a staircase. This can be viewed as a partitioning problem, though in this case not all possible partitions are valid under the given constraints of what constitutes a valid staircase. 

> _In number theory and combinatorics, a partition of a positive integer `n`, also called an integer partition, is a way of writing `n` as a sum of positive integers. Two sums that differ only in the order of their summands are considered the same partition. If order matters, the sum becomes a composition_ ([Wikipedia](#references)).

[Knuth (2014)](#references) describes some approaches for generating sets of partitions. In this case, we are not interested in all possible partitions. We are only interested in the partitions that form a valid staircase. 


## Implementation
The code for my solution and all related tests is in [solution.py](solution.py).

This problem is known as Euler's distinct partition problem. My solution uses the memoization optimization technique, dynamic programming and recursion to check different staircase combinations and find the optimal number of staircases that can be built.

### Memoization and Dynamic Programming

[Kwong & Karpinski (2020)](#references) have a nice description of the motivation for using memoization and dynamic programming:

"_In developing software, we often face a situation where the speed of execution is constrained by many factors. Maybe a function needs to read a large amount of historical data from disk (also known as I/O-bound). Or a function just needs to perform some complex calculation that takes a lot of time (also known as CPU-bound). When these functions are called repeatedly, application performance can suffer greatly._"

"_Memoization is a powerful concept to address these problems. In recent years, it has become more popular as functional programming is becoming more mainstream. The idea is really simple. When a function is called for the first time, the return value is stored in a cache. If the function is called again with the exact same argument as before, we can look up the value from the cache and return the result immediately._"

An example often used for introducing this topic is calculating the Fibonacci sequence.

### Implementing the `solution(n)` function

This is the main function, `solution(n)`:

```python
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
```
### Memoization implementation
I created the `staircase_combinations()` function to abstract out the logic for recursively working out the number of possible staircase combinations, using a technique called _memoization_.

In computing, memoization or memoisation is an optimization technique used primarily to speed up computer programs by storing the results of expensive function calls and returning the cached result when the same inputs occur again ([Wikipedia](#references)).
```python
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
```

### Unit Tests
Google provided the following two test cases.
```text
Input:
solution.solution(200)
Output:
    487067745

Input:
solution.solution(3)
Output:
    1
```

I implemented these as unit tests, and also developed several more tests as I was developing the solution.

```python
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
```

## References

* Donald E. Knuth, 2014. _Art of Computer Programming, Volume 4A, The: Combinatorial Algorithms, Part 1_. Addison-Wesley Professional.
* Dan Zingaro, 2020. _Algorithmic Thinking. Chapter 3: Memoization and Dynamic Programming._ No Starch Press.
* Micheal Lanham, 2020. _Hands-On Reinforcement Learning for Games._ Packt Publishing.
* Benjamin Baka, 2017. _Python Data Structures and Algorithms_. Packt Publishing.
* Sakis Kasampalis; Dr. Gabriele Lanaro; Quan Nguyen, 2019. _Advanced Python Programming_. Packt Publishing.
* Tom Kwong; Stefan Karpinski, 2020. _Hands-On Design Patterns and Best Practices with Julia_. Packt Publishing.
* educative. [What is Dynamic Programming?](https://www.educative.io/courses/grokking-dynamic-programming-patterns-for-coding-interviews/m2G1pAq0OO0)  
* Wikipedia. [Partitions](https://en.wikipedia.org/wiki/Partition_(number_theory))
* Wikipedia. [Memoization](https://en.wikipedia.org/wiki/Memoization)
* Wikipedia. [Euler's Pentagonal Number Theorem](https://en.wikipedia.org/wiki/Pentagonal_number_theorem)
* George E. Andrews, 1983. _[Euler's Pentagonal Number Theorem](https://faculty.math.illinois.edu/~reznick/2690367.pdf)_. Mathematics Magazine, _Vol. 56, No. 5 (Nov., 1983)_, pp. 279-284
