from __future__ import annotations

from Pointer_Counting import pointer_get, pointer_set


class AtomicNode:
    def __init__(self, value) -> None:
        self._value = value
        self._next = None
        self._data = None
    
    
    @property
    def value(self):
        return self._value

    @property
    def next(self) -> AtomicNode:
        pointer_get()
        return self._next
    
    @next.setter
    def next(self, next: AtomicNode) -> None:
        pointer_set()
        self._next = next


    @property
    def data(self) -> AtomicNode:
        pointer_get()
        return self._data
    
    @data.setter
    def data(self, data: AtomicNode) -> None:
        pointer_set()
        self._data = data


    def __str__(self):
        return f"AtomicNode({self._value})"
