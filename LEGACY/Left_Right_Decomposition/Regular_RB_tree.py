import util


class Node:
    def __init__(self, key: int) -> None:
        self._key = key
        self._parent = None
        self._left = None
        self._right = None
        self._is_red = True

    def is_red(self):
        return self._is_red
    
    def is_black(self):
        return not self._is_red
    
    def set_red(self):
        self._is_red = True
    
    def set_black(self):    
        self._is_red = False


class RB_tree:
    def __init__(self) -> None:
        self._root = None
    

    def _left_rotate(self, node: Node) -> None:
        y = node._right
        node._right = y._left
        if y._left != None:
            y._left._parent = node
        y._parent = node._parent
        if node._parent == None:
            self._root = y
        elif node == node._parent._left:
            node._parent._left = y
        else:
            node._parent._right = y
        y._left = node
        node._parent = y

    def _right_rotate(self, node: Node) -> None:
        y = node._left
        node._left = y._right
        if y._right != None:
            y._right._parent = node
        y._parent = node._parent
        if node._parent == None:
            self._root = y
        elif node == node._parent._right:
            node._parent._right = y
        else:
            node._parent._left = y
        y._right = node
        node._parent = y


    def search(self, key: int) -> bool:
        raise NotImplementedError("Search operation is not implemented in this snippet")


    def insert(self, key: int) -> None:
        new_node = Node(key)
        self._insert(new_node)
    
    def _insert(self, z: Node) -> None:
        x = self._root
        y = None
        while x != None:
            y = x
            if z._key < x._key:
                x = x._left
            else:
                x = x._right
        z._parent = y
        if y == None:
            self._root = z
        elif z._key == y._key:  # No duplicate keys allowed
            return
        elif z._key < y._key:
            y._left = z
        else:
            y._right = z
        z._left = None
        z._right = None
        z.set_red()
        self._insert_fixup(z)

    def _insert_fixup(self, z: Node) -> None:
        while z._parent != None and z._parent.is_red():
            if z._parent == z._parent._parent._left:
                y = z._parent._parent._right
                if y != None and y.is_red():
                    z._parent.set_black()
                    y.set_black()
                    z._parent._parent.set_red()
                    z = z._parent._parent
                else:
                    if z == z._parent._right:
                        z = z._parent
                        self._left_rotate(z)
                    z._parent.set_black()
                    z._parent._parent.set_red()
                    self._right_rotate(z._parent._parent)
            else:
                y = z._parent._parent._left
                if y != None and y.is_red():
                    z._parent.set_black()
                    y.set_black()
                    z._parent._parent.set_red()
                    z = z._parent._parent
                else:
                    if z == z._parent._left:
                        z = z._parent
                        self._right_rotate(z)
                    z._parent.set_black()
                    z._parent._parent.set_red()
                    self._left_rotate(z._parent._parent)
        self._root.set_black()
    
    def _insert_fixup_no_rotate(self, z: Node) -> None:
        while z._parent != None and z._parent.is_red():
            if z._parent == z._parent._parent._left:
                y = z._parent._parent._right
                if y != None and y.is_red():
                    z._parent.set_black()
                    y.set_black()
                    z._parent._parent.set_red()
                    z = z._parent._parent
                else:
                    break
            else:
                y = z._parent._parent._left
                if y != None and y.is_red():
                    z._parent.set_black()
                    y.set_black()
                    z._parent._parent.set_red()
                    z = z._parent._parent
                else:
                    break
        self._root.set_black()


    def delete(self, key: int) -> None:
        raise NotImplementedError("Delete operation is not implemented in this snippet")


    def is_valid_RB_tree(self, verbose=False) -> bool:
        if verbose:
            print("The tree is:", self.to_tuple())
            a = self._all_pointers_set(self._root)
            b = self._root_is_black()
            c = self._no_two_red(self._root)
            d = self._black_height(self._root) != -1
            e = self._is_sorted()
            print("All pointers are set:", a)
            print("Root is black:", b)
            print("No two red nodes are adjacent:", c)
            print("Black height is consistent:", d)
            print("Nodes are sorted:", e)
            return a and b and c and d and e

        return self._all_pointers_set(self._root) and \
               self._root_is_black() and \
               self._no_two_red(self._root) and \
               self._black_height(self._root) != -1 and \
               self._is_sorted()

    def _all_pointers_set(self, node: Node) -> bool:
        if node == None:
            return True
        if node._left != None and node._left._parent != node or node._right != None and node._right._parent != node:
            return False
        return self._all_pointers_set(node._left) and self._all_pointers_set(node._right)

    def _root_is_black(self) -> bool:
        return self._root.is_black()

    def _black_height(self, node: Node) -> int:
        if node == None:
            return 0
        left_black_height = self._black_height(node._left)
        right_black_height = self._black_height(node._right)
        if left_black_height == -1 or right_black_height == -1 or left_black_height != right_black_height:
            return -1
        if node.is_black():
            return left_black_height + 1
        return left_black_height

    def _no_two_red(self, node: Node) -> bool:
        if node == None:
            return True
        if node.is_red() and node._parent.is_red():
            return False
        return self._no_two_red(node._left) and self._no_two_red(node._right)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: Node, lower_bound: float, upper_bound: float) -> bool:
            if node == None:
                return True
            if lower_bound < node._key < upper_bound:
                return node_within_bounds(node._left, lower_bound, node._key) and node_within_bounds(node._right, node._key, upper_bound)
            return False
        
        return node_within_bounds(self._root, float('-inf'), float('inf'))


    def to_tuple(self, data_formatter=lambda key, is_red: (key, "BR"[is_red])) -> tuple:
        def tuple_nodes(node):
            if node == None:
                return ()
            return (*data_formatter(node._key, node._is_red), tuple_nodes(node._left), tuple_nodes(node._right))

        return tuple_nodes(self._root)


    # TODO: is this used?
    def _inorder_nodes(self, node):
        if node == None:
            return
        yield from self._inorder_nodes(node._left)
        yield node
        yield from self._inorder_nodes(node._right)

    def inorder_iter(self) -> iter:
        for node in self._inorder_nodes(self._root):
            yield node._key


    def print(self) -> None:
        util.print_ascii_tree(self.to_tuple(util.regular_colored_node_data_formatter), ignore_terminal_codes=True)
