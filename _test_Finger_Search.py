from Finger_Search import (
        _is_the_pred_node,
        _finger_search_search_down,
        _finger_search_search_exp_larger,
        _finger_search_search_exp_smaller,
        finger_search_LCA_version,
        _finger_search_LCA_version_search_larger,
        _finger_search_LCA_version_search_smaller,
        finger_search_paper_version,
        _finger_search_paper_version_search_larger,
        _finger_search_paper_version_search_smaller,
        finger_search_whiteboard_version,
        _finger_search_whiteboard_version_search_larger,
        _finger_search_whiteboard_version_search_smaller,
        _finger_search_whiteboard_version_search_larger_optimized,
        _finger_search_whiteboard_version_search_smaller_optimized,
)
from Many_Pointers_Red_Black_Tree import Red_Black_Tree, Red_Black_Node
import random

import Pointer_Counting

from __test_decorators import test, test_group, test_file


# ---------------------------------------------
#                Tree creators
# ---------------------------------------------

def create_tree(n, seed=42, do_wrap=False):
    """
    Create a Red-Black Tree with n nodes, using the given seed for randomization.
    """
    tree = Red_Black_Tree()
    values = list(range(n))
    random.seed(seed)
    random.shuffle(values)

    if do_wrap:
        values = [Pointer_Counting.compare_wrap_value(v) for v in values]

    for value in values:
        tree.insert(value)

    return tree


class Deactivate_Pred_Succ_Node:
    def __init__(self, node):
        self._node = node

    @property
    def value(self):
        return self._node.value

    @property
    def parent(self):
        return deactivate_pred_succ(self._node.parent)
    
    @parent.setter
    def parent(self, parent):
        raise AttributeError("Cannot set parent of Deactivate_Pred_Succ_Node")

    @property
    def left(self):
        return deactivate_pred_succ(self._node.left)
    
    @left.setter
    def left(self, left):
        raise AttributeError("Cannot set left of Deactivate_Pred_Succ_Node")

    @property
    def right(self):
        return deactivate_pred_succ(self._node.right)
    
    @right.setter
    def right(self, right):
        raise AttributeError("Cannot set right of Deactivate_Pred_Succ_Node")

    @property
    def pred(self):
        raise AttributeError("Cannot get pred of Deactivate_Pred_Succ_Node")
    
    @pred.setter
    def pred(self, pred):
        raise AttributeError("Cannot set pred of Deactivate_Pred_Succ_Node")
    
    @property
    def succ(self):
        raise AttributeError("Cannot get succ of Deactivate_Pred_Succ_Node")
    
    @succ.setter
    def succ(self, succ):
        raise AttributeError("Cannot set succ of Deactivate_Pred_Succ_Node")

    @property
    def is_red(self):
        raise AttributeError("Cannot get is_red of Deactivate_Pred_Succ_Node")
    
    @property
    def is_black(self):
        raise AttributeError("Cannot get is_black of Deactivate_Pred_Succ_Node")

    def set_red(self):
        raise AttributeError("Cannot set red of Deactivate_Pred_Succ_Node")
    
    def set_black(self):
        raise AttributeError("Cannot set black of Deactivate_Pred_Succ_Node")

    def __repr__(self):
        return self._node.__repr__()

def deactivate_pred_succ(node):
    if node is None:
        return None
    return Deactivate_Pred_Succ_Node(node)

# ---------------------------------------------
#                Test helpers
# ---------------------------------------------

@test
def test_is_pred_node():
    node1 = Red_Black_Node(1)
    node2 = Red_Black_Node(2)
    node3 = Red_Black_Node(3)
    node4 = Red_Black_Node(4)

    node1.succ = node2
    node2.succ = node3
    node3.succ = node4
    node2.pred = node1
    node3.pred = node2
    node4.pred = node3

    # Pred is equal to the value
    assert _is_the_pred_node(node1, 1) == True
    assert _is_the_pred_node(node2, 2) == True
    assert _is_the_pred_node(node3, 3) == True
    assert _is_the_pred_node(node4, 4) == True

    # Pred is not equal to the value
    assert _is_the_pred_node(node1, 1.5) == True
    assert _is_the_pred_node(node2, 2.5) == True
    assert _is_the_pred_node(node3, 3.5) == True

    # Pred is the last node
    assert _is_the_pred_node(node4, 4.5) == True
    assert _is_the_pred_node(node4, 10) == True

    # Pred is None
    assert _is_the_pred_node(node1, 0) == False
    assert _is_the_pred_node(node1, -10) == False

    # Pred is later
    assert _is_the_pred_node(node1, 2) == False
    assert _is_the_pred_node(node1, 3) == False
    assert _is_the_pred_node(node2, 3) == False
    assert _is_the_pred_node(node3, 5) == False
    assert _is_the_pred_node(node3, 5) == False

    # Pred is earlier
    assert _is_the_pred_node(node2, 1) == False
    assert _is_the_pred_node(node3, 2) == False
    assert _is_the_pred_node(node4, 2) == False

