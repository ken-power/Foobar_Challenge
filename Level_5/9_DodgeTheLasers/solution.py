import unittest

from decimal import Decimal, getcontext


def beatty_sequence(alpha, n):
    """
    A Beatty sequence (or homogeneous Beatty sequence) is the sequence of integers found by taking the floor of the
    positive multiples of a positive irrational number. Beatty sequences are named after Samuel Beatty, who wrote about
    them in 1926.

    From The Online Encyclopedia of Integer Sequences:
         Beatty sequence: a(n) = floor(n*sqrt(2))

    Since at each step n is approximately multiplied by sqrt(2)-1, the arguments decrease exponentially.
    For n=10**100 (which is our given upper limit) we need approximately ceil(100 log 10 / log(sqrt(2) -1)) = 262 steps
    to complete the recursion.

    https://en.wikipedia.org/wiki/Beatty_sequence
    https://mathworld.wolfram.com/BeattySequence.html
    https://oeis.org/A001951
    https://math.stackexchange.com/questions/2052179/how-to-find-sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s/2053713#2053713

    :param alpha: some irrational positive number, e.g., square root of 2
    :param n: defines the range 1 to n
    :return: the Beatty sequence of n
    """
    if n == 1:
        return 1
    if n < 1:
        return 0

    if alpha >= 2:
        beta = alpha - 1
    else:
        beta = alpha

    # From the Beatty Sequence proof:
    # n' = floor((alpha - 1) * n)
    n_prime = int((alpha - 1) * n)

    # S(alpha, n) = (n * n') + n(n+1)/2 - n'(n' + 1)/2 - S(beta,n')
    p = n * n_prime  # Let p = (n * n')
    q = n * (n + 1) // 2  # Let q = n'(n' + 1)/2
    r = n_prime * (n_prime + 1) // 2  # Let r = n'(n' + 1)/2

    # S(alpha, n) = p + q - r - S(beta,n')
    return p + q - r - beatty_sequence(beta, n_prime)


def solution(s):
    """
    Given the string representation of an integer n, for every number i in the range 1 to n, add up all of
    the integer portions of i*sqrt(2).

    :param s: string representation of an integer n
    :return: the sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string
    """
    # check the input string is a valid length
    min_length = 1
    max_length = 101

    if len(s) < min_length or len(s) > max_length:
        return ''

    # need to handle integers between 1 and 10^100, so up to 101 decimal places of precision
    # The Python default is 28 significant figures
    # https://www.geeksforgeeks.org/setting-precision-in-python-using-decimal-module/
    getcontext().prec = max_length

    n = int(s)
    alpha = Decimal(2).sqrt()
    sequence = beatty_sequence(alpha, n)

    return str(int(sequence))


class BeattySequenceTests(unittest.TestCase):

    def test_1(self):
        str_n = '77'
        expected_sequence = '4208'

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)

    def test_2(self):
        str_n = '5'
        expected_sequence = '19'

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)

    def test_10_exp_100_digits(self):
        str_n = str(10 ** 100)
        expected_sequence = '70710678118654752440084436210484903928483593768847403658833986899536623923105351' \
                            '94251937671638207863882176012341109009525468542384102725348056545173973715745405982' \
                            '3250037671948325191776995310741236436'

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)

    def test_101_digits(self):
        str_n = '123456789012345678901234567890123456789012345678901234567890123456789012345678901' \
                '23456789012345678901'
        expected_sequence = '107774236924039859632044810881278020158277641612068310357589977725221362646591451' \
                            '082548927428153331053477645008279833575656700346327082289577362441794327936796969132' \
                            '662041870868815485920720321329378915'

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)

    def test_102_digits(self):
        str_n = '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567' \
                '890123456789012'
        expected_sequence = ''

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)

    def test_0_digits(self):
        str_n = ''
        expected_sequence = ''

        sequence = solution(str_n)
        self.assertEqual(expected_sequence, sequence)
