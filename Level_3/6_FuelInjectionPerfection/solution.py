import unittest


def reduce_to_one(n):
    """
    Return the minimum number of operations to reduce 'n' to `1`.

    :param n: an integer value
    :return: the minimum number of operations, and
             the path from n to 1, and
             the sequence of operations (useful for debugging and understanding)
    """
    operation_count = 0
    path = [n]
    operations_sequence = []

    while n != 1:  # keep going until we transform the number of pellets to 1

        if n % 2 == 0:  # if we have an even number of pellets
            # Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum
            # antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even
            # number of pellets)
            n = n / 2
            operations_sequence.append("DIVIDE")

        # Use bitwise "and" to make it easier to work out when we need to remove a pellet
        elif (n == 3) or (n & (n + 1)) > ((n - 2) & (n - 1)):
            # Remove one fuel pellet
            n -= 1
            operations_sequence.append("REMOVE")
        else:
            # Add one fuel pellet
            n += 1
            operations_sequence.append("ADD")

        path.append(n)
        operation_count += 1

    return operation_count, path, operations_sequence


def solution(n):
    """
    Minions dump pellets in bulk into the fuel intake. This function figures out the most efficient way to sort and
    shift the pellets down to a single pellet at a time. The fuel intake control panel can only display a number up to
    309 digits long, so there won't ever be more pellets than you can express in that many digits.

    :param n: a positive integer as a string representing the number of pellets dumped in bulk
    :return: the minimum number of operations needed to transform the number of pellets to 1
    """
    try:
        if len(n) > 309:
            return 0

        n = int(n)
    except ValueError:
        return 0
    except TypeError:
        return 0

    if n == 0:
        return 0

    count, _, _ = reduce_to_one(n)

    return count


def list_to_string(s):
    stringified_list = ""

    for character in s:
        stringified_list += character

    return stringified_list


class OperationCountTests(unittest.TestCase):

    def test_15_pellets(self):
        fuel_pellets = '15'
        expected = 5

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_4_pellets(self):
        fuel_pellets = '4'
        expected = 2

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_0_pellets(self):
        fuel_pellets = '0'
        expected = 0

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_157_pellets(self):
        fuel_pellets = '157'
        expected = 10

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_137_steps(self):
        fuel_pellets = '881442566340248816440069375573'
        expected = 137

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_max_pellets(self):
        """
        The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more
        pellets than you can express in that many digits.
        """
        max_pellets = list_to_string(['9'] * 309)
        fuel_pellets = max_pellets
        expected = 1278

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_too_many_pellets(self):
        """
        The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more
        pellets than you can express in that many digits.
        """
        fuel_pellets = list_to_string(['9'] * 310)
        expected = 0

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_pellets_not_a_number(self):
        fuel_pellets = 'eleventy-six'
        expected = 0

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)

    def test_pellets_is_None(self):
        fuel_pellets = None
        expected = 0

        min_operations_needed = solution(fuel_pellets)
        self.assertEqual(expected, min_operations_needed)


class PathTests(unittest.TestCase):

    def test_15_pellets_path(self):
        fuel_pellets = 15
        expected_path = [15, 16, 8, 4, 2, 1]

        _, path, _ = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)

    def test_4_pellets_path(self):
        fuel_pellets = 4
        expected_path = [4, 2, 1]

        _, path, _ = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)

    def test_157_pellets_path(self):
        fuel_pellets = 157
        expected_path = [157, 156, 78, 39, 40, 20, 10, 5, 4, 2, 1]

        _, path, _ = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)


class SequenceOfOperationsTests(unittest.TestCase):

    def test_15_pellets_path(self):
        fuel_pellets = 15
        expected_operations = ['ADD', 'DIVIDE', 'DIVIDE', 'DIVIDE', 'DIVIDE']

        _, _, operations = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_operations, operations)

    def test_4_pellets_path(self):
        fuel_pellets = 4
        expected_operations = ['DIVIDE', 'DIVIDE']

        _, _, operations = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_operations, operations)

    def test_157_pellets_path(self):
        fuel_pellets = 157
        expected_operations = ['REMOVE',
                               'DIVIDE',
                               'DIVIDE',
                               'ADD',
                               'DIVIDE',
                               'DIVIDE',
                               'DIVIDE',
                               'REMOVE',
                               'DIVIDE',
                               'DIVIDE']

        _, _, operations = reduce_to_one(fuel_pellets)
        self.assertEqual(expected_operations, operations)
