from __test_decorators import test, test_group, test_file

from SLL_Atomic_Node import AtomicNode
from SLL_Metanode import Metanode


# ---------------------------------------------
#          Create simple metanodes
# ---------------------------------------------

def create_non_proper():
    a = AtomicNode(0)
    b = AtomicNode(1)
    c = AtomicNode(2)

    a.next = b
    b.next = c
    c.next = None

    a.data = a
    b.data = None
    c.data = a

    return Metanode(a)

def create_proper(buffer_elems=0, tail_is_last=True):
    assert 0 <= buffer_elems < 8

    # Create base
    head = AtomicNode(0)
    parent = AtomicNode(1)
    left = AtomicNode(2)
    right = AtomicNode(3)
    pred = AtomicNode(4)
    succ = AtomicNode(5)
    color = AtomicNode(6)
    tail = AtomicNode(7 + buffer_elems)

    # Create pointing to
    parent_node = AtomicNode("PARENT")
    left_node = AtomicNode("LEFT")
    right_node = AtomicNode("RIGHT")
    pred_node = AtomicNode("PRED")
    succ_node = AtomicNode("SUCC")
    tail_node = AtomicNode("TAIL")
    parent_node.data = parent_node
    left_node.data = left_node
    right_node.data = right_node
    pred_node.data = pred_node
    succ_node.data = succ_node
    tail_node.data = tail_node

    # Set next pointers
    head.next = parent
    parent.next = left
    left.next = right
    right.next = pred
    pred.next = succ
    succ.next = color
    at = color
    for i in range(7, 7 + buffer_elems):
        buff = AtomicNode(i)
        at.next = buff
        at = buff
    at.next = tail
    
    if not tail_is_last:
        tail.next = tail_node

    # Set data pointers
    head.data = head
    parent.data = parent_node
    left.data = left_node
    right.data = right_node
    pred.data = pred_node
    succ.data = succ_node
    tail.data = head

    # Return the atomics
    return {
        "head": head,
        "parent": parent,
        "left": left,
        "right": right,
        "pred": pred,
        "succ": succ,
        "color": color,
        "tail": tail,
        "parent_node": parent_node,
        "left_node": left_node,
        "right_node": right_node,
        "pred_node": pred_node,
        "succ_node": succ_node,
        "tail_node": tail_node
    }

def create_double_proper():
    atomics = [
        AtomicNode(i) for i in range(2 * 8)
    ]
    
    for i in range(2 * 8 - 1):
        atomics[i].next = atomics[i + 1]

    for i in [0, 8]:
        atomics[i].data = atomics[i]
        atomics[i + 7].data = atomics[i]

    atomics[5].data = atomics[8]
    atomics[8 + 4].data = atomics[0]

    return Metanode(atomics[0]), Metanode(atomics[8])


@test
def test_create_proper():
    atomics = create_proper()
    head = atomics["head"]
    metanode = Metanode(head)
    assert metanode._is_proper == True

    _head, _tail = metanode._get_head_and_tail()
    assert _head == head
    assert _tail == atomics["tail"]

    assert Metanode._is_head(atomics["parent_node"])
    assert Metanode._is_head(atomics["left_node"])
    assert Metanode._is_head(atomics["right_node"])
    assert Metanode._is_head(atomics["pred_node"])
    assert Metanode._is_head(atomics["succ_node"])
    assert Metanode._is_head(atomics["tail_node"])

    assert metanode.is_valid()

@test
def test_create_double_proper():
    A, B = create_double_proper()
    assert A._is_proper == True
    assert B._is_proper == True

    assert Metanode._is_head(A._head)
    assert Metanode._is_tail(A._tail)
    assert Metanode._is_head(B._head)
    assert Metanode._is_tail(B._tail)

    assert A.succ == B
    assert B.pred == A

    assert A._tail.next == B._head

    assert A.is_valid()
    assert B.is_valid()

@test_group
def test_create():
    test_create_proper()
    test_create_double_proper()


# ---------------------------------------------
#              Non proper behavior
# ---------------------------------------------

