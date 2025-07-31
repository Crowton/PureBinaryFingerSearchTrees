from FT_Atomic_Node import AtomicNode
from FT_Three_Pointer_Atomic_Node import Three_Pointer_Atomic_Node
from FT_Metanode import Metanode
from util import link_left, link_right

from __test_decorators import test, test_group, test_file


# ---------------------------------------------
#              Tree creations
# ---------------------------------------------

def get_base_metanode_and_atomics():
    n1 = Three_Pointer_Atomic_Node(AtomicNode(1))
    n2 = Three_Pointer_Atomic_Node(AtomicNode(2))
    n3 = Three_Pointer_Atomic_Node(AtomicNode(3))
    n4 = Three_Pointer_Atomic_Node(AtomicNode(4))
    n5 = Three_Pointer_Atomic_Node(AtomicNode(5))
    n6 = Three_Pointer_Atomic_Node(AtomicNode(6))
    n7 = Three_Pointer_Atomic_Node(AtomicNode(7))
    n8 = Three_Pointer_Atomic_Node(AtomicNode(8))
    
    link_left(n2, n1)
    link_right(n2, n8)
    link_left(n8, n7)
    link_left(n7, n6)
    link_left(n6, n5)
    link_left(n5, n4)
    link_left(n4, n3)

    return Metanode(n2), n1, n2, n3, n4, n5, n6, n7, n8


# ---------------------------------------------
#     Test manipulation of non-proper node
# ---------------------------------------------

@test
def repeat_insert_pred_non_proper(verbose=False):
    root = Three_Pointer_Atomic_Node(AtomicNode(8))
    metanode = Metanode(root)
    at = root
    for i in range(1, 8)[::-1]:
        assert not metanode._is_proper
        new = Three_Pointer_Atomic_Node(AtomicNode(i))
        metanode.insert_pred(at, new)

        assert at.left == new
        assert new.parent == at
        assert new.left == None
        assert new.right == None

        at = new

        if verbose:
            print(f"After inserting {i}:")
            metanode.print()

    assert metanode._is_proper

@test
def repeat_insert_succ_non_proper(verbose=False):
    root = Three_Pointer_Atomic_Node(AtomicNode(1))
    metanode = Metanode(root)
    at = root
    for i in range(2, 9):
        assert not metanode._is_proper
        new = Three_Pointer_Atomic_Node(AtomicNode(i))
        metanode.insert_succ(at, new)

        assert at.parent == new
        assert new.left == at
        assert at.right == None
        assert at.right == None

        at = new

        if verbose:
            print(f"After inserting {i}:")
            metanode.print()
    
    assert metanode._is_proper

@test_group
def test_non_proper_insert():
    repeat_insert_pred_non_proper()
    repeat_insert_succ_non_proper()


# ---------------------------------------------
#      Tests on setting and getting bits
# ---------------------------------------------

@test
def test_set_red():
    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_red()

    assert metanode._root == n2
    assert n8.left == n6
    assert n6.right != None

@test
def test_set_black():
    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_black()

    assert metanode._root == n2
    assert n8.left == n7
    assert n7.right == None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_black()

    assert metanode._root == n2
    assert n8.left == n7
    assert n7.right == None

@test
def test_set_is_left_path():
    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_left_path()

    assert metanode._root == n2
    assert n6.left == n4
    assert n4.right != None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_left_path()

    assert metanode._root == n2
    assert n6.left == n4
    assert n4.right != None

@test
def test_set_is_right_path():
    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_right_path()

    assert metanode._root == n2
    assert n6.left == n5
    assert n5.right == None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_left_path()
    metanode.set_right_path()

    assert metanode._root == n2
    assert n6.left == n5
    assert n5.right == None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_right_path()

    assert metanode._root == n2
    assert n6.left == n5
    assert n5.right == None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    metanode.set_left_path()
    metanode.set_red()
    metanode.set_right_path()

    assert metanode._root == n2
    assert n6.left == n5
    assert n5.right == None

@test_group
def test_set_bits():
    test_set_red()
    test_set_black()
    test_set_is_left_path()
    test_set_is_right_path()

@test
def test_is_red():
    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_red()
    assert metanode.is_red

@test
def test_is_black():
    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_black()
    assert metanode.is_black

    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_black()
    assert metanode.is_black

@test
def test_is_left_path():
    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_left_path()
    assert metanode.is_left_path

    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_left_path()
    assert metanode.is_left_path

