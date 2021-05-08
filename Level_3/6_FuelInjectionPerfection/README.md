# Fuel Injection Perfection: Figure out the minimum number of operations required to reduce a given number to 1

## The problem
The fuel control mechanisms have three operations:

1. **Add** one fuel pellet
2. **Remove** one fuel pellet
3. **Divide** the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter
pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called `solution(n)` which takes a positive integer as a string and returns the minimum number of
operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up
to 309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
* `solution(4)` returns `2`: `4 -> 2 -> 1`
* `solution(15)` returns `5`: `15 -> 16 -> 8 -> 4 -> 2 -> 1`

## Solution
Given a number, and given 3 operations: add one, remove one, or divide by 2 only if the number is even, you have to find the quickest way to reduce this number to 1. 

Example 1: `solution(4)` returns `2`: `4 -> 2 -> 1`. The minimum number of operations is 2, i.e., `divide -> divide`.

Example 2:  `solution(15)` returns `5`: `15 -> 16 -> 8 -> 4 -> 2 -> 1`. The minimum number of operations is 5, i.e., `add - > divide -> divide - > divide -> divide`. 

There are three sets of unit tests below, one set each for demonstrating the operation count, the path, and the sequence of operations.

## Implementation

```python
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
```

I wrote a separate function called `transform_to_one()` that takes one argument, a pellet count, and returns the minimum number of operations to get from the pellet count to 1. It also returns the path taken. The solution just requires the number of operations, not the path, but I found the path useful to help me debug the solution and develop my understanding of what's happening.
```python
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
```

## Unit Tests
Google provided the following two test cases.
```text
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2
```

I implemented these as unit tests, and also developed several more tests as I was developing the solution.

### Testing the minimum operations

```python
class FuelInjectionTests(unittest.TestCase):

    def test_15_pellets(self):
        fuel_pellets = '15'
        expected = 5

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_4_pellets(self):
        fuel_pellets = '4'
        expected = 2

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_0_pellets(self):
        fuel_pellets = '0'
        expected = 0

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_157_pellets(self):
        fuel_pellets = '157'
        expected = 10

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_max_pellets(self):
        """
        The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more
        pellets than you can express in that many digits.
        """
        max_pellets = list_to_string(['9'] * 309)
        fuel_pellets = max_pellets
        expected = 1278

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_too_many_pellets(self):
        """
        The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more
        pellets than you can express in that many digits.
        """
        fuel_pellets = list_to_string(['9'] * 310)
        fuel_pellets = fuel_pellets
        expected = 0

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_pellets_not_a_number(self):
        fuel_pellets = 'eleventy-six'
        expected = 0

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)

    def test_pellets_is_None(self):
        fuel_pellets = None
        expected = 0

        transform_to_one_needed = solution(fuel_pellets)
        self.assertEqual(expected, transform_to_one_needed)
```

### Testing the path

The following tests demonstrate the path taken to get from the input number to 1.

```python
class PathTests(unittest.TestCase):

    def test_15_pellets_path(self):
        fuel_pellets = 15
        expected_path = [15, 16, 8, 4, 2, 1]

        _, path, _ = transform_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)

    def test_4_pellets_path(self):
        fuel_pellets = 4
        expected_path = [4, 2, 1]

        _, path, _ = transform_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)

    def test_157_pellets_path(self):
        fuel_pellets = 157
        expected_path = [157, 156, 78, 39, 40, 20, 10, 5, 4, 2, 1]

        _, path, _ = transform_to_one(fuel_pellets)
        self.assertEqual(expected_path, path)
```
### Testing the sequence of operations

The following tests demonstrate the sequence of operations taken to get from the input number to 1.

```python
class SequenceOfOperationsTests(unittest.TestCase):

    def test_15_pellets_path(self):
        fuel_pellets = 15
        expected_operations = ['ADD', 'DIVIDE', 'DIVIDE', 'DIVIDE', 'DIVIDE']

        _, _, operations = transform_to_one(fuel_pellets)
        self.assertEqual(expected_operations, operations)

    def test_4_pellets_path(self):
        fuel_pellets = 4
        expected_operations = ['DIVIDE', 'DIVIDE']

        _, _, operations = transform_to_one(fuel_pellets)
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

        _, _, operations = transform_to_one(fuel_pellets)
        self.assertEqual(expected_operations, operations)
```
## References

