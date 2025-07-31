import random

from ZigZag_RB_tree import ZigZag_RB_tree as Z_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node

from Regular_RB_tree import RB_tree
from convert import convert_regular_to_zigzag, convert_zigzag_to_regular
from tree_equality import regular_and_zigzag_tree_equality


# ---------------------------------------------
#              Test tree creation
# ---------------------------------------------

def get_tree_in_order(n: int) -> Z_tree:
    tree = RB_tree()

    for i in range(1, n+1):
        tree.insert(i)

    return convert_regular_to_zigzag(tree)

def get_random_regular_tree(n: int, seed=None) -> RB_tree:
    tree = RB_tree()
    elements = list(range(1, n + 1))

    if seed is not None:
        random.seed(seed)
    random.shuffle(elements)

    for i in elements:
        tree.insert(i)

    return tree

def get_random_tree(n: int, seed=None) -> Z_tree:
    return convert_regular_to_zigzag(get_random_regular_tree(n, seed=seed))


# ---------------------------------------------
# Adding elements to lower double chunks does not fail getters
# ---------------------------------------------

def test_add_elements_to_lower_double_chunks(verbose=False):
    if not verbose:
        z_tree = get_random_tree(1000, seed=42)
    
    else:
        z_tree = get_random_tree(100, seed=42)
        print("Initial tree")
        z_tree.print()
        print()

    for node in z_tree._inorder_nodes(z_tree._root):
        if node._is_lower:
            if node.is_left_path() and node._right != None and node._right._is_lower:
                # Insert top
                new_node = Z_Node("x")
                new_node.set_red()
                new_node.set_left_path()

                new_node._parent = node._parent
                new_node._left = node._left
                new_node._right = node

                if new_node._parent != None:
                    new_node._parent._left = new_node
                if new_node._left != None:
                    new_node._left._parent = new_node
                new_node._right._parent = new_node
                
                node._left = None

                try:
                    assert z_tree._all_regular_pointers_correct(z_tree._root, verbose=True)
                except AssertionError:
                    print("Failing on node:", node._key)
                    z_tree.print()
                    print()
                    raise

                node._parent = new_node._parent
                if node._parent != None:
                    node._parent._left = node
                node._left = new_node._left
                if node._left != None:
                    node._left._parent = node

                # Insert mid
                new_node = Z_Node("x")
                new_node.set_red()
                new_node.set_left_path()

                new_node._parent = node
                new_node._left = node._right._left
                new_node._right = node._right

                node._right = new_node
                if new_node._left != None:
                    new_node._left._parent = new_node
                new_node._right._parent = new_node

                new_node._right._left = None

                try:
                    assert z_tree._all_regular_pointers_correct(z_tree._root, verbose=True)
                except AssertionError:
                    print("Failing on node:", node._key)
                    z_tree.print()
                    print()
                    raise
                
                node._right = new_node._right
                if node._right != None:
                    node._right._parent = node
                node._right._left = new_node._left
                if node._right._left != None:
                    node._right._left._parent = node._right

            elif node.is_right_path() and node._left != None and node._left._is_lower:
                # Insert top
                new_node = Z_Node("x")
                new_node.set_red()
                new_node.set_right_path()

                new_node._parent = node._parent
                new_node._left = node
                new_node._right = node._right

                if new_node._parent != None:
                    new_node._parent._right = new_node
                new_node._left._parent = new_node
                if new_node._right != None:
                    new_node._right._parent = new_node

                node._right = None

                try:
                    assert z_tree._all_regular_pointers_correct(z_tree._root, verbose=True)
                except AssertionError:
                    print("Failing on node:", node._key)
                    z_tree.print()
                    print()
                    raise

                node._parent = new_node._parent
                if node._parent != None:
                    node._parent._right = node
                node._right = new_node._right
                if node._right != None:
                    node._right._parent = node

                # Insert mid
                new_node = Z_Node("x")
                new_node.set_red()
                new_node.set_right_path()

                new_node._parent = node
                new_node._left = node._left
                new_node._right = node._left._right

                node._left = new_node
                if new_node._right != None:
                    new_node._right._parent = new_node
                new_node._left._parent = new_node

                new_node._left._right = None

                try:
                    assert z_tree._all_regular_pointers_correct(z_tree._root, verbose=True)
                except AssertionError:
                    print("Failing on node:", node._key)
                    z_tree.print()
                    print()
                    raise

                node._left = new_node._left
                if node._left != None:
                    node._left._parent = node
                node._left._right = new_node._right
                if node._left._right != None:
                    node._left._right._parent = node._left


