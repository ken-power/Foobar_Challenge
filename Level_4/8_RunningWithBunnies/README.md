# Running with Bunnies: All-Pairs Shortest Paths using the Floyd-Warshall Algorithm 

## The problem
The problem description is framed as follows:

You and the bunny workers need to get out of this collapsing death trap of a space station -- and fast! Unfortunately, some of the bunnies have been weakened by their long work shifts and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close.

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave -- you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form `solution(times, time_limit)` to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID, with the first bunny being 0. There are at most 5 bunnies, and `time_limit` is a non-negative integer that is at most `999`.
## Solution
The solution involves recognizing that this is a problem of finding the shortest path through a directed, weighted graph. Similar problems show up when working with computer networks or mapping software. 

For example, suppose that we have a schedule that tells us the driving time between `n` cities at a given time of day and that we want to compute the shortest driving time between all pairs of cities ([Zhang, et al., 2013](#References)). This is an instance of the all-pairs shortest-paths problem. 

In computer science, the Floyd–Warshall algorithm (also known as Floyd's algorithm, the Roy–Warshall algorithm, the Roy–Floyd algorithm, or the WFI algorithm) is an algorithm for finding shortest paths in a directed weighted graph with positive or negative edge weights (but with no negative cycles).

## Implementation
The natural representation for a graph in the Floyd-Warshall algorithm is an adjacency matrix. 

I approached the implementation in three parts:
1. Implement the Floyd-Warshall Algorithm to find all-pairs shortest paths
2. Implement a function to calculate the path through a given list of nodes
3. Use the above two functions to implement the overall solution 

The following sections show the code and unit tests for each part. All the code is in [solution.py](solution.py).

### Calculating All-Pairs Shortest Paths

The Floyd-Warshall algorithm is the method of choice for solving the all-pairs shortest-paths problem in dense graphs method. The algorithm checks distances for each edge to determine whether that edge is part of a new shorter path.

In other words, the Floyd–Warshall Algorithm finds the shortest path between all ordered pairs of nodes (s,v), {s,v}, v∈V. 

Each iteration yields the path with the shortest weight between all pair of nodes under the constraint that only nodes {1,2,…n}, n∈|V|, can be used as intermediary nodes on the computed paths.

An example of the _Floyd-Warshall Algorithm_ is shown in the following figure (from Fig 2.1.17 of [_Advanced Wireless Networks_](#References)), where the matrices represent the edge weights.

![](./floyd-warshall.gif)


The `all_pairs_shortest_paths(matrix)` function implements the Floyd-Warshall algorithm to calculate the shortest paths.

The algorithm operates on an undirected graph `G` with `N` nodes whose nodes are numbered `1...N`. Define a path as a sequence of nodes such that no node index is repeated. The length of the path is the number of edges in it. We want to find the shortest path from any node `i` to any node `j` ([Keshav, 2012](#References)).


```python
def all_pairs_shortest_paths(graph):
    """
    This implementation uses the Floyd-Warshall algorithm to find the shortest path for all (row, col) pairs in the
    given graph. The Floyd-Warshall algorithm is a good choice for computing paths between all pairs of vertices in
    dense graphs, in which most or all pairs of vertices are connected by edges.
    https://en.wikipedia.org/wiki/Floyd-Warshall_algorithm

    :param graph: a dense graph represented as a square matrix
    """
    n = len(graph)

    for k in range(n):  # step
        for i in range(n):  # row
            for j in range(n):  # column

                # If an edge is found to reduce distance, update the shortest paths
                if graph[i][j] > graph[i][k] + graph[k][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
```

### Performance Analysis of Floyd-Warshall
The total running time of the Floyd-Warshall algorithm is `O(n^3)`.

The Floyd-Warshall algorithm computes the cost matrix of the cheapest paths between all pairs of vertices of a directed graph `G = (V, E)` in `O(|V|^3)` time and `O(|V|^2)` space.

The running time of the Floyd-Warshall algorithm might appear to be slower than performing a DFS of a directed graph from each of its vertices, but this depends upon the representation of the graph. 

If a graph is represented using an adjacency matrix, then running the DFS method once on a directed graph `G` takes `O(n^2)` time. Thus, running DFS n times takes `O(n^3)` time, which is no better than a single execution of the Floyd-Warshall algorithm, but the Floyd-Warshall algorithm is much simpler to implement. Nevertheless, if the graph were represented using an adjacency list structure, then running the DFS algorithm n times would take `O(n(n + m))` time to compute the transitive closure. Even so, if the graph is dense, that is, if it has `Ω(n^2)` edges, then this approach still runs in `O(n^3)` time and is more complicated than a single instance of the Floyd-Warshall algorithm. 

The only case where repeatedly calling the DFS method is better is when the graph is not dense and is represented using an adjacency list structure ([Mount, et al (2011)](#References)).


### Unit Tests for the Floyd-Warshall Algorithm

The `all_pairs_shortest_paths()` function works a matrix, so we can test it in isolation from the overall solution. The following unit tests verify that the `all_pairs_shortest_paths()` function is correctly calculating all-pairs shortest-paths using the Floyd-Warshall algorithm.

```python
class AllPairsShortestPathsTests(unittest.TestCase):
    """
    Given a matrix, verify that the all_pairs_shortest_paths() function is correctly calculating all-pairs
    shortest-paths using the Floyd-Warshall algorithm.
    """

    def test_1(self):
        times = [
            [0, 2, 2, 2, -1],
            [9, 0, 2, 2, -1],
            [9, 3, 0, 2, -1],
            [9, 3, 2, 0, -1],
            [9, 3, 2, 2, 0]
        ]
        expected_shortest_paths = [
            [0, 2, 1, 1, -1],
            [8, 0, 1, 1, -1],
            [8, 2, 0, 1, -1],
            [8, 2, 1, 0, -1],
            [9, 3, 2, 2, 0]
        ]

        all_pairs_shortest_paths(times)
        self.assertEqual(expected_shortest_paths, times)

    def test_2(self):
        times = [
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ]
        expected_shortest_paths = [
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ]

        all_pairs_shortest_paths(times)
        self.assertEqual(expected_shortest_paths, times)

    def test_3(self):
        times = [
            [0, 2, 2, 2, -1],
            [9, 0, 2, 2, 0],
            [9, 3, 0, 2, 0],
            [9, 3, 2, 0, 0],
            [-1, 3, 2, 2, 0]
        ]
        expected_shortest_paths = [
            [-2, 0, 0, 0, -3],
            [-1, 0, 1, 1, -2],
            [-1, 1, 0, 1, -2],
            [-1, 1, 1, 0, -2],
            [-3, -1, -1, -1, -4]
        ]

        all_pairs_shortest_paths(times)
        self.assertEqual(expected_shortest_paths, times)

    def test_4(self):
        times = [
            [0, 3, 2, 2, -1],
            [8, 0, 1, 2, -1],
            [8, 3, 2, 2, -1],
            [9, 2, 3, 0, -1],
            [9, 3, 1, 2, 0],
        ]
        expected_shortest_paths = [
            [0, 2, 0, 1, -1],
            [8, 0, 0, 1, -1],
            [8, 2, 0, 1, -1],
            [8, 2, 0, 0, -1],
            [9, 3, 1, 2, 0]
        ]

        all_pairs_shortest_paths(times)
        self.assertEqual(expected_shortest_paths, times)
```

### Finding a path through a set of nodes
The `path()` function calculates the path followed to pick up the bunnies.

```python
def path(bunnies):
    """
    Given a list of bunnies, return a path to pick up the bunnies.

    :param bunnies: a list of bunnies
    :return: a path that visits the list of bunnies
    """
    bunnies = [0] + bunnies + [-1]
    path_to_bunnies = list()

    for i in range(1, len(bunnies)):
        path_to_bunnies.append((bunnies[i - 1], bunnies[i]))

    return path_to_bunnies
```

I want to make sure the `path()` function is returning the correct path through a given list of nodes. We can test the `path()` function separately from the rest of the code because it just takes a `list` as input and returns the path. The following unit tests help verify that paths are correctly calculated.

```python
class PathTests(unittest.TestCase):
    """
    Given a list of nodes, verify that the path() function is returning the correct path through those nodes.
    """

    def test_3_nodes_123(self):
        bunny_ids = list((1, 2, 3))
        expected_path = [(0, 1), (1, 2), (2, 3), (3, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_3_nodes_132(self):
        bunny_ids = list((1, 3, 2))
        expected_path = [(0, 1), (1, 3), (3, 2), (2, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_3_nodes_321(self):
        bunny_ids = list((3, 2, 1))
        expected_path = [(0, 3), (3, 2), (2, 1), (1, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_4_nodes_1234(self):
        bunny_ids = list((1, 2, 3, 4))
        expected_path = [(0, 1), (1, 2), (2, 3), (3, 4), (4, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_4_nodes_3142(self):
        bunny_ids = list((3, 1, 4, 2))
        expected_path = [(0, 3), (3, 1), (1, 4), (4, 2), (2, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_4_nodes_4321(self):
        bunny_ids = list((4, 3, 2, 1))
        expected_path = [(0, 4), (4, 3), (3, 2), (2, 1), (1, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)

    def test_5_nodes_15234(self):
        bunny_ids = list((1, 5, 2, 3, 4))
        expected_path = [(0, 1), (1, 5), (5, 2), (2, 3), (3, 4), (4, -1)]

        path_to_bunnies = path(bunny_ids)

        self.assertEqual(expected_path, path_to_bunnies)
```

### Solution for Rescuing Bunnies
We can bring the `path()` calculation and the Floyd-Warshall implementation together to create the overall solution for rescuing bunnies. The `solution()` function returns a list of rescued bunny ids.

```python
import itertools

def solution(times, time_limit):
    """
    Calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead
    before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies
    with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID,
    with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at
    most 999.

    :param times: a matrix
    :param time_limit: the time limit
    :return: the ids of the rescued bunnies
    """
    max_time_limit = 999
    if time_limit < 0 or time_limit > max_time_limit:  # time_limit is a non-negative integer that is at most 999
        return []

    all_pairs_shortest_paths(times)

    n = len(times)  # number of rows
    bunny_count = n - 2  # first row is "Start", last row is "Bulkhead"
    rescued_bunnies = []

    for bunny in range(n):
        if times[bunny][bunny] < 0:  # check the diagonal
            rescued_bunnies = [bunny for bunny in range(bunny_count)]
            return rescued_bunnies

    for bunny in reversed(range(bunny_count + 1)):

        for bunnies in itertools.permutations(range(1, bunny_count + 1), r=bunny):
            total_time = 0

            path_to_bunnies = path(list(bunnies))

            for start_time, end_time in path_to_bunnies:
                total_time += times[start_time][end_time]

            if total_time <= time_limit:
                rescued_bunnies = sorted(list(bunny - 1 for bunny in bunnies))
                return rescued_bunnies

    return rescued_bunnies
```


## Unit Tests for the Overall Solution
Google provide the following two sample tests. 
```text
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
```

There are also a bunch of hidden tests that the code must pass, but they don't tell you what those tests are. This is the set of unit test I built up along the way.

```python
class RescuedBunniesTests(unittest.TestCase):
    """
    Given an input matrix where the inner rows designate the starting point, bunny 0...N, and the bulkhead door exit
    respectively, verify that the solution results in the set of rescued bunnies under the given time constraint.
    """

    def test_1(self):
        times = [
            # start, end, delta, time, status
            [0, 2, 2, 2, -1],  # 0 = Start
            [9, 0, 2, 2, -1],  # 1 = Bunny 0
            [9, 3, 0, 2, -1],  # 2 = Bunny 1
            [9, 3, 2, 0, -1],  # 3 = Bunny 2
            [9, 3, 2, 2, 0],  # 4 = Bulkhead
        ]
        time_limit = 1
        expected_bunny_ids = [1, 2]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_2(self):
        times = [
            # start, end, delta, time, status
            [0, 1, 1, 1, 1],  # 0 = Start
            [1, 0, 1, 1, 1],  # 1 = Bunny 0
            [1, 1, 0, 1, 1],  # 2 = Bunny 1
            [1, 1, 1, 0, 1],  # 3 = Bunny 2
            [1, 1, 1, 1, 0]  # 4 = Bulkhead
        ]
        time_limit = 3
        expected_bunny_ids = [0, 1]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_infinite_negative_cycle(self):
        times = [
            # start, end, delta, time, status
            [0, 2, 2, 2, -1],
            [9, 0, 2, 2, 0],
            [9, 3, 0, 2, 0],
            [9, 3, 2, 0, 0],
            [-1, 3, 2, 2, 0]
        ]

        time_limit = 200
        expected_bunny_ids = [0, 1, 2]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_non_rescuable_bunnies(self):
        times = [
            # start, end, delta, time, status
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]

        time_limit = 1
        expected_bunny_ids = []

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_one_bunny(self):
        times = [
            # start, end, delta, time, status
            [0, 1, 1, 1, -1],  # 0 = Start
            [9, 0, 2, 2, -1],  # 1 = Bunny 0
            [1, 1, 1, 1, 0],  # 4 = Bulkhead
        ]

        time_limit = 2
        expected_bunny_ids = [0]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_multiple_revisits(self):
        times = [
            # start, end, delta, time, status
            [0, 5, 11, 11, 1],
            [10, 0, 1, 5, 1],
            [10, 1, 0, 4, 0],
            [10, 1, 5, 0, 1],
            [10, 10, 10, 10, 0]
        ]

        time_limit = 10
        expected_bunny_ids = [0, 1]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_multiple_revisits_2(self):
        times = [
            # start, end, delta, time, status
            [0, 10, 10, 10, 1],
            [0, 0, 10, 10, 10],
            [0, 10, 0, 10, 10],
            [0, 10, 10, 0, 10],
            [1, 1, 1, 1, 0]
        ]

        time_limit = 5
        expected_bunny_ids = [0, 1]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_travel_time(self):
        times = [
            # start, end, delta, time, status
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        time_limit = 1
        expected_bunny_ids = [0, 1, 2]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_no_bunnies(self):
        times = [
            [2, 2],
            [2, 2]
        ]

        time_limit = 1
        expected_bunny_ids = []

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_backward_bunny_path(self):
        times = [
            # start, end, delta, time, status
            [0, 10, 10, 1, 10],
            [10, 0, 10, 10, 1],
            [10, 1, 0, 10, 10],
            [10, 10, 1, 0, 10],
            [1, 10, 10, 10, 0]
        ]

        time_limit = 6
        expected_bunny_ids = [0, 1, 2]

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_empty_matrix(self):
        times = []

        time_limit = 10
        expected_bunny_ids = []

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)

    def test_max_time_limit_exceeded(self):
        times = [
            # start, end, delta, time, status
            [0, 2, 2, 2, -1],  # 0 = Start
            [9, 0, 2, 2, -1],  # 1 = Bunny 0
            [9, 3, 0, 2, -1],  # 2 = Bunny 1
            [9, 3, 2, 0, -1],  # 3 = Bunny 2
            [9, 3, 2, 2, 0],  # 4 = Bulkhead
        ]
        time_limit = 1000
        expected_bunny_ids = []

        rescued_bunnies = solution(times, time_limit)
        self.assertEqual(expected_bunny_ids, rescued_bunnies)
```

## References

* Wikipedia. [Floyd's algorithm](https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm)
* Geeks for Geeks. [Python implementation of Floyd-Warshall](https://www.geeksforgeeks.org/floyd-warshall-algorithm-dp-16/)
* FoxHub. [Example code and test cases](https://github.com/FoxHub/Google-FooBar/blob/master/Level-4/foobar_4-2_running_with_bunnies.py)
* SciPy.org. [Documentation for `floyd_warshall` implementation in scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.floyd_warshall.html#scipy.sparse.csgraph.floyd_warshall)
* V. Anton Spraul, 2015. How Software Works, Chapter 9: Map Routes.
* Savo G. Gilsic, 2016. Advanced Wireless Networks, 3rd Edition, Chapter 2: Adaptive Network Layer. Wiley.
* David M. Mount; Michael T. Goodrich; Roberto Tamassi, 2011. Data Structures and Algorithms in C++, Second Edition, Chapter 13: Graph Algorithms. Wiley.
* Christofer Larsson, 2014. Design of Modern Communication Networks, Chapter 2: Networks and Flow. Academic Press.
* Stanley Selkow; Gary Pollice; George T. Heineman, 2015. Algorithms in a Nutshell, 2nd Edition, Chapter 6: Graph Algorithms. O'Reilly Media, Inc.
* John Baras; George Theodorakopoulos, 2010. Path Problems in Networks. Morgan & Claypool Publishers.
* Ping Zhang; Jay Yellen; Jonathan L. Gross, 2013. Handbook of Graph Theory, 2nd Edition. Chapman and Hall/CRC.
* Srinivasan Keshav, 2012. Mathematical Foundations of Computer Networking, Chapter 4: Optimization. Addison-Wesley Professional.
* Robert Sedgewick, 2003. Algorithms in Java, Part 5: Graph Algorithms, Third Edition, Chapter 21: Shortest Paths. Addison-Wesley Professional.