@test
def test_single_node():
    head = AtomicNode(0)
    head.data = head

    metanode = Metanode(head)
    assert metanode._is_proper == False
    _head, _tail = metanode._get_head_and_tail()
    assert _head == head
    assert _tail == head

    assert metanode.is_valid()

@test
def test_three_nodes():
    a, b, c = [AtomicNode(i) for i in range(3)]
    a.next = b
    b.next = c
    a.data = a
    c.data = a

    metanode = Metanode(a)
    assert metanode._is_proper == False
    _head, _tail = metanode._get_head_and_tail()
    assert _head == a
    assert _tail == c

    assert metanode.is_valid()

@test_group
def test_non_proper():
    test_single_node()
    test_three_nodes()


# ---------------------------------------------
#             Pointers and bits
# ---------------------------------------------

@test
def test_get_parent():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.parent._head == atomics["parent_node"]

    non_proper = create_non_proper()
    assert non_proper.parent == None

@test
def test_get_left():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.left._head == atomics["left_node"]

    non_proper = create_non_proper()
    assert non_proper.left == None

@test
def test_get_right():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.right._head == atomics["right_node"]

    non_proper = create_non_proper()
    assert non_proper.right == None

@test
def test_get_pred():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.pred._head == atomics["pred_node"]

    non_proper = create_non_proper()
    assert non_proper.pred == None

@test
def test_get_succ():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.succ._head == atomics["succ_node"]

    non_proper = create_non_proper()
    assert non_proper.succ == None

@test_group
def test_get_pointers():
    test_get_parent()
    test_get_left()
    test_get_right()
    test_get_pred()
    test_get_succ()

@test
def test_set_parent():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    new_node = AtomicNode("NEW_PARENT")
    new_node.data = new_node
    new_metanode = Metanode(new_node)

    metanode.parent = new_metanode
    assert metanode.parent == new_metanode

    metanode.parent = None
    assert metanode.parent == None

@test
def test_set_left():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    new_node = AtomicNode("NEW_LEFT")
    new_node.data = new_node
    new_metanode = Metanode(new_node)

    metanode.left = new_metanode
    assert metanode.left == new_metanode

    metanode.left = None
    assert metanode.left == None

@test
def test_set_right():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    new_node = AtomicNode("NEW_RIGHT")
    new_node.data = new_node
    new_metanode = Metanode(new_node)

    metanode.right = new_metanode
    assert metanode.right == new_metanode

    metanode.right = None
    assert metanode.right == None

@test
def test_set_pred():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    new_node = AtomicNode("NEW_PRED")
    new_node.data = new_node
    new_metanode = Metanode(new_node)

    metanode.pred = new_metanode
    assert metanode.pred == new_metanode

    metanode.pred = None
    assert metanode.pred == None

@test
def test_set_succ():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    new_node = AtomicNode("NEW_SUCC")
    new_node.data = new_node
    new_metanode = Metanode(new_node)

    metanode.succ = new_metanode
    assert metanode.succ == new_metanode

    metanode.succ = None
    assert metanode.succ == None

@test_group
def test_set_pointers():
    test_set_parent(verbose=True, raise_error=True)
    test_set_left()
    test_set_right()
    test_set_pred()
    test_set_succ()

@test
def test_get_color():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.is_red == False
    assert metanode.is_black == True

@test
def test_set_color():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])

    metanode.set_black()
    metanode.set_red()
    assert metanode.is_red == True
    assert metanode.is_black == False

    metanode.set_black()
    assert metanode.is_red == False
    assert metanode.is_black == True

@test_group
def test_get_and_set_pointers_and_bit():
    test_get_pointers()
    test_set_pointers()
    test_get_color()
    test_set_color()


# ---------------------------------------------
#                  Search
# ---------------------------------------------

@test
def test_smallest():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.smallest_atomic() == atomics["head"]

@test
def test_must_contain():
    metanode = Metanode(create_proper(tail_is_last=True)["head"])
    assert metanode.must_contain(-1) == False
    assert metanode.must_contain(0) == True
    assert metanode.must_contain(1) == True
    assert metanode.must_contain(7) == True
    assert metanode.must_contain(9) == True

    atomics = create_proper(tail_is_last=False)
    tail = atomics["tail"]
    new_tail = AtomicNode(8)
    new_tail.data = new_tail
    tail.next = new_tail
    metanode = Metanode(atomics["head"])
    assert metanode.must_contain(8) == False

