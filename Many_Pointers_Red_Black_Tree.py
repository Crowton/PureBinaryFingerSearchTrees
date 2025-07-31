from __future__ import annotations

from Pointer_Counting import pointer_get, pointer_set, bit_get, bit_set

import Finger_Search
import util


class Red_Black_Node:
    def __init__(self, value, is_red: bool = True,
                 parent: Red_Black_Node = None, left: Red_Black_Node = None, right: Red_Black_Node = None,
                 pred: Red_Black_Node = None, succ: Red_Black_Node = None) -> None:
        self._value = value
        self._is_red = is_red
        self._parent = parent
        self._left = left
        self._right = right
        self._pred = pred
        self._succ = succ

    @property
    def value(self):
        return self._value

    @property
    def parent(self) -> Red_Black_Node:
        pointer_get()
        return self._parent
    
    @parent.setter
    def parent(self, parent: Red_Black_Node) -> None:
        pointer_set()
        self._parent = parent

    @property
    def left(self) -> Red_Black_Node:
        pointer_get()
        return self._left
    
    @left.setter
    def left(self, left: Red_Black_Node) -> None:
        pointer_set()
        self._left = left

    @property
    def right(self) -> Red_Black_Node:
        pointer_get()
        return self._right
    
    @right.setter
    def right(self, right: Red_Black_Node) -> None:
        pointer_set()
        self._right = right

    @property
    def pred(self) -> Red_Black_Node:
        pointer_get()
        return self._pred
    
    @pred.setter
    def pred(self, pred: Red_Black_Node) -> None:
        pointer_set()
        self._pred = pred
    
    @property
    def succ(self) -> Red_Black_Node:
        pointer_get()
        return self._succ
    
    @succ.setter
    def succ(self, succ: Red_Black_Node) -> None:
        pointer_set()
        self._succ = succ

    @property
    def is_red(self) -> bool:
        bit_get()
        return self._is_red
    
    @property
    def is_black(self) -> bool:
        bit_get()
        return not self._is_red

    def set_red(self) -> None:
        bit_set()
        self._is_red = True
    
    def set_black(self) -> None:
        bit_set()
        self._is_red = False

    
    def __repr__(self):
        return f"Node({self.value}, {'BR'[self.is_red]})"


