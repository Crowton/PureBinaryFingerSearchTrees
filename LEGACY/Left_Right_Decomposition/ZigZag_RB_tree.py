import util
from enum import Enum
from typing import NewType


class ZigZag_Node:
    def __init__(self, key) -> None:
        self._key = key
        self._parent = None
        self._left = None
        self._right = None
        self._is_red = True
        self._is_left_path = True
    
    def is_red(self):
        return self._is_red
    
    def is_black(self):
        return not self._is_red
    
    def set_red(self):
        self._is_red = True
    
    def set_black(self):
        self._is_red = False
    
    def is_left_path(self):
        return self._is_left_path

    def is_right_path(self):
        return not self._is_left_path
    
    def set_left_path(self):
        self._is_left_path = True
    
    def set_right_path(self):
        self._is_left_path = False


Child = Enum('Child', ['left', 'right', 'none'])
ZigZag_Node_Parent = NewType('ZigZag_Node_Parent', tuple[ZigZag_Node, Child])


class ZigZag_RB_tree:
    def __init__(self) -> None:
        self._root = None

    # TODO: allow to set property of the Node type chosen for this tree
    # TODO: decide if the property should be property or function
    def node_property(node_function):
        setattr(ZigZag_Node, node_function.__name__, property(node_function))
        # setattr(ZigZag_Node, node_function.__name__, lambda self: node_function(self))
    
    # TODO: function to chunk lower path
    # TODO: simplify using help function '_node_is_not_left_path(node): return node == nil or node.is_right_path()'

    @node_property
    def _is_upper(node: ZigZag_Node) -> bool:
        # Decompose to left and right paths
        if node.is_left_path():
            # Top node of path is always upper
            if node._parent == None or node._parent.is_right_path():
                return True
            
            # If node is left child, it must be lower
            if node == node._parent._left:
                return False

            # If node is right and parent is red, it must be lower
            if node._parent.is_left_path() and node._parent.is_red():
                return False
            
            # Otherwise, it must be upper
            return True
        
        else:
            # Top node is always upper
            if node._parent == None or node._parent.is_left_path():
                return True
            
            # If node is right child, it must be lower
            if node == node._parent._right:
                return False
            
            # If node is left and parent is red, it must be lower
            if node._parent.is_right_path() and node._parent.is_red():
                return False
            
            # Otherwise, it must be upper
            return True

    @node_property
    def _is_lower(node: ZigZag_Node) -> bool:
        return not node._is_upper
    
    @node_property
    def _is_midpoint(node: ZigZag_Node) -> bool:
        # Midpoint is defined to be upper
        if node._is_lower:
            return False

        # TODO: help function "is_left_or_nil" and "is_right_or_nil"

        # Decompose to left and right paths
        if node.is_left_path():
            assert node._right == None or node._right.is_right_path()
            
            # Midpoint is at the end of the chain
            if node._left == None or node._left.is_right_path():
                return True

            # Midpoint is above one lower chunk with no upper chunk below
            
            # Lower chunk is single node
            if node._left._right == None:
                return True
            if node._left._right.is_left_path() and node._left._right._is_upper:
                return False
        
            # Lower chunk is double node
            if node._left._right._right == None:
                return True
            if node._left._right._right.is_left_path() and node._left._right._right._is_upper:
                return False
            
            # Lower chunk is triple node
            if node._left._right._right._right != None and node._left._right._right._right.is_left_path() and node._left._right._right._right._is_upper:
                return False

            # Node is midpoint
            return True

        else:
            assert node._left == None or node._left.is_left_path()

            # Midpoint is at the end of the chain
            if node._right == None or node._right.is_left_path():
                return True

            # Midpoint is above one lower chunk
            
            # Lower chunk is single node
            if node._right._left == None:
                return True
            if node._right._left.is_right_path() and node._right._left._is_upper:
                return False
            
            # Lower chunk is double node
            if node._right._left._left == None:
                return True
            if node._right._left._left.is_right_path() and node._right._left._left._is_upper:
                return False
            
            # Lower chunk is triple node
            if node._right._left._left._left != None and node._right._left._left._left.is_right_path() and node._right._left._left._left._is_upper:
                return False
            
            # Node is midpoint
            return True
    
    @node_property
    def _is_minimum(node: ZigZag_Node) -> bool:
        # Only left nodes are minimum (edge case: single right node)
        if node.is_right_path():
            return False

        # Midpoint is minimum, if no other node exists
        if node._is_midpoint:
            return node._left == None or node._left.is_right_path()
        
        # Node is minimum if parent is the top node of the path
        if node._parent != None and (node._parent._parent == None or node._parent._parent.is_right_path()):
            return True
        
        return False

    @node_property
    def _is_maximum(node: ZigZag_Node) -> bool:
        # Only right nodes are maximum (edge case: single left node)
        if node.is_left_path():
            return False
        
        # Midpoint is maximum, if no other node exists
        if node._is_midpoint:
            return node._right == None or node._right.is_left_path()
        
        # Node is maximum if parent is the top node of the path
        if node._parent != None and (node._parent._parent == None or node._parent._parent.is_left_path()):
            return True
        
        return False

    # TODO: this propbably have an error, as not all cases consider lower triple chunks. All tests parse. Tests may not be sufficient enough
    @node_property
    def _get_parent_of(node: ZigZag_Node) -> ZigZag_Node:
        # Root of tree is preserved
        if node._parent == None:
            return None

        if node.is_left_path():
            if node._is_upper:
                # Left upper

                # Node is root of path
                if node._parent.is_right_path():
                    # Parent is upper chunk
                    if node._parent._is_upper:
                        # Node is left of parent -> parent is parent of node
                        if node._parent._left == node:
                            return node._parent
                        
                        # Node is right of parent -> parent is parent of parent of node
                        return node._parent._parent
                    
                    # Parent is lower chunk

                    # Node is left of parent -> parent is parent of node
                    if node._parent._left == node:
                        return node._parent

                    # Parent is single node chunk
                    if node._parent._parent._is_upper:
                        return node._parent._parent._parent
                    
                    # Parent is double or triple node chunk
                    return node._parent._parent
                
                # Lower chunk above is single node
                if node._parent._parent._left == node._parent:
                    return node._parent._parent

                # Lower chunk above is double nodes
                if node._parent._parent._parent._left == node._parent._parent:
                    return node._parent._parent._parent

                # Lower chunk above is triple nodes
                return node._parent._parent._parent._parent

            else:
                # Left lower

                # Node is bottom node of path
                if node._right == None or node._right.is_right_path():
                    # Parent is upper chunk above
                    # Lower chunk is single node
                    if node._parent._is_upper:
                        return node._parent
                    
                    # Lower chunk is double node
                    if node._parent._parent._is_upper:
                        return node._parent._parent

                    # Lower chunk is triple node
                    return node._parent._parent._parent
                
                # Node is part of chunk, with element(s) below
                if node._right._is_lower:
                    return node._right

                # Node is bottom node of chunk
                # If lower chunk exists below, it is the parent
                if node._right._left != None and node._right._left.is_left_path():
                    return node._right._left

                # Node is the bottom lower chunk node
                return node._right

        else:
            if node._is_upper:
                # Right upper

                if node._parent.is_left_path():
                    # Parent is upper chunk
                    if node._parent._is_upper:
                        # Node is right of parent -> parent is parent of node
                        if node._parent._right == node:
                            return node._parent
                        
                        # Node is left of parent -> parent is parent of parent of node
                        return node._parent._parent
                    
                    # Parent is lower chunk

                    # Node is right of parent -> parent is parent of node
                    if node._parent._right == node:
                        return node._parent

                    # Parent is single node chunk
                    if node._parent._parent._is_upper:
                        return node._parent._parent._parent
                    
                    # Parent is double or triple node chunk
                    return node._parent._parent
                
                # Lower chunk above is single node
                if node._parent._parent._right == node._parent:
                    return node._parent._parent

                # Lower chunk above is double nodes
                if node._parent._parent._parent._right == node._parent._parent:
                    return node._parent._parent._parent

                # Lower chunk above is triple nodes
                return node._parent._parent._parent._parent

            else:
                # Right lower

                # Node is bottom node of path
                if node._left == None or node._left.is_left_path():
                    # Parent is upper chunk above
                    # Lower chunk is single node
                    if node._parent._is_upper:
                        return node._parent

                    # Lower chunk is double node
                    if node._parent._parent._is_upper:
                        return node._parent._parent
                    
                    # Lower chunk is triple node
                    return node._parent._parent._parent
                
                # Node is part of chunk, with element(s) below
                if node._left._is_lower:
                    return node._left

                # Node is bottom node of chunk
                # If lower chunk exists below, it is the parent
                if node._left._right != None and  node._left._right.is_right_path():
                    return node._left._right

                # Node is the bottom lower chunk node
                return node._left

    @node_property
    def _to_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        # If no parent, return None
        if node._parent == None:
            return None, Child.none
        
        # Check if node is left or right of parent
        if node == node._parent._left:
            return node._parent, Child.left
        return node._parent, Child.right

    # TODO: this propbably have an error, as not all cases consider lower triple chunks. All tests parse. Tests may not be sufficient enough
    @node_property
    def _get_left_of_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        if node.is_left_path():
            if node._is_upper:
                # Left upper
                
                # Node is the midpoint
                if node._is_midpoint:
                    # No lower chunk below
                    if node._left == None or node._left.is_right_path():
                        # Parent is right path -> Node is single node on path
                        if node._parent == None or node._parent.is_right_path():
                            return node, Child.left

                        # Parent is left path
                        return node._parent._to_parent
                    
                    # Lower chunk is single node
                    if node._left._right == None or node._left._right.is_right_path():
                        return node, Child.left
                    
                    # Lower chunk is double node
                    if node._left._right._right == None or node._left._right._right.is_right_path():
                        return node._left, Child.right

                    # Lower chunk is triple node
                    return node._left._right, Child.right
                
                # Node is not midpoint -> Lower chunk and upper chunk exists below. Fetch upper chunk below
                # Lower chunk is single node
                if node._left._right._is_upper:
                    return node._left, Child.right
                
                # Lower chunk is double node
                if node._left._right._right._is_upper:
                    return node._left._right, Child.right

                # Lower chunk is triple node
                return node._left._right._right, Child.right
            
            else:
                # Left lower
                assert node._parent.is_left_path()

                # Node above is lower in same path
                if node._parent._is_lower:
                    return node._parent._to_parent

                # Node above above is lower in same path
                if node._parent._is_upper and node._parent._parent != None and node._parent._parent.is_left_path() and node._parent._parent._is_lower:
                    return node._parent._parent._to_parent
                
                # Node is the bottom of the chain
                return node, Child.left
        
        else:
            if node._is_upper:
                # Right upper

                # Node preserved left
                return node, Child.left
            
            else:
                # Right lower

                # Node is bottom of chain, left is preserved
                if node._left == None or node._left.is_left_path():
                    return node, Child.left

                # Node is top of double chunk
                if node._left.is_right_path() and node._left._is_lower:
                    return node._left, Child.right
                
                # Node is bottom of chunk
                # Node is bottom of last chunk (upper chunk below)
                if node._left._right == None or node._left._right.is_left_path():
                    return node._left, Child.right
                
                # Lower chunk exists below
                return node._left._right, Child.right

    # TODO: this propbably have an error, as not all cases consider lower triple chunks. All tests parse. Tests may not be sufficient enough
    @node_property
    def _get_right_of_parent(node: ZigZag_Node) -> ZigZag_Node_Parent:
        if node.is_right_path():
            if node._is_upper:
                # Right upper
                
                # Node is the midpoint
                if node._is_midpoint:
                    # No lower chunk below
                    if node._right == None or node._right.is_left_path():
                        # Parent is left path -> Node is single node on path
                        if node._parent == None or node._parent.is_left_path():
                            return node, Child.right

                        # Parent is right path
                        return node._parent._to_parent

                    # Lower chunk is single node
                    if node._right._left == None or node._right._left.is_left_path():
                        return node, Child.right
                    
                    # Lower chunk is double node
                    if node._right._left._left == None or node._right._left._left.is_left_path():
                        return node._right, Child.left

                    # Lower chunk is triple node
                    return node._right._left, Child.left
                
                # Node is not midpoint -> Lower chunk and upper chunk exists below. Fetch upper chunk below
                # Lower chunk is single node
                if node._right._left._is_upper:
                    return node._right, Child.left
                
                # Lower chunk is double node
                if node._right._left._left._is_upper:
                    return node._right._left, Child.left
                
                # Lower chunk is triple node
                return node._right._left._left, Child.left
            
            else:
                # Right lower
                assert node._parent.is_right_path()

                # Node above is lower in same path
                if node._parent._is_lower:
                    return node._parent._to_parent
                
                # Node above above is lower in same path
                if node._parent._is_upper and node._parent._parent != None and node._parent._parent.is_right_path() and node._parent._parent._is_lower:
                    return node._parent._parent._to_parent
                
                # Node is the bottom of the chain
                return node, Child.right
        
        else:
            if node._is_upper:
                # Left upper

                # Node preserved right
                return node, Child.right
            
            else:
                # Left lower

                # Node is bottom of chain, right is preserved
                if node._right == None or node._right.is_right_path():
                    return node, Child.right

                # Node is top of double chunk
                if node._right.is_left_path() and node._right._is_lower:
                    return node._right, Child.left
                
                # Node is bottom of chunk
                # Node is bottom of last chunk (upper chunk below)
                if node._right._left == None or node._right._left.is_right_path():
                    return node._right, Child.left
                
                # Lower chunk exists below
                return node._right._left, Child.left

    # TODO: code duplication?
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
    
    @node_property
    def _get_right_of(node: ZigZag_Node) -> ZigZag_Node:
        # Fecth parent node and if the desired node is the left or right child
        parent_node, child_type = node._get_right_of_parent

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

    def _get_path_root_from_minimum(self, minimum_node: ZigZag_Node) -> ZigZag_Node:
        assert minimum_node._is_minimum

        # If minimum is the root, then the path root is the minimum
        if minimum_node._parent == None or minimum_node._parent.is_right_path():
            return minimum_node
    
        # Otherwise, the path root is the parent of the minimum
        return minimum_node._parent
    
    def _get_path_root_from_maximum(self, maximum_node: ZigZag_Node) -> ZigZag_Node:
        assert maximum_node._is_maximum

        # If maximum is the root, then the path root is the maximum
        if maximum_node._parent == None or maximum_node._parent.is_left_path():
            return maximum_node
    
        # Otherwise, the path root is the parent of the maximum
        return maximum_node._parent

    def _set_child(self, parent: tuple[ZigZag_Node, bool], child: ZigZag_Node) -> None:
        parent_node, child_type = parent
        child._parent = parent_node
        if child_type == Child.left:
            parent_node._left = child
        else:
            parent_node._right = child


    # TODO: test below
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
    
    # TODO: test below
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


    def insert(self, key: int) -> None:
        # Tree is empty
        if self._root == None:
            self._root = ZigZag_Node(key)
            self._root.set_black()
            self._root.set_left_path()
            self._root._left = None
            self._root._right = None
            return

        x, y = self._search_key_and_parent(key)

        if x != None:
            return  # Key already exists
        
        if key < y._key:
            self.insert_predecessor(y, key)
        else:
            self.insert_successor(y, key)

    def insert_predecessor(self, node: ZigZag_Node, key: int) -> None:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return
        
        # TODO: check if value is in bounds

        if node.is_left_path():
            # If left subtree is empty, insert as new minimum on this path
            if node._get_left_of == None:
                path_root = self._get_path_root_from_minimum(node)
                self._push_minimum(None, path_root, key)
                return

            # If left subtree is not empty, insert as new maximum on left right subtree
            self._push_maximum(node._get_left_of._get_right_of_parent, node._get_left_of._get_right_of, key)

        else:
            # If left subtree is empty, insert as new subtree
            if node._get_left_of == None:
                self._push_maximum(node._get_left_of_parent, node._get_left_of, key)
                return

            # Insert as new maximum in the left right subtree
            self._push_maximum(node._get_left_of._get_right_of_parent, node._get_left_of._get_right_of, key)
    
    def insert_successor(self, node: ZigZag_Node, key: int) -> None:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return
        
        # TODO: check if value is in bounds

        if node.is_right_path():
            # If right subtree is empty, insert as new maximum on this path
            if node._get_right_of == None:
                path_root = self._get_path_root_from_maximum(node)
                self._push_maximum(None, path_root, key)
                return

            # If right subtree is not empty, insert as new minimum on right left subtree
            self._push_minimum(node._get_right_of._get_left_of_parent, node._get_right_of._get_left_of, key)
        
        else:
            # If right subtree is empty, insert as new subtree
            if node._get_right_of == None:
                self._push_minimum(node._get_right_of_parent, node._get_right_of, key)
                return

            # Insert as new minimum in the right left subtree
            self._push_minimum(node._get_right_of._get_left_of_parent, node._get_right_of._get_left_of, key)

    def _push_minimum(self, path_root_parent: ZigZag_Node_Parent, path_root: ZigZag_Node, new_minimum: int) -> None:
        if path_root != None:
            assert path_root.is_left_path()

        # Create new node
        new_node = ZigZag_Node(new_minimum)
        new_node.set_red()
        new_node.set_left_path()
        
        # If tree is empty, insert as new tree under path_root_parent
        if path_root == None:
            assert path_root_parent[0] != None
            self._set_child(path_root_parent, new_node)

            # Path type must be different from path_root_parent
            new_node._is_left_path = not path_root_parent[0]._is_left_path
            return
        
        # Must be pushed to a left path
        new_node.set_left_path()

        # If tree is not empty, insert at new minimum position (left of root)
        path_root_left = path_root._left
        new_node._parent = path_root
        path_root._left = new_node
        new_node._right = path_root_left
        if path_root_left != None:
            path_root_left._parent = new_node

        # Call fixup on new node
        self._insert_fixup(new_node)
    
    def _push_maximum(self, path_root_parent: ZigZag_Node_Parent, path_root: ZigZag_Node, new_maximum: int) -> None:
        if path_root != None:
            assert path_root.is_right_path()
        
        # Create new node
        new_node = ZigZag_Node(new_maximum)
        new_node.set_red()

        # If tree is empty, insert as new tree under path_root_parent
        if path_root == None:
            assert path_root_parent[0] != None
            self._set_child(path_root_parent, new_node)

            # Path type must be different from path_root_parent
            new_node._is_left_path = not path_root_parent[0]._is_left_path
            return
        
        # Must be pushed to a right path
        new_node.set_right_path()

        # If tree is not empty, insert at new maximum position (right of root)
        path_root_right = path_root._right
        new_node._parent = path_root
        path_root._right = new_node
        new_node._left = path_root_right
        if path_root_right != None:
            path_root_right._parent = new_node
        
        # Call fixup on new node
        self._insert_fixup(new_node)

    '''
    # TODO: can the functions below be simplified using the get_left and get_right functions?
    def insert_predecessor(self, node: ZigZag_Node, key: int) -> None:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return  # Key already exists

        if not (key < node._key):
            raise ValueError("Key must be less than node key")

        # TODO: get pred, and check that key > pred
        
        # Create new_node with empty pointers. No color or path type yet
        new_node = ZigZag_Node(key)
        new_node._parent = None
        new_node._left = None
        new_node._right = None

        # Insert new_node as predesessor of node
        self._insert_predecessor(node, new_node)

    def insert_successor(self, node: ZigZag_Node, key: int) -> None:
        if node == None:
            raise ValueError("Node cannot be nil")
        
        if node._key == key:
            return  # Key already exists
        
        if not (key > node._key):
            raise ValueError("Key must be greater than node key")
        
        # Create new_node with empty pointers. No color or path type yet
        new_node = ZigZag_Node(key)
        new_node._parent = None
        new_node._left = None
        new_node._right = None

        # Insert new_node as successor of node
        self._insert_successor(node, new_node)

    def _insert_predecessor(self, node: ZigZag_Node, new_node: ZigZag_Node) -> None:
        # Decompose into node being left and right path type
        if node.is_left_path():
            # Left path

            # If node is minimum, then new_node becomes new minimum of this subtree
            if node._is_minimum:
                assert node._left == None

                path_root = self._get_path_root_from_minimum(node)  # Path root is node or node._parent, so this call is O(1)
                self._push_minimum(path_root, new_node)
                return

            # If node is lower node, then left subtree must be the predesessor subtree.
            # Therefore new_node is the new minimum in this subtree
            if node._is_lower:
                if node._left == None:
                    # TODO: This pushes maximum to an empty subtree, can this be part of _puch_max for simplification?
                    new_node.set_red()
                    new_node.set_right_path()
                    node._left = new_node
                    new_node._parent = node
                    self._insert_fixup(new_node)
                    return
                
                else:
                    self._push_maximum(node._left, new_node)
                    return
            
            # If node is upper node, then the right subtree must be the successor subtree.
            # Insert new_node at node position, and push node as new minimum into the successor subtree
            assert node._is_upper

            self._set_new_node_at_node(node, new_node)

            # Push old node into successor tree
            self._push_minimum(new_node._right, node)
            return

        else:
            # Right path

            # Replace node with new_node, and insert node as successor to new_node
            self._set_new_node_at_node(node, new_node)
            self._insert_successor(new_node, node)

    def _insert_successor(self, node: ZigZag_Node, new_node: ZigZag_Node) -> None:
        # Decompose into node being left and right path type
        if node.is_right_path():
            # Right path

            # If node is maximum, then new_node becomes new maximum of this subtree
            if node._is_maximum:
                assert node._right == None

                path_root = self._get_path_root_from_maximum(node)
                self._push_maximum(path_root, new_node)
                return
            
            # If node is lower node, then right subtree must be the successor subtree.
            # Therefore new_node is the new maximum in this subtree
            if node._is_lower:
                if node._right == None:
                    new_node.set_red()
                    new_node.set_left_path()
                    node._right = new_node
                    new_node._parent = node
                    self._insert_fixup(new_node)
                    return
                
                else:
                    self._push_minimum(node._right, new_node)
                    return
                
            # If node is upper node, then the left subtree must be the predesessor subtree.
            # Insert new_node at node position, and push node as new maximum into the predesessor subtree
            assert node._is_upper

            self._set_new_node_at_node(node, new_node)

            # Push old node into predesessor tree
            self._push_maximum(new_node._left, node)
            return
        
        else:
            # Left path

            # Replace node with new_node, and insert node as predesessor to new_node
            self._set_new_node_at_node(node, new_node)
            self._insert_predecessor(new_node, node)

    def _set_new_node_at_node(self, node: ZigZag_Node, new_node: ZigZag_Node) -> None:
        assert node != None
        assert new_node != None

        # Update new_node pointers
        new_node._parent = node._parent
        new_node._left = node._left
        new_node._right = node._right
        new_node._is_red = node._is_red
        new_node._is_left_path = node._is_left_path

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

        # Update node pointer
        node._parent = None
        node._left = None
        node._right = None

    def _push_minimum(self, path_root: ZigZag_Node, new_node: ZigZag_Node) -> None:
        assert path_root != None
        
        if path_root.is_left_path():
            new_node.set_red()
            new_node.set_left_path()

            if path_root._left == None:
                path_root._left = new_node
                new_node._parent = path_root
            
            else:
                assert path_root._left._left == None
                path_root._left._left = new_node
                new_node._parent = path_root._left
                self._right_rotate(path_root._left)
            
            self._insert_fixup(new_node)

        else:
            if path_root._is_maximum:
                self._set_new_node_at_node(path_root, new_node)
                self._push_maximum(new_node, path_root)
            else:
                self._push_minimum(path_root._left, new_node)

    def _push_maximum(self, path_root: ZigZag_Node, new_node: ZigZag_Node) -> None:
        assert path_root != None
        
        if path_root.is_right_path():
            new_node.set_red()
            new_node.set_right_path()

            if path_root._right == None:
                path_root._right = new_node
                new_node._parent = path_root
            
            else:
                assert path_root._right._right == None
                path_root._right._right = new_node
                new_node._parent = path_root._right
                self._left_rotate(path_root._right)
            
            self._insert_fixup(new_node)
        
        else:
            if path_root._is_minimum:
                self._set_new_node_at_node(path_root, new_node)
                self._push_minimum(new_node, path_root)
            else:
                self._push_maximum(path_root._right, new_node)
    '''

    def _insert_fixup(self, z: ZigZag_Node) -> None:
        assert z.is_red()
        assert z.is_left_path() and z._is_minimum or z.is_right_path() and z._is_maximum
        
        # TODO: it may be the case that lower chunks contain 3 and not 2 elements. Get parent, left and right may therefore fail

        while z._get_parent_of != None and z._get_parent_of.is_red():
            if z._get_parent_of == z._get_parent_of._get_parent_of._get_left_of:
                y = z._get_parent_of._get_parent_of._get_right_of
                if y != None and y.is_red():
                    z._get_parent_of.set_black()
                    y.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    z = z._get_parent_of._get_parent_of
                else:
                    if z == z._get_parent_of._get_right_of:
                        z = z._get_parent_of
                        self._left_rotate(z)
                    z._get_parent_of.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    self._right_rotate(z._get_parent_of._get_parent_of)
            else:
                y = z._get_parent_of._get_parent_of._get_left_of
                if y != None and y.is_red():
                    z._get_parent_of.set_black()
                    y.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    z = z._get_parent_of._get_parent_of
                else:
                    if z == z._get_parent_of._get_left_of:
                        z = z._get_parent_of
                        self._right_rotate(z)
                    z._get_parent_of.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    self._left_rotate(z._get_parent_of._get_parent_of)
        self._root.set_black()

    def _insert_fixup_no_rotate(self, z: ZigZag_Node) -> None:
        assert z.is_red()
        assert z.is_left_path() and z._is_minimum or z.is_right_path() and z._is_maximum
        
        # TODO: it may be the case that lower chunks contain 3 and not 2 elements. Get parent, left and right may therefore fail

        while z._get_parent_of != None and z._get_parent_of.is_red():
            if z._get_parent_of == z._get_parent_of._get_parent_of._get_left_of:
                y = z._get_parent_of._get_parent_of._get_right_of
                if y != None and y.is_red():
                    z._get_parent_of.set_black()
                    y.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    z = z._get_parent_of._get_parent_of
                else:
                    break
            else:
                y = z._get_parent_of._get_parent_of._get_left_of
                if y != None and y.is_red():
                    z._get_parent_of.set_black()
                    y.set_black()
                    z._get_parent_of._get_parent_of.set_red()
                    z = z._get_parent_of._get_parent_of
                else:
                    break
        self._root.set_black()


    def delete(self, key: int) -> None:
        raise NotImplementedError("TODO: implement me!")


    def _all_pointers_set(self, node: ZigZag_Node) -> bool:
        if node == None:
            return True
        if node._left != None and node._left._parent != node or node._right != None and node._right._parent != node:
            return False
        return self._all_pointers_set(node._left) and self._all_pointers_set(node._right)
    
    # TODO: make function not take root node as initial arg
    def _all_regular_pointers_correct(self, node: ZigZag_Node, verbose=False) -> bool:
        if node == None:
            return True
        left = node._get_left_of
        right = node._get_right_of
        if left != None and left._get_parent_of != node or right != None and right._get_parent_of != node:
            if verbose:
                print(f"node: {node._key}\nleft: {left._key if left != None else None}\nright: {right._key if right != None else None}\nleft_parent: {left._get_parent_of._key if left != None else None}\nright_parent: {right._get_parent_of._key if right != None else None}\n")
            return False
        return self._all_regular_pointers_correct(node._left, verbose) and self._all_regular_pointers_correct(node._right, verbose)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: ZigZag_Node, lower_bound: float, upper_bound: float) -> bool:
            if node == None:
                return True
            if lower_bound < node._key < upper_bound:
                return node_within_bounds(node._left, lower_bound, node._key) and node_within_bounds(node._right, node._key, upper_bound)
            return False
        
        return node_within_bounds(self._root, float('-inf'), float('inf'))

    def to_tuple(self, data_formatter=lambda key, is_red, is_left_path: (key, "BR"[is_red], "RL"[is_left_path])) -> tuple:
        def tuple_nodes(node: ZigZag_Node) -> tuple:
            if node == None:
                return ()
            return (*data_formatter(node._key, node._is_red, node._is_left_path), tuple_nodes(node._left), tuple_nodes(node._right))

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
        util.print_ascii_tree(self.to_tuple(util.zigzag_colored_node_data_formatter), ignore_terminal_codes=True)

