import unittest


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

        # p cannot have more than 10000 converters
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