class Red_Black_Tree:
    def __init__(self):
        self._root = None
    

    # ---------------------------------------------
    #                  Query
    # ---------------------------------------------

    def search(self, value) -> Red_Black_Node:
        current = self._root
        while current is not None:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def pred_search(self, value) -> Red_Black_Node:
        current = self._root
        pred = None
        while current is not None:
            if current.value <= value:
                pred = current
                current = current.right
            else:
                current = current.left
        return pred
    
    def succ_search(self, value) -> Red_Black_Node:
        current = self._root
        succ = None
        while current is not None:
            if current.value >= value:
                succ = current
                current = current.left
            else:
                current = current.right
        return succ

    def finger_search(self, node: Red_Black_Node, value, algorithm=Finger_Search.Version.PAPER) -> Red_Black_Node:
        return Finger_Search.finger_search(node, value, algorithm=algorithm)


    # ---------------------------------------------
    #                 Rotations
    # ---------------------------------------------

    def _rotate_left(self, node: Red_Black_Node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self._root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child
    
    def _rotate_right(self, node: Red_Black_Node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self._root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child


    # ---------------------------------------------
    #                  Update
    # ---------------------------------------------

    def insert(self, value):
        new_node = Red_Black_Node(value)
        self._insert(new_node)

    def _insert(self, node: Red_Black_Node):
        if self._root is None:
            self._root = node
            self._root.set_black()
            return

        current = self._root
        while True:
            if node.value < current.value:
                if current.left is None:
                    current.left = node
                    node.parent = current
                    self._insert_linked_list(node, current.pred, current)
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = node
                    node.parent = current
                    self._insert_linked_list(node, current, current.succ)
                    break
                else:
                    current = current.right

        node.set_red()

        # Fix the red-black tree properties after insertion
        self._fix_insert(node)

    def _insert_linked_list(self, node: Red_Black_Node, pred: Red_Black_Node, succ: Red_Black_Node):
        node.pred = pred
        node.succ = succ
        if pred is not None:
            pred.succ = node
        if succ is not None:
            succ.pred = node

    def _fix_insert(self, node: Red_Black_Node):
        while node != self._root and node.parent.is_red:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.is_red:
                    # Case 1: Uncle is red
                    node.parent.set_black()
                    uncle.set_black()
                    node.parent.parent.set_red()
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is right child
                        node = node.parent
                        self._rotate_left(node)
                    # Case 3: Node is left child
                    node.parent.set_black()
                    node.parent.parent.set_red()
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.is_red:
                    # Case 1: Uncle is red
                    node.parent.set_black()
                    uncle.set_black()
                    node.parent.parent.set_red()
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Case 2: Node is left child
                        node = node.parent
                        self._rotate_right(node)
                    # Case 3: Node is right child
                    node.parent.set_black()
                    node.parent.parent.set_red()
                    self._rotate_left(node.parent.parent)

        self._root.set_black()


    # ---------------------------------------------
    #                  Iterators
    # ---------------------------------------------

    def _smallest(self) -> Red_Black_Node:
        current = self._root
        while current.left is not None:
            current = current.left
        return current

    def __iter__(self):
        current = self._smallest()
        while current is not None:
            yield current
            current = current.succ

    # ---------------------------------------------
    #                Meta operations
    # ---------------------------------------------

    def __eq__(self, value):
        if not isinstance(value, Red_Black_Tree):
            return False
        return self._root == value._root
    
    def _to_tuple(self, data_formatter=None) -> tuple:
        def inner(node):
            if node == None:
                return ()
            return (*data_formatter(node.value, node.is_red), inner(node._left), inner(node._right))

        if data_formatter is None:
            data_formatter = self.uncolored_node_data_formatter
        return inner(self._root)
    
    @staticmethod
    def colored_node_data_formatter(key, is_red):
        return (("\u001b[31m" if is_red else "\u001b[37m") + str(key) + "\u001b[0m",)

    @staticmethod
    def uncolored_node_data_formatter(key, is_red):
        return (f"{key}({'BR'[is_red]})",)

    def str_block(self, colored=True) -> str:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        _, block = util.ascii_tree(self._to_tuple(formatter), str_len=util.visible_str_len)
        return block

    def print(self, colored=True) -> None:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        util.print_ascii_tree(self._to_tuple(formatter), str_len=util.visible_str_len)


    # ---------------------------------------------
    #                 Validation
    # ---------------------------------------------

    def is_valid(self, verbose=False) -> bool:
        a = self._all_pointers_set()
        b = self._root_is_black()
        c = self._no_two_red()
        d = self._black_height() != -1
        e = self._is_sorted()
        f = self._linked_list_is_valid()

        if verbose:
            print("All pointers are set:", a)
            print("Root is black:", b)
            print("No two red nodes are adjacent:", c)
            print("Black height is consistent:", d)
            print("Nodes are sorted:", e)
            print("Linked list is valid:", f)
        
        return a and b and c and d and e and f

    def _all_pointers_set(self) -> bool:
        return self._all_pointers_set_from(self._root)

    def _all_pointers_set_from(self, node: Red_Black_Node) -> bool:
        if node == None:
            return True
        if node.left != None and node.left.parent != node or node.right != None and node.right.parent != node:
            return False
        return self._all_pointers_set_from(node.left) and self._all_pointers_set_from(node.right)

    def _root_is_black(self) -> bool:
        return self._root == None or self._root.is_black

    def _black_height(self) -> int:
        return self._black_height_from(self._root)

    def _black_height_from(self, node: Red_Black_Node) -> int:
        if node == None:
            return 0
        left_black_height = self._black_height_from(node.left)
        right_black_height = self._black_height_from(node.right)
        if left_black_height == -1 or right_black_height == -1 or left_black_height != right_black_height:
            return -1
        if node.is_black:
            return left_black_height + 1
        return left_black_height

    def _no_two_red(self) -> bool:
        return self._no_two_red_from(self._root)

    def _no_two_red_from(self, node: Red_Black_Node) -> bool:
        if node == None:
            return True
        if node.is_red and node.parent.is_red:
            return False
        return self._no_two_red_from(node.left) and self._no_two_red_from(node.right)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: Red_Black_Node, lower_bound: float|None, upper_bound: float|None) -> bool:
            if node == None:
                return True
            if lower_bound != None and not lower_bound < node.value:
                return False
            if upper_bound != None and not node.value < upper_bound:
                return False
            
            return node_within_bounds(node.left, lower_bound, node.value) and node_within_bounds(node.right, node.value, upper_bound)
        
        return node_within_bounds(self._root, None, None)
    
    def _linked_list_is_valid(self) -> bool:
        return self._linked_list_is_valid_from(self._root)
    
    def _linked_list_is_valid_from(self, node: Red_Black_Node) -> bool:
        if node == None:
            return True
        if node.pred != None and node.pred.succ != node:
            return False
        if node.succ != None and node.succ.pred != node:
            return False
        return self._linked_list_is_valid_from(node.left) and self._linked_list_is_valid_from(node.right)




if __name__ == "__main__":
    from random import shuffle, seed
    # seed(42)
    seed(6)   # (6, 84, 88, 5, 105)
    keys = list(range(100))
    shuffle(keys)

    tree = Red_Black_Tree()
    for k in keys:
        tree.insert(k)
    
    print(tree.is_valid())
    tree.print(colored=False)

    # print(list(iter(tree)))

    # node_7 = tree.search(7)
    # print(node_7)
    # print(tree.finger_search(node_7, 35))

    # node_7 = tree.search(7)
    # print(node_7)
    # print(tree.finger_search(node_7, 35, algorithm=Finger_Search.Version.WHITEBOARD))

    # node_35 = tree.search(35)
    # print(node_35)
    # print(tree.finger_search(node_35, 7))

    # node_7 = tree.search(7)
    # print(node_7)
    # print(tree.finger_search(node_7, 58.03))
