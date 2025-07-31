from convert import link_left, link_right, convert_regular_to_zigzag, convert_zigzag_to_regular

from Regular_RB_tree import Node, RB_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_tree

import tree_equality
import random


# ---------------------------------------------
#               Test tree creation
# ---------------------------------------------

def get_left_path_tree() -> RB_tree:
    tree = RB_tree()
    
    a = Node("x_k")
    b = Node("x_k-1")
    c = Node("x_k-2")
    d = Node("x_k-3")
    e = Node("x_m")
    f = Node("x_6")
    g = Node("x_5")
    h = Node("x_4")
    i = Node("x_3")
    j = Node("x_2")
    k = Node("x_1")

    t_a = Node("T_k")
    t_b = Node("T_k-1")
    t_c = Node("T_k-2")
    t_d = Node("T_k-3")
    t_e = Node("T_m")
    t_f = Node("T_6")
    t_g = Node("T_5")
    t_h = Node("T_4")
    t_i = Node("T_3")
    t_j = Node("T_2")
    t_k = Node("T_1")

    tree._root = a

    a._parent = None
    link_left(a, b)
    link_left(b, c)
    link_left(c, d)
    link_left(d, e)
    link_left(e, f)
    link_left(f, g)
    link_left(g, h)
    link_left(h, i)
    link_left(i, j)
    link_left(j, k)
    k._left = None

    link_right(a, t_a)
    link_right(b, t_b)
    link_right(c, t_c)
    link_right(d, t_d)
    link_right(e, t_e)
    link_right(f, t_f)
    link_right(g, t_g)
    link_right(h, t_h)
    link_right(i, t_i)
    link_right(j, t_j)
    link_right(k, t_k)

    t_a._left = t_a._right = None
    t_b._left = t_b._right = None
    t_c._left = t_c._right = None
    t_d._left = t_d._right = None
    t_e._left = t_e._right = None
    t_f._left = t_f._right = None
    t_g._left = t_g._right = None
    t_h._left = t_h._right = None
    t_i._left = t_i._right = None
    t_j._left = t_j._right = None
    t_k._left = t_k._right = None

    a.set_black()
    b.set_black()
    c.set_red()
    d.set_black()
    e.set_black()
    f.set_black()
    g.set_black()
    h.set_red()
    i.set_black()
    j.set_black()
    k.set_red()

    t_a.set_black()
    t_b.set_black()
    t_c.set_black()
    t_d.set_black()
    t_e.set_black()
    t_f.set_black()
    t_g.set_black()
    t_h.set_black()
    t_i.set_black()
    t_j.set_black()
    t_k.set_black()

    assert tree._all_pointers_set(tree._root)

    return tree

def get_right_path_tree() -> RB_tree:
    tree = RB_tree()
    a = Node("x_r")
    b = Node("x_k")
    c = Node("x_k-1")
    d = Node("x_k-2")
    e = Node("x_k-3")
    f = Node("x_m")
    g = Node("x_6")
    h = Node("x_5")
    i = Node("x_4")
    j = Node("x_3")
    k = Node("x_2")
    l = Node("x_1")

    t_a = Node("T_r")
    t_b = Node("T_k")
    t_c = Node("T_k-1")
    t_d = Node("T_k-2")
    t_e = Node("T_k-3")
    t_f = Node("T_m")
    t_g = Node("T_6")
    t_h = Node("T_5")
    t_i = Node("T_4")
    t_j = Node("T_3")
    t_k = Node("T_2")
    t_l = Node("T_1")

    tree._root = a

    a._parent = None
    link_right(a, b)
    link_right(b, c)
    link_right(c, d)
    link_right(d, e)
    link_right(e, f)
    link_right(f, g)
    link_right(g, h)
    link_right(h, i)
    link_right(i, j)
    link_right(j, k)
    link_right(k, l)
    l._right = None

    link_left(a, t_a)
    link_left(b, t_b)
    link_left(c, t_c)
    link_left(d, t_d)
    link_left(e, t_e)
    link_left(f, t_f)
    link_left(g, t_g)
    link_left(h, t_h)
    link_left(i, t_i)
    link_left(j, t_j)
    link_left(k, t_k)
    link_left(l, t_l)

    t_a._left = t_a._right = None
    t_b._left = t_b._right = None
    t_c._left = t_c._right = None
    t_d._left = t_d._right = None
    t_e._left = t_e._right = None
    t_f._left = t_f._right = None
    t_g._left = t_g._right = None
    t_h._left = t_h._right = None
    t_i._left = t_i._right = None
    t_j._left = t_j._right = None
    t_k._left = t_k._right = None
    t_l._left = t_l._right = None

    a.set_black()
    b.set_black()
    c.set_black()
    d.set_red()
    e.set_black()
    f.set_black()
    g.set_black()
    h.set_black()
    i.set_red()
    j.set_black()
    k.set_black()
    l.set_red()

    t_a.set_black()
    t_b.set_black()
    t_c.set_black()
    t_d.set_black()
    t_e.set_black()
    t_f.set_black()
    t_g.set_black()
    t_h.set_black()
    t_i.set_black()
    t_j.set_black()
    t_k.set_black()
    t_l.set_black()

    assert tree._all_pointers_set(tree._root)

    return tree

