from test_decorators import test, test_group, test_file

from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_RB_tree

from test_tree_creation import *
from convert import convert_regular_to_zigzag, convert_zigzag_to_regular
from util import print_ascii_tree_side, link_left, link_right
from tree_equality import zigzag_tree_equality, regular_tree_equality
import random


# ---------------------------------------------
#              Helper functions
# ---------------------------------------------

def traverse_down_left_path_from(node: Z_Node):
    yield node

    node = node._left

    while node != None and not node._is_path_root():
        yield node

        if node._right == None or node._right._is_path_root():
            node = node._left
        else:
            node = node._right

def delete_fixup_only_color(z_tree: Z_RB_tree) -> None:
    z_tree._delete_fixup = lambda x, y: x._set_black()


# ---------------------------------------------
#             Test validity checks
# ---------------------------------------------

def black():
    return Z_Node(None, is_red=False, is_path_root=False)

def red():
    return Z_Node(None, is_red=True, is_path_root=False)

def black_root():
    return Z_Node(None, is_red=False, is_path_root=True)

def red_root():
    return Z_Node(None, is_red=True, is_path_root=True)

def rooted_valid():
    return black_root()

def rooted_invalid():
    a = black_root()
    b = red()
    c = black()
    d = black()
    link_left(a, b)
    link_right(b, c)
    link_left(c, d)
    return a

@test
def test_zigzag_empty_tree():
    assert Z_RB_tree()._correct_left_path_zigzag_from(None)

@test
def test_zigzag_single_node_root():
    a = black_root()
    assert Z_RB_tree()._correct_left_path_zigzag_from(a)

    b = red_root()
    assert Z_RB_tree()._correct_left_path_zigzag_from(b)

@test
def test_zigzag_single_node_inner():
    a = black()
    assert not Z_RB_tree()._correct_left_path_zigzag_from(a)

    b = red()
    assert not Z_RB_tree()._correct_left_path_zigzag_from(b)

@test
def test_zigzag_single_node_with_right_valid():
    a = black_root()
    b = black_root()
    link_right(a, b)
    assert Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_single_node_with_right_invalid():
    a = black_root()
    b = black()
    link_right(a, b)
    assert not Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_lower_chunk_valid():
    #      a
    #     /
    #  chunk
    #     \
    #      c
    #     /
    #    d

    for chunk in [(black(),), (red(), black())]:
        a = black_root()
        c = black()
        d = red()
        link_left(a, chunk[0])
        for i, j in zip(chunk, chunk[1:] + (c,)):
            link_right(i, j)
        link_left(c, d)
        assert Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_lower_chunk_invalid():
    #      a
    #     /
    #  chunk
    #     \
    #      c
    #     /
    #    d

    for chunk in [(red(),), (black(), black()), (red(), red(), black()), (red(), black(), red()), (red(), black(), black())]:
        a = black_root()
        c = black()
        d = red()
        link_left(a, chunk[0])
        for i, j in zip(chunk, chunk[1:] + (c,)):
            link_right(i, j)
        link_left(c, d)
        assert not Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_last_chunk_valid():
    #         a
    #        /
    #       b
    #        \
    #         c
    #        /
    #  last chunk

    for last_chunk in [
        (red(),), (black(),),
        (red(), black()), (black(), red()), (red(), red()), (black(), black()),
        (red(), red(), black()), (red(), black(), red()), (red(), red(), red()), (red(), black(), black())
    ]:
        a = black_root()
        b = black()
        c = black()
        link_left(a, b)
        link_right(b, c)
        link_left(c, last_chunk[0])
        for i, j in zip(last_chunk, last_chunk[1:]):
            link_right(i, j)
        assert Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_last_chunk_invalid():
    #         a
    #        /
    #       b
    #        \
    #         c
    #        /
    #  last chunk

    for last_chunk in [
        (black(), red(), black()), (black(), black(), red()), (black(), red(), red()), (black(), black(), black()),
        (red(), black(), red(), black()), (red(), black(), black(), black()), (black(), red(), black(), black()),
        (black(), red(), black(), black(), black()),
    ]:
        a = black_root()
        b = black()
        c = black()
        link_left(a, b)
        link_right(b, c)
        link_left(c, last_chunk[0])
        for i, j in zip(last_chunk, last_chunk[1:]):
            link_right(i, j)
        assert not Z_RB_tree()._correct_left_path_zigzag_from(a)

@test
def test_zigzag_rooted_predicates():
    assert Z_RB_tree()._correct_left_path_zigzag_from(rooted_valid())
    assert not Z_RB_tree()._correct_left_path_zigzag_from(rooted_invalid())