@test
def test_finger_search_down():
    tree = create_tree(100, seed=42)
    root = tree._root

    # Exact search
    for i in range(100):
        found_node = _finger_search_search_down(root, i)
        assert found_node is not None
        assert found_node.value == i
    
    # Search between
    for i in range(99):
        found_node = _finger_search_search_down(root, i + 0.5)
        assert found_node is not None
        assert found_node.value == i
    
    # Search before first, yields first node
    found_node = _finger_search_search_down(root, -1)
    assert found_node is not None
    assert found_node.value == 0

    # Search after last, yields last node
    found_node = _finger_search_search_down(root, 100)
    assert found_node is not None
    assert found_node.value == 99

    # Search in subtree which does not have largest, yields largest in the subtree
    found_node = _finger_search_search_down(root.left, 99)
    assert found_node is not None
    assert found_node.value != 99
    assert found_node.right is None

@test
def test_finger_search_exp_larger_non_fails():
    tree = create_tree(100, seed=42)
    smallest = tree._root
    while smallest.left is not None:
        smallest = smallest.left
    
    assert smallest is not None
    assert smallest.value == 0

    # Excact search
    for to_value in range(1, 100):
        found_node = _finger_search_search_exp_larger(smallest, to_value)
        assert found_node is not None
        assert found_node.value == to_value
    
    # Search between
    for to_value in range(1, 100):
        found_node = _finger_search_search_exp_larger(smallest, to_value + 0.5)
        assert found_node is not None
        assert found_node.value == to_value
    
    # Search after last yields last node
    found_node = _finger_search_search_exp_larger(smallest, 100)
    assert found_node is not None
    assert found_node.value == 99

@test
def test_finger_search_exp_larger_may_fail():
    tree = create_tree(100, seed=42)
    non_smallest = tree._root.left.right
    while non_smallest.left is not None:
        non_smallest = non_smallest.left
    
    assert non_smallest is not None

    # Search for values in the subtree does not fail
    for to_value in range(non_smallest.value + 1, tree._root.value):
        found_node = _finger_search_search_exp_larger(non_smallest, to_value)
        assert found_node is not None
        assert found_node.value == to_value, (found_node, to_value)

    # Search for values not contained in the subtree fails
    for to_value in range(tree._root.value, 100):
        found_node = _finger_search_search_exp_larger(non_smallest, to_value)
        assert found_node is not None
        assert not _is_the_pred_node(found_node, to_value)
        assert found_node.value < to_value

@test
def test_finger_search_exp_smaller_non_fails():
    tree = create_tree(100, seed=42)
    largest = tree._root
    while largest.right is not None:
        largest = largest.right
    
    assert largest is not None
    assert largest.value == 99

    # Exact search
    for to_value in range(0, 99):
        found_node = _finger_search_search_exp_smaller(largest, to_value)
        assert found_node is not None
        assert found_node.value == to_value
    
    # Search between
    for to_value in range(0, 99):
        found_node = _finger_search_search_exp_smaller(largest, to_value + 0.5)
        assert found_node is not None
        assert found_node.value == to_value
    
    # Search before first yields None
    found_node = _finger_search_search_exp_smaller(largest, -1)
    assert found_node is None

