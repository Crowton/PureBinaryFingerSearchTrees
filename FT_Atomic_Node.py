from __future__ import annotations

# from Pointer_Counting import pointer_getter, pointer_setter
from Pointer_Counting import pointer_get, pointer_set


class AtomicNode:
    def __init__(self, value) -> None:
        self._value = value
        self._left = None
        self._sibling_parent = None
    
    
    @property
    def value(self):
        return self._value

    @property
    # @pointer_getter
    def left(self) -> AtomicNode:
        pointer_get()
        return self._left
    
    @left.setter
    # @pointer_setter
    def left(self, left: AtomicNode) -> None:
        pointer_set()
        self._left = left


    @property
    # @pointer_getter
    def sibling_parent(self) -> AtomicNode:
        pointer_get()
        return self._sibling_parent
    
    @sibling_parent.setter
    # @pointer_setter
    def sibling_parent(self, sibling_parent: AtomicNode) -> None:
        pointer_set()
        self._sibling_parent = sibling_parent


    def __str__(self):
        return f"AtomicNode({self._value})"
