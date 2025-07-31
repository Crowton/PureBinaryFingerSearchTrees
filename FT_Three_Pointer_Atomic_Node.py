from __future__ import annotations

import FT_Atomic_Node as Atomic_Node


class Three_Pointer_Atomic_Node:  # type alias 'Atomic_3'
    # TODO: input a value, and create underlying atomic node?
    def __init__(self, atomic_node: Atomic_Node) -> None:
        self._atomic_node = atomic_node


    def _from_atomic(self, atomic: Atomic_Node) -> Atomic_3:
        if atomic is None:
            return None
        return Three_Pointer_Atomic_Node(atomic)

    @property
    def value(self):
        return self._atomic_node.value

    @property
    def parent(self) -> Atomic_3:
        a = self._atomic_node
        
        # No sibling/parent => No parent present
        if a.sibling_parent == None:
            return None

        # a is the only child of its parent
        if a.sibling_parent.left == a:
            return self._from_atomic(a.sibling_parent)

        # a is the left child of its parent
        spsp = a.sibling_parent.sibling_parent
        if spsp != None and spsp.left == a:
            return self._from_atomic(spsp)
        
        # a is the right child of its parent
        return self._from_atomic(a.sibling_parent)
    
    @parent.setter
    def parent(self, parent: Atomic_3) -> None:
        a = self._atomic_node
        atomic_parent = parent._atomic_node if parent != None else None
        
        # a has no current parent
        if a.sibling_parent == None:
            a.sibling_parent = atomic_parent
            return

        # a is the only child of its parent
        if a.sibling_parent.left == a:
            a.sibling_parent = atomic_parent
            return
        
        # a is the left child of its parent
        spsp = a.sibling_parent.sibling_parent
        if spsp != None and spsp.left == a:
            a.sibling_parent.sibling_parent = atomic_parent
            return
        
        # a is the right child of its parent
        a.sibling_parent = atomic_parent


    @property
    def left(self) -> Atomic_3:
        return self._from_atomic(self._atomic_node.left)
    
    @left.setter
    def left(self, left: Atomic_3) -> None:
        atomic_left = left._atomic_node if left != None else None
        atomic_right = self.right._atomic_node if self.right != None else None
        
        if atomic_left == None and atomic_right != None:
            raise ValueError("Cannot remove left child, when right child is present")

        self._atomic_node.left = atomic_left

        if atomic_right != None:
            atomic_left.sibling_parent = atomic_right
        elif atomic_left != None:
            atomic_left.sibling_parent = self._atomic_node

    @property
    def right(self) -> Atomic_3:
        a = self._atomic_node

        # No right child exists
        if a.left == None or a.left.sibling_parent == a:
            return None
        
        return self._from_atomic(a.left.sibling_parent)
    
    @right.setter
    def right(self, right: Atomic_3) -> None:
        a = self._atomic_node
        atomic_right = right._atomic_node if right != None else None

        if a.left == None and atomic_right != None:
            raise ValueError("Cannot set right child, when left child is not present")
        
        # If setting right to none, then preserve left
        if atomic_right == None:
            if a.left != None:
                a.left.sibling_parent = a
            return

        # Update the right child
        a.left.sibling_parent = atomic_right


    def rotate_left(self) -> None:
        #   parent               parent
        #     |                    |
        #    self                child
        #    /  \       -->      /    \
        #   a  child           self    c
        #      /   \           /  \
        #     b     c         a    b

        # Fetch parent and child
        parent = self.parent
        child = self.right
        assert child != None

        # Link child and parent
        if parent != None:
            if parent.left == self:
                parent.left = child
            else:
                parent.right = child
        child.parent = parent

        # Fetch b and c and unlink
        b = child.left
        c = child.right
        child.right = None
        child.left = None
        if b != None:
            b.parent = None
        if c != None:
            c.parent = None

        # Link self and child
        self.parent = child
        child.left = self

        # Link self to b
        self.right = b
        if b != None:
            b.parent = self

        # Link child to c
        child.right = c
        if c != None:
            c.parent = child
    
    def rotate_right(self) -> None:
        #      parent            parent
        #        |                 |
        #       self             child
        #       /  \     -->     /   \
        #    child  c           a    self
        #    /   \                   /  \
        #   a     b                 b    c
        
        # REQUIRES: a != None
        # REQUIRES: c != None  -->  b != None

        # Fetch parent and child
        parent = self.parent
        child = self.left
        assert child != None

        # Fetch b and c and unlink
        b = child.right
        c = self.right
        child.right = None
        self.right = None
        if b != None:
            b.parent = None
        if c != None:
            c.parent = None

        # Unlink self and child
        self.left = None
        child.parent = None

        # Link child and parent
        if parent != None:
            if parent.left == self:
                parent.left = child
            else:
                parent.right = child
        child.parent = parent

        # Link self and child
        child.right = self
        self.parent = child

        # Link self and b
        self.left = b
        if b != None:
            b.parent = self
        
        # Link self and c
        self.right = c
        if c != None:
            c.parent = self


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Atomic_3):
            return False
        return self._atomic_node == value._atomic_node

    def __str__(self) -> str:
        return f"Atomic_3({self._atomic_node.value})"


Atomic_3 = Three_Pointer_Atomic_Node
