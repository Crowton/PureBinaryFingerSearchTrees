from __test_decorators import test, test_group, test_file

from SLL_Red_Black_Tree import RB_Tree
from SLL_Metanode import Metanode
from SLL_Atomic_Node import AtomicNode

import random

from util import print_ascii_tree


class Mock_Metanode:
    def __init__(self, value, left=None, right=None, parent=None, pred=None, succ=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.pred = pred
        self.succ = succ
    
    # def must_contain(self, value):
    #     assert isinstance(value, list)
    #     return self.value[0] <= value < self.value[-1]

    # def smallest_value(self):
    #     return self.value[0]

    # def predesessor_search(self, value):
    #     for a, b in zip(self.value, self.value[1:]):
    #         if a <= value < b:
    #             return a

    def __str__(self):
        return f"Mock_Metanode({self.value})"
    
    def to_tuple(self):
        def inner(node):
            if node is None:
                return ()
            return (node.value, inner(node.left), inner(node.right))
        return inner(self)

    def print(self):
        print_ascii_tree(self.to_tuple())
    
    def check_pointers(self):
        if self.left is not None:
            assert self.left.parent == self
        if self.right is not None:
            assert self.right.parent == self
        if self.pred is not None:
            assert self.pred.succ == self
        if self.succ is not None:
            assert self.succ.pred == self

# ---------------------------------------------
#                   Rotations
# ---------------------------------------------

@test
def test_left_rotate():
    for has_parent in [True, False]:
        for is_left_child in ([True, False] if has_parent else [False]):
            for has_a in [True, False]:
                for has_b in [True, False]:
                    for has_c in [True, False]:
                        tree = RB_Tree()
                        p, s, x, y, a, b, c = [Mock_Metanode(c) for c in "PSXYABC"]
                        if not has_parent:
                            p = s = None
                        if not has_a:
                            a = None
                        if not has_b:
                            b = None
                        if not has_c:
                            c = None

                        if has_parent:
                            tree._root = p
                            if is_left_child:
                                p.left = x
                                p.right = s
                            else:
                                p.left = s
                                p.right = x
                            x.parent = p
                            s.parent = p
                        x.right = y
                        y.parent = x
                        if has_a:
                            x.left = a
                            a.parent = x
                        if has_b:
                            y.left = b
                            b.parent = y
                        if has_c:
                            y.right = c
                            c.parent = y

                        nodes = [a, y, b, x, c]
                        if has_parent:
                            if is_left_child:
                                nodes = nodes + [p, s]
                            else:
                                nodes = [s, p] + nodes
                        nodes = [n for n in nodes if n is not None]

                        for n1, n2 in zip(nodes, nodes[1:]):
                            n1.succ = n2
                            n2.pred = n1

                        print("Contains:", [str(n) for n in nodes])

                        print("Before:")
                        if p is not None:
                            p.print()
                        else:
                            x.print()
                        print()

                        for n in nodes:
                            n.check_pointers()

                        tree._left_rotate(x)

                        print("After:")
                        if p is not None:
                            p.print()
                        else:
                            y.print()
                        print()

                        for n in nodes:
                            n.check_pointers()

                        if has_parent:
                            assert tree._root == p
                            if is_left_child:
                                assert p.left == y
                            else:
                                assert p.right == y
                            assert y.parent == p
                        
                        assert y.left == x
                        assert x.parent == y

                        if has_a:
                            assert a.parent == x
                            assert x.left == a
                        if has_b:
                            assert b.parent == x
                            assert x.right == b
                        if has_c:
                            assert c.parent == y
                            assert y.right == c

                        for n1, n2 in zip(nodes, nodes[1:]):
                            assert n1.succ == n2
                            assert n2.pred == n1

@test
def test_right_rotate():
    for has_parent in [True, False]:
        for is_left_child in ([True, False] if has_parent else [False]):
            for has_a in [True, False]:
                for has_b in [True, False]:
                    for has_c in [True, False]:
                        tree = RB_Tree()
                        p, s, x, y, a, b, c = [Mock_Metanode(c) for c in "PSXYABC"]
                        if not has_parent:
                            p = s = None
                        if not has_a:
                            a = None
                        if not has_b:
                            b = None
                        if not has_c:
                            c = None

                        if has_parent:
                            tree._root = p
                            if is_left_child:
                                p.left = x
                                p.right = s
                            else:
                                p.left = s
                                p.right = x
                            x.parent = p
                            s.parent = p
                        x.left = y
                        y.parent = x
                        if has_a:
                            y.left = a
                            a.parent = y
                        if has_b:
                            y.right = b
                            b.parent = y
                        if has_c:
                            x.right = c
                            c.parent = x

                        nodes = [a, y, b, x, c]
                        if has_parent:
                            if is_left_child:
                                nodes = nodes + [p, s]
                            else:
                                nodes = [s, p] + nodes
                        nodes = [n for n in nodes if n is not None]

                        for n1, n2 in zip(nodes, nodes[1:]):
                            n1.succ = n2
                            n2.pred = n1

                        print("Before:")
                        if p is not None:
                            p.print()
                        else:
                            x.print()
                        print()

                        for n in nodes:
                            n.check_pointers()

                        tree._right_rotate(x)

                        print("After:")
                        if p is not None:
                            p.print()
                        else:
                            y.print()
                        print()

                        for n in nodes:
                            n.check_pointers()

                        if has_parent:
                            assert tree._root == p
                            if is_left_child:
                                assert p.left == y
                            else:
                                assert p.right == y
                            assert y.parent == p
                        
                        assert y.right == x
                        assert x.parent == y

                        if has_a:
                            assert a.parent == y
                            assert y.left == a
                        if has_b:
                            assert b.parent == x
                            assert x.left == b
                        if has_c:
                            assert c.parent == x
                            assert x.right == c

                        for n1, n2 in zip(nodes, nodes[1:]):
                            assert n1.succ == n2
                            assert n2.pred == n1

@test_group
def test_rotation():
    test_left_rotate()
    test_right_rotate()


# ---------------------------------------------
#                    Search
# ---------------------------------------------

def create_small_proper_tree():
    metas = []
    for i in [0, 20, 40]:
        atomic = AtomicNode(i)
        atomic.data = atomic
        meta = Metanode(atomic)
        for j in range(1, 10):
            new_atomic = AtomicNode(i + j)
            meta.insert_succ(atomic, new_atomic)
            atomic = new_atomic
        metas.append(meta)
    
    A, B, C = metas
    B.left = A
    B.right = C
    A.parent = B
    C.parent = B
    A.succ = B
    B.pred = A
    B.succ = C
    C.pred = B

    A._tail.next = B._head
    B._tail.next = C._head

    tree = RB_Tree()
    tree._root = B
    return tree


@test
def test_exact_search():
    tree = create_small_proper_tree()

    for v in [0, 1, 2, 9, 20, 21, 23, 40, 44, 49]:
        node = tree.exact_search(v)
        assert node != None
        assert node.value == v
    
    for v in [-1, 10, 19, 30, 39, 50]:
        node = tree.exact_search(v)
        assert node == None

@test
def test_predesessor():
    tree = create_small_proper_tree()

    # Hits exact
    for v in [1, 21, 23, 44]:
        node = tree.predesessor(v)
        assert node != None
        assert node.value == v
    
    # Hits nodes, but the pred
    for v, pred in [(1.5, 1), (9.5, 9), (21.5, 21), (39.5, 29), (60, 49)]:
        node = tree.predesessor(v)
        assert node != None
        assert node.value == pred

    # Is outside
    node = tree.predesessor(-1)
    assert node == None
        

@test
def test_successor():
    tree = create_small_proper_tree()

    # Hits exact
    for v in [1, 21, 23, 44]:
        node = tree.predesessor(v)
        assert node != None
        assert node.value == v
    
    # Hits nodes, but the succ
    for v, succ in [(1.5, 2), (2.5, 3), (9.5, 20), (21.5, 22), (39.5, 40), (42.5, 43)]:
        node = tree.successor(v)
        assert node != None
        assert node.value == succ
    
    # Is outside
    node = tree.successor(50)
    assert node == None

@test
def test_node_predesessor():
    tree = create_small_proper_tree()

    for v, pred in [(1, 0), (2, 1), (9, 8), (20, 9), (21, 20), (23, 22), (40, 29), (44, 43)]:
        node = tree.node_predesessor(tree.exact_search(v))
        assert node != None
        assert node == tree.exact_search(pred)

    assert tree.node_predesessor(tree.exact_search(0)) == None

@test
def test_node_successor():
    tree = create_small_proper_tree()

    for v, succ in [(0, 1), (1, 2), (8, 9), (9, 20), (20, 21), (22, 23), (29, 40), (43, 44)]:
        node = tree.node_successor(tree.exact_search(v))
        assert node != None
        assert node == tree.exact_search(succ)
    
    assert tree.node_successor(tree.exact_search(49)) == None

@test_group
def test_search():
    test_exact_search()
    test_predesessor()
    test_successor()
    test_node_predesessor()
    test_node_successor()


# ---------------------------------------------
#                  Insertion
# ---------------------------------------------

@test
def test_single_insertion():
    tree = RB_Tree()

    atomic_1 = tree.insert(1)
    meta = Metanode(atomic_1)

    assert tree._root == meta
    assert Metanode._is_head(atomic_1)
    assert tree.atomic_size() == 1
    assert tree.size() == 1

@test
def test_multiple_insertion_non_proper():
    tree = RB_Tree()

    values = [4, 5, 2, 1, 6, 3, 7]
    for v in values:
        print("Inserting:", v)
        tree.insert(v)
        tree.print()
        assert tree.exact_search(v) != None


    assert tree._root._is_proper == False
    assert tree.atomic_size() == len(values)
    assert tree.size() == 1

@test
def test_insert_pred():
    tree = RB_Tree()
    atomics = {}
    atomics[8] = tree.insert(8)

    for pred, value in [(3, 8), (2, 3), (5, 8), (4, 5), (1, 2)]:
        value_node = atomics[value]
        atomics[pred] = tree.insert_pred(value_node, pred)
        assert tree.exact_search(pred) == atomics[pred]
        assert tree.node_predesessor(value_node) == atomics[pred]

@test
def test_insert_pred_node():
    tree = RB_Tree()
    atomics = {}
    atomics[8] = tree.insert(8)

    for pred, value in [(3, 8), (2, 3), (5, 8), (4, 5), (1, 2)]:
        value_node = atomics[value]
        pred_node = AtomicNode(pred)
        atomics[pred] = pred_node
        res = tree._insert_pred_node(value_node, pred_node)
        assert res == None
        assert tree.exact_search(pred) == pred_node
        assert tree.node_predesessor(value_node) == pred_node

@test
def test_insert_succ():
    tree = RB_Tree()
    atomics = {}
    atomics[3] = tree.insert(3)

    for succ, value in [(8, 3), (9, 8), (5, 3), (6, 5), (10, 9)]:
        value_node = atomics[value]
        atomics[succ] = tree.insert_succ(value_node, succ)
        assert tree.exact_search(succ) == atomics[succ]
        assert tree.node_successor(value_node) == atomics[succ]

@test
def test_insert_succ_node():
    tree = RB_Tree()
    atomics = {}
    atomics[3] = tree.insert(3)

    for succ, value in [(8, 3), (9, 8), (5, 3), (6, 5), (10, 9)]:
        value_node = atomics[value]
        succ_node = AtomicNode(succ)
        atomics[succ] = succ_node
        res = tree._insert_succ_node(value_node, succ_node)
        assert res == None
        assert tree.exact_search(succ) == succ_node
        assert tree.node_successor(value_node) == succ_node

@test
def test_insertion_ignore_duplicates():
    tree = create_small_proper_tree()

    for v in [0, 2, 5, 6, 9, 20, 25, 42]:
        tree.insert(v)
        assert tree.exact_search(v) != None
        assert tree.atomic_size() == 30

@test
def test_insert_pred_ignore_duplicates():
    tree = create_small_proper_tree()

    for v, pred in [(3, 3), (8, 8), (21, 21), (42, 42), (0, 1), (3, 4), (20, 21), (44, 45)]:
        pred_node = tree.exact_search(pred)
        value_node = tree.exact_search(v)
        node_res = tree.insert_pred(pred_node, v)
        assert value_node == node_res
        assert tree.atomic_size() == 30

@test
def test_insert_succ_ignore_duplicates():
    tree = create_small_proper_tree()

    for v, succ in [(3, 3), (8, 8), (21, 21), (42, 42), (1, 0), (4, 3), (21, 20), (45, 44)]:
        succ_node = tree.exact_search(succ)
        value_node = tree.exact_search(v)
        node_res = tree.insert_succ(succ_node, v)
        assert value_node == node_res
        assert tree.atomic_size() == 30

@test_group
def test_insertion_no_splits():
    test_insert_pred()
    test_insert_pred_node()
    test_insert_succ()
    test_insert_succ_node()

    test_single_insertion()
    test_multiple_insertion_non_proper()

    test_insertion_ignore_duplicates()
    test_insert_pred_ignore_duplicates()
    test_insert_succ_ignore_duplicates()

@test
def test_multiple_insertion_proper_with_split():
    tree = RB_Tree()

    values = [11, 4, 9, 5, 2, 10, 14, 1, 8, 15, 6, 12, 13, 3, 16, 7]
    for v in values:
        tree.insert(v)
        assert tree.exact_search(v) != None

    assert tree._root._is_proper == True
    assert tree.atomic_size() == len(values)
    assert tree.size() == 2
    assert tree.is_valid()

@test
def test_insert_inorder():
    tree = RB_Tree()
    last = tree.insert(0)

    for i in range(1, 1000):
        last = tree.insert_succ(last, i)

    assert tree.is_valid()
    assert tree.atomic_size() == 1000

@test
def test_insert_random_order():
    for s in range(10):
        random.seed(s)
        values = list(range(1000))
        random.shuffle(values)
        
        tree = RB_Tree()
        for v in values:
            tree.insert(v)

        assert tree.is_valid()

@test_group
def test_insertion_with_splits():
    test_multiple_insertion_proper_with_split()
    test_insert_inorder()
    test_insert_random_order()

@test_group
def test_insertion():
    test_insertion_no_splits()
    test_insertion_with_splits()


# ---------------------------------------------
#                  Deletion
# ---------------------------------------------

@test
def test_simple_deletion():
    raise NotImplementedError()

@test
def test_delete_node():
    raise NotImplementedError()

@test
def test_delete_last():
    raise NotImplementedError()

@test_group
def test_deletion():
    test_simple_deletion()
    test_delete_node()
    test_delete_last()


# ---------------------------------------------
#               Finger Searching
# ---------------------------------------------

@test
def test_finger_search_same_metanode_exact():
    tree = create_small_proper_tree()

    for metanode in [tree._root, tree._root.left, tree._root.right]:
        for start_node in metanode:
            for end_node in metanode:
                found_node = tree.finger_search(start_node, end_node.value)
                assert found_node == end_node

@test
def test_finger_search_same_metanode_pred():
    tree = create_small_proper_tree()

    for metanode in [tree._root, tree._root.left, tree._root.right]:
        for start_node in metanode:
            for end_node in metanode:
                found_node = tree.finger_search(start_node, end_node.value + 0.5)
                assert found_node == end_node

@test
def test_finger_search_any_metanode_exact():
    tree = create_small_proper_tree()

    metanodes = [tree._root, tree._root.left, tree._root.right]
    nodes = [node for meta in metanodes for node in meta]

    for start_node in nodes:
        for end_node in nodes:
            found_node = tree.finger_search(start_node, end_node.value)
            assert found_node == end_node

@test
def test_finger_search_any_metanode_pred():
    tree = create_small_proper_tree()

    metanodes = [tree._root, tree._root.left, tree._root.right]
    nodes = [node for meta in metanodes for node in meta]

    for start_node in nodes:
        for end_node in nodes:
            found_node = tree.finger_search(start_node, end_node.value + 0.5)
            assert found_node == end_node

@test
def test_finger_search_any_metanode_edgecases():
    tree = create_small_proper_tree()

    node = tree.exact_search(0)
    found_node = tree.finger_search(node, -1)
    assert found_node == None

    node = tree.exact_search(45)
    found_node = tree.finger_search(node, -1)
    assert found_node == None

    node = tree.exact_search(7)
    found_node = tree.finger_search(node, 100)
    assert found_node != None
    assert found_node.value == 49

@test
def test_finger_search_larger_tree_exact():
    tree = RB_Tree()

    random.seed(0)
    values = list(range(1000))
    random.shuffle(values)

    for v in values:
        tree.insert(v)
    
    assert tree.is_valid()

    for start_value in random.sample(values, k=50):
        start_node = tree.exact_search(start_value)
        assert start_node != None
        assert start_node.value == start_value
        for end_value in random.sample(values, k=50):
            found_node = tree.finger_search(start_node, end_value)
            assert found_node.value == end_value

@test
def test_finger_search_larger_tree_pred():
    tree = RB_Tree()

    random.seed(42)
    values = list(range(1000))
    random.shuffle(values)

    for v in values:
        tree.insert(v)
    
    assert tree.is_valid()

    for start_value in random.sample(values, k=50):
        start_node = tree.exact_search(start_value)
        assert start_node != None
        assert start_node.value == start_value
        for end_value in random.sample(values, k=50):
            found_node = tree.finger_search(start_node, end_value + 0.5)
            assert found_node.value == end_value

@test_group
def test_finger_search():
    test_finger_search_same_metanode_exact()
    test_finger_search_same_metanode_pred()
    test_finger_search_any_metanode_exact()
    test_finger_search_any_metanode_pred()
    test_finger_search_any_metanode_edgecases()

    test_finger_search_larger_tree_exact()
    test_finger_search_larger_tree_pred()


# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_rotation()
    test_search()
    test_insertion()
    test_deletion()
    test_finger_search()

if __name__ == '__main__':
    test_all()