@test
def test_contains():
    metanode = Metanode(create_proper()["head"])
    assert metanode.contains(-1) == False
    assert metanode.contains(0) == True
    assert metanode.contains(1) == True
    assert metanode.contains(7) == True
    assert metanode.contains(8) == False

@test
def test_exact_search():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])
    assert metanode.exact_search(0) == atomics["head"]
    assert metanode.exact_search(1) == atomics["parent"]
    assert metanode.exact_search(2) == atomics["left"]
    assert metanode.exact_search(3) == atomics["right"]
    assert metanode.exact_search(4) == atomics["pred"]
    assert metanode.exact_search(5) == atomics["succ"]
    assert metanode.exact_search(6) == atomics["color"]
    assert metanode.exact_search(7) == atomics["tail"]
    assert metanode.exact_search(-1) == None
    assert metanode.exact_search(8) == None

@test
def test_predessor_search():
    atomics = create_proper(tail_is_last=True)
    metanode = Metanode(atomics["head"])
    assert metanode.predesessor_search(2) == atomics["left"]
    assert metanode.predesessor_search(2.5) == atomics["left"]
    assert metanode.predesessor_search(2.999) == atomics["left"]
    assert metanode.predesessor_search(3) == atomics["right"]
    assert metanode.predesessor_search(-1) == None
    assert metanode.predesessor_search(42) == atomics["tail"]

    # Only search within node
    atomics = create_proper(tail_is_last=False)
    metanode = Metanode(atomics["head"])
    new_tail = AtomicNode(8)
    new_tail.data = new_tail
    atomics["tail"].next = new_tail
    assert metanode.predesessor_search(42) == None

@test
def test_successor_search():
    assert False

@test
def test_node_predesessor():
    A, B = create_double_proper()

    assert A.node_predesessor(A._head) == None
    assert A.node_predesessor(A._head.next) == A._head
    assert A.node_predesessor(A._head.next.next) == A._head.next

    assert B.node_predesessor(B._head) == A._tail
    assert B.node_predesessor(B._head.next) == B._head
    assert B.node_predesessor(B._head.next.next) == B._head.next

@test
def test_node_successor():
    A, B = create_double_proper()

    assert A.node_successor(A._head) == A._head.next
    assert A.node_successor(A._head.next) == A._head.next.next
    assert A.node_successor(A._tail) == B._head

    assert B.node_successor(B._head) == B._head.next
    assert B.node_successor(B._head.next) == B._head.next.next
    assert B.node_successor(B._tail) == None

@test_group
def test_search():
    test_smallest()
    test_must_contain()
    test_contains()
    test_exact_search()
    test_predessor_search()
    test_successor_search()
    test_node_predesessor()
    test_node_successor()


# ---------------------------------------------
#                 Insertion
# ---------------------------------------------

@test
def test_insert_pred_non_proper():
    head = AtomicNode(0)
    head.data = head
    metanode = Metanode(head)

    new_head = AtomicNode(-1)
    update_head, spill_out = metanode.insert_pred(head, new_head)

    assert update_head == True
    assert spill_out == None

    assert metanode._head == new_head
    assert Metanode._is_head(new_head)
    assert new_head.next == head
    assert Metanode._is_tail(head)
    assert metanode._tail.data == new_head

    new_node = AtomicNode(-0.5)
    update_head, spill_out = metanode.insert_pred(head, new_node)

    assert update_head == False
    assert spill_out == None

    assert Metanode._is_head(new_head)
    assert new_head.next == new_node
    assert new_node.next == head
    assert Metanode._is_tail(head)

    new_new_head = AtomicNode(-2)
    update_head, spill_out = metanode.insert_pred(new_head, new_new_head)

    assert update_head == True
    assert spill_out == None

    assert metanode._head == new_new_head
    assert Metanode._is_head(new_new_head)
    assert new_new_head.next == new_head
    assert metanode._tail.data == new_new_head

    assert metanode.is_valid()

