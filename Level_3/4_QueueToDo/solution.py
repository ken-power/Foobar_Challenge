import unittest


def xor_of_sequence(first, last):
    """
    Get the XOR of a sequence of numbers. We can take advantage of the fact that the XOR operation repeats itself for
    sequential numbers.

    :param first: the first number in the sequence
    :param last: the last number in the sequence
    :return: the XOR of the sequence
    """
    if first % 2 == 0:  # if the first number in the sequence is even
        xor_pattern = [last, 1, last + 1, 0]
    else:  # if the first number in the sequence is odd
        xor_pattern = [first, first ^ last, first - 1, (first - 1) ^ last]

    return xor_pattern[(last - first) % 4]  # the XOR pattern repeats every 4 numbers


def solution(start, length):
    """
    A function that returns the same security checksum that the bunny trainers would have after they
    would have checked all the workers through. Fortunately, the workers' orderly nature causes them to always
    line up in numerical order without any gaps.

    :param start: a positive integer representing the ID of the first worker to be checked
    :param length: a positive integer representing the length of the line before the automatic review occurs
    :return: the same security checksum that the bunny trainers would have after they would have checked all
             the workers through
    """
    # All worker IDs (including the first worker) are between 0 and 2000000000 inclusive, and the checkpoint line
    # will always be at least 1 worker long.
    max_id = 2000000000
    range_boundary = start + length * length

    if range_boundary > max_id or start < 0 or length < 0:
        return None

    security_checksum = 0

    for security_id in range(0, length):  # treat each 'row' as a sequence of numbers
        first = start + (length * security_id)  # the first number in the row / sequence
        last = first + (length - security_id) - 1  # the last number in the row / sequence

        security_checksum ^= xor_of_sequence(first, last)  # update the checksum with the XOR for each row

    return security_checksum


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(ChecksumTests)
    suite.addTest(XorTests)

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_tests())


class ChecksumTests(unittest.TestCase):
    """
    Test cases to validate the security checksum calculated based on just the length of the line, and the ID of the
    first worker in the line.
    """

    def test_line_length_3(self):
        """
        If the first worker in line has ID 0 and the security checkpoint line holds three workers,
        the process would look like this:

        0 1 2 /
        3 4 / 5
        6 / 7 8

        where the trainers' XOR (^) checksum is 0^1^2^3^4^6 == 2.
        """
        id_of_first_worker_to_be_checked = 0
        line_length = 3
        expected_checksum = 2

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_line_length_4(self):
        """
        If the first worker has ID 17 and the checkpoint holds four workers,
        the process would look like:

        17 18 19 20 /
        21 22 23 / 24
        25 26 / 27 28
        29 / 30 31 32

        which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.
        """
        id_of_first_worker_to_be_checked = 17
        line_length = 4
        expected_checksum = 14

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_line_length_5(self):
        """
        If the first worker has ID 35 and the checkpoint holds five workers,
        the process would look like:

        35 36 37 38 39 /
        40 41 42 43 / 44
        45 46 47 / 48 49
        50 51 / 52 53 54
        55 / 56 57 58 59

        which produces the checksum 35^36^37^38^39^40^41^42^43^45^46^47^50^51^55 == 57.
        """
        id_of_first_worker_to_be_checked = 35
        line_length = 5
        expected_checksum = 57

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_line_length_1000(self):
        """
        If the first worker has ID 11 and the checkpoint holds 1000 workers,
        that gives us 1 million workers:
        """
        id_of_first_worker_to_be_checked = 11
        line_length = 1000
        expected_checksum = 532896

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_line_length_2000(self):
        """
        If the first worker has ID 1 and the checkpoint holds 2000 workers,
        that gives us 2 million workers:
        """
        id_of_first_worker_to_be_checked = 1
        line_length = 20000
        expected_checksum = 391607840

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_line_too_long(self):
        id_of_first_worker_to_be_checked = 1
        line_length = 2000000001
        expected_checksum = None

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_negative_line(self):
        id_of_first_worker_to_be_checked = 34
        line_length = -4
        expected_checksum = None

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)

    def test_negative_start_id(self):
        id_of_first_worker_to_be_checked = -34
        line_length = 334
        expected_checksum = None

        checksum = solution(id_of_first_worker_to_be_checked, line_length)
        self.assertEqual(expected_checksum, checksum)


class XorTests(unittest.TestCase):
    """
    Test cases for the XOR calculation. Contains tests for single sequences and chains of sequences.
    """

    def test_17_to_20(self):
        self.assertEqual(17, xor_of_sequence(17, 29))

    def test_0_to_16(self):
        self.assertEqual(16, xor_of_sequence(0, 16))

    def test_12_to_22(self):
        self.assertEqual(23, xor_of_sequence(12, 22))

    def test_17_to_32(self):
        self.assertEqual(48, xor_of_sequence(17, 32))

    def test_sequence_17_29(self):
        checksum = xor_of_sequence(17, 20)
        checksum ^= xor_of_sequence(21, 23)
        checksum ^= xor_of_sequence(25, 26)
        checksum ^= xor_of_sequence(29, 29)

        self.assertEqual(14, checksum)

    def test_sequence_0_6(self):
        checksum = xor_of_sequence(0, 2)
        checksum ^= xor_of_sequence(3, 4)
        checksum ^= xor_of_sequence(6, 6)

        self.assertEqual(2, checksum)

    def test_sequence_35_55(self):
        checksum = xor_of_sequence(35, 39)
        checksum ^= xor_of_sequence(40, 43)
        checksum ^= xor_of_sequence(45, 47)
        checksum ^= xor_of_sequence(50, 51)
        checksum ^= xor_of_sequence(55, 55)

        self.assertEqual(57, checksum)
