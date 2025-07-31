from __test_decorators import test, test_group, test_file

from Many_Pointers_Red_Black_Tree import Red_Black_Tree, Red_Black_Node
from Mock_FT_Folded_Tree import Mock_Folded_Tree
from Finger_Search import Version
from util import link_left, link_right

import random



# ---------------------------------------------
#                 Generators
# ---------------------------------------------

def get_folded_tree_from_paper():
    x_11 = Red_Black_Node("x_11", is_red=False)
    x_10 = Red_Black_Node("x_10", is_red=False)
    x_9 = Red_Black_Node("x_9", is_red=True)
    x_8 = Red_Black_Node("x_8", is_red=False)
    x_7 = Red_Black_Node("x_7", is_red=True)
    x_6 = Red_Black_Node("x_6", is_red=False)
    x_5 = Red_Black_Node("x_5", is_red=False)
    x_4 = Red_Black_Node("x_4", is_red=True)
    x_3 = Red_Black_Node("x_3", is_red=False)
    x_2 = Red_Black_Node("x_2", is_red=False)
    x_1 = Red_Black_Node("x_1", is_red=True)

    T_11 = Red_Black_Node("T_11", is_red=False)
    T_10 = Red_Black_Node("T_10", is_red=False)
    T_9 = Red_Black_Node("T_9", is_red=False)
    T_8 = Red_Black_Node("T_8", is_red=False)
    T_7 = Red_Black_Node("T_7", is_red=False)
    T_6 = Red_Black_Node("T_6", is_red=False)
    T_5 = Red_Black_Node("T_5", is_red=False)
    T_4 = Red_Black_Node("T_4", is_red=False)
    T_3 = Red_Black_Node("T_3", is_red=False)
    T_2 = Red_Black_Node("T_2", is_red=False)
    T_1 = Red_Black_Node("T_1", is_red=False)

    link_left(x_11, x_10)
    link_left(x_10, x_9)
    link_left(x_9, x_8)
    link_left(x_8, x_7)
    link_left(x_7, x_6)
    link_left(x_6, x_5)
    link_left(x_5, x_4)
    link_left(x_4, x_3)
    link_left(x_3, x_2)
    link_left(x_2, x_1)

    link_right(x_11, T_11)
    link_right(x_10, T_10)
    link_right(x_9, T_9)
    link_right(x_8, T_8)
    link_right(x_7, T_7)
    link_right(x_6, T_6)
    link_right(x_5, T_5)
    link_right(x_4, T_4)
    link_right(x_3, T_3)
    link_right(x_2, T_2)
    link_right(x_1, T_1)

    tree = Red_Black_Tree()
    tree._root = x_11

    folded_tree = Mock_Folded_Tree.create_folded_tree(tree)

    return folded_tree


def get_node_map(tree):
    node_map = {}
    for node in tree:
        node_map[node.value] = node
    return node_map


def random_folded_tree(n, seed=None, include_unfolded=False):
    if seed is not None:
        random.seed(seed)
    
    values = list(range(n))
    random.shuffle(values)

    tree = Red_Black_Tree()
    for value in values:
        tree.insert(value)
    
    folded_tree = Mock_Folded_Tree.create_folded_tree(tree)

    if include_unfolded:
        return tree, folded_tree

    return folded_tree



# ---------------------------------------------
#             Test upper and lower
# ---------------------------------------------

@test_group
def test_upper_lower():
    node_map = get_node_map(get_folded_tree_from_paper())

    for key in ["x_11", "x_10", "x_9", "x_8"]:
        assert node_map[key].is_upper
    
    for key in ["x_1", "x_2", "x_3", "x_4", "x_5", "x_6", "x_7"]:
        assert node_map[key].is_lower


# ---------------------------------------------
#        Test unfolded parent, left, right
# ---------------------------------------------