@test
def test_insert_pred_proper_no_split():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])

    new_node = AtomicNode(3.4)
    metanode.insert_pred(atomics["pred"], new_node)

    assert atomics["right"].next == new_node
    assert new_node.next == atomics["pred"]

    assert metanode.pred == Metanode(atomics["pred_node"])
    assert metanode.succ == Metanode(atomics["succ_node"])

    assert metanode._head == atomics["head"]
    assert metanode._tail == atomics["tail"]
    assert metanode._tail.next == None
    assert metanode.size() == 9

    assert metanode.is_valid()

    
    for i in range(0, 11):
        atomics = create_proper(buffer_elems=3)
        metanode = Metanode(atomics["head"])
        metanode.set_red()

        node = metanode.exact_search(i)
        new_node = AtomicNode(i - 0.5)
        metanode.insert_pred(node, new_node)

        assert metanode.is_valid()


@test
def test_insert_pred_proper_split():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    a = AtomicNode(3.1)
    b = AtomicNode(3.2)
    c = AtomicNode(3.3)
    d = AtomicNode(3.4)
    e = AtomicNode(3.5)

    updates, res = metanode.insert_pred(atomics["pred"], e)
    assert updates == False
    assert res == None
    updates, res = metanode.insert_pred(e, d)
    assert updates == False
    assert res == None
    updates, res = metanode.insert_pred(d, c)
    assert updates == False
    assert res == None
    updates, res = metanode.insert_pred(c, b)
    assert updates == False
    assert res == None
    
    updates, res = metanode.insert_pred(b, a)

    assert res != None
    assert metanode._head == atomics["head"]
    assert metanode._tail == d
    assert metanode._tail.next == e
    assert res._head == e
    assert res._tail == atomics["tail"]
    assert res._tail.next == None

    assert metanode.is_valid()
    assert res.is_valid()


@test
def test_insert_succ_non_proper():
    head = AtomicNode(0)
    head.data = head
    metanode = Metanode(head)

    new_tail = AtomicNode(20)
    metanode.insert_succ(head, new_tail)

    assert Metanode._is_head(head)
    assert Metanode._is_tail(new_tail)

    assert head.next == new_tail
    assert new_tail.next == None
    assert new_tail.data == head

    new_node = AtomicNode(5)
    metanode.insert_succ(head, new_node)

    assert head.next == new_node
    assert new_node.next == new_tail
    assert new_node.data == None
    assert new_tail.next == None

    assert metanode.is_valid()

@test
def test_insert_succ_proper_no_split():
    atomics = create_proper()
    metanode = Metanode(atomics["head"])

    new_node = AtomicNode(3.4)
    metanode.insert_succ(atomics["right"], new_node)

    assert atomics["right"].next == new_node
    assert new_node.next == atomics["pred"]

    assert metanode.pred == Metanode(atomics["pred_node"])
    assert metanode.succ == Metanode(atomics["succ_node"])

    assert metanode._tail == atomics["tail"]
    assert metanode._tail.next == None
    assert metanode.size() == 9

    assert metanode.is_valid()


    for i in range(0, 11):
        atomics = create_proper(buffer_elems=3)
        metanode = Metanode(atomics["head"])
        metanode.set_red()
        
        node = metanode.exact_search(i)
        new_node = AtomicNode(i + 0.5)
        metanode.insert_succ(node, new_node)

        assert metanode.is_valid()

@test
def test_insert_succ_proper_split():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    a = AtomicNode(3.1)
    b = AtomicNode(3.2)
    c = AtomicNode(3.3)
    d = AtomicNode(3.4)
    e = AtomicNode(3.5)

    res = metanode.insert_succ(atomics["right"], a)
    assert res == None
    res = metanode.insert_succ(a, b)
    assert res == None
    res = metanode.insert_succ(b, c)
    assert res == None
    res = metanode.insert_succ(c, d)
    assert res == None
    
    res = metanode.insert_succ(d, e)

    assert res != None
    assert metanode._head == atomics["head"]
    assert metanode._tail == d
    assert metanode._tail.next == e
    assert res._head == e
    assert res._tail == atomics["tail"]
    assert res._tail.next == None

    assert metanode.is_valid()
    assert res.is_valid()

    assert metanode._is_proper
    assert res._is_proper

