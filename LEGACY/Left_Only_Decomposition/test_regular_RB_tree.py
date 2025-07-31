from test_decorators import test, test_group, test_file

import Regular_RB_tree
from test_tree_creation import get_random_tree_from_insertions
import random

# ---------------------------------------------
#               Rotation tests
# ---------------------------------------------

@test
def test_small_left_rotate():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree._left_rotate(tree._root)
    assert tree._is_sorted()

@test
def test_small_right_rotate():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(3)
    tree.insert(2)
    tree.insert(1)
    tree._right_rotate(tree._root)
    assert tree._is_sorted()

@test_group
def test_all_rotations():
    test_small_left_rotate()
    test_small_right_rotate()


# ---------------------------------------------
#               Insertion tests
# ---------------------------------------------

@test
def test_small_increasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    assert tree.is_valid_RB_tree()

@test
def test_small_decreasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(3)
    tree.insert(2)
    tree.insert(1)
    assert tree.is_valid_RB_tree()

@test
def test_duplicate_insertion():
    tree = Regular_RB_tree.RB_tree()
    for k in [6, 4, 2, 3, 1, 1, 7, 9, 4, 5, 2]:
        tree.insert(k)
    tree.print()
    assert tree.is_valid_RB_tree()

@test
def test_large_increasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    for i in range(1000):
        tree.insert(i)
    assert tree.is_valid_RB_tree()

@test
def test_large_decreasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    for i in range(1000)[::-1]:
        tree.insert(i)
    assert tree.is_valid_RB_tree()

@test
def test_random_order_insertion(n, seed=42):
    tree = get_random_tree_from_insertions(n, seed=seed)
    assert tree.is_valid_RB_tree()

@test
def test_insertion_with_pred(verbose=False):
    tree = Regular_RB_tree.RB_tree()
    for elm in [1, 2, 3, 4, 5, 7, 8, 9]:
        tree.insert(elm)
    
    if verbose:
        print("Before insertion:")
        tree.print()
        print()

    tree._insert_predecessor(6, 7)
    assert tree.is_valid_RB_tree()

    if verbose:
        print("After insertion:")
        tree.print()
        print()

@test_group
def test_all_insertions():
    test_small_increasing_insertion()
    test_small_decreasing_insertion()
    test_duplicate_insertion()
    test_large_increasing_insertion()
    test_large_decreasing_insertion()
    test_random_order_insertion(1000)
    test_random_order_insertion(100000)
    test_insertion_with_pred()


# ---------------------------------------------
#               Deletion tests
# ---------------------------------------------

@test
def test_small_deletion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.delete(2)
    assert tree.is_valid_RB_tree()

@test
def test_medium_deletion_leaf():
    tree = Regular_RB_tree.RB_tree()
    for k in [6, 2, 3, 1, 7, 9, 4, 5]:
        tree.insert(k)
    tree.delete(9)
    assert tree.is_valid_RB_tree(verbose=True)

def helper_test_deletion_in_order(order, n, seed=42, check_valid_last_only=False, check_size=False, check_contains=False, **kwargs):
    tree = get_random_tree_from_insertions(n, seed=seed)
    expected_size = n
    for i in order:
        tree.delete(i)
        expected_size -= 1
        
        if not check_valid_last_only:
            assert tree.is_valid_RB_tree()
        if check_size:
            assert tree.size() == expected_size
        if check_contains:
            assert not tree.contains(i)

    assert tree.size() == 0
    if check_valid_last_only:
        assert tree.is_valid_RB_tree()

@test
def test_increasing_deletion(n, seed=42, **kwargs):
    helper_test_deletion_in_order(range(1, n + 1), n, seed=seed, **kwargs)

@test
def test_decreasing_deletion(n, seed=42, **kwargs):
    helper_test_deletion_in_order(range(1, n + 1)[::-1], n, seed=seed, **kwargs)
    
@test
def test_random_order_deletion(n, seed=42, **kwargs):
    order = list(range(1, n + 1))
    random.seed(-seed)
    random.shuffle(order)
    helper_test_deletion_in_order(order, n, seed=seed, **kwargs)

@test_group
def test_all_deletions():
    test_small_deletion()
    test_medium_deletion_leaf()
    for func in [test_increasing_deletion, test_decreasing_deletion, test_random_order_deletion]:
        func(20, check_size=True, check_contains=True)
        func(100, check_size=True, check_contains=True)
        func(1000, check_size=True, check_contains=True)
        func(100000, check_valid_last_only=True)


# ---------------------------------------------
#                Mixed tests
# ---------------------------------------------

@test
def test_insert_delete_random_order(n, seed=42, check_valid_last_only=False, check_size=False, check_contains=False):
    tree = Regular_RB_tree.RB_tree()
    expected_size = 0
    random.seed(seed)
    to_insert = list(range(1, n + 1))
    to_delete = []
    while to_insert or to_delete:
        total_options = len(to_insert) + len(to_delete)
        choose = random.randint(0, total_options - 1)
        if choose < len(to_insert):
            to_insert[choose], to_insert[-1] = to_insert[-1], to_insert[choose]
            elm = to_insert.pop()
            tree.insert(elm)
            expected_size += 1
            if check_contains:
                assert tree.contains(elm)
            to_delete.append(elm)
        else:
            choose -= len(to_insert)
            to_delete[choose], to_delete[-1] = to_delete[-1], to_delete[choose]
            elm = to_delete.pop()
            tree.delete(elm)
            expected_size -= 1
            if check_contains:
                assert not tree.contains(elm)
        
        if check_size:
            assert tree.size() == expected_size
        
        if not check_valid_last_only:
            assert tree.is_valid_RB_tree()
    
    if check_valid_last_only:
        assert tree.is_valid_RB_tree()

@test_group
def test_all_mixed_operations():
    test_insert_delete_random_order(20, check_size=True, check_contains=True)
    test_insert_delete_random_order(100, check_size=True, check_contains=True)
    test_insert_delete_random_order(1000, check_size=True, check_contains=True)
    test_insert_delete_random_order(100000, check_valid_last_only=True)


# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_all_rotations()
    test_all_insertions()
    test_all_deletions()
    test_all_mixed_operations()

if __name__ == "__main__":
    test_all()
