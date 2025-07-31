from util import link_left, link_right
from convert import convert_regular_to_zigzag

from Regular_RB_tree import Node, RB_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_RB_tree

import random


def get_left_path_tree() -> RB_tree:
    tree = RB_tree()
    
    red = True
    black = False

    nodes = [Node(f"x_{i}") for i in range(1, 11 + 1)[::-1]]
    colors = [black, black, red, black, black, black, black, red, black, black, red]
    subtrees = [Node(f"T_{i}", is_red=False) for i in range(1, 11 + 1)[::-1]]

    tree._root = nodes[0]

    for a, b in zip(nodes, nodes[1:]):
        link_left(a, b)

    for a, t_a in zip(nodes, subtrees):
        link_right(a, t_a)

    for a, c_r_a in zip(nodes, colors):
        a._set_red() if c_r_a else a._set_black()

    assert tree._all_pointers_set()

    return tree

def get_right_path_tree() -> RB_tree:
    tree = RB_tree()
    
    red = True
    black = False

    nodes = [Node(f"x_{i}") for i in range(1, 11 + 1)]
    colors = [black, black, red, black, black, black, black, red, black, black, red]
    subtrees = [Node(f"T_{i}", is_red=False) for i in range(1, 11 + 1)]

    tree._root = nodes[0]

    for a, b in zip(nodes, nodes[1:]):
        link_right(a, b)

    for a, t_a in zip(nodes, subtrees):
        link_left(a, t_a)

    for a, c_r_a in zip(nodes, colors):
        a._set_red() if c_r_a else a._set_black()

    assert tree._all_pointers_set()

    return tree

def get_insert_n_elements_tree(n: int) -> RB_tree:
    tree = RB_tree()

    for i in range(1, n + 1):
        tree.insert(i)
    
    assert tree.is_valid_RB_tree()

    return tree

def get_random_tree_from_insertions(n: int, seed=None) -> RB_tree:
    tree = RB_tree()
    elements = list(range(1, n + 1))

    if seed is not None:
        random.seed(seed)
    random.shuffle(elements)

    for i in elements:
        tree.insert(i)
    
    assert tree.is_valid_RB_tree()

    return tree