@test
def test_finger_search_exp_smaller_may_fail():
    tree = create_tree(100, seed=42)
    non_largest = tree._root.right.left
    while non_largest.right is not None:
        non_largest = non_largest.right
    
    assert non_largest is not None
    
    # Search for values in the subtree does not fail
    for to_value in range(tree._root.value + 1, non_largest.value - 1):
        found_node = _finger_search_search_exp_smaller(non_largest, to_value)
        assert found_node is not None
        assert found_node.value == to_value

    # Search for values not contained in the subtree fails
    for to_value in range(tree._root.value + 1):
        found_node = _finger_search_search_exp_smaller(non_largest, to_value)
        assert found_node is not None, (found_node, to_value)
        assert not _is_the_pred_node(found_node, to_value)
        assert found_node.value > to_value

@test_group
def test_helpers():
    test_is_pred_node()
    test_finger_search_down()

    test_finger_search_exp_larger_non_fails()
    test_finger_search_exp_larger_may_fail()
    test_finger_search_exp_smaller_non_fails()
    test_finger_search_exp_smaller_may_fail()


# ---------------------------------------------
#                Test LCA version
# ---------------------------------------------

@test
def test_LCA_version_exact_search_larger():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = _finger_search_LCA_version_search_larger(start, end_value)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value

@test
def test_LCA_version_pred_search_larger():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = _finger_search_LCA_version_search_larger(start, end_value + 0.5)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value

@test
def test_LCA_version_exact_search_smaller():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = _finger_search_LCA_version_search_smaller(start, end_value)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value

@test
def test_LCA_version_pred_search_smaller():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = _finger_search_LCA_version_search_smaller(start, end_value + 0.5)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value, (start, found_node, end_value)

@test
def test_LCA_version_exact_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = finger_search_LCA_version(start, end_value)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value

@test
def test_LCA_version_pred_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = deactivate_pred_succ(tree.search(start_value))
                assert start is not None and start.value == start_value
                found_node = finger_search_LCA_version(start, end_value + 0.5)
                assert found_node is not None
                assert isinstance(found_node, Deactivate_Pred_Succ_Node)
                assert found_node.value == end_value

@test
def test_LCA_version_edge_cases():
    tree = create_tree(100, seed=42)
    node7 = deactivate_pred_succ(tree.search(7))
    assert node7 is not None
    assert node7.value == 7

    # Searching for the same value as node
    found_node = finger_search_LCA_version(node7, 7)
    assert found_node is not None
    assert isinstance(found_node, Deactivate_Pred_Succ_Node)
    assert found_node.value == 7

    # Searching for emmidiatlye smaller node
    found_node = finger_search_LCA_version(node7, 6.5)
    assert found_node is not None
    assert isinstance(found_node, Deactivate_Pred_Succ_Node)
    assert found_node.value == 6

    # Searching for larger than all values
    found_node = finger_search_LCA_version(node7, 200)
    assert found_node is not None
    assert isinstance(found_node, Deactivate_Pred_Succ_Node)
    assert found_node.value == 99

    # Searching for smaller than all values
    found_node = finger_search_LCA_version(node7, -1)
    assert found_node is None

    # Searching for larger node from the largest node
    node99 = deactivate_pred_succ(tree.search(99))
    assert node99 is not None
    assert node99.value == 99
    found_node = finger_search_LCA_version(node99, 100)
    assert found_node is not None
    assert isinstance(found_node, Deactivate_Pred_Succ_Node)
    assert found_node.value == 99

    # Searching from the smallest node
    node0 = deactivate_pred_succ(tree.search(0))
    assert node0 is not None
    assert node0.value == 0
    found_node = finger_search_LCA_version(node0, -1)
    assert found_node is None

@test
def test_LCA_version_pointer_counters():
    tree = create_tree(100, seed=42, do_wrap=True)
    node_values = [7, 9, 13, 17, 19, 35, 56, 98]

    for start in node_values:
        for end in node_values:
            if start == end:
                continue
            # Reset pointer counts
            Pointer_Counting.reset_counts()
            Pointer_Counting.set_do_count(True)

            # Search for the start and end nodes
            start_node = deactivate_pred_succ(tree.search(start))
            assert start_node is not None and start_node.value == start
            end_node = finger_search_LCA_version(start_node, end)
            assert end_node is not None
            assert isinstance(end_node, Deactivate_Pred_Succ_Node)

            # Check the counts
            assert Pointer_Counting.get_pointer_count() != 0
            assert Pointer_Counting.set_pointer_count() == 0
            assert Pointer_Counting.get_bit_count() == 0
            assert Pointer_Counting.set_bit_count() == 0
            assert Pointer_Counting.total_count_pointers() == Pointer_Counting.get_pointer_count()
            assert Pointer_Counting.get_compare_count() != 0

