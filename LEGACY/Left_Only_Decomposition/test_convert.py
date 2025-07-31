from test_decorators import test, test_group, test_file

from test_tree_creation import *
from convert import convert_regular_to_zigzag

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
    print_tree_and_zigzag_tree(get_insert_n_elements_tree(20))
    print_tree_and_zigzag_tree(get_random_tree_from_insertions(20, seed=42))


# ---------------------------------------------
#            Conversion sets pointers
# ---------------------------------------------

@test
def test_parent_of_children_is_self_random(n, itr=100):
    for seed in range(itr):
        z_tree = convert_regular_to_zigzag(get_random_tree_from_insertions(n, seed))
        assert z_tree._all_pointers_set()

@test_group
def test_conversion_sets_pointers():
    test_parent_of_children_is_self_random(20, itr=1000)
    test_parent_of_children_is_self_random(100, itr=100)
    test_parent_of_children_is_self_random(1000, itr=20)


# ---------------------------------------------
#       Conversion returns valid zig zags
# ---------------------------------------------

@test
def test_conversion_returns_valid_tree_random(n, itr=100):
    for seed in range(itr):
        z_tree = convert_regular_to_zigzag(get_random_tree_from_insertions(n, seed))
        assert z_tree._correct_zigzag()

@test_group
def test_conversion_returns_valid_tree():
    test_conversion_returns_valid_tree_random(20, itr=1000)
    test_conversion_returns_valid_tree_random(100, itr=100)
    test_conversion_returns_valid_tree_random(1000, itr=20)


# ---------------------------------------------
#                    Main
# ---------------------------------------------

@test_file
def test_all():
    test_conversion_sets_pointers()
    test_conversion_returns_valid_tree()

if __name__ == "__main__":
    print_all_trees()
    # test_all()
