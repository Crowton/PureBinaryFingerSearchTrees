from FT_Three_Pointer_Atomic_Node import Three_Pointer_Atomic_Node
from FT_Atomic_Node import AtomicNode
from util import link_left, link_right

from __test_decorators import test, test_group, test_file



# ---------------------------------------------
#        Tree creations and helpers
# ---------------------------------------------

def print_tree_3(a):
    from FT_Metanode import Metanode
    Metanode(a).print(print_all=True)

def get_small_atomic_tree():
    # Returns
    #     a
    #    /
    #   b
    #  / \
    # c - d

    a = AtomicNode("a")
    b = AtomicNode("b")
    c = AtomicNode("c")
    d = AtomicNode("d")

    a.left = b
    b.left = c
    b.sibling_parent = a
    c.sibling_parent = d
    d.sibling_parent = b

    return a, b, c, d

def get_small_atomic_tree_3():
    a, b, c, d = get_small_atomic_tree()

    a3 = Three_Pointer_Atomic_Node(a)
    b3 = Three_Pointer_Atomic_Node(b)
    c3 = Three_Pointer_Atomic_Node(c)
    d3 = Three_Pointer_Atomic_Node(d)

    return a3, b3, c3, d3


# ---------------------------------------------
#             Test small trees
# ---------------------------------------------

@test
def test_singleton():
    node = AtomicNode(42)
    atomic_3 = Three_Pointer_Atomic_Node(node)
    assert atomic_3.parent == None
    assert atomic_3.left == None
    assert atomic_3.right == None

@test
def test_parent():
    a, b, c, d = get_small_atomic_tree_3()

    assert a.parent == None
    assert b.parent == a
    assert c.parent == b
    assert d.parent == b

@test
def test_left():
    a, b, c, d = get_small_atomic_tree_3()

    assert a.left == b
    assert b.left == c
    assert c.left == None
    assert d.left == None

@test
def test_right():
    a, b, c, d = get_small_atomic_tree_3()

    assert a.right == None
    assert b.right == d
    assert c.right == None
    assert d.right == None

@test
def test_setting_pointers_simple_left_right():
    n1 = Three_Pointer_Atomic_Node(AtomicNode(1))
    n2 = Three_Pointer_Atomic_Node(AtomicNode(2))
    n3 = Three_Pointer_Atomic_Node(AtomicNode(3))

    link_left(n2, n1)
    link_right(n2, n3)

    assert n1.parent == n2
    assert n1.left == None
    assert n1.right == None
    assert n2.parent == None
    assert n2.left == n1
    assert n2.right == n3
    assert n3.parent == n2
    assert n3.left == None
    assert n3.right == None

@test
def test_setting_pointers_paper_example():
    a = Three_Pointer_Atomic_Node(AtomicNode("a"))
    b = Three_Pointer_Atomic_Node(AtomicNode("b"))
    c = Three_Pointer_Atomic_Node(AtomicNode("c"))
    d = Three_Pointer_Atomic_Node(AtomicNode("d"))

    # TODO: update to link_left/right?
    a.left = b
    b.parent = a
    b.left = c
    c.parent = b
    b.right = d
    d.parent = b

    assert a.parent == None
    assert a.left == b
    assert a.right == None
    assert b.parent == a
    assert b.left == c
    assert b.right == d
    assert c.parent == b
    assert c.left == None
    assert c.right == None
    assert d.parent == b
    assert d.left == None
    assert d.right == None

@test_group
def test_small():
    test_singleton()
    test_parent()
    test_left()
    test_right()
    test_setting_pointers_simple_left_right()
    test_setting_pointers_paper_example()


# ---------------------------------------------
#              Test rotations
# ---------------------------------------------

@test
def test_rotate_left(verbose=False):
    #     p                p
    #     |                |
    #     u                v
    #    / \      -->     / \
    #   a   v            u   c
    #      / \          / \
    #     b   c        a   b

    # s is sibling of u

    for p_val in ("p", None):
        for s_val in (("s", None) if p_val != None else (None,)):
            for u_is_left in ((True, False) if s_val != None else (True,)):
                for b_val in ("b", None):
                    for c_val in (("c", None) if b_val != None else (None,)):
                        p = Three_Pointer_Atomic_Node(AtomicNode(p_val)) if p_val is not None else None
                        s = Three_Pointer_Atomic_Node(AtomicNode(s_val)) if s_val is not None else None
                        u = Three_Pointer_Atomic_Node(AtomicNode("u"))
                        v = Three_Pointer_Atomic_Node(AtomicNode("v"))
                        a = Three_Pointer_Atomic_Node(AtomicNode("a"))
                        b = Three_Pointer_Atomic_Node(AtomicNode(b_val)) if b_val is not None else None
                        c = Three_Pointer_Atomic_Node(AtomicNode(c_val)) if c_val is not None else None

                        if s is None:
                            link_left(p, u)
                        elif u_is_left:
                            link_left(p, u)
                            link_right(p, s)
                        else:
                            link_left(p, s)
                            link_right(p, u)
                        link_left(u, a)
                        link_right(u, v)
                        link_left(v, b)
                        link_right(v, c)
                        
                        if verbose:
                            print("Before:")
                            print_tree_3(p if p is not None else u)

                        u.rotate_left()

                        if verbose:
                            print("Before:")
                            print_tree_3(p if p is not None else v)

                        if p is not None:
                            assert p.parent == None
                            if s is None:
                                assert p.left == v
                                assert p.right == None
                            elif u_is_left:
                                assert p.left == v
                                assert p.right == s
                            else:
                                assert p.left == s
                                assert p.right == v
                        
                        if s is not None:
                            assert s.parent == p
                            assert s.left == None
                            assert s.right == None
                        
                        assert v.parent == p
                        assert v.left == u
                        assert v.right == c

                        assert u.parent == v
                        assert u.left == a
                        assert u.right == b

                        assert a.parent == u
                        assert a.left == None
                        assert a.right == None

                        if b is not None:
                            assert b.parent == u
                            assert b.left == None
                            assert b.right == None

                        if c is not None:
                            assert c.parent == v
                            assert c.left == None
                            assert c.right == None

