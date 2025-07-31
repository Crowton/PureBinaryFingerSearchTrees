from Level_Linked_ab_Tree import Level_Linked_ab_Tree, Level_Internal_Node, Level_Leaf_Node

from __test_decorators import test, test_group, test_file



# ---------------------------------------------
#                  Helpers
# ---------------------------------------------

def create_tree(n, seed=42):
    import random

    values = list(range(n))
    random.seed(seed)
    random.shuffle(values)

    tree = Level_Linked_ab_Tree()

    for val in values:
        tree.insert(val)
    
    return tree


# ---------------------------------------------
#                   Query
# ---------------------------------------------

@test
def test_search():
    for seed in range(10):
        tree = create_tree(100, seed)
        for i in range(100):
            node = tree.search(i)
            assert node is not None
            assert node.value == i
        
        assert tree.search(-1) is None
        assert tree.search(100) is None

@test
def test_pred_search_exact():
    for seed in range(10):
        tree = create_tree(100, seed)
        for i in range(100):
            node = tree.pred_search(i)
            assert node is not None
            assert node.value == i
        
        assert tree.pred_search(-1) is None
        assert tree.pred_search(100) is not None

@test
def test_pred_search_non_exact():
    for seed in range(10):
        tree = create_tree(100, seed)
        for i in range(100):
            node = tree.pred_search(i + 0.5)
            assert node is not None
            assert node.value == i

@test
def test_finger_search_exact():
    for seed in range(10):
        tree = create_tree(100, seed)
        for start_node in tree:
            for i in range(100):
                node = tree.finger_search(start_node, i)
                assert node is not None
                assert node.value == i
            
            assert tree.finger_search(start_node, -1) is None
            assert tree.finger_search(start_node, 100) is not None

@test
def test_finger_search_non_exact():
    for seed in range(10):
        tree = create_tree(100, seed)
        for start_node in tree:
            for i in range(100):
                node = tree.finger_search(start_node, i + 0.5)
                assert node is not None
                assert node.value == i

@test_group
def test_queries():
    test_search()
    test_pred_search_exact()
    test_pred_search_non_exact()

    test_finger_search_exact()
    test_finger_search_non_exact()


# ---------------------------------------------
#                   Updates
# ---------------------------------------------

@test
def test_single_insert():
    tree = Level_Linked_ab_Tree()
    tree.insert(1)
    
    assert tree._root is not None
    assert isinstance(tree._root, Level_Leaf_Node)
    assert tree.is_valid()

@test
def test_double_insert():
    tree = Level_Linked_ab_Tree()
    tree.insert(1)
    tree.insert(2)
    
    assert tree._root is not None
    assert isinstance(tree._root, Level_Internal_Node)
    assert tree.is_valid()

def test_insertion_of(values):
    tree = Level_Linked_ab_Tree()

    for value in values:
        tree.insert(value)
        assert tree.is_valid()
    
    assert tree.size() == len(values)

@test
def test_insert_increasing():
    values = list(range(200))
    test_insertion_of(values)

@test
def test_insert_decreasing():
    values = list(range(200))[::-1]
    test_insertion_of(values)

@test
def test_insert_random_order():
    from random import shuffle, seed

    for s in range(30):
        seed(s)
        values = list(range(200))
        shuffle(values)
        test_insertion_of(values)
    

@test_group
def test_insert():
    test_single_insert()
    test_double_insert()

    test_insert_increasing()
    test_insert_decreasing()
    test_insert_random_order()


# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_queries()
    test_insert()

if __name__ == "__main__":
    test_all()
