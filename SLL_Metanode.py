from __future__ import annotations
from typing import Iterator

from SLL_Atomic_Node import AtomicNode


# Used for Finger Searching
class Wrap_Values:
    def __init__(self, metanode: Metanode):
        head, tail = metanode._get_head_and_tail()
        self._min = head.value
        self._max = tail.value
    
    def __lt__(self, other) -> bool:
        assert not isinstance(other, Wrap_Values)
        return self._max < other

    def __le__(self, other):
        assert not isinstance(other, Wrap_Values)
        return self._min <= other

    def __gt__(self, other):
        assert not isinstance(other, Wrap_Values)
        return other < self._min

    def __ge__(self, other):
        assert not isinstance(other, Wrap_Values)
        return other <= self._max
    
    def __eq__(self, other):
        assert not isinstance(other, Wrap_Values)
        return self._min <= other <= self._max

    def __ne__(self, other):
        assert not isinstance(other, Wrap_Values)
        return not self.__eq__(other)


class Metanode:
    def __init__(self, atomic_node: AtomicNode, atomic_is_head=False):
        if not atomic_is_head:
            atomic_node = Metanode._get_head(atomic_node)

        self._head = atomic_node
        self._is_proper = self.size() >= Metanode._minimum_size()


    # ---------------------------------------------
    #           Checks for head and tail
    # ---------------------------------------------

    @staticmethod
    def _get_head(node: AtomicNode) -> AtomicNode:
        # If node is head, return
        if Metanode._is_head(node):
            return node

        # Otherwise, find the tail and return head from data
        while not Metanode._is_tail(node):
            node = node.next
        return node.data
    
    @staticmethod
    def _get_tail(node: AtomicNode) -> AtomicNode:
        while not Metanode._is_tail(node):
            node = node.next
        return node

    @staticmethod
    def _is_head(node: AtomicNode) -> bool:
        # Head is a node with data pointing to itself
        return node.data == node

    @staticmethod
    def _is_tail(node: AtomicNode) -> bool:
        # Tail is a node with next pointing to None or head of the next Metanode
        return node.next == None or Metanode._is_head(node.next)

    @property
    def _tail(self) -> AtomicNode:
        return Metanode._get_tail(self._head)


    # ---------------------------------------------
    #                   Iterator
    # ---------------------------------------------
    
    def __iter__(self) -> Iterator[int]:
        at = self._head
        while not Metanode._is_tail(at):
            yield at
            at = at.next
        yield at


    # ---------------------------------------------
    #               Size of Metanode
    # ---------------------------------------------

    @staticmethod
    def _minimum_size():
        return 8

    @staticmethod
    def _maximum_size():
        return 15

    def size(self) -> int:
        s = 1
        at = self._head
        while not Metanode._is_tail(at):
            at = at.next
            s += 1
        return s


    # ---------------------------------------------
    #             Pointer and bits
    # ---------------------------------------------

    @staticmethod
    def _wrap_atomic_head(node: AtomicNode) -> Metanode:
        if node == None:
            return None
        return Metanode(node)

    def _get_pointer(self, idx: int) -> Metanode:
        if not self._is_proper:
            return None
        at = self._head.next
        for _ in range(idx):
            at = at.next
        return Metanode._wrap_atomic_head(at.data)

    def _set_pointer(self, idx: int, value: Metanode) -> None:
        assert self._is_proper
        at = self._head.next
        for _ in range(idx):
            at = at.next
        atomic_value = value._head if value != None else None
        at.data = atomic_value

    @property
    def parent(self) -> Metanode:
        return self._get_pointer(0)

    @parent.setter
    def parent(self, parent: Metanode) -> None:
        self._set_pointer(0, parent)

    @property
    def left(self) -> Metanode:
        return self._get_pointer(1)

    @left.setter
    def left(self, left: Metanode) -> None:
        self._set_pointer(1, left)

    @property
    def right(self) -> Metanode:
        return self._get_pointer(2)

    @right.setter
    def right(self, right: Metanode) -> None:
        self._set_pointer(2, right)

    @property
    def pred(self) -> Metanode:
        return self._get_pointer(3)

    @pred.setter
    def pred(self, pred: Metanode) -> None:
        self._set_pointer(3, pred)

    @property
    def succ(self) -> Metanode:
        return self._get_pointer(4)

    @succ.setter
    def succ(self, succ: Metanode) -> None:
        self._set_pointer(4, succ)


    def _get_color_node(self) -> AtomicNode:
        assert self._is_proper
        return self._head.next.next.next.next.next.next

    @property
    def is_red(self) -> bool:
        return self._get_color_node().data != None

    @property
    def is_black(self) -> bool:
        return not self.is_red

    def set_red(self) -> None:
        color_node = self._get_color_node()
        color_node.data = color_node.next
    
    def set_black(self) -> None:
        color_node = self._get_color_node()
        color_node.data = None


    # Used for Finger Searching
    @property
    def value(self):
        return Wrap_Values(self)
    

    # ---------------------------------------------
    #                  Search
    # ---------------------------------------------
    
    def smallest_atomic(self) -> AtomicNode:
        return self._head

    def smallest_value(self):
        return self._head.value

    def largest_value(self):
        return self._tail.value

    def _get_head_and_tail(self) -> tuple[AtomicNode, AtomicNode]:
        return self._head, Metanode._get_tail(self._head)
    
    def must_contain(self, value) -> bool:
        head, tail = self._get_head_and_tail()
        if tail.next == None:
            return head.value <= value
        return head.value <= value < tail.next.value
    
    def contains(self, value) -> bool:
        return self.exact_search(value) != None

    def exact_search(self, value) -> AtomicNode:
        for node in self:
            if node.value == value:
                return node
        return None

    def predesessor_search(self, value) -> AtomicNode:
        # Search may only return node inside this Metanode
        # If value is too small, it is not contained
        if value < self._head.value:
            return None
        
        # Test all pair of nodes in the Metanode
        nodes = list(self)
        for a, b in zip(nodes, nodes[1:]):
            if a.value <= value < b.value:
                return a
        
        # Test if result is the tail
        tail = nodes[-1]
        if tail.next == None and tail.value <= value or tail.value <= value < tail.next.value:
            return tail

        # Value is greater than inside this Metanode
        return None

    def succesessor_search(self, value) -> AtomicNode:
        raise NotImplementedError()

    
    def node_predesessor(self, node: AtomicNode) -> AtomicNode:
        assert node != None
        # node must be in this metanode

        # If node is the head node, then the pred is the tail of the pred metanode
        if node == self._head:
            # The pred is the tail of the pred metanode
            pred_meta = self.pred
            if pred_meta == None:
                return None
            return pred_meta._tail

        # Otherwise, the pred is inside the metanode
        for pred in self:
            if pred.next == node:
                return pred

    def node_successor(self, node: AtomicNode) -> AtomicNode:
        assert node != None
        return node.next

    # ---------------------------------------------
    #                  Update
    # ---------------------------------------------

    def _split(self) -> Metanode:
        head = self._head
        buffer_head = self._head.next.next.next.next.next.next.next
        tail = self._tail

        # Create new Metanode
        buffer_head.data = head
        buffer_head.next.data = buffer_head.next
        tail.data = buffer_head.next
        return Metanode(buffer_head.next, atomic_is_head=True)

    def insert(self, node: AtomicNode) -> None:
        raise NotImplementedError()

    def insert_pred(self, node: AtomicNode, pred: AtomicNode) -> tuple[bool, Metanode]:
        updates_head = (node == self._head)
        update_color_node = self._is_proper and self.is_red

        # Insert pred into the linked list
        old_pred = self.node_predesessor(node)
        if old_pred != None:
            old_pred.next = pred
        pred.next = node
        
        # If metanode is a sinlge node, special case:
        if node == self._head and node == self._tail:
            assert not self._is_proper
            self._head = pred
            pred.data = pred
            node.data = pred
            return True, None

        # Move the data pointers forward
        at = pred
        while not Metanode._is_tail(at.next):
            at.data = at.next.data
            at = at.next
            at.data = None

        # If node is the head, update the data pointer
        if updates_head:
            self._head = pred
            pred.data = pred
            self._tail.data = pred
        
        # If the node is proper and red, update the color node
        if update_color_node:
            self.set_red()

        size = self.size()

        # Check if the metanode is now proper
        if not self._is_proper and size >= Metanode._minimum_size():
            self._is_proper = True
        
        # Check if the metanode needs to split
        if self._is_proper and size > Metanode._maximum_size():
            return updates_head, self._split()

        # No split
        return updates_head, None

    def insert_succ(self, node: AtomicNode, succ: AtomicNode) -> Metanode:
        node_is_tail = Metanode._is_tail(node)
        update_color_node = self._is_proper and self.is_red

        # Insert succ into the linked list
        succ.next = self.node_successor(node)
        node.next = succ

        # If metanode is a sinlge node, special case:
        if node == self._head and succ == self._tail:
            assert not self._is_proper
            succ.data = node
            return None

        # If node is the strict tail, update tail to succ
        if node_is_tail:
            succ.data = node.data
            node.data = None
        
        # Else, move data pointers forward
        else:
            at = succ
            while not Metanode._is_tail(at.next):
                at.data = at.next.data
                at = at.next
                at.data = None
            
            # If the node is proper and red, update the color node
            if update_color_node:
                self.set_red()

        size = self.size()

        # Check if the metanode is now proper
        if not self._is_proper and size >= Metanode._minimum_size():
            self._is_proper = True
        
        # Check if the metanode needs to split
        if self._is_proper and size > Metanode._maximum_size():
            return self._split()
        
        # No split
        return None
    
    def delete(self, node: AtomicNode) -> None:
        raise NotImplementedError()


    # ---------------------------------------------
    #              Meta operations
    # ---------------------------------------------

    def __eq__(self, other) -> bool:
        if not isinstance(other, Metanode):
            return False
        return self._head == other._head

    def __str__(self) -> str:
        head, tail = self._get_head_and_tail()
        return f"[{head.value}, {tail.value}]"
    
    def full_string(self) -> str:
        return str([node.value for node in self])

    def print(self):
        for node in self:
            print(f"{node}, next={node.next}, data={node.data}") 


    # ---------------------------------------------
    #                 Validation
    # ---------------------------------------------

    def is_valid(self, verbose=False) -> bool:
        # Check if the head is the head of the metanode
        if not Metanode._is_head(self._head):
            if verbose: print(self, "Head is not head of metanode")
            return False
        
        # Check if the tail is the tail of the metanode
        if not Metanode._is_tail(self._tail):
            if verbose: print(self, "Tail is not tail of metanode")
            return False
        
        # Check that head and tail points to head
        if self._head.data != self._head:
            if verbose: print(self, "Head does not point to itself")
            return False
        if self._tail.data != self._head:
            if verbose: print(self, "Tail does not point to head")
            return False

        # Check only head is head
        for node in list(self)[1:]:
            if Metanode._is_head(node):
                if verbose: print(self, "There is a head inside the metanode")
                return False

        # Non proper checks
        if not self._is_proper:
            # Check size
            if self.size() >= Metanode._minimum_size():
                if verbose: print(self, "The non_proper metanode is too big")
                return False

            # Check if the data pointers are correct
            for node in list(self)[1:-1]:
                if node.data != None:
                    if verbose: print(self, "The non_proper data pointers are set")
                    return False
            return True

        # Proper checks
        # Check size
        if not (Metanode._minimum_size() <= self.size() <= Metanode._maximum_size()):
            if verbose: print(self, "The proper metanode is not in the right size")
            return False

        # Check pointers do not point inward
        for p in [self.parent, self.left, self.right, self.pred, self.succ]:
            if p == self:
                if verbose: print(self, "Pointer points inward")
                return False

        # Check bit
        color_node = self._get_color_node()
        if color_node.data != None and color_node.data != color_node.next:
            if verbose: print(self, "The color node is not set correctly", color_node, color_node.data, color_node.next)
            return False

        # Check the buffer nodes data pointers
        buffer = color_node.next
        while not Metanode._is_tail(buffer):
            if buffer.data != None:
                if verbose: print(self, "The buffer node data pointer is set")
                return False
            buffer = buffer.next
        
        # Check the values are in order
        last = self._head
        for node in list(self)[1:]:
            if not (last.value < node.value):
                if verbose: print(self, "The values are not in order")
                return False
            last = node

        return True