@test
def test_rotate_right(verbose=False):
    #       p              p
    #       |              |
    #       v              u
    #      / \     -->    / \
    #     u   c          a   v
    #    / \                / \
    #   a   b              b   c

    # s is sibling of v

    for p_val in ("p", None):
        for s_val in (("s", None) if p_val != None else (None,)):
            for v_is_left in ((True, False) if s_val != None else (True,)):
                for b_val in ("b", None):
                    for c_val in (("c", None) if b_val != None else (None,)):
                        p = Three_Pointer_Atomic_Node(AtomicNode(p_val)) if p_val is not None else None
                        s = Three_Pointer_Atomic_Node(AtomicNode(s_val)) if s_val is not None else None
                        u = Three_Pointer_Atomic_Node(AtomicNode("u"))
                        v = Three_Pointer_Atomic_Node(AtomicNode("v"))
                        a = Three_Pointer_Atomic_Node(AtomicNode("a"))
                        b = Three_Pointer_Atomic_Node(AtomicNode(b_val)) if b_val is not None else None
                        c = Three_Pointer_Atomic_Node(AtomicNode(c_val)) if c_val is not None else None

                        link_left(v, u)
                        link_right(v, c)
                        link_left(u, a)
                        link_right(u, b)
                        if s is None:
                            link_left(p, v)
                        elif v_is_left:
                            link_left(p, v)
                            link_right(p, s)
                        else:
                            link_left(p, s)
                            link_right(p, v)

                        if verbose:
                            print("Before:")
                            print_tree_3(p if p is not None else v)

                        v.rotate_right()

                        if verbose:
                            print("After:")
                            print_tree_3(p if p is not None else u)

                        if p is not None:
                            assert p.parent == None
                            if s is None:
                                assert p.left == u
                                assert p.right == None
                            elif v_is_left:
                                assert p.left == u
                                assert p.right == s
                            else:
                                assert p.left == s
                                assert p.right == u
                        
                        if s is not None:
                            assert s.parent == p
                            assert s.left == None
                            assert s.right == None

                        assert u.parent == p
                        assert u.left == a
                        assert u.right == v

                        assert v.parent == u
                        assert v.left == b
                        assert v.right == c

                        assert a.parent == u
                        assert a.left == None
                        assert a.right == None
                        
                        if b is not None:
                            assert b.parent == v
                            assert b.left == None
                            assert b.right == None
                        
                        if c is not None:
                            assert c.parent == v
                            assert c.left == None
                            assert c.right == None

@test
def test_rotate_right_negative():
    #      v
    #     / \
    #    u   c
    #   / \
    #  *   *

    v = Three_Pointer_Atomic_Node(AtomicNode("v"))
    u = Three_Pointer_Atomic_Node(AtomicNode("u"))
    c = Three_Pointer_Atomic_Node(AtomicNode("c"))

    link_left(v, u)
    link_right(v, c)

    try:
        v.rotate_right()
        assert False
    except ValueError:
        pass


    #      v
    #     / \
    #    u   c
    #   / \
    #  a   *

    v = Three_Pointer_Atomic_Node(AtomicNode("v"))
    u = Three_Pointer_Atomic_Node(AtomicNode("u"))
    a = Three_Pointer_Atomic_Node(AtomicNode("a"))
    c = Three_Pointer_Atomic_Node(AtomicNode("c"))

    link_left(v, u)
    link_right(v, c)
    link_left(u, a)

    try:
        v.rotate_right()
        assert False
    except ValueError:
        pass

@test_group
def test_rotations():
    test_rotate_left()
    test_rotate_right()
    test_rotate_right_negative()


# ---------------------------------------------
#                  Main
# ---------------------------------------------

@test_file
def test_all():
    test_small()
    test_rotations()


if __name__ == "__main__":
    test_all()