@test
def test_is_right_path():
    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_right_path()
    assert metanode.is_right_path

    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_left_path()
    metanode.set_right_path()
    assert metanode.is_right_path

    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_right_path()
    assert metanode.is_right_path

    metanode, *_ = get_base_metanode_and_atomics()
    metanode.set_red()
    metanode.set_left_path()
    metanode.set_right_path()
    assert metanode.is_right_path

@test_group
def test_get_bits():
    test_is_red()
    test_is_black()
    test_is_left_path()
    test_is_right_path()

@test_group
def test_bits():
    test_set_bits()
    test_get_bits()


# ---------------------------------------------
#    Test insert into proper without split
# ---------------------------------------------

@test
def test_insert_pred_into_base_proper_no_bits():
    # Inserting on left spine
    for n in [1, 2]:
        metanode, *ns = get_base_metanode_and_atomics()
        ns = [None] + ns
        new = Three_Pointer_Atomic_Node(AtomicNode(n - 0.5))
        metanode.insert_pred(ns[n], new)

        print(f"After inserting {new.value}:")
        metanode.print()

        assert ns[2].parent == ns[3]
        assert ns[2].left == None
        assert ns[2].right == None
    
    # Inserting into the bits or buffer
    for n in [8, 7, 6, 5, 4, 3]:
        metanode, *ns = get_base_metanode_and_atomics()
        ns = [None] + ns
        new = Three_Pointer_Atomic_Node(AtomicNode(n - 0.5))
        metanode.insert_pred(ns[n], new)

        print(f"After inserting {new.value}:")
        metanode.print()
        assert metanode._root == ns[2]
        assert new.parent == ns[n]
        assert new.left == (ns[n - 1] if n != 3 else None)

@test
def test_insert_succ_into_base_proper_no_bits():
    # Inserting on left spine
    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    new = Three_Pointer_Atomic_Node(AtomicNode(1.5))
    metanode.insert_succ(n1, new)
    assert n2.parent == n3
    assert n2.left == None
    assert n2.right == None

    metanode, n1, n2, n3, n4, n5, n6, n7, n8 = get_base_metanode_and_atomics()
    new = Three_Pointer_Atomic_Node(AtomicNode(2.5))
    metanode.insert_succ(n2, new)
    assert new.parent == n3
    assert new.left == None
    assert new.right == None
    
    # Inserting into the bits or buffer
    for n in [8, 7, 6, 5, 4, 3]:
        metanode, *ns = get_base_metanode_and_atomics()
        ns = [None] + ns
        new = Three_Pointer_Atomic_Node(AtomicNode(n + 0.5))
        metanode.insert_succ(ns[n], new)

        print(f"After inserting {new.value}:")
        metanode.print()
        assert metanode._root == ns[2]
        assert new.parent == (ns[n + 1] if n != 8 else ns[2])
        assert new.left == ns[n]

@test
def test_insert_pred_into_base_proper_set_bits():
    for set_red in [True, False]:
        for set_left_path in [True, False]:
            for i in range(8):
                metanode, *ns = get_base_metanode_and_atomics()
                if set_red:
                    metanode.set_red()
                if set_left_path:
                    metanode.set_left_path()
                new = Three_Pointer_Atomic_Node(AtomicNode("a"))
                metanode.insert_pred(ns[i], new)
                assert metanode.is_red == set_red
                assert metanode.is_left_path == set_left_path


@test_group
def test_insert_proper_no_split():
    test_insert_pred_into_base_proper_no_bits()
    test_insert_succ_into_base_proper_no_bits()
    test_insert_pred_into_base_proper_set_bits()

# ---------------------------------------------
#    Test insert into proper with split
# ---------------------------------------------

@test
def test_insert_with_split():
    metanode, *ns = get_base_metanode_and_atomics()
    metanode.set_red()
    at = ns[-1]
    for i in range(9, 16):
        new = Three_Pointer_Atomic_Node(AtomicNode(i))
        new_metanode = metanode.insert_succ(at, new)
        at = new

        assert new_metanode == None

    n16 = Three_Pointer_Atomic_Node(AtomicNode(16))
    new_metanode = metanode.insert_succ(at, n16)

    metanode.print()
    new_metanode.print()
    
    assert new_metanode != None
    assert new_metanode._root.value == 10
    assert metanode._root.value == 2


# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_non_proper_insert()
    test_bits()
    test_insert_proper_no_split()
    test_insert_with_split()

if __name__ == "__main__":
    test_all()