@test
def test_unfolded_parent_left_right_paper_tree():
    node_map = get_node_map(get_folded_tree_from_paper())

    left_path = [f"x_{i}" for i in range(1, 11 + 1)[::-1]]

    for parent_key, child_key in zip(left_path, left_path[1:]):
        parent = node_map[parent_key]
        child = node_map[child_key]

        assert parent.unfolded_left == child
        assert child.unfolded_parent == parent
    
    right_subtree_roots = [f"T_{i}" for i in range(1, 11 + 1)[::-1]]

    for parent_key, child_key in zip(left_path, right_subtree_roots):
        parent = node_map[parent_key]
        child = node_map[child_key]

        assert parent.unfolded_right == child
        assert child.unfolded_parent == parent

    assert node_map["x_11"].unfolded_parent == None
    assert node_map["x_1"].unfolded_left == None

@test
def test_unfolded_parent_left_right_random_tree_check_links():
    n = 1000
    for seed in range(10):
        folded_tree = random_folded_tree(n=n, seed=seed)

        for folded_node in folded_tree:
            assert folded_node.unfolded_left is None or folded_node.unfolded_left.unfolded_parent == folded_node
            assert folded_node.unfolded_right is None or folded_node.unfolded_right.unfolded_parent == folded_node

@test
def test_unfolded_parent_left_right_random_tree_compare_to_unfolded():
    def assert_is_equal(node_a, node_b):
        assert (node_a is None and node_b is None) or \
            (node_a is not None and node_b is not None and node_a.value == node_b.value)

    n = 1000
    for seed in range(10):
        tree, folded_tree = random_folded_tree(n=n, seed=seed, include_unfolded=True)
        tree_node_map = get_node_map(tree)

        for folded_node in folded_tree:
            unfolded_node = tree_node_map[folded_node.value]
            assert_is_equal(folded_node.unfolded_parent, unfolded_node.parent)
            assert_is_equal(folded_node.unfolded_left, unfolded_node.left)
            assert_is_equal(folded_node.unfolded_right, unfolded_node.right)

@test_group
def test_unfolded_parent_left_right():
    test_unfolded_parent_left_right_paper_tree()
    test_unfolded_parent_left_right_random_tree_check_links()
    test_unfolded_parent_left_right_random_tree_compare_to_unfolded()


# ---------------------------------------------
#        Test predecessor and successor
# ---------------------------------------------

@test
def test_predecessor_and_succesor():
    n = 5000
    for seed in range(10):
        folded_tree = random_folded_tree(n=n, seed=seed)

        for node in folded_tree:
            pred = node.predecessor
            succ = node.successor

            print(pred, node, succ)

            assert (node.value == 0 and pred is None) or node.value - 1 == pred.value
            assert (node.value == n - 1 and succ is None) or node.value + 1 == succ.value


# ---------------------------------------------
#             Test folding function
# ---------------------------------------------

@test
def test_random_trees_are_folding():
    n = 10_000

    for seed in range(10):
        folded_tree = random_folded_tree(n, seed)
        assert folded_tree.is_valid()

@test_group
def test_folding_function():
    test_random_trees_are_folding()


# ---------------------------------------------
#           Test finger searching
# ---------------------------------------------

@test
def test_finger_search_random_trees_for_version(version):
    n = 1000
    for seed in range(10):
        folded_tree = random_folded_tree(n, seed=seed)

        nodes = list(folded_tree)
        random.seed(seed)

        for start_node in random.sample(nodes, 50):
            for end_value in random.sample(range(n), 20):
                end_node = Mock_Folded_Tree.finger_search(start_node, end_value, algorithm=version)
                assert end_node.value == end_value

@test_group
def test_finger_search():
    test_finger_search_random_trees_for_version(Version.LCA)
    test_finger_search_random_trees_for_version(Version.PAPER)
    test_finger_search_random_trees_for_version(Version.WHITEBOARD)

# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_upper_lower()
    test_unfolded_parent_left_right()
    test_predecessor_and_succesor()
    test_folding_function()
    test_finger_search()

if __name__ == '__main__':
    test_all()