@test
def test_zigzag_subtree_checks_valid():
    #     a
    #    /
    #   b
    #    \
    #     c
    #      \
    #       d
    #      /
    #     e
    #      \
    #       f

    a = black_root()
    b = red()
    c = black()
    d = red()
    e = black()
    f = black()
    link_left(a, b)
    link_right(b, c)
    link_right(c, d)
    link_left(d, e)
    link_right(e, f)
    assert Z_RB_tree()._correct_left_path_zigzag_from(a)

    t = rooted_valid()
    
    for on_left, on_node in [(False, a), (True, b), (True, c), (False, d), (True, e), (True, f), (False, f)]:
        link = link_left if on_left else link_right
        link(on_node, t)
        assert Z_RB_tree()._correct_left_path_zigzag_from(a)
        link(on_node, None)

@test
def test_zigzag_subtree_checks_invalid():
    #     a
    #    /
    #   b
    #    \
    #     c
    #      \
    #       d
    #      /
    #     e
    #      \
    #       f

    a = black_root()
    b = red()
    c = black()
    d = red()
    e = black()
    f = black()
    link_left(a, b)
    link_right(b, c)
    link_right(c, d)
    link_left(d, e)
    link_right(e, f)
    assert Z_RB_tree()._correct_left_path_zigzag_from(a)

    t = rooted_invalid()
    
    for on_left, on_node in [(False, a), (True, b), (True, c), (False, d), (True, e), (True, f), (False, f)]:
        link = link_left if on_left else link_right
        link(on_node, t)
        assert not Z_RB_tree()._correct_left_path_zigzag_from(a)
        link(on_node, None)

@test
def test_zigzag_unrooted_subtree_checks_invalid():
    #     a
    #    /
    #   b
    #    \
    #     c
    #      \
    #       d
    #      /
    #     e
    #      \
    #       f

    a = black_root()
    b = red()
    c = black()
    d = red()
    e = black()
    f = black()
    link_left(a, b)
    link_right(b, c)
    link_right(c, d)
    link_left(d, e)
    link_right(e, f)
    assert Z_RB_tree()._correct_left_path_zigzag_from(a)

    t = black()
    
    for on_left, on_node in [(False, a), (True, b), (True, c), (False, d), (True, e)]:
        link = link_left if on_left else link_right
        link(on_node, t)
        assert not Z_RB_tree()._correct_left_path_zigzag_from(a)
        link(on_node, None)

@test
def test_zigzag_regular_path_invalid():
    a = black_root()
    b = red()
    c = black()
    link_left(a, b)
    link_left(b, c)
    assert not Z_RB_tree()._correct_left_path_zigzag_from(a)

@test_group
def test_validity_checks():
    test_zigzag_empty_tree()
    test_zigzag_single_node_root()
    test_zigzag_single_node_inner()
    test_zigzag_single_node_with_right_valid()
    test_zigzag_single_node_with_right_invalid()
    test_zigzag_lower_chunk_valid()
    test_zigzag_lower_chunk_invalid()
    test_zigzag_last_chunk_valid()
    test_zigzag_last_chunk_invalid()
    test_zigzag_rooted_predicates()
    test_zigzag_subtree_checks_valid()
    test_zigzag_subtree_checks_invalid()
    test_zigzag_unrooted_subtree_checks_invalid()
    test_zigzag_regular_path_invalid()


# ---------------------------------------------
#              Test node primitives
# ---------------------------------------------

@test
def test_specific_left_path_is_lower_upper_midpoint(verbose=False):
    z_tree = convert_regular_to_zigzag(get_left_path_tree())

    if verbose:
        z_tree.print()
        print()

    # Get the left path
    left_path = list(traverse_down_left_path_from(z_tree._root))

    # Expected values
    is_lower = [False, True, True, False, True, False, True, True, False, True, True]
    is_upper = [True, False, False, True, False, True, False, False, True, False, False]
    is_midpoint = [False, False, False, False, False, False, False, False, True, False, False]

    # Test
    for node, l, u, m in zip(left_path, is_lower, is_upper, is_midpoint):
        if verbose:
            print("Node:", node._key, "is_lower:", node._is_lower, "is_upper:", node._is_upper, "is_midpoint:", node._is_midpoint)

        assert node._is_lower == l
        assert node._is_upper == u
        assert node._is_midpoint == m