def create_almost_proper_metanode():
    head = AtomicNode(0)
    head.data = head
    metanode = Metanode(head)

    for i in range(1, 7)[::-1]:
        node = AtomicNode(i)
        metanode.insert_succ(head, node)

    assert metanode._is_proper == False

    return metanode

@test
def test_insert_pred_update_proper_and_head():
    meta = create_almost_proper_metanode()
    new_node_head = AtomicNode(-1)
    updates, res = meta.insert_pred(meta._head, new_node_head)
    assert updates == True
    assert res == None
    assert meta._is_proper == True
    assert meta._head == new_node_head

    meta = create_almost_proper_metanode()
    new_node_mid = AtomicNode(3.5)
    old_head = meta._head
    mid_node = meta._head.next.next.next.next
    assert mid_node.value == 4
    updates, res = meta.insert_pred(mid_node, new_node_mid)
    assert updates == False
    assert res == None
    assert meta._is_proper == True
    assert meta._head == old_head

@test
def test_insert_succ_update_proper_and_head():
    meta = create_almost_proper_metanode()
    new_node_mid = AtomicNode(3.5)
    old_head = meta._head
    old_tail = meta._tail
    mid_node = meta._head.next.next.next
    assert mid_node.value == 3
    res = meta.insert_succ(mid_node, new_node_mid)
    assert res == None
    assert meta._is_proper == True
    assert meta._head == old_head
    assert meta._tail == old_tail

    meta = create_almost_proper_metanode()
    new_node_tail = AtomicNode(7)
    old_head = meta._head
    res = meta.insert_succ(meta._tail, new_node_tail)
    assert res == None
    assert meta._is_proper == True
    assert meta._head == old_head
    assert meta._tail == new_node_tail

@test_group
def test_insert():
    test_insert_pred_non_proper()
    test_insert_pred_proper_no_split()
    test_insert_pred_proper_split()
    test_insert_succ_non_proper()
    test_insert_succ_proper_no_split()
    test_insert_succ_proper_split()

    test_insert_pred_update_proper_and_head()
    test_insert_succ_update_proper_and_head()


# ---------------------------------------------
#              Test value wrapper
# ---------------------------------------------

@test
def test_value_values():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])
    
    val = metanode.value
    assert val._min == 0
    assert val._max == 10

@test
def test_value_lt():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value < 20
    assert not metanode.value < 5

@test
def test_value_le():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value <= 20
    assert metanode.value <= 5
    assert metanode.value <= 0
    assert not metanode.value <= -1

@test
def test_value_gt():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value > -1
    assert not metanode.value > 5

@test
def test_value_ge():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value >= -1
    assert metanode.value >= 0
    assert metanode.value >= 5
    assert metanode.value >= 10
    assert not metanode.value >= 11

@test
def test_value_eq():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value == 0
    assert metanode.value == 5
    assert metanode.value == 10

@test
def test_value_ne():
    atomics = create_proper(buffer_elems=3)
    metanode = Metanode(atomics["head"])

    assert metanode.value != -1
    assert metanode.value != 11

@test_group
def test_value_wrapper():
    test_value_values()
    test_value_lt()
    test_value_le()
    test_value_gt()
    test_value_ge()
    test_value_eq()
    test_value_ne()

# ---------------------------------------------
#              Test valid function
# ---------------------------------------------

@test
def test_valid_double_head_cuts():
    a = AtomicNode(0)
    b = AtomicNode(1)
    c = AtomicNode(2)

    a.next = b
    b.next = c
    c.next = None

    a.data = a
    b.data = b
    c.data = a

    metanode_a = Metanode(a)
    assert metanode_a.is_valid()
    assert metanode_a.size() == 1

    metanode_b = Metanode(b)
    assert not metanode_b.is_valid()
    assert metanode_b.size() == 2

@test_group
def test_valid():
    test_valid_double_head_cuts()

# ---------------------------------------------
#                   Main
# ---------------------------------------------

@test_file
def test_all():
    test_create()
    test_non_proper()
    test_get_and_set_pointers_and_bit()
    test_search()
    test_insert()
    test_valid()
    test_value_wrapper()

if __name__ == "__main__":
    test_all()
