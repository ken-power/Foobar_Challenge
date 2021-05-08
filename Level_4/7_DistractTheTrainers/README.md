# Distract the Trainers: Constructing Maximum Matchings on Graphs using the Blossom Algorithm

**Contents**
* [Problem desccription](#the-problem)
* [Solution description](#solution)
* [Implementation](#implementation)
* [References](#references)

## The problem
The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! `1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4` and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function `solution(banana_list)` which, given a list of positive integers depicting the amount of bananas each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element `i` of the list will be the number of bananas that trainer `i` (counting from `0`) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. `2^30 -1`). Some of them stockpile a LOT of bananas.

## Solution

1. Create a wrestling tournament graph from the list of trainers. This is implemented in the `create_wrestling_tournament(banana_list)` function.
2. Calculate how many trainers have been distracted by using the tournament graph to pair off the trainers into wrestling matches. This is implemented in the `distract_the_trainers(tournament_graph)` function. 
3. Calculate how many trainers are remaining by subtracting the distracted trainers from the original count of trainers. 

The first step involves building a graph from an initial list of values. As you [can see below](#create-a-wrestling-tournament-from-a-list-of-trainers), I opted to represent the graph as an adjacency list. Creating the graph is a necessary setup for the next step. I wanted to decouple the problem of creating the graph from the problem of figuring out if trainers are distracted.

The second step is really the core problem, i.e., [calculating how many trainers have been distracted](#distract-the-trainers). The solution involves recognizing that this is a problem of maximum matching in graphs. I chose to implement the Blossom Algorithm to solve it.

To create the wrestling tournament, we need to determine whether two numbers (in this case, representing number of bananas held by each of the pair of trainers) will enter an infinite loop. I created the `results_in_infinite_loop(banana_count_a, banana_count_b)` function to figure this out.
* The result of a wrestling match is calculated as `numerator // denominator`, where `numerator` is the sum of the two banana counts. The `denominator` is the greatest common divisor of the two banana counts. I chose to create a separate function `gcd(a, b)` and used Euclid's algorithm to calculate the greatest common divisor. 
* The wrestling match will enter an infinite loop if the result is NOT a power of 2. I created the `is_power_of_two(n)` function to determine if a number is a power of 2.

The blossom algorithm is used in several applications including the assignment problem, the marriage problem, and the Hamiltonian cycle and path problems (i.e., Traveling Salesman Problem) ([Shoemaker and Vare, 2016](#references))

## Implementation

All the solution code and unit tests are in [`solution.py`](solution.py). 

The core of my solution is these three lines:
```python
    tournament_graph = create_wrestling_tournament(banana_list)
    distracted_trainers = distract_the_trainers(tournament_graph)
    remaining_trainers = len(banana_list) - distracted_trainers
```

This section is organized as follows:
* [Main `solution()` function](#main-solution-function)
* [Create a wrestling tournament graph](#create-a-wrestling-tournament-from-a-list-of-trainers)
* [Distract the trainers by pairing them in thumb wrestling matches](#distract-the-trainers)
* [Supporting functions and tests](#supporting-functions-and-tests)
    * [Determining whether two numbers will result in an infinite loop](#determining-whether-two-numbers-will-result-in-an-infinite-loop)
    * [Using Euclid's Algorithm to find the greatest common divisor of two numbers](#using-euclids-algorithm-to-find-the-greatest-common-divisor-of-two-numbers)
    * [Determining if a number is a power of two](#determining-if-a-number-is-a-power-of-two)
    * [Compare graph elements](#compare-graph-elements)
  
### Main solution function

```python
def solution(banana_list):
    """
    A function to pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb
    wrestling loop! The number of trainers will be at least 1 and not more than 100, and the number of bananas each
    trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile
    a LOT of bananas.

    :param banana_list: a list of positive integers depicting the amount of bananas each trainer starts with;
                        Element i of the list will be the number of bananas that trainer i (counting from 0) starts with
    :return: the fewest possible number of bunny trainers that will be left to watch the workers; returns None if any
             of the noted preconditions are violated
    """
    # First, let's check the preconditions that are specified in the problem description
    num_trainers = len(banana_list)

    # The number of trainers will be at least 1 and not more than 100
    if num_trainers < 1 or num_trainers > 100:
        return None

    if num_trainers == 2 and banana_list[0] == banana_list[1]:
        return num_trainers

    # the number of bananas each trainer starts with must be a positive
    # integer no more than 1073741823 (i.e. 2^30 -1)
    max_bananas_per_trainer_at_start = pow(2, 30) - 1

    # If any trainer has more than the allowed starting number of bananas then we won't start a tournament
    for banana_count in banana_list:
        if banana_count > max_bananas_per_trainer_at_start:
            return None

    # if the preconditions are satisfied, we can proceed with figuring out the tournament graph,
    # number of distracted trainers, and remaining trainers
    tournament_graph = create_wrestling_tournament(banana_list)
    distracted_trainers = distract_the_trainers(tournament_graph)
    remaining_trainers = len(banana_list) - distracted_trainers

    return remaining_trainers
```

### Unit Tests
Google provide the following two test cases.
```
Input:
solution.solution(1,1)
Output:
    2

Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0
```
Here, I implement these two test cases as unit tests. The code in [solution.py](solution.py) contains many more unit tests that I built up along the way. 

```python
class SolutionTests(unittest.TestCase):

    def test_2_trainers(self):
        bananas_per_trainer = [1, 1]
        expected_trainers_remaining = 2

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_6_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 19]
        expected_trainers_remaining = 0

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_2_trainers_different_amount(self):
        bananas_per_trainer = [7, 4]
        expected_trainers_remaining = 0

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)


```
### Create a wrestling tournament from a list of trainers

```python
def create_wrestling_tournament(banana_list):
    """
    Create a graph of the wrestling matches.

    :param banana_list: specifies how many bananas each trainer has
    :return: a graph representing the simultaneous wrestling matches
    """
    tournament_graph = {i: [] for i in range(len(banana_list))}

    for i in range(len(banana_list)):
        for j in range(i, len(banana_list)):
            if i != j and results_in_infinite_loop(banana_list[i], banana_list[j]):
                tournament_graph[i].append(j)
                tournament_graph[j].append(i)

    return tournament_graph
```

```python
class WrestlingTournamentGraphTests(unittest.TestCase):

    def test_6_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 19]
        expected_graph = {
            0: [3, 4, 5],
            1: [2, 4, 5],
            2: [1, 5],
            3: [0, 4, 5],
            4: [0, 1, 3],
            5: [0, 1, 2, 3]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_2_trainers_1_each(self):
        bananas_per_trainer = [1, 1]
        expected_graph = {
            0: [],
            1: []
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_0_trainers(self):
        bananas_per_trainer = []
        expected_graph = {}
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_2_trainers_same_amount_even(self):
        bananas_per_trainer = [4, 4]
        expected_graph = {
            0: [],
            1: []
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_2_trainers_same_amount_odd(self):
        bananas_per_trainer = [9, 9]
        expected_graph = {
            0: [],
            1: []
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_2_trainers_different_amount_7_4(self):
        bananas_per_trainer = [7, 4]

        expected_graph = {
            0: [1],
            1: [0]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_2_trainers_different_amount_17_11(self):
        bananas_per_trainer = [17, 11]

        expected_graph = {
            0: [1],
            1: [0]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_4_trainers_different_amount(self):
        bananas_per_trainer = [17, 11, 3, 82]

        expected_graph = {
            0: [1, 2, 3],
            1: [0, 2, 3],
            2: [0, 1, 3],
            3: [0, 1, 2]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_18_trainers(self):
        bananas_per_trainer = [1, 10, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]

        expected_graph = {
            0: [1, 4, 5, 6, 7, 8, 9, 13, 14, 15, 17],
            1: [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            2: [1, 3, 5, 6, 8, 9, 12, 14, 15, 16, 17],
            3: [1, 2, 6, 9, 11, 15, 17],
            4: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            5: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            6: [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 16, 17],
            7: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            8: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            9: [0, 1, 2, 3, 4, 7, 10, 11, 12, 13, 16, 17],
            10: [1, 4, 5, 6, 7, 8, 9, 13, 14, 15, 17],
            11: [1, 3, 5, 6, 8, 9, 12, 14, 15, 16, 17],
            12: [1, 2, 6, 9, 11, 15, 17],
            13: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            14: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            15: [0, 1, 2, 3, 4, 7, 10, 11, 12, 13, 16, 17],
            16: [1, 2, 6, 9, 11, 15, 17],
            17: [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

    def test_17_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]

        expected_graph = {
            0: [3, 4, 5, 6, 7, 8, 12, 13, 14, 16], 1: [2, 4, 5, 7, 8, 11, 13, 14, 15, 16],
            2: [1, 5, 8, 10, 14, 16],
            3: [0, 4, 5, 7, 8, 9, 13, 14, 16],
            4: [0, 1, 3, 5, 6, 9, 10, 12, 16],
            5: [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 15, 16],
            6: [0, 4, 5, 7, 8, 9, 13, 14, 16],
            7: [0, 1, 3, 5, 6, 9, 10, 12, 16],
            8: [0, 1, 2, 3, 6, 9, 10, 11, 12, 15, 16],
            9: [3, 4, 5, 6, 7, 8, 12, 13, 14, 16],
            10: [2, 4, 5, 7, 8, 11, 13, 14, 15, 16],
            11: [1, 5, 8, 10, 14, 16],
            12: [0, 4, 5, 7, 8, 9, 13, 14, 16],
            13: [0, 1, 3, 5, 6, 9, 10, 12, 16],
            14: [0, 1, 2, 3, 6, 9, 10, 11, 12, 15, 16],
            15: [1, 5, 8, 10, 14, 16],
            16: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)
```

### Distract the trainers
Pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop. This is the function that implements the [Blossom Algorithm](#references).

The blossom algorithm is an algorithm in graph theory for constructing maximum matchings on graphs. The [blossom algorithm (Edmonds 1965)](#references) finds a maximum independent edge set in a (possibly weighted) graph ([MathWorld](#references)). The algorithm was developed by Jack Edmonds in 1961, and published in 1965. Given a general graph `G = (V, E)`, the algorithm finds a matching `M` such that each vertex in `V` is incident with at most one edge in `M` and `|M|` is maximized. The matching is constructed by iteratively improving an initial empty matching along augmenting paths in the graph. ([Wikipedia](#references))

The blossom algorithm checks for the existence of an augmenting path by a tree search as in the bipartite case, but with special handling for the odd-length cycles that can arise in the general case. Such a cycle is called a **blossom**.

```python
def distract_the_trainers(graph):
    """
    Pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop.

    We don't pair off trainers with the same number of bananas (if we do, their game will end and they will go back to
    work). We know enough trainer psychology to know that the one who has more bananas always gets over-confident and
    loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both
    of them have the same number of bananas. Once that happens, both of them will lose interest and go back to
    supervising the bunny workers, and you don't want THAT to happen!

    The following proved useful and interesting for this implementation:

    References:
    Micali, S. and Vazirani, V.V., 1980, October. "An O (v| v| c| E|) algorithm for finding maximum matching in general
    graphs". In 21st Annual Symposium on Foundations of Computer Science (SFCS 1980) (pp. 17-27). IEEE.
    Wikipedia. Blossom Algorithm. https://en.wikipedia.org/wiki/Blossom_algorithm
    Wolfram. Blossom Algorithm. https://mathworld.wolfram.com/BlossomAlgorithm.html

    :param graph: a graph
    :return: the number of trainers that have gone into an infinite thumb wrestling loop and are now distracted
    """
    distracted_trainers = 0
    remaining_nodes = len(graph)

    while len(graph) > 1 and remaining_nodes >= 1:
        # Find the first min-length path in the graph. Note, there might be multiple paths of the same shortest length.
        min_length_path = min(graph, key=graph_comparator(graph))

        if (len(graph[min_length_path])) < 1:
            del graph[min_length_path]
        else:
            matched_pair = [len(graph[graph[min_length_path][0]]) + 1, 1]

            for node in graph[min_length_path]:
                if len(graph[node]) < matched_pair[0]:
                    matched_pair = [len(graph[node]), node]

                for i in range(len(graph[node])):
                    if graph[node][i] == min_length_path:
                        # We don't pair off trainers with the same number of bananas
                        del graph[node][i]
                        break

            for node in graph[matched_pair[1]]:
                for i in range(len(graph[node])):
                    if graph[node][i] == matched_pair[1]:
                        # We don't pair off trainers with the same number of bananas
                        del graph[node][i]
                        break

            del graph[min_length_path]
            del graph[matched_pair[1]]
            distracted_trainers += 2

        if len(graph) > 1:
            remaining_nodes = len(graph)

    return distracted_trainers
```
The following unit tests help to validate the `distract_the_trainers()` function.
```python
class DistractTheTrainersTests(unittest.TestCase):

    def test_2_trainers(self):
        bananas_per_trainer = [1, 1]
        graph = create_wrestling_tournament(bananas_per_trainer)
        distracted_trainers = distract_the_trainers(graph)

        self.assertEqual(0, distracted_trainers)

    def test_6_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 19]
        graph = create_wrestling_tournament(bananas_per_trainer)
        distracted_trainers = distract_the_trainers(graph)

        self.assertEqual(6, distracted_trainers)

    def test_5_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13]
        graph = create_wrestling_tournament(bananas_per_trainer)
        distracted_trainers = distract_the_trainers(graph)

        self.assertEqual(4, distracted_trainers)

    def test_2_trainers_different_amount(self):
        bananas_per_trainer = [7, 4]
        graph = create_wrestling_tournament(bananas_per_trainer)
        distracted_trainers = distract_the_trainers(graph)

        self.assertEqual(2, distracted_trainers)

    def test_18_trainers(self):
        bananas_per_trainer = [1, 10, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]
        graph = create_wrestling_tournament(bananas_per_trainer)
        distracted_trainers = distract_the_trainers(graph)

        self.assertEqual(18, distracted_trainers)
```

## Supporting functions and tests
This section contains a number of functions used to support [creating a wrestling tournament from a list of trainers](#create-a-wrestling-tournament-from-a-list-of-trainers). These are all called from within the `create_wrestling_tournament()` function.
* [Determining whether two numbers will result in an infinite loop](#determining-whether-two-numbers-will-result-in-an-infinite-loop)
* [Using Euclid's Algorithm to find the greatest common divisor of two numbers](#using-euclids-algorithm-to-find-the-greatest-common-divisor-of-two-numbers)
* [Determining if a number is a power of two](#determining-if-a-number-is-a-power-of-two)
* [Compare graph elements](#compare-graph-elements)

### Determining whether two numbers will result in an infinite loop

```python
def results_in_infinite_loop(banana_count_a, banana_count_b):
    """
    Knowing we must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb
    wrestling loop, this function determines if a specific pair of trainers will enter into an infinite loop.

    :param banana_count_a: the amount of bananas held by trainer a
    :param banana_count_b: the amount of bananas held by trainer b
    :return: True if the two trainers will enter an infinite loop based on their banana count, otherwise return False
    """
    numerator = banana_count_a + banana_count_b
    denominator = gcd(banana_count_a, banana_count_b)
    result = numerator // denominator

    # the wrestling match will enter an infinite loop if result is NOT a power of 2
    return not (is_power_of_two(result))
```


```python
class LoopTests(unittest.TestCase):
    infinite_loop_pairs = [
        (1, 10),
        (1, 21),
        (1, 13),
        (1, 109),
        (1, 19),
        (10, 1),
        (10, 7),
        (109, 7),
        (109, 3),
        (21, 13),
        (3, 54),
        (13, 9)
    ]

    non_infinite_loop_pairs = [
        (1, 7),
        (1, 3),
        (1, 1),
        (10, 54),
        (13, 19),
        (13, 3)
    ]

    def test_no_loop_if_sum_is_power_of_two(self):
        """
        Do not loop when the sum of the pair of numbers IS a power of 2
        i.e., if the pair of numbers will NOT enter an infinite loop, the sum of the pairs are powers of 2
        """
        for pair in self.non_infinite_loop_pairs:
            self.assertFalse(results_in_infinite_loop(pair[0], pair[1]))
            self.assertTrue(is_power_of_two(pair[0] + pair[1]))

    def test_loop_if_sum_is_not_power_of_two(self):
        """
        Loop when the sum of the pair of numbers IS NOT a power of 2
        i.e., if the pair of numbers will enter an infinite loop, the sum of the pairs are NOT powers of 2
        """
        for pair in self.infinite_loop_pairs:
            self.assertTrue(results_in_infinite_loop(pair[0], pair[1]))
            self.assertFalse(is_power_of_two(pair[0] + pair[1]))
```

### Using Euclid's Algorithm to find the greatest common divisor of two numbers


```python
def gcd(a, b):
    """
    Find the greatest common divisor of two numbers. This implementation uses Euclid's algorithm.

    Euclid's algorithm, is an efficient method for computing the greatest common divisor (GCD) of two integers, the
    largest number that divides them both without a remainder. It is named after the ancient Greek mathematician Euclid,
    who first described it in his Elements (c. 300 BC).
    https://en.wikipedia.org/wiki/Euclidean_algorithm

    function gcd(a, b)
        while b != 0
            t := b
            b := a mod b
            a := t
        return a

    See also: https://www.geeksforgeeks.org/gcd-in-python/

    :param a: the first number
    :param b: the second number
    :return: the greatest common denominator of the two numbers
    """
    while b:
        a, b = b, a % b

    return a
```

```python
class GCDTests(unittest.TestCase):

    def test_1(self):
        a = 3
        b = 5
        result = gcd(a, b)
        self.assertEqual(1, result)

    def test_2(self):
        a = 1
        b = 4
        result = gcd(a, b)
        self.assertEqual(1, result)

    def test_3(self):
        # GCD(A,0) = A
        a = 3
        b = 0
        result = gcd(a, b)
        self.assertEqual(a, result)

    def test_4(self):
        # GCD(0,B) = B
        a = 0
        b = 99
        result = gcd(a, b)
        self.assertEqual(b, result)
```


### Determining if a number is a power of two

```python
def is_power_of_two(n):
    """
    Determine if a given number is a power of 2.

    :param n: an integer
    :return: True if the given integer is a power of 2, otherwise return False
    """

    # Every power of 2 has exactly 1 bit set to 1 (the bit in that number's log base-2 index). So when
    # subtracting 1 from it, that bit flips to 0 and all preceding bits flip to 1. That makes
    # these 2 numbers the inverse of each other so when AND-ing them, we will get 0 as the result.
    #
    #     https://stackoverflow.com/questions/57025836/how-to-check-if-a-given-number-is-a-power-of-two
    return (n & (n - 1) == 0) and n != 0
```

```python
class PowersOfTwoTests(unittest.TestCase):

    def test_4_is_power_of_two(self):
        a = 2
        b = 2
        self.assertTrue(is_power_of_two(a + b))

    def test_16_is_power_of_two(self):
        a = 12
        b = 4
        self.assertTrue(is_power_of_two(a + b))

    def test_1024_is_power_of_two(self):
        a = 1001
        b = 23
        self.assertTrue(is_power_of_two(a + b))

    def test_17_is_not_power_of_two(self):
        a = 13
        b = 4
        self.assertFalse(is_power_of_two(a + b))

    def test_1023_is_not_power_of_two(self):
        a = 1021
        b = 2
        self.assertFalse(is_power_of_two(a + b))

    def test_negative4_is_not_power_of_two(self):
        a = 2
        b = -2
        self.assertFalse(is_power_of_two(a + b))
```

### Compare graph elements
In the `distract_the_trainers()` function we need a way to compare graph elements. I chose to factor that logic to its own function `graph_comparator()`. The element comparison in this function is based on the length of the nodes for each element.  

```python
def graph_comparator(graph):
    """
    Compare the graph elements by the length of each of their nodes.
    """
    return lambda x: len(graph[x])
```

```python
class MinimumWeightNodeTests(unittest.TestCase):

    def test_6_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 19]
        graph = create_wrestling_tournament(bananas_per_trainer)

        min_weight_node = 2
        connections = graph[min_weight_node]
        comparator = graph_comparator(graph)
        self.assertEqual(min_weight_node, min(graph, key=comparator))
        self.assertEqual(connections, graph[min(graph, key=comparator)])

    def test_2_trainers_1_each(self):
        bananas_per_trainer = [1, 1]
        graph = create_wrestling_tournament(bananas_per_trainer)

        min_weight_node = 0
        connections = graph[min_weight_node]
        comparator = graph_comparator(graph)
        self.assertEqual(min_weight_node, min(graph, key=comparator))
        self.assertEqual(connections, graph[min(graph, key=comparator)])

    def test_18_trainers(self):
        bananas_per_trainer = [1, 10, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]
        graph = create_wrestling_tournament(bananas_per_trainer)

        min_weight_node = 3
        connections = graph[min_weight_node]
        comparator = graph_comparator(graph)
        self.assertEqual(min_weight_node, min(graph, key=comparator))
        self.assertEqual(connections, graph[min(graph, key=comparator)])

    def test_18_trainers_multiple_nodes_can_have_same_min_weight(self):
        bananas_per_trainer = [1, 10, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]

        expected_graph = {
            0: [1, 4, 5, 6, 7, 8, 9, 13, 14, 15, 17],
            1: [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            2: [1, 3, 5, 6, 8, 9, 12, 14, 15, 16, 17],
            3: [1, 2, 6, 9, 11, 15, 17],
            4: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            5: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            6: [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 16, 17],
            7: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            8: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            9: [0, 1, 2, 3, 4, 7, 10, 11, 12, 13, 16, 17],
            10: [1, 4, 5, 6, 7, 8, 9, 13, 14, 15, 17],
            11: [1, 3, 5, 6, 8, 9, 12, 14, 15, 16, 17],
            12: [1, 2, 6, 9, 11, 15, 17],
            13: [0, 1, 5, 6, 8, 9, 10, 14, 15, 17],
            14: [0, 1, 2, 4, 6, 7, 10, 11, 13, 17],
            15: [0, 1, 2, 3, 4, 7, 10, 11, 12, 13, 16, 17],
            16: [1, 2, 6, 9, 11, 15, 17],
            17: [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        }
        graph = create_wrestling_tournament(bananas_per_trainer)
        self.assertEqual(expected_graph, graph)

        node = 3
        connections = graph[node]
        comparator = graph_comparator(graph)
        self.assertEqual(node, min(graph, key=comparator))
        min_weight_connections = graph[min(graph, key=comparator)]
        self.assertEqual(connections, min_weight_connections)

        # Validate that nodes 12 and 16 also satisfy the min weight criteria
        self.assertEqual(graph[12], min_weight_connections)
        self.assertEqual(graph[16], min_weight_connections)
        self.assertEqual(graph[16], graph[3])

        # Just for sanity, validate some notes do not contain min weight connections
        self.assertNotEqual(graph[0], min_weight_connections)
        self.assertNotEqual(graph[11], min_weight_connections)
```




## References

* Edmonds, J. (1965). [Paths, Trees, and Flowers](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/paths-trees-and-flowers/08B492B72322C4130AE800C0610E0E21). Canadian Journal of Mathematics, 17, 449-467. doi:10.4153/CJM-1965-045-4
* Ping Zhang; Jay Yellen; Jonathan L. Gross, 2013. Handbook of Graph Theory, 2nd Edition. Chapter 11: Networks and Flows. Published by Chapman and Hall/CRC.
* Suely Oliveira, 2013. Network Algorithms For Protein Interactions. In Yi Pan; Jianxin Wang; Min Li, (Eds)._Algorithmic and Artificial Intelligence Methods for Protein Bioinformatics_  Published by Wiley-IEEE Press.
* Vazirani, V.V., 1994. [A theory of alternating paths and blossoms for proving correctness of the O (sqrt(V)E) general graph maximum matching algorithm](http://ftp.eecs.umich.edu/~pettie/matching/Vazirani-matching-proof-1994.pdf). Combinatorica, 14(1), pp.71-109.
* Wikipedia. [Blossom Algorithm](https://en.wikipedia.org/wiki/Blossom_algorithm)
* Matthew Kusner and Stan Wagon, 2011. [The Blossom Algorithm for Maximum Matching](https://demonstrations.wolfram.com/TheBlossomAlgorithmForMaximumMatching/). Wolfram.
* Stan Wagon. [Blossom Algorithm](https://mathworld.wolfram.com/BlossomAlgorithm.html). MathWorld.
* Amy Shoemaker and Sagar Vare. June 6, 2016 [Edmonds’ Blossom Algorithm](https://stanford.edu/~rezab/classes/cme323/S16/projects_reports/shoemaker_vare.pdf). 
* Micali & Vazirni, 1980. [An O(sqrt(|v|) |E|) Algorithm for Finding Maximum Matching in General Graphs](https://www.researchgate.net/publication/221499631_An_Osqrtv_E_Algorithm_for_Finding_Maximum_Matching_in_General_Graphs)
