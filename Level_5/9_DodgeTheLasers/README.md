# Dodge the Lasers: Implementing the Beatty Sequence
## The problem
Given the string representation of an integer `n`, return the sum of `(floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2)))` as a string. That is, for every number `i` in  the range `1` to `n`, add up all the integer portions of `i*sqrt(2)`.

For example, if `str_n` was `"5"`, the solution would be calculated as
```
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
```
so the function would return `"19"`.

`str_n` will be a positive integer between `1` and `10^100`, inclusive.

## Solution
This problem is an example of the [Beatty Sequence](https://en.wikipedia.org/wiki/Beatty_sequence). "_In mathematics, a Beatty sequence (or homogeneous Beatty sequence) is the sequence of integers found by taking the floor of the positive multiples of a positive irrational number. Beatty Sequences are named after Samuel Beatty, who wrote about them in 1926._" (Wikipedia).

From [The Online Encyclopedia of Integer Sequences](https://oeis.org/A001951):
> Beatty sequence: `a(n) = floor(n*sqrt(2))`

A spectrum sequence is a sequence formed by successive multiples of a real number `a` rounded down to the nearest integer `s_n=floor(na)`. If `a` is irrational, the spectrum is called a Beatty sequence.

An [irrational number](https://mathworld.wolfram.com/IrrationalNumber.html) is a number that cannot be expressed as a fraction `p/q` for any integers `p` and `q`. Irrational numbers have decimal expansions that neither terminate nor become periodic. Every transcendental number is irrational.  The most famous irrational number is `sqrt(2)`.

## Implementation
Since `n` can be very large (up to 101 digits), using  just `sqrt(2)` and a loop won't work. This is the implementation of the function with the specified signature `def solution(s):`.

```python
from decimal import Decimal, getcontext

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
```

I implemented the Beatty Sequence in a separate function. For the purpose of the `Foobar` challenge, I didn't really need to parameterize `alpha`. I could have hardcoded the function to use `sqrt(2)`. However, some [references I read](#References) pointed to the Beatty Sequence working with other positive irrational numbers; `sqrt(2)` just happens to be the most famous one. So, the requirement to work with `sqrt(2)` is captured in the `solution(s)` function, and `solution()` passes `sqrt(2)` to the `beatty_sequnce()` as the `alpha` parameter.

```python
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
```

## Unit Tests
These are the 2 test cases provided by Google. 
```text
Input:
solution.solution('77')
Output:
    4208

Input:
solution.solution('5')
Output:
    19
```

There are also a bunch of hidden tests that the code must pass, but they don't tell you what those tests are. This is the set of unit test I built up along the way.  

```python
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
```

## References
* Wikipedia. [Beatty Sequence](https://en.wikipedia.org/wiki/Beatty_sequence)
* Weisstein, Eric W. ["Beatty Sequence."](https://mathworld.wolfram.com/BeattySequence.html) From MathWorld--A Wolfram Web Resource.
* https://www.cut-the-knot.org/proofs/Beatty.shtml
* https://www.cut-the-knot.org/proofs/Beatty2.shtml
* https://mathworld.wolfram.com/SpectrumSequence.html
* https://mathworld.wolfram.com/IrrationalNumber.html
* https://oeis.org/A001951
* Kevin O’Bryant, 2002. [A Generating Function Technique for Beatty Sequences and Other Step Sequences](https://www.researchgate.net/publication/222660942_A_Generating_Function_Technique_for_Beatty_Sequences_and_Other_Step_Sequences). Journal of Number Theory
* Stolarsky, K.B., 1976. [Beatty sequences, continued fractions, and certain shift operators](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/D243EA5C706BB0DD0C85419AAE4235C3/S0008439500063979a.pdf/div-class-title-beatty-sequences-continued-fractions-and-certain-shift-operators-div.pdf). Canadian Mathematical Bulletin, 19(4), pp.473-482.
* Vandervelde, S., [Beyond Beatty sequences: complementary lattices](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/abs/beyond-beatty-sequences-complementary-lattices/9B065104110E7B0A1F9D1A1C3CEDCB65). Canadian Mathematical Bulletin, pp.1-13.
* [mercio](https://math.stackexchange.com/users/17445/mercio), 2016. [How to find ∑𝑖=1...n ⌊ 𝑖 √2⌋ A001951 A Beatty sequence: a(n) = floor(n*sqrt(2))](https://math.stackexchange.com/questions/2052179/how-to-find-sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s/2053713#2053713)
* [Variation of a Beatty Sequence](https://math.stackexchange.com/questions/2828779/variation-of-a-beatty-sequence)
* [How to precisely find the sum of a Beatty Sequence](https://math.stackexchange.com/questions/4019479/how-to-precisely-find-the-sum-of-a-beatty-sequence)

## Related code examples
* https://www.geeksforgeeks.org/beatty-sequence/
* https://github.com/oneshan/foobar/tree/master/dodge_the_lasers
* https://vitaminac.github.io/Google-Foobar-Dodge-The-Lasers/
* https://github.com/sun-mylove/google-foobar/blob/master/lev05_ch01.py
* https://github.com/arinkverma/google-foobar/blob/master/5.1_dodge_the_lasers.py
