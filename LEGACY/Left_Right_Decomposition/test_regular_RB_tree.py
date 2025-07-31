import Regular_RB_tree
from random import shuffle

# ---------------------------------------------
#               Rotation tests
# ---------------------------------------------

def test_small_left_rotate():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree._left_rotate(tree._root)
    assert tree._is_sorted()

def test_small_right_rotate():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(3)
    tree.insert(2)
    tree.insert(1)
    tree._right_rotate(tree._root)
    assert tree._is_sorted()

def test_all_rotations():
    test_small_left_rotate()
    test_small_right_rotate()


# ---------------------------------------------
#               Insertion tests
# ---------------------------------------------

def test_small_increasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    assert tree.is_valid_RB_tree()

def test_small_decreasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(3)
    tree.insert(2)
    tree.insert(1)
    assert tree.is_valid_RB_tree()

def test_large_increasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    for i in range(1000):
        tree.insert(i)
    assert tree.is_valid_RB_tree()

def test_large_decreasing_insertion():
    tree = Regular_RB_tree.RB_tree()
    for i in range(1000)[::-1]:
        tree.insert(i)
    assert tree.is_valid_RB_tree()

def test_random_order_insertion(n):
    tree = Regular_RB_tree.RB_tree()
    elements = list(range(n))
    shuffle(elements)
    for key in elements:
        tree.insert(key)
    assert tree.is_valid_RB_tree()

def test_large_random_order_insertion():
    test_random_order_insertion(1000)

def test_huge_random_order_insertion():
    test_random_order_insertion(100000)

def test_all_insertions():
    test_small_increasing_insertion()
    test_small_decreasing_insertion()
    test_large_increasing_insertion()
    test_large_decreasing_insertion()
    test_large_random_order_insertion()
    test_huge_random_order_insertion()


# ---------------------------------------------
#               Deletion tests
# ---------------------------------------------

def test_small_deletion():
    tree = Regular_RB_tree.RB_tree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.delete(2)
    assert tree.is_valid_RB_tree()

def test_all_deletions():
    test_small_deletion()


# ---------------------------------------------
#                   Main
# ---------------------------------------------

def test_all():
    test_all_rotations()
    test_all_insertions()
    # test_all_deletions()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")
