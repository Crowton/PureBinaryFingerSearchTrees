from FT_Atomic_Node import AtomicNode

from __test_decorators import test, test_file


@test
def create_atomic_node():
    a = AtomicNode(42)
    assert a.left == None
    assert a.sibling_parent == None


@test_file
def test_all():
    create_atomic_node()

if __name__ == '__main__':
    test_all()
