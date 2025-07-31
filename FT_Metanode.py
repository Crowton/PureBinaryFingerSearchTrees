from __future__ import annotations

from FT_Three_Pointer_Atomic_Node import Atomic_3

from util import link_left, link_right, print_ascii_tree


class Metanode:
    def __init__(self, atomic_node: Atomic_3, atomic_is_root=False, bit_count=2) -> None:
        if not atomic_is_root:
            atomic_node = Metanode.get_root_atomic_node(atomic_node)
        self._root = atomic_node
        self._bit_count = bit_count
        self._is_proper = atomic_node.right != None

    @staticmethod
    def get_root_atomic_node(inner_atomic_node: Atomic_3) -> Atomic_3:
        while not Metanode.is_root_atomic_node(inner_atomic_node) and inner_atomic_node.parent != None:
            inner_atomic_node = inner_atomic_node.parent
        return inner_atomic_node

    @staticmethod
    def is_root_atomic_node(atomic_node: Atomic_3) -> bool:
        l = atomic_node.left
        r = atomic_node.right
        rl = r.left if r != None else None
        ll = l.left if l != None else None
        llr = ll.right if ll != None else None
        llrl = llr.left if llr != None else None
        return l != None and r != None and rl != None and (ll == None or (llr != None and llrl != None))

    @property
    def parent(self) -> Metanode:
        assert self._is_proper
        if self._root.parent is None:
            return None
        return Metanode(self._root.parent.parent, atomic_is_root=True)
    
    @parent.setter
    def parent(self, parent: Metanode) -> None:
        assert self._is_proper
        if parent == None:
            self._root.parent = None
            return
        
        atomic_parent = parent._root
        if atomic_parent.left.left == self._root:
            self._root.parent = atomic_parent.left.left
        else:
            self._root.parent = atomic_parent.right.right

    @property
    def left(self) -> Metanode:
        assert self._is_proper
        if self._root.left.left is None:
            return None
        return Metanode(self._root.left.left, atomic_is_root=True)
    
    @left.setter
    def left(self, left: Metanode) -> None:
        assert self._is_proper
        self._root.left.left = left

    @property
    def right(self) -> Metanode:
        assert self._is_proper
        if self._root.right.right is None:
            return None
        return Metanode(self._root.right.right, atomic_is_root=True)
    
    @right.setter
    def right(self, right: Metanode) -> None:
        assert self._is_proper
        self._root.right.right = right


    def _atomic_rotate_left(self, node: Atomic_3) -> None:
        node.rotate_left()
        if self._root == node:
            self._root = node.parent

    def _atomic_rotate_right(self, node: Atomic_3) -> None:
        node.rotate_right()
        if self._root == node:
            self._root = node.parent


    def _get_bit_root(self, idx: int) -> Atomic_3:
        # Traverse to the first node on the bit/buffer path
        a = self._root.right.left

        # If idx is 0, then the root is found,
        # otherwise traverse over the bits inbetween
        for _ in range(idx):
            if a.right == None:
                a = a.left
            a = a.left
        
        return a
    
    def _get_bit(self, idx: int) -> bool:
        bit_root = self._get_bit_root(idx)

        # If root has node on the right, the bit is true
        return bit_root.right != None

    def _set_bit(self, idx: int, value: bool) -> None:
        bit_root = self._get_bit_root(idx)

        # If correct value, do nothing
        if value == (bit_root.right != None):
            return 
        
        # Rotate left / right, depending on new value
        if value:
            self._atomic_rotate_right(bit_root)
        else:
            self._atomic_rotate_left(bit_root)


    # TODO: save the bit as field after the first read, and update it on updates?
    @property
    def is_red(self) -> bool:
        assert self._is_proper
        return self._get_bit(0)
    
    @property
    def is_black(self) -> bool:
        assert self._is_proper
        return not self._get_bit(0)

    def set_red(self) -> None:
        assert self._is_proper
        self._set_bit(0, True)
    
    def set_black(self) -> None:
        assert self._is_proper
        self._set_bit(0, False)
    

    @property
    def is_left_path(self) -> bool:
        assert self._is_proper
        return self._get_bit(1)
    
    @property
    def is_right_path(self) -> bool:
        assert self._is_proper
        return not self._get_bit(1)

    def set_left_path(self) -> None:
        assert self._is_proper
        self._set_bit(1, True)
    
    def set_right_path(self) -> None:
        assert self._is_proper
        self._set_bit(1, False)


    def _get_size(self) -> int:
        if not self._is_proper:
            size = 1
            at = self._root
            while at.left != None:
                at = at.left
                size += 1
            return size

        size = 3
        at = self._root.right
        while at.left != None:
            at = at.left
            size += 1
            if at.right != None:
                size += 1

        return size

    def _minimum_proper_size(self) -> int:
        return 3 + 2 * self._bit_count + 1

    def _maximum_proper_size(self) -> int:
        return 3 + 2 * self._bit_count + 4 + 2 * self._bit_count

    def _convert_to_proper(self) -> None:
        assert not self._is_proper

        # Fetch the node y
        y = self._root
        while y.left.left != None:
            y = y.left

        # Rotate y upwards untill it becomes the root
        while y.parent != None:
            self._atomic_rotate_right(y.parent)

        # Update proper flag
        self._is_proper = True


    def _get_value_range(self):
        if not self._is_proper:
            left_most = self._root
            while left_most.left != None:
                left_most = left_most.left
            
            return left_most.value, self._root.value

        return self._root.left.left.value, self._root.right.value

    def range_contains_value(self, value) -> bool:
        small, large = self._get_value_range()
        return small <= value <= large

    def exact_search(self, value) -> Atomic_3:
        at = self._root
        while at != None:
            if value == at.value:
                return at
            if value < at.value:
                at = at.left
            else:
                at = at.right

        return None

    def predecessor(self, value) -> Atomic_3:
        raise NotImplementedError()
    
    def successor(self, value) -> Atomic_3:
        raise NotImplementedError()
    

    def insert_pred(self, node: Atomic_3, pred: Atomic_3) -> Metanode:
        # Insert pred as left child of node
        old_left = node.left
        link_left(node, pred)
        link_left(pred, old_left)

        # If the metanode is non-proper, check if the size allows it to be converted
        if not self._is_proper:
            size = self._get_size()
            if size >= self._minimum_proper_size():
                self._convert_to_proper()
            
            return None

        # The metanode is proper

        # If pred is inserted on the left spine, move root to the end of buffer
        if self._root.left == pred or self._root.left.left == pred:
            r = self._root
            new_r = r.left
            link_right(new_r, r.right)
            if r.parent != None:
                if r.parent.left == r:
                    link_left(r.parent, new_r)
                else:
                    link_right(r.parent, new_r)
            self._root = new_r

            link_right(r, None)
            link_left(r, None)

            at = new_r.right
            while at.left != None:
                at = at.left
            link_left(at, r)
        
        # Pred is inserted into the bits or buffer
        else:
            # Pred is inserted onto a true bit
            if pred.parent != self._root and pred.parent.right == pred:
                bit_node = pred.parent
                self._atomic_rotate_left(pred.parent.parent)
                pred = bit_node

            # Pred must now be on the buffer or bit path
            # Move true bits upwards to fix them
            at = pred
            while at.left != None:
                if at.left.right != None:
                    self._atomic_rotate_left(at.left)
                    self._atomic_rotate_right(at)
                    at = at.parent.left
                else:
                    at = at.left

        # If size does not allow to split, return
        size = self._get_size()
        if size <= self._maximum_proper_size():
            return 

        # Split the node and return the new node
        # Save the bits and reset them
        bits = []
        for i in range(self._bit_count):
            bits.append(self._get_bit(i))
            self._set_bit(i, False)
        
        # Save metanode parent, left and right child and unlink
        metanode_parent = self.parent
        metanode_left = self.left
        metanode_right = self.right
        
        if metanode_parent != None:
            if metanode_parent.left == self:
                self_is_left = True
                metanode_parent.left = None
            else:
                self_is_left = False
                metanode_parent.right = None
        if metanode_left != None:
            metanode_left.parent = None
        if metanode_right != None:
            metanode_right.parent = None

        self.parent = None
        self.left = None
        self.right = None

        # Save metanode largest value and new root
        pred_root = self._root
        z = self._root.right

        # Fetch root of buffer
        buffer_root = self._root.right.left
        for _ in range(self._bit_count):
            buffer_root = buffer_root.left.left
        
        # Extract buffer for new metanode
        pred_buffer_path_root = buffer_root.left.left.left
        pred_buffer_path_root.parent.left = None
        link_right(self._root, pred_buffer_path_root)
        
        # Setup new header for this metanode
        y = buffer_root.left
        buffer_root.left = None
        link_right(y, z)
        self._root = y
        self._root.parent = None

        # Set saved parent, left and right child
        if metanode_parent != None:
            if self_is_left:
                link_left(metanode_parent, self)
            else:
                link_right(metanode_parent, self)
        link_left(self, metanode_left)
        link_right(self, metanode_right)

        # Set saved bits
        for i, v in enumerate(bits):
            self._set_bit(i, v)

        return Metanode(pred_root, atomic_is_root=True)


    def insert_succ(self, node: Atomic_3, succ: Atomic_3) -> Metanode:
        # TODO: insert without splice?
        # TODO: forgetting to set parents child, breaks?

        #     p
        #     |
        #    node
        #    /  \
        #   l    r

        p = node.parent
        l = node.left
        r = node.right

        if p != None:
            if p.left == node:
                link_left(p, succ)
            else:
                link_right(p, succ)
        link_left(succ, l)
        link_right(succ, r)

        # TODO: can this be done with setting parent, left and right?
        node._atomic_node.left = None
        node._atomic_node.sibling_parent = None

        if self._root == node:
            self._root = succ

        # After splicing, insert the node as pred, and fetch result
        pred_res = self.insert_pred(succ, node)
        if pred_res is None:
            return 

        # If pred returns new metanode, then splice these again
        # Copy bits
        for i in range(self._bit_count):
            pred_res._set_bit(i, self._get_bit(i))
            self._set_bit(i, False)
        
        # Copy pointers
        if self.parent != None:
            if self.parent.left == self:
                link_left(self.parent, pred_res)
            else:
                link_right(self.parent, pred_res)
        link_left(pred_res, self.left)
        link_right(pred_res, self.right)

        self.parent = None
        self.left = None
        self.right = None

        # Move into new metanode, and replace self with pred_res
        succ_res = Metanode(self._root, atomic_is_root=True)
        self._root = pred_res._root

        return succ_res


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Metanode):
            return False
        return self._root == value._root_atomic_node


    @staticmethod
    def _to_tuple_rep_all(node: Atomic_3):
        def inner(node: Atomic_3):
            if node == None:
                return ()
            return (node.value, inner(node.left), inner(node.right))

        return inner(node)

    def to_tuple_rep(self):
        if not self._is_proper:
            return Metanode._to_tuple_rep_all(self._root)
        
        return (
            self._root.value,
            (self._root.left.value, (), ()),
            (self._root.right.value, self._to_tuple_rep_all(self._root.right.left), ())
        )

    def print(self, end_line=True, print_all=False):
        tuple_rep = self.to_tuple_rep() if not print_all else Metanode._to_tuple_rep_all(self._root)
        print_ascii_tree(tuple_rep)
        if end_line:
            print()
