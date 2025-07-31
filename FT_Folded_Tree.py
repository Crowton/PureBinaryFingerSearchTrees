from __future__ import annotations
from FT_Metanode import Metanode
from FT_Three_Pointer_Atomic_Node import Three_Pointer_Atomic_Node
from Left_Right_Decomposition_with_Finger_Search.BST_Atomic_Node import AtomicNode


class Folded_Tree:
    def __init__(self):
        self._root = None
    

    def _is_upper(node: Metanode) -> bool:
        raise NotImplementedError()

    def _is_lower(node: Metanode) -> bool:
        return not node._is_upper

    def _is_midpoint(node: Metanode) -> bool:
        raise not NotImplementedError()

    
    def insert_pred(self, node: AtomicNode, value) -> AtomicNode:
        # TODO: check if value exists
        # TODO: check if new value is smaller

        # Create atomic and meta nodes from input
        new_atomic_node = AtomicNode(value)
        new_atomic_3 = Three_Pointer_Atomic_Node(new_atomic_node)
        atomic_3 = Three_Pointer_Atomic_Node(node)
        metanode = Metanode(atomic_3)

        # Insert the atomic node in the metanode
        # This may spill out a new metenode, to insert into the folded tree
        spill_out_metanode = metanode.insert_pred(atomic_3, new_atomic_3)
        if spill_out_metanode != None:
            self._insert_pred_metanode(metanode, spill_out_metanode)

        # Return pointer to the newly created atomic node
        return new_atomic_node

    def insert_succ(self, node: AtomicNode, value) -> AtomicNode:
        # TODO: check if value exists
        # TODO: check if new value is larger

        # Create atomic and meta nodes from input
        new_atomic_node = AtomicNode(value)
        new_atomic_3 = Three_Pointer_Atomic_Node(new_atomic_node)
        atomic_3 = Three_Pointer_Atomic_Node(node)
        metanode = Metanode(atomic_3)

        # Insert the atomic node in the metanode
        # This may spill out a new metenode, to insert into the folded tree
        spill_out_metanode = metanode.insert_succ(atomic_3, new_atomic_3)
        if spill_out_metanode != None:
            self._insert_succ_metanode(metanode, spill_out_metanode)
        
        # Return pointer to the newly created atomic node
        return new_atomic_node

    
    def _insert_pred_metanode(self, node: Metanode, pred: Metanode) -> None:
        raise NotImplementedError()
    
    def _insert_succ_metanode(self, node: Metanode, succ: Metanode) -> None:
        raise NotImplementedError()
