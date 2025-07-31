import util
from enum import Enum
from typing import NewType
from math import log2


class ZigZag_Node:
    def __init__(self, key, parent=None, left=None, right=None, is_red=True, is_path_root=False) -> None:
        self._key = key
        self._parent = parent
        self._left = left
        self._right = right
        self._is_red_bool = is_red
        self._is_path_root_bool = is_path_root
    
    def _is_red(self):
        return self._is_red_bool
    
    def _is_black(self):
        return not self._is_red_bool
    
    def _set_red(self):
        self._is_red_bool = True
    
    def _set_black(self):
        self._is_red_bool = False
    
    def _is_path_root(self):
        return self._is_path_root_bool
    
    def _set_path_root(self):
        self._is_path_root_bool = True
    
    def _set_path_inner(self):
        self._is_path_root_bool = False


Child = Enum('Child', ['left', 'right', 'none'])
ZigZag_Node_Parent = NewType('ZigZag_Node_Parent', tuple[ZigZag_Node, Child])


class ZigZag_RB_tree:
    def __init__(self) -> None:
        self._root = None

    
    # ------------------- Node property functions -------------------
    # TODO: allow to set property of the Node type chosen for this tree
    # TODO: decide if the property should be property or function
    def node_property(node_function):
        setattr(ZigZag_Node, node_function.__name__, property(node_function))

    @node_property
    def _is_upper(node: ZigZag_Node) -> bool:
        # Root nodes are always upper
        if node._is_path_root():
            return True
        
        # Upper nodes must have node on the same path to the left
        if node._left == None or node._left._is_path_root():
            return False
        
        # Must be upper
        return True
    
    @node_property
    def _is_lower(node: ZigZag_Node) -> bool:
        return not node._is_upper
    
    @node_property
    def _is_midpoint(node: ZigZag_Node) -> bool:
        # Lower nodes cannot be midpoint
        if node._is_lower:
            return False
        
        # Sanity check: if node is root, and left exits, then it cannot be a path root
        if node._is_path_root() and node._left != None:
            assert not node._left._is_path_root()

        # If path is a single node, it is the midpoint
        if node._is_path_root() and node._left == None:
            return True

        # Midpoint is the last upper node on the path
        # Traverse down the lower chunk below
        lower_node = node._left
        assert lower_node != None and lower_node._is_lower
        while lower_node._right != None and not lower_node._right._is_path_root():
            lower_node = lower_node._right

        # If end of lower chunk is upper node, then this node was not the midpoint
        if lower_node._is_upper:
            return False
        return True

    @node_property
    def _is_minimum(node: ZigZag_Node) -> bool:
        # Single node paths are minimum
        if node._is_path_root() and node._left == None:
            return True
        
        # Top lower node is minimum
        if node._parent._is_path_root():
            assert node._parent._left == node
            return True

        # Node is not minimum
        return False
    
    @node_property
    def _get_parent_of(node: ZigZag_Node) -> ZigZag_Node:
        # Root of tree is preserved
        if node._parent == None:
            return None
        
        # Root of paths have parent in outer path
        if node._is_path_root():
            # If the parent is upper node, then the parent is preserved
            if node._parent._is_upper:
                return node._parent
            
            # If the parent is lower node, and the node is to the right of the parent, then the parent is preserved
            if node._parent._right == node:
                return node._parent
            
            # Else, the parent is the lower node above the parent node
            node = node._parent._parent
            if node._is_upper:
                node = node._parent
            assert node._is_lower
            return node
        
        # All other nodes have parent in the same path
        # Upper nodes parent is the upper node above it
        if node._is_upper:
            assert node._parent._is_lower  # Upper cannot be path root, therefore the parent must be a lower chunk
            node = node._parent._parent
            while node._is_lower:
                node = node._parent
            return node

        # Lower nodes parent is the lower node below it
        # Except for the last lower node, which has the midpoint upper node above it as parent
        if node._right == None or node._right._is_path_root():
            node = node._parent
            while node._is_lower:
                node = node._parent
            assert node._is_midpoint
            return node
        
        # Next node must be to the right
        assert node._right != None and not node._right._is_path_root()

        # Right node is parent, if it is lower, else the left child of the right node
        node = node._right
        if node._is_upper:
            node = node._left
        assert node._is_lower
        return node
    
    @node_property
    def _to_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        # If no parent, return None
        if node._parent == None:
            return None, Child.none
        
        # Check if node is left or right of parent
        if node == node._parent._left:
            return node._parent, Child.left
        return node._parent, Child.right

    @node_property
    def _get_left_of_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        raise NotImplementedError("TODO: implement me!")
    
    @node_property
    def _get_right_of_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        # Upper nodes preserve right child
        if node._is_upper:
            return node, Child.right
        
        # Last lower node preserves right child
        if node._right == None or node._right._is_path_root():
            return node, Child.right

        # Lower nodes right child is the left child of the next lower node
        # Lower node in the same chunk
        if node._right._is_lower:
            return node._right, Child.left
        
        # Lower node in the next chunk
        return node._right._left, Child.left
    
    # TODO: code duplication?
    '''
    @node_property
    def _get_left_of(node: ZigZag_Node) -> ZigZag_Node:
        # Fecth parent node and if the desired node is the left or right child
        parent_node, child_type = node._get_left_of_parent

        # If the parent is None, then the result must be the root of the tree
        if parent_node == None:
            # However, access to the root is not allowed on a node basis
            # Return self._root

            # It must be close, so traverse up the tree to find the root
            while node._parent != None:
                node = node._parent
            
            return node

        # Parent exists -> find the desired node as the left or right
        if child_type == Child.left:
            return parent_node._left
        return parent_node._right
    '''
    
    @node_property
    def _get_left_of(node: ZigZag_Node) -> ZigZag_Node_Parent:
        # If the node is single node path, then it has no left node
        # The location to insert left node is to the left of this node
        if node._is_path_root() and node._left == None:
            return None

        # Upper nodes, which are not the midpoint, have the upper node below it as the left child
        # Midpoint has the bottom node of the lower chunk below as the left child
        # This can be combined to find the bottom node of the right path spanning from the left
        if node._is_upper:
            mid = node._is_midpoint
            assert node._left._is_lower
            node = node._left
            while node._right != None and not node._right._is_path_root():
                node = node._right
            assert not node._is_path_root()
            if mid: assert node._is_lower
            else: assert node._is_upper
            return node

        # Lower nodes have the left child as the first lower node above it
        assert node._is_lower
        
        # The top lower node does not have a left element
        if node._parent._is_path_root():
            return None
        
        # The left child is the parent node, if it is not upper, else the parents parent
        node = node._parent
        if node._is_upper:
            node = node._parent
        return node

    @node_property
    def _get_right_of(node: ZigZag_Node) -> ZigZag_Node:
        # Fecth parent node and if the desired node is the left or right child
        parent_node, child_type = node._get_right_of_parent

        # All right elements must have a parent
        assert parent_node != None

        # Parent exists -> find the desired node as the left or right
        if child_type == Child.left:
            return parent_node._left
        return parent_node._right

    def _set_child(self, parent: ZigZag_Node_Parent, child: ZigZag_Node) -> None:
        parent_node, child_type = parent
        if parent_node != None:
            if child_type == Child.left:
                parent_node._left = child
            else:
                parent_node._right = child

        if child != None:
            child._parent = parent_node
    

    # ------------------- Helper functions -------------------
    def _left_rotate(self, node: ZigZag_Node) -> None:
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
    
    def _right_rotate(self, node: ZigZag_Node) -> None:
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


    # ------------------- Contains and search functions -------------------
    def contains(self, key: int) -> bool:
        x = self.search(key)
        return x != None

    def search(self, key: int) -> ZigZag_Node:
        x, _ = self._search_key_and_parent(key)
        return x

    def _search_key_and_parent(self, key: int) -> tuple[ZigZag_Node, ZigZag_Node]:
        x = self._root
        y = None
        while x != None:
            y = x
            if key < x._key:
                x = x._left
            elif key > x._key:
                x = x._right
            else:
                return x, y
        return None, y


    # ------------------- Insert functions -------------------
    def insert(self, key: int) -> ZigZag_Node:
        # Tree is empty
        if self._root == None:
            self._root = ZigZag_Node(key, is_red=False, is_path_root=True)
            return self._root

        x, y = self._search_key_and_parent(key)

        if x != None:
            return x
        
        if key < y._key:
            return self.insert_predecessor(y, key)
        else:
            return self.insert_successor(y, key)

    def insert_predecessor(self, node: ZigZag_Node, key: int) -> ZigZag_Node:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return node
        
        # TODO: check if value is in bounds

        # Create new node at the location of the node to predecessor
        new_node = ZigZag_Node(
            key,
            parent=node._parent, left=node._left, right=node._right,
            is_red=node._is_red(), is_path_root=node._is_path_root()
        )

        # Update parent
        if node._parent != None:
            if node == node._parent._left:
                node._parent._left = new_node
            else:
                node._parent._right = new_node
        else:
            self._root = new_node

        # Update left child
        if node._left != None:
            node._left._parent = new_node
        # Update right child
        if node._right != None:
            node._right._parent = new_node
        
        # Reset node to be floating
        node._parent = None
        node._left = None
        node._right = None
        node._set_red()
        node._set_path_inner()

        # Set node as the successor of new_node
        self._insert_successor(new_node, node)

        return new_node

    def insert_successor(self, node: ZigZag_Node, key: int) -> ZigZag_Node:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return node
        
        # TODO: check if value is in bounds

        # Create new floating node
        new_node = ZigZag_Node(key)

        # Insert new_node as the successor of node
        self._insert_successor(node, new_node)

        return new_node

    def _insert_successor(self, node: ZigZag_Node, new_node: ZigZag_Node) -> None:
        # Push new_node into the right subtree of node
        right = node._get_right_of

        # If empty, new_node becomes new path root
        if right == None:
            new_node._set_path_root()
            right_parent = node._get_right_of_parent
            self._set_child(right_parent, new_node)
        
        # Else, insert new_node as the new minimum node in right
        else:
            # Tree is non empty -> minimum location is to the left of the root
            new_node._parent = right
            new_node._right = right._left
            right._left = new_node
            if new_node._right != None:
                new_node._right._parent = new_node

        # Call fixup on the new node
        self._insert_fixup(new_node)

    def _insert_fixup(self, z: ZigZag_Node) -> None:
        assert z._is_red()
        assert z._is_minimum

        while z._get_parent_of != None and z._get_parent_of._is_red():
            if z._get_parent_of == z._get_parent_of._get_parent_of._get_left_of:
                y = z._get_parent_of._get_parent_of._get_right_of
                if y != None and y._is_red():
                    z._get_parent_of._set_black()
                    y._set_black()
                    z._get_parent_of._get_parent_of._set_red()
                    self._insert_fixup_node_color_change(z._get_parent_of)
                    self._insert_fixup_node_color_change(y)
                    self._insert_fixup_node_color_change(z._get_parent_of._get_parent_of)
                    z = z._get_parent_of._get_parent_of
                else:
                    if z == z._get_parent_of._get_right_of:
                        z = z._get_parent_of
                        self._real_left_rotate(z)
                    a = z._get_parent_of
                    a._set_black()
                    b = z._get_parent_of._get_parent_of
                    b._set_red()
                    self._real_right_rotate(z._get_parent_of._get_parent_of)
                    self._insert_fixup_node_color_change(b)
                    self._insert_fixup_node_color_change(a)
            else:
                y = z._get_parent_of._get_parent_of._get_left_of
                if y != None and y._is_red():
                    z._get_parent_of._set_black()
                    y._set_black()
                    z._get_parent_of._get_parent_of._set_red()
                    self._insert_fixup_node_color_change(z._get_parent_of)
                    self._insert_fixup_node_color_change(y)
                    self._insert_fixup_node_color_change(z._get_parent_of._get_parent_of)
                    z = z._get_parent_of._get_parent_of
                else:
                    if z == z._get_parent_of._get_left_of:
                        z = z._get_parent_of
                        self._real_right_rotate(z)
                    a = z._get_parent_of
                    a._set_black()
                    b = z._get_parent_of._get_parent_of
                    b._set_red()
                    self._real_left_rotate(z._get_parent_of._get_parent_of)
                    self._insert_fixup_node_color_change(b)
                    self._insert_fixup_node_color_change(a)
        self._root._set_black()

    def _insert_fixup_node_color_change(self, node: ZigZag_Node) -> None:
        # If upper node is changed, nothing happens
        if node._is_upper:
            return
        
        # If lower node is changed, then the chunk may need to be updated
        # If internal chunk, and node is last in chunk, and node is now red, node is pushed down
        if node._right != None and node._right._is_upper and not node._right._is_path_root():
            # Last on internal chunk
            if node._is_red():
                self._left_rotate(node)
            return
        
        # Check if the chunk is the last chunk and split if needed
        self._fixup_split_possible_last_chunk(node)

    # ------------------- Deletion functions -------------------
    def delete(self, key: int) -> None:
        z = self.search(key)
        if z == None:
            return
        
        self.delete_node(z)

    def delete_node(self, z: ZigZag_Node) -> None:
        # z: node to delete
        # y: node to replace z with
        # x: node to fixup from
        # dummy: if removing the minimum node on a path, this may leave the top lower chunk empty
        #        a dummy node is inserted, to preserve the structure, which over the fixup method is to be removed
        #        This is also used, if the node to run fixup from is nil

        dummy = None

        # If right subtree is non-empty, then find the successor of z in z._right
        if z._get_right_of != None:
            # Find the minimum node in the right subtree
            y = z._get_right_of
            if y._left != None:
                y = y._left
            y_original_black = y._is_black()

            assert y._is_minimum
            assert y._left == None

            # If y has a right child, insert it at y's location
            if y._get_right_of != None:
                right = y._get_right_of
                assert right._is_red()
                assert right._right == None
                assert right._left == None
                assert right._is_path_root()
                x = right
                if right._parent._left == right:
                    right._parent._left = None
                else:
                    right._parent._right = None
                right._parent = y._parent
                right._right = y._right
                if y._right != None:
                    y._right._parent = right
                if not y._is_path_root():
                    right._set_path_inner()
                child = right
            
            # If y is a black leaf element a dummy node is needed
            elif y._is_black():
                dummy = ZigZag_Node(None, parent=y._parent, right=y._right, is_red=False, is_path_root=y._is_path_root())
                if y._right != None:
                    y._right._parent = dummy
                x = dummy
                child = dummy
            
            # Else, y can freely be removed
            else:
                child = y._right
            
            # Free y
            if child != None:
                child._parent = y._parent
            if y._parent._left == y:
                y._parent._left = child
            else:
                y._parent._right = child
            y._parent = None
            y._right = None
        
        # If right subtree is empty, but the left is not, then the left is excactly the predecessor of z
        elif z._get_left_of != None:
            y = z._get_left_of
            y_original_black = y._is_black()
            x = y

            assert y._is_red()
            assert y._is_minimum
            assert y._get_left_of == None
            assert y._get_right_of == None
            assert y._get_parent_of._get_left_of == y
            
            # Free y
            y._parent._left = y._right
            if y._right != None:
                y._right._parent = y._parent
            y._parent = None
            y._right = None
        
        # If both subtrees are empty, then z is a leaf. The parent is then either the successor or the predecessor of z
        elif z._get_parent_of != None:
            y = z
            y_original_black = y._is_black()

            # If y is black, then it must be replaced by a dummy node
            if y_original_black:
                dummy = ZigZag_Node(None, parent=y._parent, right=y._right, is_red=False, is_path_root=y._is_path_root())
                if y._right != None:
                    y._right._parent = dummy
                x = dummy
                child = dummy
            
            # Else, y can freely be removed
            else:
                child = y._right
            
            # Free y
            if child != None:
                child._parent = y._parent
            if y._parent._left == y:
                y._parent._left = child
            else:
                y._parent._right = child
            y._parent = None
            y._right = None

        # The root is the only node in the tree
        else:
            self._root = None
            return
        
        # Replace z with y
        if y != z:
            y._parent = z._parent
            if z._parent == None:
                self._root = y
            elif z._parent._left == z:
                z._parent._left = y
            else:
                z._parent._right = y
            y._left = z._left
            if y._left != None:
                y._left._parent = y
            y._right = z._right
            if y._right != None:
                y._right._parent = y
            y._is_red_bool = z._is_red_bool
            y._is_path_root_bool = z._is_path_root_bool
        
        # Run fixup from x if needed
        if y_original_black:
            self._delete_fixup(x, dummy)

    def _delete_fixup(self, x: ZigZag_Node, dummy: ZigZag_Node) -> None:
        # while x != self._root and x._is_black():
        #     if x == x._parent._left:
        #         w = x._parent._right
        #         if w._is_red():
        #             w._set_black()
        #             x._parent._set_red()
        #             self._left_rotate(x._parent)
        #             w = x._parent._right
        #         if w._left._is_black() and w._right._is_black():
        #             w._set_red()
        #             x = x._parent
        #         else:
        #             if w._right._is_black():
        #                 w._left._set_black()
        #                 w._set_red()
        #                 self._right_rotate(w)
        #                 w = x._parent._right
        #             w._is_red_bool = x._parent._is_red()
        #             x._parent._set_black()
        #             w._right._set_black()
        #             self._left_rotate(x._parent)
        #             x = self._root
        #     else:
        #         w = x._parent._left
        #         if w._is_red():
        #             w._set_black()
        #             x._parent._set_red()
        #             self._right_rotate(x._parent)
        #             w = x._parent._left
        #         if w._right._is_black() and w._left._is_black():
        #             w._set_red()
        #             x = x._parent
        #         else:
        #             if w._left._is_black():
        #                 w._right._set_black()
        #                 w._set_red()
        #                 self._left_rotate(w)
        #                 w = x._parent._left
        #             w._is_red_bool = x._parent._is_red()
        #             x._parent._set_black()
        #             w._left._set_black()
        #             self._right_rotate(x._parent)
        #             x = self._root
        # x._set_black()

        # TODO: remove dummy if needed

        raise NotImplementedError("Delete fixup not implemented")
    

    # ------------------- Rotation and shared fixup functions -------------------
    def _fixup_split_possible_last_chunk(self, some_node: ZigZag_Node) -> None:
        assert some_node != None
        # TODO: assert some_node is lower node

        # Fetch the current chunk
        # TODO: chunk does not need to be a list, only the top, bot and len is needed
        top = some_node
        while top._parent._is_lower:
            top = top._parent
        assert top._is_lower
        bot = top
        chunk_size = 1
        while bot._right != None and bot._right._is_lower:
            bot = bot._right
            chunk_size += 1

        # If the chunk is the last chunk, check the size
        if bot._right == None or bot._right._is_path_root():
            assert 1 <= chunk_size <= 6

            # Extract upper lower chunk of size 1
            if chunk_size >= 3 and top._is_black():
                for _ in range(chunk_size - 2):
                    self._left_rotate(bot._parent)
                return

            # Extract upper lower chunk of size 2
            if chunk_size >= 4 and top._is_red() and top._right._is_black():
                for _ in range(chunk_size - 3):
                    self._left_rotate(bot._parent)
                return

    def _real_left_rotate(self, node: ZigZag_Node) -> None:
        #    x                  y
        #   / \      -->       / \
        #  a   y              x   c
        #     / \            / \
        #    b   c          a   b

        x = node
        assert x != None
        y = node._get_right_of
        assert y != None
        a = x._get_left_of
        b = y._get_left_of
        c = y._get_right_of

        # x_parent = x._to_parent

        # Pop the root of the left path spanning from y
        y_free, b_root = self._pop_path_root(y)
        assert y_free == y
        assert b_root == b

        # Insert b_root as the right real child of x
        self._set_child(x._get_right_of_parent, b_root)

        # Push y_free and c in on x
        self._push_node(x, y_free, c)

        # Link y to x's parent
        # self._set_child(x_parent, y_free)

        # If x was the global root, y is now global root
        if x == self._root:
            self._root = y

    def _real_right_rotate(self, node: ZigZag_Node) -> None:
        #      x              y
        #     / \    -->     / \
        #    y   c          a   x
        #   / \                / \
        #  a   b              b   c

        x = node
        assert x != None
        y = node._get_left_of
        assert y != None
        a = y._get_left_of
        b = y._get_right_of
        c = x._get_right_of

        # x_parent = x._to_parent

        # Pop x from the path
        x_free = self._pop_node(x)
        assert x_free == x

        # Push x_free onto the left path spanning from b
        self._push_path_root(b, x_free, c)
        
        # Set x_free as the right child of y
        self._set_child(y._get_right_of_parent, x_free)

        # Link y to x's parent
        # self._set_child(x_parent, y)

        # If x was the global root, y is now global root
        if x == self._root:
            self._root = y

    def _pop_node(self, node: ZigZag_Node) -> ZigZag_Node:
        # Partition the pop into the three cases: path root, upper node, lower node
        if node._is_path_root():
            node_parent = node._to_parent
            node_free, new_node = self._pop_path_root(node)
            self._set_child(node_parent, new_node)
        
        elif node._is_upper:
            node_parent = node._to_parent
            node_free, new_node = self._pop_upper_node(node)
            self._set_child(node_parent, new_node)

        else:
            assert node._is_lower
            node_parent = node._to_parent
            node_free, new_node = self._pop_lower_node(node)
            self._set_child(node_parent, new_node)

        # If the node was the root, then update the root
        if self._root == node:
            self._root = new_node

        return node_free

    def _push_node(self, node: ZigZag_Node, new_node: ZigZag_Node, new_node_right: ZigZag_Node) -> None:
        # If the node is the root, then update the root
        if self._root == node:
            self._root = new_node

        # Partition the push into the three cases: path root, upper node, lower node
        if node._is_path_root():
            node_parent = node._to_parent
            self._push_path_root(node, new_node, new_node_right)
            self._set_child(node_parent, new_node)
            return
        
        if node._is_upper:
            node_parent = node._to_parent
            self._push_upper_node(node, new_node, new_node_right)
            self._set_child(node_parent, new_node)
            return

        assert node._is_lower
        self._push_lower_node(node, new_node, new_node_right)

    def _pop_path_root(self, path_root: ZigZag_Node) -> tuple[ZigZag_Node, ZigZag_Node]:
        assert path_root != None
        assert path_root._is_path_root()

        path_root, new_path_root = self._pop_upper_node(path_root)
        path_root._set_path_inner()
        if new_path_root != None:
            new_path_root._set_path_root()
        return path_root, new_path_root

    def _push_path_root(self, path_root: ZigZag_Node, new_path_root: ZigZag_Node, new_path_root_right: ZigZag_Node) -> None:
        assert new_path_root != None

        # If path_root is None, then only linking node to the right is needed
        if path_root == None:
            new_path_root._right = new_path_root_right
            if new_path_root_right != None:
                new_path_root_right._parent = new_path_root
            new_path_root._set_path_root()
            return

        # Push the new path root as upper node
        self._push_upper_node(path_root, new_path_root, new_path_root_right)
        
        # Set path root flags
        path_root._set_path_inner()
        new_path_root._set_path_root()

    def _pop_upper_node(self, node: ZigZag_Node) -> tuple[ZigZag_Node, ZigZag_Node]:
        assert node != None
        assert node._is_upper

        # Flag check if node is the midpoint
        mid = node._is_midpoint
        node_parent = node._parent
        node_left = node._left

        # Pop parent link
        if node._parent != None:
            if node._parent._left == node:
                node._parent._left = None
            else:
                node._parent._right = None
        node._parent = None

        # Right subtree pops off - callers responsible to catch this node
        right_subtree = node._right
        assert right_subtree == node._get_right_of
        if right_subtree != None:
            right_subtree._parent = None
        node._right = None

        # Single node path pops single element
        if node_left == None:
            return node, None
        
        # Midpoint is popped, pop lower node to take its place
        if mid:
            # If single node in lower chunk
            if node._left._right == None or node._left._right._is_path_root():
                node_left._parent = None
                node._left = None
                return node, node_left

            # Traverse down the lower chunk below
            lower_node = node._left
            assert lower_node != None and lower_node._is_lower
            while lower_node._right != None and not lower_node._right._is_path_root():
                lower_node = lower_node._right
            assert lower_node._is_lower
            
            # Extract the last lower node
            lower_node._parent._right = lower_node._left
            if lower_node._left != None:
                lower_node._left._parent = lower_node._parent
            
            # Insert it here
            lower_node._left = node._left
            node._left._parent = lower_node
            node._left = None

            # If lower chunk exists above, link and fix
            if not node._is_path_root():
                assert node_parent != None
                node_parent._right = lower_node
                lower_node._parent = node_parent
                self._fixup_split_possible_last_chunk(lower_node)
            
            return node, lower_node

        # Setup loop variables
        last_upper_parent = None
        last_upper_left = node._left
        new_node = None
        node._left = None

        # Traverse down the left path and move upper elements up, untill the last is reached
        while True:
            assert last_upper_left != None
            assert last_upper_left._is_lower
            if last_upper_parent != None:
                assert last_upper_parent._is_lower
            
            # Fetch the next upper node
            upper_node = last_upper_left
            while upper_node._is_lower:
                upper_node = upper_node._right
            
            # First upper found is the new node at old node location
            if new_node == None:
                new_node = upper_node

            # Save if the node is the midpoint
            # (after the code below, it is above itself,
            #  and can therefore not see that it is not the midpoint)
            mid_flag = upper_node._is_midpoint

            # Remember next local nodes
            next_upper_parent = upper_node._parent
            next_upper_left = upper_node._left

            # Move the upper node up
            upper_node._parent = last_upper_parent
            if last_upper_parent != None:
                last_upper_parent._right = upper_node
            upper_node._left = last_upper_left
            last_upper_left._parent = upper_node

            # Swap to next local nodes
            last_upper_parent = next_upper_parent
            last_upper_left = next_upper_left

            # If the midpoint is found, then fix the last lower chunk
            if mid_flag:
                # Merge the last two lower chunks
                if last_upper_parent != None:
                    last_upper_parent._right = last_upper_left
                last_upper_left._parent = last_upper_parent

                # Check if the block is too large and split if needed
                self._fixup_split_possible_last_chunk(last_upper_parent)
                break
        
        assert new_node != None

        return node, new_node

    def _push_upper_node(self, node: ZigZag_Node, new_node: ZigZag_Node, new_node_right: ZigZag_Node) -> None:
        assert node != None
        assert node._is_upper
        assert new_node != None
        assert not new_node._is_path_root(), new_node._key

        # Free the node
        if node._parent != None:
            if node._parent._left == node:
                node._parent._left = None
            else:
                node._parent._right = None
        node._parent = None

        # Set the right subtree of the new node
        new_node._right = new_node_right
        if new_node_right != None:
            new_node_right._parent = new_node

        # If path is single node, then place the old node as the left lower chunk
        if node._left == None:
            node._parent = new_node
            new_node._left = node
            return

        # Free new_node
        new_node._parent = None
        new_node._left = None

        # Push upper nodes down, untill the midpoint is reached
        free_upper = new_node
        next_upper = node
        while True:
            assert next_upper._is_upper
            assert next_upper._left != None, next_upper._key

            # Overset new node
            free_upper._parent = next_upper._parent
            if free_upper._parent != None:
                free_upper._parent._right = free_upper
            free_upper._left = next_upper._left
            free_upper._left._parent = free_upper

            # If the overset node is the midpoint, the the last node is to move into the last lower chunk
            if next_upper._is_midpoint:
                # Fecth end of lower chunk
                mid_node = next_upper
                last_lower = mid_node._left
                while last_lower._right != None and not last_lower._right._is_path_root():
                    last_lower = last_lower._right
                assert last_lower._is_lower
                
                # Update pointers
                mid_node._left = last_lower._right
                if mid_node._left != None:
                    mid_node._left._parent = mid_node
                last_lower._right = mid_node
                mid_node._parent = last_lower

                # The mid_node may also be the root, which then would not allow the last split. Force internal (safe)
                mid_node._set_path_inner()

                # Possible split of the last lower chunk
                self._fixup_split_possible_last_chunk(last_lower)
                break

            # Fetch the next next upper
            next_next_upper = next_upper._left
            while next_next_upper._is_lower:
                next_next_upper = next_next_upper._right
            assert next_next_upper._is_upper

            # Free next upper
            next_upper._parent = None
            next_upper._left = None

            # Move variables
            free_upper = next_upper
            next_upper = next_next_upper

    def _pop_lower_node(self, node: ZigZag_Node) -> tuple[ZigZag_Node, ZigZag_Node]:
        assert node != None
        assert node._is_lower

        # Only allow to pop red nodes for now
        assert node._is_red()

        # Fetch the parent and the right child, as well as the next_lower_node
        node_parent = node._parent
        node_left = node._left
        node_right = node._right
        next_lower_node = node._get_parent_of
        assert next_lower_node != None
        next_lower_is_mid = next_lower_node._is_midpoint

        # Free the node
        node._parent = None
        node._left = None
        node._right = None
        if node_parent != None:
            if node_parent._left == node:
                node_parent._left = None
            else:
                node_parent._right = None
        if node_right != None:
            node_right._parent = None

        # Popping last lower node
        if node_right == None or node_right._is_path_root():
            assert next_lower_is_mid
            return node, node_left

        # Not the last lower node, the left subtree is the right subtree of the previous lower node
        # The real right subtree of node is the next_lower_node's left subtree
        assert next_lower_node._is_lower
        next_lower_node._left = node_left
        if node_left != None:
            node_left._parent = next_lower_node

        return node, node_right
    
    def _push_lower_node(self, node: ZigZag_Node, new_node: ZigZag_Node, new_node_right: ZigZag_Node) -> None:
        assert node != None
        assert node._is_lower
        assert new_node != None

        # Only allow to push red nodes for now
        # assert new_node._is_red()
        # Must allow black nodes, during left rotations after recoloring has appeared

        # Detach node's right subtree
        node_right = node._get_right_of
        if node_right != None:
            if node_right._parent._left == node_right:
                node_right._parent._left = None
            else:
                node_right._parent._right = None
            node_right._parent = None   

        # Insert new_node as the right child of node
        new_node._parent = node
        new_node._right = node._right
        node._right = new_node
        if new_node._right != None:
            new_node._right._parent = new_node
        
        # Insert node's right subtree as the left child of new_node
        new_node._left = node_right
        if node_right != None:
            node_right._parent = new_node

        # Push new_right_subtree
        if new_node_right != None:
            new_node_right_parent = new_node._get_right_of_parent
            self._set_child(new_node_right_parent, new_node_right)

        # If the new node is the last read in a non last block, it must be pushed down
        if new_node._is_red() and new_node._right != None and not new_node._right._is_path_root() and new_node._right._is_upper:
            self._left_rotate(new_node)

        # Possible split of the last lower chunk
        self._fixup_split_possible_last_chunk(new_node)



    # ------------------- Validation functions -------------------
    def is_valid_ZigZag_RB_tree(self, verbose=False) -> bool:
        if verbose:
            print("All pointers set:", self._all_pointers_set())
            print("Correct zigzag:", self._correct_zigzag())
            print("All regular pointers correct:", self._all_regular_pointers_correct())
            print("Root is black:", self._root_is_black())
            print("Is sorted:", self._is_sorted())
            print("Real black height:", self._real_black_height() != -1)
            print("Real no two red:", self._real_no_two_red())
            print("Zigzag max depth double black height:", self._zigzag_max_depth_double_black_height())
            print("Height is bounded by 4 * log(size):", self._height_is_log())

        return self._all_pointers_set() and \
               self._correct_zigzag() and \
               self._all_regular_pointers_correct() and \
               self._root_is_black() and \
               self._is_sorted() and \
               self._real_black_height() != -1 and \
               self._real_no_two_red() and \
               self._zigzag_max_depth_double_black_height() and \
               self._height_is_log()

    def _all_pointers_set(self) -> bool:
        return self._all_pointers_set_from(self._root)

    def _all_pointers_set_from(self, node: ZigZag_Node) -> bool:
        if node == None:
            return True
        if node._left != None and node._left._parent != node or node._right != None and node._right._parent != node:
            print("Error on", node._key)
            return False
        return self._all_pointers_set_from(node._left) and self._all_pointers_set_from(node._right)
    
    def _all_regular_pointers_correct(self) -> bool:
        return self._all_regular_pointers_correct_from(self._root)
    
    def _all_regular_pointers_correct_from(self, node: ZigZag_Node) -> bool:
        if node == None:
            return True
        left = node._get_left_of
        right = node._get_right_of
        if left != None and left._get_parent_of != node or right != None and right._get_parent_of != node:
            return False
        return self._all_regular_pointers_correct_from(node._left) and self._all_regular_pointers_correct_from(node._right)

    def _root_is_black(self) -> bool:
        return self._root == None or self._root._is_black()

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: ZigZag_Node, lower_bound: float, upper_bound: float) -> bool:
            if node == None:
                return True
            if lower_bound < node._key < upper_bound:
                return node_within_bounds(node._left, lower_bound, node._key) and node_within_bounds(node._right, node._key, upper_bound)
            return False
        
        return node_within_bounds(self._root, float('-inf'), float('inf'))

    def _real_black_height(self) -> int:
        return self._real_black_height_from(self._root)

    def _real_black_height_from(self, node: ZigZag_Node) -> int:
        if node == None:
            return 0
        left_real_black_height = self._real_black_height_from(node._get_left_of)
        right_real_black_height = self._real_black_height_from(node._get_right_of)
        if left_real_black_height == -1 or right_real_black_height == -1 or left_real_black_height != right_real_black_height:
            return -1
        if node._is_black():
            return left_real_black_height + 1
        return left_real_black_height

    def _real_no_two_red(self) -> bool:
        return self._real_no_two_red_from(self._root)

    def _real_no_two_red_from(self, node: ZigZag_Node) -> bool:
        if node == None:
            return True
        if node._is_red() and node._get_parent_of._is_red():
            return False
        return self._real_no_two_red_from(node._left) and self._real_no_two_red_from(node._right)

    def _correct_zigzag(self) -> bool:
        return self._correct_left_path_zigzag_from(self._root)

    def _correct_left_path_zigzag_from(self, path_root: ZigZag_Node) -> bool:
        # Empty paths are correct
        if path_root == None:
            return True
        
        # Path root must be set
        if not path_root._is_path_root():
            return False
        
        # Single node is correct
        if path_root._left == None:
            return True and self._correct_left_path_zigzag_from(path_root._right)

        # Traverse down the left path
        node = path_root
        while True:
            # First node must be upper
            if not node._is_upper:
                return False
            
            # The right child must be a valid path
            if not self._correct_left_path_zigzag_from(node._right):
                return False
            
            # The left path must be a lower part
            if node._left == None:
                return False
            node = node._left
            if not node._is_lower:
                return False
            
            lower_len = 0
            colors = []
            while node != None and node._is_lower:
                lower_len += 1
                colors.append(node._is_red())
                if not self._correct_left_path_zigzag_from(node._left):
                    return False
                if node._right == None or node._right._is_path_root():
                    break
                node = node._right
            
            # If standing on an upper node, chunk must be not the last
            if node._is_upper:
                # Lower chunks contains 1-2 nodes
                if not (1 <= lower_len <= 2):
                    return False

                # Colors must be either single black or red followed by black
                if not (colors == [False] or colors == [True, False]):
                    return False
            
            # Else, the chunk must be the last
            else:
                # Lower chunks contains 1-3 nodes
                if not (1 <= lower_len <= 3):
                    return False

                # If three elements in chunk, and top node is black, then another zig-zag is needed
                if len(colors) == 3 and colors[0] == False:
                    return False

                # Check the final right tree
                if not self._correct_left_path_zigzag_from(node._right):
                    return False
                
                break

        return True

    def _zigzag_max_depth_double_black_height(self) -> bool:
        return self._zigzag_max_depth_double_black_height_from_path_root(self._root)

    def _zigzag_max_depth_double_black_height_from_path_root(self, path_root: ZigZag_Node) -> bool:
        if path_root == None:
            return True

        # Get the black height by traversing down the right path, counting the black nodes
        black_height = 0
        right = path_root
        while right != None:
            black_height += right._is_black()
            right = right._right
        
        # Get the max height by traversing down all paths
        height = self._height_from(path_root)

        # The normal regular height must be at most 2 times the black height
        # For each upper node, the lower chunks above add at most 2 to the height + 1 for the last lower chunk
        # The height of the zigzag must increase by at most a constant factor
        if height > max(1, 5 * black_height):
            return False

        # Check all path_roots spanning from this path
        node = path_root
        while True:
            left_root = node._left == None or node._left._is_path_root()
            right_root = node._right == None or node._right._is_path_root()

            if left_root:
                if not self._zigzag_max_depth_double_black_height_from_path_root(node._left):
                    return False
                node = node._right
            else:
                assert right_root
                if not self._zigzag_max_depth_double_black_height_from_path_root(node._right):
                    return False
                node = node._left
            
            if left_root and right_root:
                break
        
        return True

    def _height_is_log(self) -> bool:
        height = self._height()
        size = self._size()
        return height <= 4 * log2(size + 1) + 1

    def _height(self) -> int:
        return self._height_from(self._root)
    
    def _height_from(self, from_node) -> int:
        if from_node == None:
            return 0
        return 1 + max(self._height_from(from_node._left), self._height_from(from_node._right))

    def _size(self) -> int:
        return self._size_from(self._root)
    
    def _size_from(self, from_node) -> int:
        if from_node == None:
            return 0
        return 1 + self._size_from(from_node._left) + self._size_from(from_node._right)

    # ------------------- Conversion and print functions -------------------
    def to_tuple(self, data_formatter=lambda key, is_red, is_path_root: (key, "BR"[is_red], "iR"[is_path_root])) -> tuple:
        def tuple_nodes(node: ZigZag_Node) -> tuple:
            if node == None:
                return ()
            return (*data_formatter(node._key, node._is_red(), node._is_path_root()), tuple_nodes(node._left), tuple_nodes(node._right))

        return tuple_nodes(self._root)
    
    @staticmethod
    def colored_node_data_formatter(key, is_red, is_path_root):
        return (("\u001b[31m" if is_red else "\u001b[37m") + str(key) + "\u001b[0m" + f"({'iR'[is_path_root]})",)

    @staticmethod
    def uncolored_node_data_formatter(key, is_red, is_path_root):
        return (str(key) + f"({'BR'[is_red]})({'iR'[is_path_root]})",)
    
    def str_block(self, colored=True) -> str:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        _, block = util.ascii_tree(self.to_tuple(formatter), str_len=util.visible_str_len)
        return block

    def print(self, colored=True) -> None:
        formatter = self.colored_node_data_formatter if colored else self.uncolored_node_data_formatter
        util.print_ascii_tree(self.to_tuple(formatter), str_len=util.visible_str_len)


if __name__ == "__main__":
    pass