@test
def test_specific_left_path_left_right_child(verbose=False):
    z_tree = convert_regular_to_zigzag(get_left_path_tree())

    if verbose:
        z_tree.print()
        print()
    
    # Get the left path
    left_path = list(traverse_down_left_path_from(z_tree._root))

    for node in left_path:
        node_number = int(node._key.replace("x_", ""))
        
        left = node._get_left_of
        if node_number == 1:
            assert left == None
        else:
            assert left._key == f"x_{node_number - 1}"
        
        right = node._get_right_of
        assert right._key == f"T_{node_number}"

@test
def test_specific_left_path_parent(verbose=False):
    z_tree = convert_regular_to_zigzag(get_left_path_tree())

    if verbose:
        z_tree.print()
        print()
    
    # Get the left path
    left_path = list(traverse_down_left_path_from(z_tree._root))

    for node in left_path:
        node_number = int(node._key.replace("x_", ""))
        
        parent = node._get_parent_of
        if node_number == 11:
            assert parent == None
        else:
            assert parent._key == f"x_{node_number + 1}"

        subtree = node._get_right_of
        if subtree != None:
            assert subtree._get_parent_of == node

@test
def test_regular_parent_of_children_is_self_random(n, itr=100):
    for seed in range(itr):
        z_tree = convert_regular_to_zigzag(get_random_tree_from_insertions(n, seed))
        assert z_tree._all_regular_pointers_correct()

@test_group
def test_node_primitives():
    test_specific_left_path_is_lower_upper_midpoint()
    test_specific_left_path_left_right_child()
    test_specific_left_path_parent()

    test_regular_parent_of_children_is_self_random(20, itr=1000)
    test_regular_parent_of_children_is_self_random(100, itr=100)
    test_regular_parent_of_children_is_self_random(1000, itr=20)


# ---------------------------------------------
#              Test path operations
# ---------------------------------------------

