# Queue To Do: Generate the correct checksum for a sequence of numbers

## The problem
You're almost ready to make your move to destroy the LAMBCHOP doomsday device, but the security checkpoints that guard the underlying systems of the LAMBCHOP are going to be a problem. You were able to take one down without tripping any alarms, which is great! Except that as Commander Lambda's assistant, you've learned that the checkpoints are about to come under automated review, which means that your sabotage will be discovered and your cover blown -- unless you can trick the automated review system.

To trick the system, you'll need to write a program to return the same security checksum that the bunny trainers would have after they would have checked all the workers through. Fortunately, Commander Lambda's desire for efficiency won't allow for hours-long lines, so the trainers at the checkpoint have found ways to quicken the pass-through rate. Instead of checking each and every worker coming through, the bunny trainers instead go over everyone in line while noting their worker IDs, then allow the line to fill back up. Once they've done that they go over the line again, this time leaving off the last worker. They continue doing this, leaving off one more worker from the line each time but recording the worker IDs of those they do check, until they skip the entire line, at which point they XOR the IDs of all the workers they noted into a checksum and then take off for lunch. Fortunately, the workers' orderly nature causes them to always line up in numerical order without any gaps.

For example, if the first worker in line has ID 0 and the security checkpoint line holds three workers, the process  would look like this:

```
0 1 2 /
3 4 / 5
6 / 7 8
```

where the trainers' `XOR` (`^`) checksum is `0^1^2^3^4^6 == 2`.

Likewise, if the first worker has ID 17 and the checkpoint holds four workers, the process would look like:

```
17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32
```

which produces the checksum `17^18^19^20^21^22^23^25^26^29 == 14`.

All worker IDs (including the first worker) are between `0` and `2000000000` inclusive, and the checkpoint line will always be at least 1 worker long.

With this information, write a function `solution(start, length)` that will cover for the missing security checkpoint by outputting the same checksum the trainers would normally submit before lunch. You have just enough time to find out the ID of the first worker to be checked (start) and the length of the line (length) before the automatic review occurs, so your program must generate the proper checksum with just those two values.

## Solution
We are told that the checksum is generated using the XOR of a sequence of numbers representing worker IDs.

The XOR operator (exclusive OR, somtimes written with the symbol ⊕) operates on two bits. The result is 0 if the bits have the same value, otherwise the result is 1. Stated another way, the result is 1 iff the values being compared are different. The following truth table illustrates this:

A|B|A ⊕ B
:---:|:---:|:----:
0|0|0
0|1|1
1|0|1
1|1|0

