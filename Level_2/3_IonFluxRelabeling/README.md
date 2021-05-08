# Ion Flux Relabeling: Finding the parents of each of a given set of nodes in a perfect binary tree

## The problem
Oh no! Commander Lambda's latest experiment to improve the efficiency of the LAMBCHOP doomsday device has backfired spectacularly. The Commander had been improving the structure of the ion flux converter tree, but something went terribly wrong and the flux chains exploded. Some of the ion flux converters survived the explosion intact, but others had their position labels blasted off. Commander Lambda is having her henchmen rebuild the ion flux converter tree by hand, but you think you can do it much more quickly -- quickly enough, perhaps, to earn a promotion!

Flux chains require perfect binary trees, so Lambda's design arranged the ion flux converters to form one. To label them, Lambda performed a post-order traversal of the tree of converters and labeled each converter with the order of that converter in the traversal, starting at 1. For example, a tree of 7 converters would look like the following:

```
   7
 3   6
1 2 4 5
```

Write a function `solution(h, q)` - where `h` is the height of the perfect tree of converters and `q` is a list of positive integers representing different flux converters - which returns a list of integers `p` where each element in `p` is the label of the converter that sits on top of the respective converter in `q`, or `-1` if there is no such converter.  For example, `solution(3, [1, 4, 7])` would return the converters above the converters at indexes `1`, `4`, and `7` in a perfect binary tree of height `3`, which is `[3, 6, -1]`.

The domain of the integer `h` is `1 <= h <= 30`, where `h = 1` represents a perfect binary tree containing only the root, `h = 2` represents a perfect binary tree with the root and two leaf nodes, `h = 3` represents a perfect binary tree with the root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists `q` and `p` contain at least one but no more than 10000 distinct integers, all of which will be between `1` and `2^h-1`, inclusive.

## Solution
We are told in the problem description that we are working with perfect binary trees.

