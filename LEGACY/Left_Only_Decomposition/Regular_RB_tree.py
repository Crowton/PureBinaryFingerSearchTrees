import util


class Node:
    def __init__(self, key: int, parent=None, left=None, right=None, is_red=True) -> None:
        self._key = key
        self._parent = parent
        self._left = left
        self._right = right
        self._is_red_bool = is_red

    def _is_red(self):
        return self._is_red_bool
    
    def _is_black(self):
        return not self._is_red_bool
    
    def _set_red(self):
        self._is_red_bool = True
    
    def _set_black(self):
        self._is_red_bool = False


class RB_tree:
    def __init__(self) -> None:
        self._root = None
    
    # ------------------- Helper functions -------------------
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

    def size(self) -> int:
        def size_from(node: Node) -> int:
            if node == None:
                return 0
            return 1 + size_from(node._left) + size_from(node._right)
        
        return size_from(self._root)


    # ------------------- Search functions -------------------
    def contains(self, key: int) -> bool:
        return self.search(key) != None

    def search(self, key: int) -> bool:
        x = self._root
        while x != None:
            if key == x._key:
                return x
            elif key < x._key:
                x = x._left
            else:
                x = x._right
        return None


    # ------------------- Insertion functions -------------------
    def insert(self, key: int) -> None:
        new_node = Node(key)
        self._insert(new_node)
    
    def _insert(self, z: Node) -> None:
        x = self._root
        y = None
        while x != None:
            y = x
            if z._key == x._key:  # No duplicate keys allowed
                return
            if z._key < x._key:
                x = x._left
            else:
                x = x._right
        z._parent = y
        if y == None:
            self._root = z
        elif z._key < y._key:
            y._left = z
        else:
            y._right = z
        # z._left = None
        # z._right = None
        # z._set_red()
        self._insert_fixup(z)

    def _insert_predecessor(self, key: int, pred_key: int) -> None:
        z = Node(key)
        x = self._root
        y = None
        while x != None:
            y = x
            # Found pred location, splice z in here, and continue right with x
            if x._key == pred_key:
                z._parent = x._parent
                if x._parent == None:
                    self._root = z
                else:
                    if x._parent._left == x:
                        x._parent._left = z
                    else:
                        x._parent._right = z
                z._left = x._left
                if z._left != None:
                    z._left._parent = z
                z._right = x._right
                if z._right != None:
                    z._right._parent = z
                z._is_red_bool = x._is_red_bool
                
                x._parent = None
                x._left = None
                x._right = None
                x._set_red()
                
                x, z = z, x
            
            elif z._key < x._key:
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
        # z._left = None
        # z._right = None
        # z._set_red()
        self._insert_fixup(z)

    def _insert_fixup(self, z: Node) -> None:
        while z._parent != None and z._parent._is_red():
            if z._parent == z._parent._parent._left:
                y = z._parent._parent._right
                if y != None and y._is_red():
                    z._parent._set_black()
                    y._set_black()
                    z._parent._parent._set_red()
                    z = z._parent._parent
                else:
                    if z == z._parent._right:
                        z = z._parent
                        self._left_rotate(z)
                    z._parent._set_black()
                    z._parent._parent._set_red()
                    self._right_rotate(z._parent._parent)
            else:
                y = z._parent._parent._left
                if y != None and y._is_red():
                    z._parent._set_black()
                    y._set_black()
                    z._parent._parent._set_red()
                    z = z._parent._parent
                else:
                    if z == z._parent._left:
                        z = z._parent
                        self._right_rotate(z)
                    z._parent._set_black()
                    z._parent._parent._set_red()
                    self._left_rotate(z._parent._parent)
        self._root._set_black()


    # ------------------- Deletion functions -------------------
    def delete(self, key: int) -> None:
        z = self.search(key)
        if z == None:
            return
        
        self._delete(z)

    def _delete(self, z: Node) -> None:
        # z: node to delete
        # y: node to replace z with
        # x: node to fixup from
        
        # Potential dummy node is needed
        dummy = None

        # If right subtree is non-empty, then find the successor of z in z._right
        if z._right != None:
            y = self._minimum(z._right)
            y_original_black = y._is_black()
            assert y._left == None
            
            # If y is not a leaf, then pull up y._right to y's position
            if y._right != None:
                assert y._right._is_red()
                x = y._right
                y._right._parent = y._parent
                child = y._right
            
            # If a black leaf element is to be removed, then a dummy node is needed
            elif y._is_black():
                dummy = Node(None, parent=y._parent, is_red=False)  # Dummy node is needed
                x = dummy
                child = dummy
            
            # Else, y can be freely removed
            else:
                child = None

            # Free y
            if y._parent._left == y:
                y._parent._left = child
            else:
                y._parent._right = child
            y._parent = None
            y._right = None
        
        # If right subtree is empty, but the left is not, then the left is excactly the predecessor of z
        elif z._left != None:
            y = z._left
            y_original_black = y._is_black()
            x = y

            # Free y
            z._left = None
            y._parent = None
        
        # If both subtrees are empty, then z is a leaf. The parent is then either the successor or the predecessor of z
        elif z._parent != None:
            y = z
            y_original_black = y._is_black()
            if y_original_black:
                dummy = Node(None, parent=z._parent, is_red=False)  # Dummy node is needed
                x = dummy
            else:
                x = None

            # Remove parent link to z
            if z._parent._left == z:
                z._parent._left = x
            else:
                z._parent._right = x
            z._parent = None

        # The root is the only node in the tree
        else:
            self._root = None
            return

        # Replace z with y
        if z != y:
            y._parent = z._parent
            y._left = z._left
            y._right = z._right
            y._is_red_bool = z._is_red_bool
            if z._parent == None:
                self._root = y
            elif z._parent._left == z:
                z._parent._left = y
            else:
                z._parent._right = y
            if y._left != None:
                y._left._parent = y
            if y._right != None:
                y._right._parent = y

        # Run fixup from x if needed
        if y_original_black:
            self._delete_fixup(x, dummy)
    
    def _minimum(self, x: Node) -> Node:
        while x._left != None:
            x = x._left
        return x

    def _delete_fixup(self, x: Node, dummy: Node) -> None:
        while x != self._root and x._is_black():
            if x == x._parent._left:
                w = x._parent._right
                if w._is_red():
                    w._set_black()
                    x._parent._set_red()
                    self._left_rotate(x._parent)
                    w = x._parent._right
                if (w._left == None or w._left._is_black()) and (w._right == None or w._right._is_black()):
                    w._set_red()
                    x = x._parent
                else:
                    if (w._right == None or w._right._is_black()):
                        w._left._set_black()
                        w._set_red()
                        self._right_rotate(w)
                        w = x._parent._right
                    w._is_red_bool = x._parent._is_red()
                    x._parent._set_black()
                    w._right._set_black()
                    self._left_rotate(x._parent)
                    x = self._root
            else:
                w = x._parent._left
                if w._is_red():
                    w._set_black()
                    x._parent._set_red()
                    self._right_rotate(x._parent)
                    w = x._parent._left
                if (w._right == None or w._right._is_black()) and (w._left == None or w._left._is_black()):
                    w._set_red()
                    x = x._parent
                else:
                    if (w._left == None or w._left._is_black()):
                        w._right._set_black()
                        w._set_red()
                        self._left_rotate(w)
                        w = x._parent._left
                    w._is_red_bool = x._parent._is_red()
                    x._parent._set_black()
                    w._left._set_black()
                    self._right_rotate(x._parent)
                    x = self._root
        x._set_black()

        # Remove dummy node, as it was an acting nil element
        if dummy != None:
            assert dummy._is_black()
            assert dummy._parent != None
            assert dummy._left == None
            assert dummy._right == None

            if dummy._parent._left == dummy:
                dummy._parent._left = None
            else:
                dummy._parent._right = None


    # ------------------- Validation functions -------------------
    def is_valid_RB_tree(self, verbose=False) -> bool:
        if verbose:
            a = self._all_pointers_set()
            b = self._root_is_black()
            c = self._no_two_red()
            d = self._black_height() != -1
            e = self._is_sorted()
            print("All pointers are set:", a)
            print("Root is black:", b)
            print("No two red nodes are adjacent:", c)
            print("Black height is consistent:", d)
            print("Nodes are sorted:", e)
            return a and b and c and d and e

        return self._all_pointers_set() and \
               self._root_is_black() and \
               self._no_two_red() and \
               self._black_height() != -1 and \
               self._is_sorted()

    def _all_pointers_set(self) -> bool:
        return self._all_pointers_set_from(self._root)

    def _all_pointers_set_from(self, node: Node) -> bool:
        if node == None:
            return True
        if node._left != None and node._left._parent != node or node._right != None and node._right._parent != node:
            return False
        return self._all_pointers_set_from(node._left) and self._all_pointers_set_from(node._right)

    def _root_is_black(self) -> bool:
        return self._root == None or self._root._is_black()

    def _black_height(self) -> int:
        return self._black_height_from(self._root)

    def _black_height_from(self, node: Node) -> int:
        if node == None:
            return 0
        left_black_height = self._black_height_from(node._left)
        right_black_height = self._black_height_from(node._right)
        if left_black_height == -1 or right_black_height == -1 or left_black_height != right_black_height:
            return -1
        if node._is_black():
            return left_black_height + 1
        return left_black_height

    def _no_two_red(self) -> bool:
        return self._no_two_red_from(self._root)

    def _no_two_red_from(self, node: Node) -> bool:
        if node == None:
            return True
        if node._is_red() and node._parent._is_red():
            return False
        return self._no_two_red_from(node._left) and self._no_two_red_from(node._right)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: Node, lower_bound: float, upper_bound: float) -> bool:
            if node == None:
                return True
            if lower_bound < node._key < upper_bound:
                return node_within_bounds(node._left, lower_bound, node._key) and node_within_bounds(node._right, node._key, upper_bound)
            return False
        
        return node_within_bounds(self._root, float('-inf'), float('inf'))


    # ------------------- Conversion and print functions -------------------
    def to_tuple(self, data_formatter=lambda key, is_red: (key, "BR"[is_red])) -> tuple:
        def tuple_nodes(node):
            if node == None:
                return ()
            return (*data_formatter(node._key, node._is_red_bool), tuple_nodes(node._left), tuple_nodes(node._right))

        return tuple_nodes(self._root)
    
    @staticmethod
    def colored_node_data_formatter(key, is_red):
        return (("\u001b[31m" if is_red else "\u001b[37m") + str(key) + "\u001b[0m",)

    @staticmethod
    def uncolored_node_data_formatter(key, is_red):
        return (f"{key}({'BR'[is_red]})",)

    def str_block(self, colored=True) -> str:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        _, block = util.ascii_tree(self.to_tuple(formatter), str_len=util.visible_str_len)
        return block

    def print(self, colored=True) -> None:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        util.print_ascii_tree(self.to_tuple(formatter), str_len=util.visible_str_len)