@test_group
def test_LCA_version():
    test_LCA_version_exact_search_larger()
    test_LCA_version_pred_search_larger()
    test_LCA_version_exact_search_smaller()
    test_LCA_version_pred_search_smaller()

    test_LCA_version_exact_search()
    test_LCA_version_pred_search()
    test_LCA_version_edge_cases()

    test_LCA_version_pointer_counters()


# ---------------------------------------------
#             Test paper version
# ---------------------------------------------

@test
def test_paper_version_exact_search_larger():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                for h in [1, 2, 4, 8, 16]:
                    start = tree.search(start_value)
                    assert start is not None and start.value == start_value
                    found_node = _finger_search_paper_version_search_larger(start, end_value, h)
                    assert found_node is not None
                    assert found_node.value == end_value or found_node.right is None

@test
def test_paper_version_pred_search_larger():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                for h in [1, 2, 4, 8, 16]:
                    start = tree.search(start_value)
                    assert start is not None and start.value == start_value
                    found_node = _finger_search_paper_version_search_larger(start, end_value + 0.5, h)
                    assert found_node is not None
                    assert found_node.value == end_value or found_node.right is None

@test
def test_paper_version_exact_search_smaller():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                for h in [1, 2, 4, 8, 16]:
                    start = tree.search(start_value)
                    assert start is not None and start.value == start_value
                    found_node = _finger_search_paper_version_search_smaller(start, end_value, h)
                    assert found_node is not None
                    assert found_node.value == end_value or found_node.left is None

@test
def test_paper_version_pred_search_smaller():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                for h in [1, 2, 4, 8, 16]:
                    start = tree.search(start_value)
                    assert start is not None and start.value == start_value
                    found_node = _finger_search_paper_version_search_smaller(start, end_value + 0.5, h)
                    assert found_node is not None
                    assert found_node.value == end_value or found_node.left is None

@test
def test_paper_version_exact_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_paper_version(start, end_value)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_paper_version_excact_search_from_value_to_itself():
    tree = create_tree(n=20, seed=1)
    start_node = tree.search(17)
    found_node = finger_search_paper_version(start_node, 17)
    assert found_node.value == 17

@test
def test_paper_version_pred_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_paper_version(start, end_value + 0.5)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_paper_version_edge_cases():
    tree = create_tree(100, seed=42)
    node7 = tree.search(7)

    # Searching for the same value as node
    found_node = finger_search_paper_version(node7, 7)
    assert found_node is not None
    assert found_node.value == 7

    # Searching for emmidiatlye smaller node
    found_node = finger_search_paper_version(node7, 6.5)
    assert found_node is not None
    assert found_node.value == 6

    # Searching for larger than all values
    found_node = finger_search_paper_version(node7, 200)
    assert found_node is not None
    assert found_node.value == 99

    # Searching for smaller than all values
    found_node = finger_search_paper_version(node7, -1)
    assert found_node is None

    # Searching for largest node from the largest node
    node99 = tree.search(99)
    found_node = finger_search_paper_version(node99, 99)
    assert found_node is not None
    assert found_node.value == 99

    # Searching for larger node from the largest node
    node99 = tree.search(99)
    found_node = finger_search_paper_version(node99, 100)
    assert found_node is not None
    assert found_node.value == 99

    # Searching from the smallest node
    node0 = tree.search(0)
    found_node = finger_search_paper_version(node0, -1)
    assert found_node is None

@test
def test_paper_version_pointer_counters():
    tree = create_tree(100, seed=42, do_wrap=True)
    node_values = [7, 9, 13, 17, 19, 35, 56, 98]

    for start in node_values:
        for end in node_values:
            if start == end:
                continue
            # Reset pointer counts
            Pointer_Counting.reset_counts()
            Pointer_Counting.set_do_count(True)

            # Search for the start and end nodes
            start_node = tree.search(start)
            assert start_node is not None and start_node.value == start
            end_node = finger_search_paper_version(start_node, end)
            assert end_node is not None

            # Check the counts
            assert Pointer_Counting.get_pointer_count() != 0
            assert Pointer_Counting.set_pointer_count() == 0
            assert Pointer_Counting.get_bit_count() == 0
            assert Pointer_Counting.set_bit_count() == 0
            assert Pointer_Counting.total_count_pointers() == Pointer_Counting.get_pointer_count()
            assert Pointer_Counting.get_compare_count() != 0

