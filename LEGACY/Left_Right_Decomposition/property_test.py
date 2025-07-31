from typing import Any
import util


class Node:
    def __init__(self, key: int) -> None:
        self._key = key
        self._parent = None
        self._left = None
        self._right = None


class Tree:
    def __init__(self) -> None:
        self._nil = None
        self._root = self._nil

    def node_property(node_function):
        setattr(Node, node_function.__name__.replace("_node", ""), lambda self: node_function(self))

    def set_root(self, key):
        self._root = Node(key)
        self._root._left = self._nil
        self._root._right = self._nil
        self._root._parent = self._nil
        return self._root

    def insert_left_of(self, node, key):
        node._left = Node(key)
        node._left._left = self._nil
        node._left._right = self._nil
        node._left._parent = node
        return node._left
    
    def insert_right_of(self, node, key):
        node._right = Node(key)
        node._right._left = self._nil
        node._right._right = self._nil
        node._right._parent = node
        return node._right


    @node_property
    def _node_get_left_left_of(node):
        return node._left._left

    @node_property
    def _node_get_right_right_of(node):
        return node._right._right

    def print(self):
        def tuple_node(node):
            if node == None:
                return ()
            return (node._key, tuple_node(node._left), tuple_node(node._right))
        util.print_ascii_tree(tuple_node(self._root))
        print()



if __name__ == "__main__":
    tree = Tree()
    root = tree.set_root(10)
    x = tree.insert_left_of(root, 6)
    x = tree.insert_left_of(x, 5)
    x = tree.insert_right_of(x, 7)
    x = tree.insert_right_of(x, 8)

    tree.print()
    
    print(Node.__dict__)

    y = root._get_left_left_of()._get_right_right_of()
    print(y._key)

    tree.insert_right_of(x._parent, 9)
    tree.print()

    print(root._get_left_left_of()._get_right_right_of()._key)