@test
def test_pop_root_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)
    old_root = z_tree._root

    if verbose:
        print("Path before popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    root, new_root = z_tree._pop_path_root(z_tree._root)
    z_tree._root = new_root
    
    if verbose:
        print("Popped:", root._key)
        print("Path after popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    # The new node may not have any pointers, but must be the same node
    assert root == old_root
    assert root._parent == None
    assert root._left == None
    assert root._right == None

    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # The new root must form a tree, equal to the regular tree spanning from the left of the old root
    tree._root = tree._root._left
    tree._root._parent = None
    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_push_root_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Path before pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    new_root = Z_Node("x_12", is_red=False)
    new_right_subtree = Z_Node("T_12", is_red=False, is_path_root=True)
    z_tree._push_path_root(z_tree._root, new_root, new_right_subtree)
    z_tree._root = new_root
    
    if verbose:
        print("Path after pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # Mimic the operation in the regular tree
    r_new_root = Node("x_12", is_red=False)
    r_new_right_subtree = Node("T_12", is_red=False)
    r_new_root._right = r_new_right_subtree
    r_new_right_subtree._parent = r_new_root
    tree._root._parent = r_new_root
    r_new_root._left = tree._root
    tree._root = r_new_root

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_pop_upper_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    x10 = z_tree._root._left._right._right
    assert x10._key == "x_10"

    if verbose:
        print("Before popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    x10_parent = x10._to_parent
    x10_free, new_node = z_tree._pop_upper_node(x10)
    z_tree._set_child(x10_parent, new_node)
    
    if verbose:
        print("Popped:", x10_free._key)
        print("After popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    # The new node may not have any pointers, but must be the same node
    assert x10_free == x10
    assert x10_free._parent == None
    assert x10_free._left == None
    assert x10_free._right == None

    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # The new path must form a tree, equal to the regular tree missing x_10
    tree._root._left = tree._root._left._left
    tree._root._left._parent = tree._root
    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_push_upper_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Before pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    x10 = z_tree._root._left._right._right
    assert x10._key == "x_10"

    new_node = Z_Node("x_", is_red=False, is_path_root=False)
    new_right_subtree = Z_Node("T_", is_red=False, is_path_root=True)

    x10_parent = x10._to_parent
    z_tree._push_upper_node(x10, new_node, new_right_subtree)
    z_tree._set_child(x10_parent, new_node)
    
    if verbose:
        print("After pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # Mimic the operation in the regular tree
    r_new_node = Node("x_", is_red=False)
    r_new_right_subtree = Node("T_", is_red=False)
    r_new_node._right = r_new_right_subtree
    r_new_right_subtree._parent = r_new_node
    r_x11 = tree._root
    assert r_x11._key == "x_11"
    r_x10 = tree._root._left
    assert r_x10._key == "x_10"
    r_x11._left = r_new_node
    r_new_node._parent = r_x11
    r_x10._parent = r_new_node
    r_new_node._left = r_x10

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_pop_lower_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    x4 = z_tree._root._left._right._right._left._right._left
    assert x4._key == "x_4"

    if verbose:
        print("Before popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    x4_parent = x4._to_parent
    x4_free, new_node = z_tree._pop_lower_node(x4)
    z_tree._set_child(x4_parent, new_node)
    
    if verbose:
        print("Popped:", x4_free._key)
        print("After popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    # The new node may not have any pointers, but must be the same node
    assert x4_free == x4
    assert x4_free._parent == None
    assert x4_free._left == None
    assert x4_free._right == None

    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # The new tree must form a tree, equal to the regular tree missing x_4
    r_x4 = tree._root._left._left._left._left._left._left._left
    assert r_x4._key == "x_4"
    r_x4._parent._left = r_x4._left
    r_x4._left._parent = r_x4._parent
    
    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_push_lower_specific(verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Before pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    x2 = z_tree._root._left._right
    assert x2._key == "x_2"

    new_node = Z_Node("x_", is_red=True, is_path_root=False)
    new_right_subtree = Z_Node("T_", is_red=False, is_path_root=True)

    z_tree._push_lower_node(x2, new_node, new_right_subtree)
    
    if verbose:
        print("After pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # Mimic the operation in the regular tree
    r_new_node = Node("x_", is_red=True)
    r_new_right_subtree = Node("T_", is_red=False)
    r_new_node._right = r_new_right_subtree
    r_new_right_subtree._parent = r_new_node
    r_x3 = tree._root._left._left._left._left._left._left._left._left
    assert r_x3._key == "x_3"
    r_x2 = tree._root._left._left._left._left._left._left._left._left._left
    assert r_x2._key == "x_2"
    r_x3._left = r_new_node
    r_new_node._parent = r_x3
    r_x2._parent = r_new_node
    r_new_node._left = r_x2

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_pop_node_specific(node_key, set_red=False, verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    node = z_tree._root
    while node._key != node_key:
        if node._left != None and not node._left._is_path_root():
            node = node._left
        else:
            node = node._right

    assert node != None
    assert node._key == node_key

    if set_red:
        node._set_red()

    if verbose:
        print("Before popping:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    node_free = z_tree._pop_node(node)
    
    if verbose:
        print("Popped:", node_free._key)
        print("New path:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # The new path must form a tree, equal to the regular tree missing the popped key
    r_node = tree._root
    while r_node._key != node_key:
        r_node = r_node._left
    
    assert r_node != None

    under = r_node._left
    over = r_node._parent
    if under != None:
        under._parent = over
    if over != None:
        over._left = under
    
    if r_node == tree._root:
        tree._root = under

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_push_node_specific(node_key, verbose=False):
    tree = get_left_path_tree()
    z_tree = convert_regular_to_zigzag(tree)

    node = z_tree._root
    while node._key != node_key:
        if node._left != None and not node._left._is_path_root():
            node = node._left
        else:
            node = node._right

    assert node != None
    assert node._key == node_key

    if verbose:
        print("Before pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    new_node = Z_Node("x_", is_red=True, is_path_root=False)
    new_right_subtree = Z_Node("T_", is_red=False, is_path_root=True)
    z_tree._push_node(node, new_node, new_right_subtree)
    
    if verbose:
        print("After pushing:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    # The new path must form a tree, equal to the regular tree with the extra key inserted
    r_node = tree._root
    while r_node._key != node_key:
        r_node = r_node._left
    
    assert r_node != None

    over = r_node._parent
    r_new_node = Node("x_", is_red=True)
    r_new_right_subtree = Node("T_", is_red=False)
    r_new_node._right = r_new_right_subtree
    r_new_right_subtree._parent = r_new_node
    r_new_node._parent = over
    r_new_node._left = r_node
    r_node._parent = r_new_node
    if over != None:
        over._left = r_new_node

    if r_node == tree._root:
        tree._root = r_new_node

    try:
        # Inserting a new red node on a lower path may create an illigal zigzag tree,
        # therefore the regular tree cannot be converted to zigzag.
        # The zigzag tree is therefore converted to regular and compared to the original tree.
        assert regular_tree_equality(convert_zigzag_to_regular(z_tree), tree)
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_rotate_left_larger_tree(verbose=False):
    colors = [True, False, True, True, False, False, True, False, True, False, False, True, False, False, True, True, False, True, True, False, False, False, True, False, True]
    nodes = [None] + [Node(key, is_red=is_red) for key, is_red in zip(range(1, 25 + 1), colors)]
    links = [
        (10, 6, 15),
        (6, 3, 8),
        (3, 2, 5),
        (2, 1, None),
        (5, 4, None),
        (8, 7, 9),
        (15, 13, 19),
        (13, 11, 14),
        (11, None, 12),
        (19, 17, 21),
        (17, 16, 18),
        (21, 20, 23),
        (23, 22, 24),
        (24, None, 25),
    ]

    for parent, left, right in links:
        if left != None:
            nodes[parent]._left = nodes[left]
            nodes[left]._parent = nodes[parent]
        if right != None:
            nodes[parent]._right = nodes[right]
            nodes[right]._parent = nodes[parent]
    
    tree = RB_tree()
    tree._root = nodes[10]

    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Initial tree:")
        print_ascii_tree_side(tree, z_tree)
    
    tree._left_rotate(tree.search(19))
    z_tree._real_left_rotate(z_tree.search(19))

    if verbose:
        print("After rotation:")
        print_ascii_tree_side(tree, z_tree)
        print()

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_rotate_left_specific(node_key, verbose=False):
    tree = get_random_tree_from_insertions(20, seed=42)
    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Rotating left around", node_key)
        print("Before rotation:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    z_node = z_tree.search(node_key)
    assert z_node != None
    z_tree._real_left_rotate(z_node)

    if verbose:
        print("After rotation:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()
    
    r_node = tree.search(node_key)
    assert r_node != None
    tree._left_rotate(r_node)

    try:
        # Inserting a new red node on a lower path may create an illigal zigzag tree,
        # therefore the regular tree cannot be converted to zigzag.
        # The zigzag tree is therefore converted to regular and compared to the original tree.
        assert regular_tree_equality(convert_zigzag_to_regular(z_tree), tree)
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test
def test_rotate_right_specific(node_key, verbose=False):
    tree = get_random_tree_from_insertions(20, seed=42)
    z_tree = convert_regular_to_zigzag(tree)

    if verbose:
        print("Rotating right around", node_key)
        print("Before rotation:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()
    
    z_node = z_tree.search(node_key)
    assert z_node != None
    z_tree._real_right_rotate(z_node)

    if verbose:
        print("After rotation:")
        print_ascii_tree_side(z_tree, convert_zigzag_to_regular(z_tree))
        print()

    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    r_node = tree.search(node_key)
    assert r_node != None
    tree._right_rotate(r_node)

    try:
        # Inserting a new red node on a lower path may create an illigal zigzag tree,
        # therefore the regular tree cannot be converted to zigzag.
        # The zigzag tree is therefore converted to regular and compared to the original tree.
        assert regular_tree_equality(convert_zigzag_to_regular(z_tree), tree)
    except AssertionError:
        print("Fails equality check. Left is output, right is expected.")
        print_ascii_tree_side(z_tree, convert_regular_to_zigzag(tree))
        raise

@test_group
def test_path_operations():
    # Test push/pop predicates
    test_pop_root_specific()
    test_push_root_specific()
    test_pop_upper_specific()
    test_push_upper_specific()
    test_pop_lower_specific()
    test_push_lower_specific()

    # Test popping all nodes
    test_pop_node_specific("x_11")
    test_pop_node_specific("x_10")
    test_pop_node_specific("x_9")
    test_pop_node_specific("x_8")
    test_pop_node_specific("x_7", set_red=True)
    test_pop_node_specific("x_4")
    test_pop_node_specific("x_1")

    # Test pushing all nodes
    test_push_node_specific("x_11")
    test_push_node_specific("x_10")
    test_push_node_specific("x_9")
    test_push_node_specific("x_8")
    test_push_node_specific("x_7")
    test_push_node_specific("x_6")
    test_push_node_specific("x_5")
    test_push_node_specific("x_4")
    test_push_node_specific("x_3")
    test_push_node_specific("x_2")
    test_push_node_specific("x_1")

    # Test rotate left
    test_rotate_left_larger_tree()
    # test_rotate_left_specific(3)  # 5 is black, and cannot be pushed to lower
    test_rotate_left_specific(6)  # 8 is black, and cannot be pushed to lower
    test_rotate_left_specific(8)
    test_rotate_left_specific(10)
    test_rotate_left_specific(11)
    # test_rotate_left_specific(13)  # 14 is black, and cannot be pushed to lower
    test_rotate_left_specific(15)
    test_rotate_left_specific(17)
    test_rotate_left_specific(19)

    # Test rotate right
    # test_rotate_right_specific(2)  # 2 is black, and cannot be popped from lower
    test_rotate_right_specific(3)
    test_rotate_right_specific(5)
    test_rotate_right_specific(6)
    test_rotate_right_specific(8)
    test_rotate_right_specific(10)
    test_rotate_right_specific(13)
    test_rotate_right_specific(15)
    # test_rotate_right_specific(17)  # 17 is black, and cannot be popped from lower
    test_rotate_right_specific(19)


# ---------------------------------------------
#              Insertion Tests
# ---------------------------------------------

@test
def test_insert_successor_large_tree_specific_key():
    k = 597
    colored = False

    tree = get_random_tree_from_insertions(1000, seed=42)
    z_tree = convert_regular_to_zigzag(tree)

    try:
        z_tree.insert_successor(z_tree.search(k), k + 0.5)
    except AssertionError:
        print("Fails insertion with internal assertion error")
        print("Tries to insert after", k)
        print("Initial state")
        print_ascii_tree_side(tree, convert_regular_to_zigzag(tree))
        print("Tree state (may be messed)")
        z_tree.print()
        raise
    
    assert z_tree._all_pointers_set()
    assert z_tree._all_regular_pointers_correct()

    tree.insert(k + 0.5)

    try:
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))
    except AssertionError:
        print("After inserting after", k)
        print("Expected:")
        convert_regular_to_zigzag(tree).print(colored=colored)
        print("Output:")
        z_tree.print(colored=colored)
        # print()
        # print("As regular trees:")
        # tree.print(colored=colored)
        # convert_zigzag_to_regular(z_tree).print(colored=colored)
        raise
    
    assert z_tree.is_valid_ZigZag_RB_tree()

@test
def test_insert_successor(n=100, seed=42):
    for k in range(1, n + 1):
        tree = get_random_tree_from_insertions(n, seed=seed)
        z_tree = convert_regular_to_zigzag(tree)

        try:
            z_tree.insert_successor(z_tree.search(k), k + 0.5)
        except AssertionError:
            print("Fails insertion with internal assertion error")
            print("Tries to insert after", k)
            print("Initial state")
            print_ascii_tree_side(tree, convert_regular_to_zigzag(tree))
            print("Tree state (may be messed)")
            z_tree.print()
            raise
        
        assert z_tree._all_pointers_set()
        assert z_tree._all_regular_pointers_correct()

        tree.insert(k + 0.5)

        try:
            assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree)), k
        except AssertionError:
            print("After inserting after", k)
            print("Error in tree equality, left is expected, right is output")
            print_ascii_tree_side(convert_regular_to_zigzag(tree), z_tree)
            raise

@test
def test_insert_incremental_equality(n=1000):
    tree = RB_tree()
    z_tree = Z_RB_tree()

    for k in range(n):
        tree.insert(k)
        z_tree.insert(k)

        assert z_tree._all_pointers_set()
        assert z_tree._all_regular_pointers_correct()

        try:
            assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)
        except AssertionError:
            print("After inserting", k)
            print("Error in tree equality, left is expected, right is output")
            print_ascii_tree_side(convert_regular_to_zigzag(tree), z_tree)
            break

@test
def test_insert_random_order(n=100, itr=100):
    for seed in range(itr):
        z_tree = Z_RB_tree()
        keys = list(range(1, n + 1))
        random.seed(seed)
        random.shuffle(keys)

        for key in keys:
            z_tree.insert(key)
            assert z_tree.contains(key)

            try:
                assert z_tree.is_valid_ZigZag_RB_tree()
            except AssertionError:
                print("Fails validity test after inserting", key, "in seed", seed)
                z_tree.is_valid_ZigZag_RB_tree(verbose=True)
                print("ZigZag tree:")
                z_tree.print()
                print()
                print("Regular view:")
                convert_zigzag_to_regular(z_tree).print()
                raise

@test
def test_insert_successor_in_order_random_order(n=100, k=10, itr=100, final_check_only=False):
    for seed in range(itr):
        random.seed(seed)
        
        z_tree = Z_RB_tree()
        initial_keys = list(range(1, n + 1, k))
        random.shuffle(initial_keys)

        for key in initial_keys:
            z_tree.insert(key)
        
        if not final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()

        tree = convert_zigzag_to_regular(z_tree)

        next_keys = [key + 1 for key in initial_keys if key != n]

        while next_keys:
            i = random.randint(0, len(next_keys) - 1)
            next_keys[i], next_keys[-1] = next_keys[-1], next_keys[i]
            key = next_keys.pop()

            tree.insert(key)
            z_tree.insert_successor(z_tree.search(key - 1), key)

            if not final_check_only:
                assert z_tree.is_valid_ZigZag_RB_tree()
                assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))

            if key != n and not z_tree.contains(key + 1):
                next_keys.append(key + 1)
    
    if final_check_only:
        assert z_tree.is_valid_ZigZag_RB_tree()
        assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))

@test
def test_insert_any_successor_random_order(n=100, itr=100, final_check_only=False):
    for seed in range(itr):
        random.seed(seed)

        z_tree = Z_RB_tree()
        z_x1 = z_tree.insert(1)
        tree = convert_zigzag_to_regular(z_tree)

        ranges = [(z_x1, 1, n + 1)]

        while ranges:
            i = random.randint(0, len(ranges) - 1)
            ranges[i], ranges[-1] = ranges[-1], ranges[i]
            z_xa, a, b = ranges.pop()

            if a + 1 == b:
                continue

            key = random.randint(a + 1, b - 1)
            z_xkey = z_tree.insert_successor(z_xa, key)

            tree.insert(key)

            if not final_check_only:
                assert z_tree.is_valid_ZigZag_RB_tree()
                assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))

            ranges.append((z_xa, a, key))
            ranges.append((z_xkey, key, b))
        
        if final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()
            assert zigzag_tree_equality(z_tree, convert_regular_to_zigzag(tree))

@test
def test_insert_predecessor_in_order_random_order(n=100, k=10, itr=100, final_check_only=False):
    for seed in range(itr):
        random.seed(seed)
        
        z_tree = Z_RB_tree()
        initial_keys = list(range(n, 0, -k))
        random.shuffle(initial_keys)

        for key in initial_keys:
            z_tree.insert(key)
        
        tree = convert_zigzag_to_regular(z_tree)
        
        if not final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()
            assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)

        next_keys = [key - 1 for key in initial_keys if key != 1]

        while next_keys:
            i = random.randint(0, len(next_keys) - 1)
            next_keys[i], next_keys[-1] = next_keys[-1], next_keys[i]
            key = next_keys.pop()

            tree._insert_predecessor(key, key + 1)
            z_tree.insert_predecessor(z_tree.search(key + 1), key)

            if not final_check_only:
                assert z_tree.is_valid_ZigZag_RB_tree()

                try:
                    assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)
                except AssertionError:
                    print("After inserting", key)
                    print("Error in tree equality, left is expected, right is output")
                    print_ascii_tree_side(convert_regular_to_zigzag(tree), z_tree)
                    print()
                    print("Regular view:")
                    print_ascii_tree_side(tree, convert_zigzag_to_regular(z_tree))
                    raise

            if key != 1 and not z_tree.contains(key - 1):
                next_keys.append(key - 1)
        
        if final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()
            assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)

@test
def test_insert_any_predecessor_random_order(n=100, itr=100, final_check_only=False):
    for seed in range(itr):
        random.seed(seed)

        z_tree = Z_RB_tree()
        z_xn = z_tree.insert(n)
        tree = convert_zigzag_to_regular(z_tree)

        ranges = [(z_xn, 0, n)]

        while ranges:
            i = random.randint(0, len(ranges) - 1)
            ranges[i], ranges[-1] = ranges[-1], ranges[i]
            z_xb, a, b = ranges.pop()

            if a + 1 == b:
                continue

            key = random.randint(a + 1, b - 1)

            z_xkey = z_tree.insert_predecessor(z_xb, key)
            tree._insert_predecessor(key, b)

            if not final_check_only:
                assert z_tree.is_valid_ZigZag_RB_tree()
                
                try:
                    assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)
                except AssertionError:
                    print("After inserting", key)
                    print("Error in tree equality, left is expected, right is output")
                    print_ascii_tree_side(convert_regular_to_zigzag(tree), z_tree)
                    print()
                    print("Regular view:")
                    print_ascii_tree_side(tree, convert_zigzag_to_regular(z_tree))
                    raise

            ranges.append((z_xkey, a, key))
            ranges.append((z_xb, key, b))
        
        if final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()
            assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)

@test
def test_insert_predecessor_and_successor_random_order(n=100, itr=100, final_check_only=False):
    for seed in range(itr):
        random.seed(seed)

        z_tree = Z_RB_tree()
        z_x1 = z_tree.insert(1)
        z_xn = z_tree.insert(n)
        tree = convert_zigzag_to_regular(z_tree)

        ranges = [(z_x1, z_xn, 1, n)]

        while ranges:
            i = random.randint(0, len(ranges) - 1)
            ranges[i], ranges[-1] = ranges[-1], ranges[i]
            z_xa, z_xb, a, b = ranges.pop()

            if a + 1 == b:
                continue

            key = random.randint(a + 1, b - 1)
            if random.choice([True, False]):
                z_xkey = z_tree.insert_predecessor(z_xb, key)
                tree._insert_predecessor(key, b)
            else:
                z_xkey = z_tree.insert_successor(z_xa, key)
                tree.insert(key)

            if not final_check_only:
                assert z_tree.is_valid_ZigZag_RB_tree()
                
                try:
                    assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)
                except AssertionError:
                    print("After inserting", key)
                    print("Error in tree equality, left is expected, right is output")
                    print_ascii_tree_side(convert_regular_to_zigzag(tree), z_tree)
                    print()
                    print("Regular view:")
                    print_ascii_tree_side(tree, convert_zigzag_to_regular(z_tree))
                    raise

            ranges.append((z_xa, z_xkey, a, key))
            ranges.append((z_xkey, z_xb, key, b))

        if final_check_only:
            assert z_tree.is_valid_ZigZag_RB_tree()
            assert zigzag_tree_equality(convert_regular_to_zigzag(tree), z_tree)

@test_group
def test_insertion():
    test_insert_successor_large_tree_specific_key()
    test_insert_successor(n=100)
    # test_insert_successor(n=1000)
    test_insert_incremental_equality()
    test_insert_random_order(n=100)

    test_insert_successor_in_order_random_order()
    test_insert_any_successor_random_order()
    test_insert_predecessor_in_order_random_order()
    test_insert_any_predecessor_random_order()
    test_insert_predecessor_and_successor_random_order()

    test_insert_successor_in_order_random_order(n=10000, itr=15, final_check_only=True)
    test_insert_any_successor_random_order(n=10000, itr=15, final_check_only=True)
    test_insert_predecessor_in_order_random_order(n=10000, itr=15, final_check_only=True)
    test_insert_any_predecessor_random_order(n=10000, itr=15, final_check_only=True)
    test_insert_predecessor_and_successor_random_order(n=10000, itr=15, final_check_only=True)

    test_insert_successor_in_order_random_order(n=100000, itr=2, final_check_only=True)
    test_insert_any_successor_random_order(n=100000, itr=2, final_check_only=True)
    test_insert_predecessor_in_order_random_order(n=100000, itr=2, final_check_only=True)
    test_insert_any_predecessor_random_order(n=100000, itr=2, final_check_only=True)
    test_insert_predecessor_and_successor_random_order(n=100000, itr=2, final_check_only=True)


# ---------------------------------------------
#              Deletion Tests
# ---------------------------------------------

@test
def test_deletion_of_single_node_tree():
    z_tree = Z_RB_tree()
    z_tree.insert(1)
    z_tree.delete(1)
    assert z_tree._root == None

@test
def test_deletion_without_fixup_is_valid_zigzag_structure(n, itr=100):
    for seed in range(itr):
        # seed = 29
        random.seed(seed)

        keys = list(range(1, n + 1))
        random.shuffle(keys)

        for key_delete in range(1, n + 1):
            z_tree = Z_RB_tree()
            delete_fixup_only_color(z_tree)

            for key in keys:
                z_tree.insert(key)

            z_tree.delete(key_delete)

            assert z_tree._all_pointers_set()
            assert z_tree._correct_zigzag()

@test
def test_deletion_without_fixup_produces_same_tree(n, itr=100):
    for seed in range(itr):
        random.seed(seed)

        keys = list(range(1, n + 1))
        random.shuffle(keys)

        for key_delete in range(1, n + 1):
            z_tree = Z_RB_tree()
            delete_fixup_only_color(z_tree)

            for key in keys:
                z_tree.insert(key)
            
            tree = convert_zigzag_to_regular(z_tree)
            delete_fixup_only_color(tree)

            tree.delete(key_delete)
            z_tree.delete(key_delete)

            assert regular_tree_equality(tree, convert_zigzag_to_regular(z_tree))


@test_group
def test_deletion():
    test_deletion_of_single_node_tree()
    test_deletion_without_fixup_is_valid_zigzag_structure(20)
    test_deletion_without_fixup_is_valid_zigzag_structure(100, itr=10)
    test_deletion_without_fixup_is_valid_zigzag_structure(500, itr=1)
    test_deletion_without_fixup_produces_same_tree(20)
    test_deletion_without_fixup_produces_same_tree(100, itr=10)
    test_deletion_without_fixup_produces_same_tree(500, itr=1)

# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_validity_checks()
    test_node_primitives()
    test_path_operations()
    test_insertion()
    test_deletion()

if __name__ == "__main__":
    test_all()