@test_group
def test_paper_version():
    test_paper_version_exact_search_larger()
    test_paper_version_pred_search_larger()
    test_paper_version_exact_search_smaller()
    test_paper_version_pred_search_smaller()

    test_paper_version_exact_search()
    test_paper_version_excact_search_from_value_to_itself()
    test_paper_version_pred_search()
    test_paper_version_edge_cases()

    test_paper_version_pointer_counters()


# ---------------------------------------------
#         Test paper version Optimized
# ---------------------------------------------

@test
def test_paper_version_optimized_exact_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_paper_version(start, end_value, optimized=True)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_paper_version_optimized_pred_search():
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_paper_version(start, end_value + 0.5, optimized=True)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_paper_version_optimized_edge_cases():
    tree = create_tree(100, seed=42)
    node7 = tree.search(7)

    # Searching for the same value as node
    found_node = finger_search_paper_version(node7, 7, optimized=True)
    assert found_node is not None
    assert found_node.value == 7

    # Searching for emmidiatlye smaller node
    found_node = finger_search_paper_version(node7, 6.5, optimized=True)
    assert found_node is not None
    assert found_node.value == 6

    # Searching for larger than all values
    found_node = finger_search_paper_version(node7, 200, optimized=True)
    assert found_node is not None
    assert found_node.value == 99

    # Searching for smaller than all values
    found_node = finger_search_paper_version(node7, -1, optimized=True)
    assert found_node is None

    # Searching for larger node from the largest node
    node99 = tree.search(99)
    found_node = finger_search_paper_version(node99, 100, optimized=True)
    assert found_node is not None
    assert found_node.value == 99

    # Searching from the smallest node
    node0 = tree.search(0)
    found_node = finger_search_paper_version(node0, -1, optimized=True)
    assert found_node is None

@test
def test_paper_version_optimized_pointer_counters():
    tree = create_tree(100, seed=42, do_wrap=True)
    node_values = [7, 9, 13, 17, 19, 35, 56, 98]

    for start in node_values:
        for end in node_values:
            if start == end:
                continue
            # Reset pointer counts
            Pointer_Counting.reset_counts()
            Pointer_Counting.set_do_count(True)

            # Search for the start and end nodes
            start_node = tree.search(start)
            assert start_node is not None and start_node.value == start
            end_node = finger_search_paper_version(start_node, end, optimized=True)
            assert end_node is not None

            # Check the counts
            assert Pointer_Counting.get_pointer_count() != 0
            assert Pointer_Counting.set_pointer_count() == 0
            assert Pointer_Counting.get_bit_count() == 0
            assert Pointer_Counting.set_bit_count() == 0
            assert Pointer_Counting.total_count_pointers() == Pointer_Counting.get_pointer_count()
            assert Pointer_Counting.get_compare_count() != 0

@test_group
def test_paper_version_optimized():
    test_paper_version_optimized_exact_search()
    test_paper_version_optimized_pred_search()
    test_paper_version_optimized_edge_cases()

    test_paper_version_optimized_pointer_counters()


# ---------------------------------------------
#           Test whiteboard version
# ---------------------------------------------

@test
def test_whiteboard_version_exact_search_larger(optimized=False):
    func = _finger_search_whiteboard_version_search_larger
    if optimized:
        func = _finger_search_whiteboard_version_search_larger_optimized

    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = func(start, end_value)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_whiteboard_version_pred_search_larger(optimized=False):
    func = _finger_search_whiteboard_version_search_larger
    if optimized:
        func = _finger_search_whiteboard_version_search_larger_optimized

    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value + 1, 100):
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = func(start, end_value + 0.5)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_whiteboard_version_exact_search_smaller(optimized=False):
    func = _finger_search_whiteboard_version_search_smaller
    if optimized:
        func = _finger_search_whiteboard_version_search_smaller_optimized

    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = func(start, end_value)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_whiteboard_version_pred_search_smaller(optimized=False):
    func = _finger_search_whiteboard_version_search_smaller
    if optimized:
        func = _finger_search_whiteboard_version_search_smaller_optimized

    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(start_value):
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = func(start, end_value + 0.5)
                assert found_node is not None
                assert found_node.value == end_value, (start, found_node, end_value)