A couple of special binary trees are as follows ([Strecansky, 2020](#references); [Wikipedia](#references)):

* **Full binary tree**: Every node sans the leaf nodes has 2 child nodes.
* **Complete binary tree**: A tree that is completely filled, sans the bottom layer. The bottom layer must be filled from left to right.
* **Perfect binary tree**: A complete binary tree in which all the interior nodes have two children and all the leaves of the tree are at the same depth or level.

So a perfect binary tree is a _complete_ binary tree, but not a complete binary trees is not necessarily a _perfect_ binary tree.

In a perfect full binary tree, `l=2^h` thus `n=2^(h+1) - 1`.


## Implementation

We already know from the problem description that we need to implement a perfect binary tree. Now, we need to choose a data structure to represent the perfect binary tree. Two basic options are a binary heap and a binary search tree ([Giladi, 2008](#references)). 

_The **binary heap**, which is often used for priority queues.This structure is an array that represents a complete binary tree (or almost); the last (lowest) level can be empty in its rightmost leaves. The array contains the values of the tree’s nodes, level after level, in the order of the nodes of the tree. The heap property is maintained, which means that a node can have a value that equals, at most, its father’s value. Some results of this data structure are as follows: The place in the array of the parent of a node `x` is `⌊x/2⌋`, its left child is `2x` and its right child is `2x + 1`. Inserting a value to the binary heap has a time complexity of `O(log n)`, where `n` is the number of elements in the binary heap, but searching is not efficient in this structure at all._

_A much better way to handle searches in terms of efficiency is with the **binary search tree (BST)**. In BST representation, every node in the binary tree is kept in a structure, along with pointers to its parent node and the left and the right children nodes. In a BST, the keys always maintain the property that if `x` is a node and `y` is a node in the left sub-tree of `x`, then `key(y) < key(x)`, and the other way around; that is, if `y` is a node in the right sub-tree of `x`, then `key(x) ≤ key(y)`._

 Working with a perfect binary tree gives us several performance advantages. The running times of BST algorithms are ultimately dependent on the shape of the trees, and the shape of the trees is dependent on the order in which the keys are inserted. Understanding this dependence is a critical factor in being able to use BSTs effectively in practical situations ([Sedgewick, et al. 2015](#references)).

_Searching for a key in BSTs starts in the root and at every level a comparison is done on the node’s key and the search may continue in one of the branches to a lower level. Thus, the search has a time complexity of `O(h)`, where `h` is the height of BST. If the binary tree is full, then the time complexity of conducting a search in the worst case will be of `θ(log n)`, where `n` is the number of nodes in the tree, since `h` in this case is `O(log n)`. However, if the BST is not representing a full tree, the time complexity is worse than of `θ(log n)`, and in the case of a linear “chained” tree, it can reach the complexity of `θ(n)`. In case of a randomly built BST, that is every added node has a randomly chosen key, then the height of the tree h is again `O(log n)`, and the search complexity is of `θ(log n)`._

This is the implementation of the `solution()` function. All code is available in [solution.py](solution.py).

```python
def solution(h, q):
    """
    :param h: the height of the perfect tree of converters
    :param q: a list of positive integers representing different flux converters
    :return: a list of integers p where each element in p is the label of the converter that sits on top of the
            respective converter in q, or -1 if there is no such converter

    The domain of the integer h is 1 <= h <= 30, where h = 1 represents a perfect binary tree containing only the root,
    h = 2 represents a perfect binary tree with the root and two leaf nodes, h = 3 represents a perfect binary tree
    with the root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists q and p
    contain at least one but no more than 10000 distinct integers, all of which will be between 1 and 2^h-1, inclusive.
    """
    max_nodes = pow(2, h + 1) - 1
    root = pow(2, h) - 1
    num_flux_converters = len(q)
    no_such_converter = -1

    print("tree height = {}; nodes = {}; root node = {}; len(q)={}".format(h, max_nodes, root, num_flux_converters))

    # The domain of h is 1 <= h <= 30
    if h < 1 or h > 30:
        return [no_such_converter]

    # There can't be more flux converters than there are nodes in the tree
    if num_flux_converters > max_nodes:
        return [no_such_converter]

    # The list q contains at least one but no more than 10000 distinct integers
    converter_size_limit = 10000
    if num_flux_converters < 1 or num_flux_converters > converter_size_limit:
        return [no_such_converter]

    p = []

    for flux_converter in q:

        # p can't have more than 10000 converters
        if len(p) >= converter_size_limit:
            break

        # No flux converter can be bigger than the max node value in the tree
        if flux_converter <= max_nodes:

            # Each node with value n is a parent for (n-1)/2 on the LEFT and (n-1) on the RIGHT.
            parent_node = parent(h, flux_converter)

            # p contains distinct integers, i.e., a flux converter can be present at most once
            if parent_node not in p:
                p.append(parent_node)

    # The list p contains at least one converter
    if len(p) < 1:
        p = [no_such_converter]

    return p
```
I factored the logic to find the parent of given node in a tree of size `h` into the `parent(h, node)` funciton.  
```python
def parent(h, node):
    """
    Find the parent of the given node.

    :param h: the height of the tree
    :param node: the node whose parent we seek
    :return: the parent of the given node
    """
    start = 1
    root = pow(2, h) - 1

    # return -1 if node is a root node
    if node == root:
        return -1

    # otherwise, let's initialize end to be same as root
    end = root

    # Find the given node
    while node > 0:
        end = end - 1

        # Find the middle node of the tree because at every level, the tree parent is divided into two halves
        middle_node = start + (end - start) // 2

        # if the node is found then return the parent;
        # the child nodes of every node is either (node / 2) or (node-1)
        if middle_node == node or end == node:
            return end + 1

        # if the node to be found is greater than the mid then search the left subtree
        elif node < middle_node:
            end = middle_node
        # else search the right subtree
        else:
            start = middle_node
```

## Unit Tests
Google offers these two test cases. There are also a bunch of hidden tests that the code must pass.

```
Input:
solution.solution(3, [7, 3, 5, 1])
Output:
    -1,7,6,3

Input:
solution.solution(5, [19, 14, 28])
Output:
    21,15,29
```
I implemented these two test cases as unit tests, and built up some more tests for different moves and conditions. All the tests are available in [solution.py](solution.py).

```python
class IonFluxRelabelingTests(unittest.TestCase):

    def test_height_3(self):
        tree_height = 3
        flux_converters = [7, 3, 5, 1]
        expected_converters = [-1, 7, 6, 3]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_height_5(self):
        tree_height = 5
        flux_converters = [19, 14, 28]
        expected_converters = [21, 15, 29]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_height_4(self):
        tree_height = 4
        flux_converters = [6]
        expected_converters = [7]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_height_2(self):
        tree_height = 2
        flux_converters = [2]
        expected_converters = [3]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_height_29(self):
        tree_height = 29
        flux_converters = [19, 14, 28, 167, 412]
        expected_converters = [21, 15, 29, 168, 413]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_height_30(self):
        tree_height = 30
        flux_converters = [19, 14, 28, 167, 412, 2147483]
        expected_converters = [21, 15, 29, 168, 413, 2147485]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_converters_must_be_distinct(self):
        tree_height = 5
        flux_converters = [26, 27, 28, 29, 30, 31]
        expected_converters = [28, 29, 30, 31, -1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_tree_height_0(self):
        tree_height = 0
        flux_converters = [1]
        expected_converters = [-1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_tree_exceeds_max_height(self):
        tree_height = 31
        flux_converters = [1, 56, 13, 7, 9]
        expected_converters = [-1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_no_converters(self):
        tree_height = 3
        flux_converters = []
        expected_converters = [-1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_converters_outside_range(self):
        tree_height = 1
        flux_converters = [423, 9231, 9334, 122]
        expected_converters = [-1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)

    def test_flux_converter_values_greater_than_possible_node_value(self):
        tree_height = 3
        flux_converters = [423, 9231, 9334, 122]
        expected_converters = [-1]

        converters = solution(tree_height, flux_converters)
        self.assertEqual(expected_converters, converters)
```

## References
* Robert Sedgewick and Kevin Wayne, 2011. _Algorithms, Fourth Edition. Chapter 3: Searching._ Addison-Wesley Professional.
* Wikipedia. [Binary Tree](https://en.wikipedia.org/wiki/Binary_tree)
* Ran Giladi, 2008. _Network Processors. Chapter 5: Packet Processing._ Morgan Kaufmann.
* Bob Strecansky, 2020. _Hands-On High Performance with Go_. Packt Publishing.
* Robert Sedgewick; Robert Dondero; Kevin Wayne, 2015. _Introduction to Programming in Python: An Interdisciplinary Approach. Chapter 4: Algorithms and Data Structures._ Addison-Wesley Professional.
