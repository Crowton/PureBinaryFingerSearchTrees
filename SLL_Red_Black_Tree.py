from __future__ import annotations

from SLL_Atomic_Node import AtomicNode
from SLL_Metanode import Metanode

import Finger_Search
import util


class RB_Tree:
    def __init__(self):
        self._root = None


    # ---------------------------------------------
    #               Size functions
    # ---------------------------------------------

    # TODO: refactor to use iterator?
    def size(self):
        def inner(node: Metanode):
            if node == None:
                return 0
            
            return 1 + inner(node.left) + inner(node.right)

        return inner(self._root)

    def atomic_size(self):
        def inner(node: Metanode):
            if node == None:
                return 0
            
            return node.size() + inner(node.left) + inner(node.right)

        return inner(self._root)


    # ---------------------------------------------
    #                 Rotations
    # ---------------------------------------------

    def _left_rotate(self, node: Metanode) -> None:
        y = node.right
        node.right = y.left
        if y.left != None:
            y.left.parent = node
        y.parent = node.parent
        if node.parent == None:
            self._root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def _right_rotate(self, node: Metanode) -> None:
        y = node.left
        node.left = y.right
        if y.right != None:
            y.right.parent = node
        y.parent = node.parent
        if node.parent == None:
            self._root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y


    # ---------------------------------------------
    #                  Search
    # ---------------------------------------------

    def exact_search(self, value) -> AtomicNode:
        at = self._root
        while at != None:
            if at.must_contain(value):
                return at.exact_search(value)
            if value < at.smallest_value():
                at = at.left
            else:
                at = at.right
        return None

    def predesessor(self, value) -> AtomicNode:
        at = self._root
        while at != None:
            if at.must_contain(value):
                return at.predesessor_search(value)
            if value < at.smallest_value():
                at = at.left
            else:
                at = at.right
        return None

    def successor(self, value) -> AtomicNode:
        pred = self.predesessor(value)

        # If pred is None, the succ may be the smallest node
        if pred == None:
            at = self._root
            smallest = None
            while at != None:
                smallest = at
                at = at.left
            if smallest != None:
                smallest_atomic = smallest.smallest_atomic()
                if value <= smallest_atomic.value:
                    return smallest_atomic
            return None
        
        # Pred may be succ if value is equal
        if pred.value == value:
            return pred

        # Otherwise, return succ
        succ = pred.next
        assert pred.value < value
        assert succ == None or value <= succ.value
        return succ


    def node_predesessor(self, node: AtomicNode) -> AtomicNode:
        assert node != None
        return Metanode(node).node_predesessor(node)

    def node_successor(self, node: AtomicNode) -> AtomicNode:
        assert node != None
        return Metanode(node).node_successor(node)


    def finger_search(self, node: AtomicNode, value, algorithm=Finger_Search.Version.PAPER) -> AtomicNode:
        metanode = Metanode(node)
        found_metanode = Finger_Search.finger_search(metanode, value, algorithm=algorithm)
        if found_metanode == None:
            return None
        return found_metanode.predesessor_search(value)


    # ---------------------------------------------
    #                  Update
    # ---------------------------------------------

    def insert(self, value) -> AtomicNode:
        # Create new node for the value
        new_node = AtomicNode(value)
        
        # If tree is empty, set root and return
        if self._root == None:
            new_node.data = new_node
            self._root = Metanode(new_node)
            return new_node
        
        # Locate predessor in the tree and insert
        pred_node = self.predesessor(value)
        if pred_node != None:
            if pred_node.value == value:
                return pred_node
            self._insert_succ_node(pred_node, new_node)

        # If no predessor, then the new node is the smallest
        # The successor must therefore exist
        else:
            succ_node = self.successor(value)
            assert succ_node.value != value
            self._insert_pred_node(succ_node, new_node)

        # Return
        return new_node

    def insert_pred(self, node: AtomicNode, value) -> AtomicNode:
        assert node != None
        assert value <= node.value

        # Check if value is already present at this location
        if node.value == value:
            return node
        old_pred_node = self.node_predesessor(node)
        if old_pred_node != None:
            assert old_pred_node.value <= value
            if old_pred_node.value == value:
                return old_pred_node
        
        # Insert the new node
        new_node = AtomicNode(value)
        self._insert_pred_node(node, new_node)
        return new_node

    # TODO: check if node value is present?
    def _insert_pred_node(self, node: AtomicNode, pred: AtomicNode) -> None:
        # Insert pred into the metanode
        # Fecth the metanode for the node
        # If node is the root, then we need to use the root metanode
        meta = Metanode(node)
        if meta == self._root:
            meta = self._root
        
        updates_head, spill_out = meta.insert_pred(node, pred)

        # If head is updated on a proper metanode, move incomming datapointers
        if updates_head and meta._is_proper:
            # TODO: this may be more efficient and readable if saving list of atomic nodes to update
            parent = meta.parent
            if parent != None:
                if parent.left == meta:
                    parent.left = meta
                else:
                    parent.right = meta
            if meta.left != None:
                meta.left.parent = meta
            if meta.right != None:
                meta.right.parent = meta
            if meta.pred != None:
                meta.pred.succ = meta
            if meta.succ != None:
                meta.succ.pred = meta

        # If spill_out is None, then we are done
        if spill_out == None:
            return
        
        # Otherwise, we need to insert the new metanode
        # The spill_out is the successor
        self._insert_succ_spill_out(meta, spill_out)

    def insert_succ(self, node: AtomicNode, value) -> AtomicNode:
        assert node != None
        assert node.value <= value

        # Check if value is already present at this location
        if node.value == value:
            return node
        old_succ_node = self.node_successor(node)
        if old_succ_node != None:
            assert value <= old_succ_node.value
            if old_succ_node.value == value:
                return old_succ_node

        # Insert the new node
        new_node = AtomicNode(value)
        self._insert_succ_node(node, new_node)
        return new_node

    # TODO: check if node value is present?
    def _insert_succ_node(self, node: AtomicNode, succ: AtomicNode) -> None:
        # Insert succ into the metanode
        # Fecth the metanode for the node
        # If node is the root, then we need to use the root metanode
        meta = Metanode(node)
        if meta == self._root:
            meta = self._root
        
        spill_out = meta.insert_succ(node, succ)

        # If spill_out is None, then we are done
        if spill_out == None:
            return
        
        # Otherwise, we need to insert the new metanode
        self._insert_succ_spill_out(meta, spill_out)

    def _insert_succ_spill_out(self, meta: Metanode, spill_out: Metanode) -> None:
        # Find a leaf to insert the new metanode
        # If right subtree is empty, insert the node here
        if meta.right == None:
            meta.right = spill_out
            spill_out.parent = meta
        
        # Otherwise, there must be something on the right
        # The succ of meta is the smallest value in the right subtree
        # Then the left child of succ is empty and must contain the spill
        else:
            succ = meta.succ
            succ.left = spill_out
            spill_out.parent = succ
        
        # Link the new metanode into the succ and pred pointers
        succ = meta.succ
        meta.succ = spill_out
        spill_out.pred = meta
        spill_out.succ = succ
        if succ != None:
            succ.pred = spill_out

        # Color the spill_out red, and call fixup
        spill_out.set_red()
        self._insert_fixup(spill_out)

    def _insert_fixup(self, z: Metanode) -> None:
        while z.parent != None and z.parent.is_red:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y != None and y.is_red:
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y != None and y.is_red:
                    z.parent.set_black()
                    y.set_black()
                    z.parent.parent.set_red()
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.set_black()
                    z.parent.parent.set_red()
                    self._left_rotate(z.parent.parent)
        self._root.set_black()


    def delete(self, value) -> None:
        node = self.search(value)
        if node == None:
            return
        self.delete_node(node)
    
    def delete_node(self, node: AtomicNode) -> None:
        raise NotImplementedError()

    def _delete_fixup(self, x: Metanode, dummy: Metanode) -> None:
        raise NotImplementedError()


    # ---------------------------------------------
    #                Meta operations
    # ---------------------------------------------

    def __eq__(self, value):
        if not isinstance(value, RB_Tree):
            return False
        return self._root == value._root
    
    def _to_tuple(self, colored=False, full=False):
        def inner(node: Metanode):
            if node == None:
                return ()
            s = str(node)
            if full:
                s = node.full_string()
            if colored and node._is_proper and node.is_red:
                s = "\033[91m" + s + "\033[0m"
            return (s, inner(node.left), inner(node.right))

        return inner(self._root)

    def print(self, colored=False, full=False) -> None:
        util.print_ascii_tree(
            self._to_tuple(colored=colored, full=full),
            str_len=util.visible_str_len
        )


    # ---------------------------------------------
    #                  Validation
    # ---------------------------------------------

    def is_valid(self, verbose=False) -> bool:
        a = self._all_metanode_is_valid()
        b = self._all_pointers_set()
        c = self._root_is_black()
        d = self._no_two_red()
        e = self._black_height() != -1
        f = self._is_sorted()

        if verbose:
            print("All metanodes are valid:", a)
            print("All pointers are set:", b)
            print("Root is black:", c)
            print("No two red nodes are adjacent:", d)
            print("Black height is consistent:", e)
            print("Nodes are sorted:", f)
        
        return a and b and c and d and e and f

    def _all_metanode_is_valid(self) -> bool:
        return self._all_metanode_is_valid_from(self._root)

    def _all_metanode_is_valid_from(self, node: Metanode) -> bool:
        if node == None:
            return True
        if not node.is_valid(verbose=True):
            return False
        return self._all_metanode_is_valid_from(node.left) and self._all_metanode_is_valid_from(node.right)

    def _all_pointers_set(self) -> bool:
        return self._all_pointers_set_from(self._root)

    def _all_pointers_set_from(self, node: Metanode) -> bool:
        if node == None:
            return True
        if node.left != None and node.left.parent != node or node.right != None and node.right.parent != node:
            return False
        return self._all_pointers_set_from(node.left) and self._all_pointers_set_from(node.right)

    def _root_is_black(self) -> bool:
        return self._root == None or not self._root._is_proper or self._root.is_black

    def _black_height(self) -> int:
        if not self._root._is_proper:
            return 1
        return self._black_height_from(self._root)

    def _black_height_from(self, node: Metanode) -> int:
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
        return not self._root._is_proper or self._no_two_red_from(self._root)

    def _no_two_red_from(self, node: Metanode) -> bool:
        if node == None:
            return True
        if node.is_red and node.parent.is_red:
            return False
        return self._no_two_red_from(node.left) and self._no_two_red_from(node.right)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: Metanode, lower_bound: float|None, upper_bound: float|None) -> bool:
            if node == None:
                return True
            if lower_bound != None and not lower_bound < node.smallest_value():
                return False
            if upper_bound != None and not node.largest_value() < upper_bound:
                return False
            
            return node_within_bounds(node.left, lower_bound, node.smallest_value()) and node_within_bounds(node.right, node.largest_value(), upper_bound)
        
        return node_within_bounds(self._root, None, None)