@test
def test_whiteboard_version_exact_search(optimized=False):
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_whiteboard_version(start, end_value, optimized=optimized)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_whiteboard_version_pred_search(optimized=False):
    for seed in [42, 39, 100, 43]:
        tree = create_tree(100, seed)
        for start_value in range(100):
            for end_value in range(100):
                if start_value == end_value:
                    continue
                start = tree.search(start_value)
                assert start is not None and start.value == start_value
                found_node = finger_search_whiteboard_version(start, end_value + 0.5, optimized=optimized)
                assert found_node is not None
                assert found_node.value == end_value

@test
def test_whiteboard_version_edge_cases(optimized=False):
    tree = create_tree(100, seed=42)
    node7 = tree.search(7)

    # Searching for the same value as node
    found_node = finger_search_whiteboard_version(node7, 7, optimized=optimized)
    assert found_node is not None
    assert found_node.value == 7

    # Searching for emmidiatlye smaller node
    found_node = finger_search_whiteboard_version(node7, 6.5, optimized=optimized)
    assert found_node is not None
    assert found_node.value == 6

    # Searching for larger than all values
    found_node = finger_search_whiteboard_version(node7, 200, optimized=optimized)
    assert found_node is not None
    assert found_node.value == 99

    # Searching for smaller than all values
    found_node = finger_search_whiteboard_version(node7, -1, optimized=optimized)
    assert found_node is None, (found_node, node7)

    # Searching for larger node from the largest node
    node99 = tree.search(99)
    found_node = finger_search_whiteboard_version(node99, 100, optimized=optimized)
    assert found_node is not None
    assert found_node.value == 99

    # Searching from the smallest node
    node0 = tree.search(0)
    found_node = finger_search_whiteboard_version(node0, -1, optimized=optimized)
    assert found_node is None

@test
def test_whiteboard_version_pointer_counters(optimized=False):
    tree = create_tree(100, seed=42, do_wrap=True)
    node_values = [7, 9, 13, 17, 19, 35, 56, 98]

    for start in node_values:
        for end in node_values:
            if start == end:
                continue
            # Reset pointer counts
            Pointer_Counting.reset_counts()
            Pointer_Counting.set_do_count(True)

            # Search for the start and end nodes
            start_node = tree.search(start)
            assert start_node is not None and start_node.value == start
            end_node = finger_search_whiteboard_version(start_node, end, optimized=optimized)
            assert end_node is not None

            # Check the counts
            assert Pointer_Counting.get_pointer_count() != 0
            assert Pointer_Counting.set_pointer_count() == 0
            assert Pointer_Counting.get_bit_count() == 0
            assert Pointer_Counting.set_bit_count() == 0
            assert Pointer_Counting.total_count_pointers() == Pointer_Counting.get_pointer_count()
            assert Pointer_Counting.get_compare_count() != 0


@test_group
def test_whiteboard_version():
    test_whiteboard_version_exact_search_larger()
    test_whiteboard_version_pred_search_larger()
    test_whiteboard_version_exact_search_smaller()
    test_whiteboard_version_pred_search_smaller()

    test_whiteboard_version_exact_search()
    test_whiteboard_version_pred_search()
    test_whiteboard_version_edge_cases()
    test_whiteboard_version_pointer_counters()


@test_group
def test_whiteboard_optimized_version():
    test_whiteboard_version_exact_search_larger(optimized=True)
    test_whiteboard_version_pred_search_larger(optimized=True)
    test_whiteboard_version_exact_search_smaller(optimized=True)
    test_whiteboard_version_pred_search_smaller(optimized=True)

    test_whiteboard_version_exact_search(optimized=True)
    test_whiteboard_version_pred_search(optimized=True)
    test_whiteboard_version_edge_cases(optimized=True)
    test_whiteboard_version_pointer_counters(optimized=True)


# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_helpers()
    test_LCA_version()
    test_paper_version()
    test_paper_version_optimized()
    test_whiteboard_version()
    test_whiteboard_optimized_version()

if __name__ == "__main__":
    test_all()
