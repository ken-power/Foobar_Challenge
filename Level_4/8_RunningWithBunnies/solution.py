import itertools
import unittest


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


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(AllPairsShortestPathsTests)
    suite.addTest(PathTests)
    suite.addTest(RescuedBunniesTests)

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_tests())


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