# ---------------------------------------------
#  Inserting elements without fixup leaves get left, right and parent working
# ---------------------------------------------

def test_insert_predecessor_elements_without_fixup_leaves_get_left_right_parent_working(n: int, itr: int=100):
    for seed in range(itr):
        for parent in range(1, n + 1):
            tree = get_random_regular_tree(n, seed=seed)
            z_tree = convert_regular_to_zigzag(tree)
            tree._insert_fixup = lambda x: None
            z_tree._insert_fixup = lambda x: None
            
            tree.insert(parent - 0.5)
            z_tree.insert_predecessor(z_tree.search(parent), parent - 0.5)

            try:
                assert z_tree._all_regular_pointers_correct(z_tree._root, verbose=True)
                assert regular_and_zigzag_tree_equality(tree, z_tree)
            except AssertionError:
                print("Parent:", parent)
                print("Regular tree:")
                tree.print()
                print()
                print("ZigZag tree:")
                z_tree.print()
                print()
                # for s in [14, 0.5, 1, 2]:
                #     x = z_tree.search(s)
                #     print(x._key, "upper", x._is_upper, "mid", x._is_midpoint)
                # print()
                # print("Expected ZigZag tree:")
                # z_tree_expected = convert_regular_to_zigzag(tree)
                # z_tree_expected.print()
                # print()
                raise

def test_insert_successor_elements_without_fixup_leaves_get_left_right_parent_working(n: int, itr: int=100):
    for seed in range(itr):
        for parent in range(1, n + 1):
            tree = get_random_regular_tree(n, seed=seed)
            z_tree = convert_regular_to_zigzag(tree)
            tree._insert_fixup = lambda x: None
            z_tree._insert_fixup = lambda x: None
            
            tree.insert(parent + 0.5)
            z_tree.insert_successor(z_tree.search(parent), parent + 0.5)

            try:
                assert z_tree._all_regular_pointers_correct(z_tree._root)
                assert regular_and_zigzag_tree_equality(tree, z_tree)
            except AssertionError:
                print("Parent:", parent)
                print("Regular tree:")
                tree.print()
                print()
                print("ZigZag tree:")
                z_tree.print()
                print()
                for s in [15, 20.5, 20, 19, 18]:
                    x = z_tree.search(s)
                    print(x._key, "upper", x._is_upper, "mid", x._is_midpoint)
                print()
                # print("Expected ZigZag tree:")
                # z_tree_expected = convert_regular_to_zigzag(tree)
                # z_tree_expected.print()
                print()
                raise


# ---------------------------------------------
#                Insertions
# ---------------------------------------------

def test_insert_no_rotations():
    tree = get_random_regular_tree(60, seed=42)
    # tree = get_random_regular_tree(200, seed=42)
    z_tree = convert_regular_to_zigzag(tree)

    print("Regular tree:")
    tree.print()
    print()
    print("ZigZag tree:")
    z_tree.print()
    print()

    tree._insert_fixup = tree._insert_fixup_no_rotate
    z_tree._insert_fixup = z_tree._insert_fixup_no_rotate

    tree.insert(0)
    z_tree.insert(0)

    print("Regular tree after insertion:")
    tree.print()
    print()
    print("ZigZag tree after insertion:")
    z_tree.print()
    print()

    print("ZigZag converted sees")
    convert_zigzag_to_regular(z_tree).print()
    print()

    assert regular_and_zigzag_tree_equality(tree, z_tree)


# ---------------------------------------------
#                    Main
# ---------------------------------------------

def test_all():
    # test_add_elements_to_lower_double_chunks(verbose=False)

    # for n, itr in [(20, 100), (100, 10)]:
    #     test_insert_predecessor_elements_without_fixup_leaves_get_left_right_parent_working(n, itr=itr)
    #     test_insert_successor_elements_without_fixup_leaves_get_left_right_parent_working(n, itr=itr)

    test_insert_no_rotations()

if __name__ == "__main__":
    test_all()

    print("All tests passed!")