def get_two_left_path() -> RB_tree:
    tree = RB_tree()
    tree.insert(2)
    tree.insert(1)
    return tree

def get_insert_n_elements_tree(n: int) -> RB_tree:
    tree = RB_tree()

    for i in range(1, n + 1):
        tree.insert(i)
    
    assert tree.is_valid_RB_tree()

    return tree

def get_random_tree(n: int, seed=None) -> RB_tree:
    tree = RB_tree()
    elements = list(range(1, n + 1))

    if seed is not None:
        random.seed(seed)
    random.shuffle(elements)

    for i in elements:
        tree.insert(i)
    
    assert tree.is_valid_RB_tree()

    return tree


# ---------------------------------------------
#                 Visual tests
# ---------------------------------------------

def print_tree_and_zigzag_tree(tree):
    print("Original tree:")
    tree.print()
    print()

    print("ZigZag tree:")
    z_tree = convert_regular_to_zigzag(tree)    
    z_tree.print()
    print()

def print_all_trees():
    print_tree_and_zigzag_tree(get_left_path_tree())
    print_tree_and_zigzag_tree(get_right_path_tree())
    print_tree_and_zigzag_tree(get_two_left_path())
    print_tree_and_zigzag_tree(get_insert_n_elements_tree(20))
    print_tree_and_zigzag_tree(get_random_tree(20, seed=42))


# ---------------------------------------------
#       Convert regular to zigzag tests
# ---------------------------------------------

def test_convert_regular_to_zigzag_examples():
    def test_convert_eq(tree):
        z_tree = convert_regular_to_zigzag(tree)
        try:
            assert tree_equality.regular_and_zigzag_tree_equality(tree, z_tree)
        except AssertionError:
            print("Trees are not equal:")
            tree.print()
            print()
            z_tree.print()
            print()
            print("Trying to rebuild tree, using view by zigzag:")
            convert_zigzag_to_regular(z_tree).print()
            print()
            raise


    left_path_tree = get_left_path_tree()
    test_convert_eq(left_path_tree)

    right_path_tree = get_right_path_tree()
    test_convert_eq(right_path_tree)

    two_left_path_tree = get_two_left_path()
    test_convert_eq(two_left_path_tree)

    n = 20
    n_elements_tree = get_insert_n_elements_tree(n)
    test_convert_eq(n_elements_tree)

    random_tree = get_random_tree(n, seed=42)
    test_convert_eq(random_tree)

def test_convert_regular_to_zigzag_random(n, itr=100):
    for seed in range(itr):
        random_tree = get_random_tree(n, seed=seed)
        try:
            z_random_tree = convert_regular_to_zigzag(random_tree)
        except AssertionError:
            print(f"Failing to build ZigZag tree from: (seed={seed})")
            random_tree.print()
            print()
            raise

        try:
            assert tree_equality.regular_and_zigzag_tree_equality(random_tree, z_random_tree)
        except AssertionError:
            print(f"Trees are not equal: (seed={seed})")
            random_tree.print()
            print()
            z_random_tree.print()
            print()
            print("Trying to rebuild tree, using view by zigzag:")
            convert_zigzag_to_regular(z_random_tree).print()
            print()
            raise

def test_convert_regular_to_zigzag():
    test_convert_regular_to_zigzag_examples()
    test_convert_regular_to_zigzag_random(10)
    test_convert_regular_to_zigzag_random(100)
    test_convert_regular_to_zigzag_random(1000, itr=40)

# ---------------------------------------------
#                    Main
# ---------------------------------------------

def test_all():
    test_convert_regular_to_zigzag()

if __name__ == "__main__":
    print_tree_and_zigzag_tree(get_left_path_tree())
    # print_tree_and_zigzag_tree(get_right_path_tree())
    exit(0)

    # print_all_trees()
    test_all()

    print("All tests passed!")
