import unittest


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


def graph_comparator(graph):
    """
    Compare the graph elements by the length of each of their nodes.
    """
    return lambda x: len(graph[x])


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


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(SolutionTests)
    suite.addTest(WrestlingTournamentGraphTests)
    suite.addTest(DistractTheTrainersTests)
    suite.addTest(GCDTests)
    suite.addTest(PowersOfTwoTests)
    suite.addTest(LoopTests)
    suite.addTest((MinimumWeightNodeTests))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_tests())


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

    def test_18_trainers(self):
        bananas_per_trainer = [1, 10, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]
        expected_trainers_remaining = 0

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_17_trainers(self):
        bananas_per_trainer = [1, 7, 3, 21, 13, 109, 21, 13, 19, 1, 7, 3, 21, 13, 19, 3, 54]
        expected_trainers_remaining = 1

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_0_trainers(self):
        bananas_per_trainer = []
        expected_trainers_remaining = None

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_101_trainers(self):
        bananas_per_trainer = [1] * 101
        expected_trainers_remaining = None

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_too_many_bananas(self):
        bananas_per_trainer = [1] * 50
        max_allowed_bananas = pow(2, 38) - 1
        bananas_per_trainer[35] = max_allowed_bananas + 3
        expected_trainers_remaining = None

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_loop_when_sum_not_power_of_2(self):
        """
        loop when the sum of the reduced pair of numbers is not a power of 2
        """
        bananas_per_trainer = [5, 4]
        expected_trainers_remaining = 0

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)

    def test_sum_is_power_of_2(self):
        """
        Does not loop when the sum of the reduced pair of numbers is a power of 2
        """
        bananas_per_trainer = [12, 4]
        expected_trainers_remaining = 2

        remaining_trainers = solution(bananas_per_trainer)
        self.assertEqual(expected_trainers_remaining, remaining_trainers)