There are 4 properties of XOR to be aware of ([Lewin, 2012](#references); [Stanford CS103](#references)). These properties hold not only when XOR is applied to a single bit, but also when it is applied bitwise to a vector of bits (e.g. a byte).

1. __Commutative__: A ⊕ B = B ⊕ A

    The XOR operation does not depend on the order of the two inputs.
    

2. __Associative__: A ⊕ ( B ⊕ C ) = ( A ⊕ B ) ⊕ C

    XOR operations can be chained together and (building on the first property) the order doesn’t matter.


3. __Identity element__: A ⊕ 0 = A

    Any value XOR’d with zero is left unchanged.


4. __Self-inverting__: A ⊕ A = 0

    Any value XOR’d with itself gives zero.

Applying these properties leads to certain observalbe patterns. The following examples illustrate the repeating pattern that occurs with XOR ([Ballais, 2017](#references)):

```
0 => 0    0000 (0)    0000 (0)    0000 (0)        Output (0 to n)
        ^ 0001 (1)    0001 (1)    0001 (1)        -----------------
        ----------  ^ 0010 (2)    0010 (2)        (0 to 0) 0000 (0) # Equals to n
          0001 (1)  ----------  ^ 0011 (3)        (0 to 1) 0001 (1)
                      0011 (3)  ----------        (0 to 2) 0011 (3) # Equals to n + 1 (2 + 1)
                                  0000 (0)        (0 to 3) 0000 (0)
```

```
  0000 (0)    0000 (0)    0000 (0)    0000 (0)    Output (0 to n)
  0001 (1)    0001 (1)    0001 (1)    0001 (1)    ---------------
  0010 (2)    0010 (2)    0010 (2)    0010 (2)    (0 to 4) 0100 (4) # Its' equal to n
  0011 (3)    0011 (3)    0011 (3)    0011 (3)    (0 to 5) 0001 (1) # Here goes this one again
^ 0100 (4)    0100 (4)    0100 (4)    0100 (4)    (0 to 6) 0111 (7) # And it's equal to n + 1
----------  ^ 0101 (5)    0101 (5)    0101 (5)    (0 to 7) 0000 (0) # And this zero.
  0100 (4)  ----------  ^ 0110 (6)    0110 (6)
              0001 (1)  ----------  ^ 0111 (7)
                          0111 (7)  ----------
                                      0000 (0)
```

 
## Implementation
All the solution code and test code is in [solution.py](solution.py). 

* [Main solution function](#main-solution-code)
* [Unit tests for `solution()`](#unit-tests-for-solution)
* [Function to calculate the XOR of a sequence of numbers in _O_(1) time](#calculate-the-xor-of-a-sequence-of-numbers)
* [Unit tests for calculating the XOR of a sequence of numbers](#unit-tests-for-xor_of_sequence)

### Main solution code
Recall from the [problem description](#the-problem) that the security checkpoint process looks like this (given start ID = 17, and a checkpoint that holds 4 workers):
```
17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32
```
Each time through the checkpoint, the checkpoint checks 1 worker fewer than the previous check. In other words, if we treat the checkpoint as a _row_, the size of the row is shrinking by 1 each time.

The `solution()` function treats each _row_ as a sequence of IDs, and apply the following algorithm: 
* Iterate through each _row_ shrinking the row length by 1 after each iteration.
* We determine the first and last ID in the sequence
* Get the XOR of that sequence
* Then we chain together the XOR of each sequence to get the final security checksum

I placed the logic to calculate the XOR of a sequence of numbers [in a separate function, described later,](#calculate-the-xor-of-a-sequence-of-numbers) called `xor_of_sequence()`. The main `solution()` function is here:

```python
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
```

### Unit Tests for `solution()`
The unit tests in this section are for the `solution()` function. Google offers these two test cases. There are also a bunch of hidden tests that the code must pass.

```
Input:
solution.solution(0, 3)
Output:
    2

Input:
solution.solution(17, 4)
Output:
    14
```
I implemented these two test cases as unit tests, and built up some more tests for different moves and conditions. All the tests are available in [solution.py](solution.py).

```python
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
```

### Calculate the XOR of a sequence of numbers
I decidede to factor the logic for calculating the XOR of a sequence of numbers into its own function. The `xor_of_sequence()` function implements the logic to calculate the XOR of a sequence of numbers from `first` to `last`, inclusive.

We can take advantage of the [XOR pattern described above](#solution) to reduce the number of XOR operations to _O(1)_, using the correct pattern depending on whether the first number in the sequence is odd or even.

```python
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
```
### Unit Tests for `xor_of_sequence()`
These test cases are specifically for the `xor_of_sequence()` function:
```python
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
```


## References
* Andrew S. Tanenbaum; David J. Wetherall, 2010. _Computer Networks, Fifth Edition. Chapter 3: The Data Link Layer._ Pearson.
* Chuck Easttom, 2015. _Modern Cryptography: Applied Mathematics for Encryption and Information Security. Chapter9: Cryptographic Hashes._ McGraw-Hill.
* Wikipedia. [Checksum](https://en.wikipedia.org/wiki/Checksum)
* Wikipedia. [Exclusive or (XOR)](https://en.wikipedia.org/wiki/Exclusive_or)
* Sean Francis N. Ballais, Jan 2017. [The XOR Pattern](https://codereview.stackexchange.com/a/153274)
* Roger Germundsson and Eric W. Weisstein. [XOR](https://mathworld.wolfram.com/XOR.html). MathWorld - A Wolfam Web Resource.
* Khan Academy. [XOR bitwise operation](https://www.khanacademy.org/computing/computer-science/cryptography/ciphers/a/xor-bitwise-operation)
* Michael Lewin. [All About XOR](https://accu.org/journals/overload/20/109/lewin_1915/). Overload, 20(109):14-19, June 2012.
* Stanford [CS103: Mathematical Foundations of Computing / Math 161: Set Theory: Direct Proofs.](https://web.stanford.edu/class/archive/cs/cs103/cs103.1142/lectures/01/Small01.pdf). See section titled _'Extended Example: XOR'_.
