from __future__ import annotations

from Pointer_Counting import pointer_get, bit_get
import Many_Pointers_Red_Black_Tree
import Finger_Search

import util
from util import link_left, link_right


class Mock_Node:
    def __init__(self, folded_tree, value, is_red: bool = True, is_left_path: bool = True):
        self._value = value
        self._folded_tree = folded_tree
        self._parent = None
        self._left = None
        self._right = None
        self._is_red = is_red
        self._is_left_path = is_left_path

    @property
    def value(self):
        return self._value
    
    @property
    def parent(self):
        pointer_get()
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        assert not self._folded_tree._finalized
        self._parent = parent

    @property
    def left(self):
        pointer_get()
        return self._left

    @left.setter
    def left(self, left):
        assert not self._folded_tree._finalized
        self._left = left

    @property
    def right(self):
        pointer_get()
        return self._right

    @right.setter
    def right(self, right):
        assert not self._folded_tree._finalized
        self._right = right

    @property
    def is_red(self):
        bit_get()
        return self._is_red

    @property
    def is_black(self):
        bit_get()
        return not self._is_red
    
    @property
    def is_left_path(self):
        bit_get()
        return self._is_left_path
    
    @property
    def is_right_path(self):
        bit_get()
        return not self._is_left_path


    @property
    def is_path_root(self) -> bool:
        return self.parent is None or self.is_left_path != self.parent.is_left_path

    @property
    def _is_last_lower_short_circuit(self) -> bool:
        return self.is_lower \
            and (self.left  is None or self.left.is_left_path  != self.is_left_path) \
            and (self.right is None or self.right.is_left_path != self.is_left_path)

    @property
    def _is_last_lower_no_short_circuit(self) -> bool:
        return self.is_lower \
            & (self.left  is None or self.left.is_left_path  != self.is_left_path) \
            & (self.right is None or self.right.is_left_path != self.is_left_path)

    is_last_lower = _is_last_lower_short_circuit

    @property
    def is_upper(self) -> bool:
        # Branching on the left or right path
        if self.is_left_path:
            # If the left child is a left path, this is an upper node
            if self.left != None and self.left.is_left_path:
                return True

            # If the path is a single node, the left is None, but then the node must be the path root
            # Just cheking if the left is None fails, as the last lower node may also have no left child
            if self.is_path_root:
                return True

            # Otherwise, the node is lower
            return False
        
        else:
            # If the right child is a right path, this is an upper node
            if self.right != None and self.right.is_right_path:
                return True

            # If the path is a single node, the right is None, but then the node must be the path root
            # Just cheking if the right is None fails, as the last lower node may also have no right child
            if self.is_path_root:
                return True

            # Otherwise, the node is lower
            return False
    
    @property
    def is_lower(self) -> bool:
        return not self.is_upper

    @property
    def unfolded_parent(self) -> Mock_Node|None:
        # Root of the tree is preserved
        if self.parent is None:
            return None
        
        # Path roots have parent in other paths
        if self.is_path_root:
            p = self.parent
            # Upper parents and last lower node preserves child
            # Pure upper is simple
            if p.is_upper:
                return p
            
            # Last lower node is dependent on path type,
            # and is only the parent if self is the correct of the two children
            if p.is_last_lower:
                if p.is_left_path and p.right == self:
                    return p
                if p.is_right_path and p.left == self:
                    return p

            # Lower parents swap children
            # Traverse up to the next lower node, over at most one upper node
            pp = p.parent
            if pp.is_lower:
                return pp

            return pp.parent

        # Parents of upper nodes and the last lower node is the next upper node above
        if self.is_upper or self.is_last_lower:
            p = self.parent
            while not p.is_upper:
                p = p.parent
            
            return p
        
        # Parents of lower nodes but the last is below
        # Below direction is path type dependent
        # At most one upper node is skipped over
        if self.is_left_path:
            r = self.right
            if r.is_lower:
                return r
            
            return r.left
        
        else:
            l = self.left
            if l.is_lower:
                return l

            return l.right 


    @property
    def unfolded_left(self) -> Mock_Node|None:
        # Path specific
        # Left paths have left children nodes on the path
        if self.is_left_path:
            # Upper nodes lefts are the upper node below, but the last upper node
            # Edge case: path is single node, where the left child is None
            if self.is_upper:
                b = self.left
                while b is not None and b.is_lower and not b.is_last_lower:
                    b = b.right
                
                return b

            # Lower nodes left are the lower node above them, at most one upper node is skipped over
            # The smallest lower has no left child. The parent is then the path root
            a = self.parent
            if a.is_path_root:
                return None
            
            if a.is_upper:
                a = a.parent

            return a

        # Right paths have nodes of the path
        # Upper nodes and the last lower node preserve the left child
        if self.is_upper or self.is_last_lower:
            return self.left
        
        # Lower nodes move left child to the right of the next lower node below
        # At most one upper node is skipped over
        b = self.left
        if b.is_upper:
            b = b.right
        
        return b.right


    @property
    def unfolded_right(self) -> Mock_Node|None:
        # Path specific
        # Right paths have right children nodes on the path
        if self.is_right_path:
            # Upper nodes rights are the upper node below, but the last upper node
            # Edge case: path is single node, where the right child is None
            if self.is_upper:
                b = self.right
                while b is not None and b.is_lower and not b.is_last_lower:
                    b = b.left
                
                return b

            # Lower nodes right are the lower node above them, at most one upper node is skipped over
            # The smallest lower has no right child. The parent is then the path root
            a = self.parent
            if a.is_path_root:
                return None
            
            if a.is_upper:
                a = a.parent

            return a

        # Left paths have nodes of the path
        # Upper nodes and the last lower node preserve the right child
        if self.is_upper or self.is_last_lower:
            return self.right
        
        # Lower nodes move left child to the right of the next lower node below
        # At most one upper node is skipped over
        b = self.right
        if b.is_upper:
            b = b.left
        
        return b.left


    @property
    def predecessor(self) -> Mock_Node|None:
        # Predecessor is the largest node in the left subtree
        l = self.unfolded_left
        if l is not None:
            # Find the right path, which is rooted as the unfolded right child of l
            # Edgecase, the right child is None, in which case l is the largest node
            lr = l.unfolded_right
            if lr is None:
                return l
            
            lr_largest = lr.right
            # Edgecase, if path is a single node
            if lr_largest is None:
                return lr
            return lr_largest

        # Predecessor is above
        # If on a right path, the predecessor is then the parent
        if self.is_right_path:
            return self.unfolded_parent

        # Otherwise, the node is the smallest node on a left path
        # Step to the path root
        p = self
        if not p.is_path_root:
            p = p.parent
        
        # Step to the unfolded parent, on the right path. If this is none, there is no predecessor
        # This check only fails if the main path is a left path (which for this implementation it is)
        rp = p.unfolded_parent
        if rp is None:
            return None
        
        # The predecessor must then be the parent of rp, which may be none if there is no predecessor
        return rp.unfolded_parent


    @property
    def successor(self) -> Mock_Node|None:
        # Successor is the smallest node in the right subtree
        r = self.unfolded_right
        if r is not None:
            # Find the left path, which is rooted as the unfolded left child of r
            # Edgecase, the left child is None, in which case r is the smallest node
            rl = r.unfolded_left
            if rl is None:
                return r
            
            rl_smallest = rl.left
            # Edgecase, if path is a single node
            if rl_smallest is None:
                return rl
            return rl_smallest

        # Successor is above
        # If on a left path, the successor is then the parent
        if self.is_left_path:
            return self.unfolded_parent

        # Otherwise, the node is the largest node on a right path
        # Step to the path root
        p = self
        if not p.is_path_root:
            p = p.parent
        
        # Step to the unfolded parent, on the left path. If this is none, there is no successor
        # This check only fails if the main path is a right path (which for this implementation it is not)
        lp = p.unfolded_parent
        if lp is None:
            return None
        
        # The successor must then be the parent of lp, which may be none if there is no successor
        return lp.unfolded_parent


    def __repr__(self):
        return f"Mock_Node({self._value}, {'BR'[self._is_red]}, {'RL'[self._is_left_path]})"


class Mock_Node_as_Unfolded:
    def __init__(self, node):
        self._node = node
    
    @staticmethod
    def wrap(node):
        if node is None:
            return None
        return Mock_Node_as_Unfolded(node)

    @staticmethod
    def unwrap(wrapped_node):
        if wrapped_node is None:
            return None
        return wrapped_node._node

    @property
    def value(self):
        return self._node.value

    @property
    def parent(self):
        return Mock_Node_as_Unfolded.wrap(self._node.unfolded_parent)

    @property
    def left(self):
        return Mock_Node_as_Unfolded.wrap(self._node.unfolded_left)
    
    @property
    def right(self):
        return Mock_Node_as_Unfolded.wrap(self._node.unfolded_right)

    @property
    def pred(self):
        return Mock_Node_as_Unfolded.wrap(self._node.predecessor)
    
    @property
    def succ(self):
        return Mock_Node_as_Unfolded.wrap(self._node.successor)
    

    def __eq__(self, other):
        return isinstance(other, Mock_Node_as_Unfolded) and self._node == other._node

    def __repr__(self):
        return f"Mock_Node_as_Unfolded({self._node.value})"


class Mock_Folded_Tree:
    def __init__(self):
        self._root = None
        self._finalized = False


    # ---------------------------------------------
    #        Create Folded Tree from RB Tree
    # ---------------------------------------------

    @staticmethod
    def create_folded_tree(rb_tree: Many_Pointers_Red_Black_Tree.Red_Black_Tree, main_path_is_left=True) -> Mock_Folded_Tree:
        def convert_left_path(folded_tree: Mock_Folded_Tree, root: Many_Pointers_Red_Black_Tree.Red_Black_Node) -> Mock_Node:
            # Empty path is converted to empty node
            if root == None:
                return None
            
            # Fetch top and bottom of the path
            next_top = root
            next_bot = root
            while next_bot.left != None:
                next_bot = next_bot.left

            # Helper variables
            new_root = None
            last_path_node = None
            last_bot_right_tree = None

            # As long as next_top is on or above next_bot, continue
            while next_top.parent != next_bot:
                # ---- Top path chunk ----
                # Create node
                new_top_node = Mock_Node(folded_tree, next_top.value, is_red=next_top.is_red, is_left_path=True)
                
                if new_root is None:
                    new_root = new_top_node

                # Set parent
                if last_path_node is not None:
                    link_right(last_path_node, new_top_node)
                else:
                    new_top_node.parent = None

                # Set temporary left
                # new_top_node.left = None

                # Set right
                new_top_node_right = convert_right_path(folded_tree, next_top.right)
                link_right(new_top_node, new_top_node_right)
                
                # If collision, final lower chunk is double or triple, and this was a lower node
                if next_top == next_bot:
                    new_last_bot_right_tree = convert_right_path(folded_tree, last_bot_right_tree)
                    link_left(new_top_node, new_last_bot_right_tree)
                    last_bot_right_tree = None
                    break

                # Advance top node
                next_top = next_top.left

                # ---- Bottom path chunk ----
                # Create node
                new_bot_node = Mock_Node(folded_tree, next_bot.value, is_red=next_bot.is_red, is_left_path=True)
                last_path_node = new_bot_node

                # Set parent
                link_left(new_top_node, new_bot_node)

                # Set left
                new_last_bot_right_tree = convert_right_path(folded_tree, last_bot_right_tree)
                link_left(new_bot_node, new_last_bot_right_tree)
                last_bot_right_tree = next_bot.right

                # Set temporary right
                # new_bot_node.right = None

                # If collision, last bottom chunk is single node
                if next_top == next_bot:
                    new_last_bot_right_tree = convert_right_path(folded_tree, last_bot_right_tree)
                    link_right(new_bot_node, new_last_bot_right_tree)
                    last_bot_right_tree = None
                    break

                # Advance bottom node
                next_bot = next_bot.parent

                # If node is red, chunk needs next node
                if new_bot_node.is_red:
                    assert next_bot.is_black

                    # Create node
                    new_bot_bot_node = Mock_Node(folded_tree, next_bot.value, is_red=next_bot.is_red, is_left_path=True)
                    last_path_node = new_bot_bot_node

                    # Set parent
                    link_right(new_bot_node, new_bot_bot_node)

                    # Set left
                    new_last_bot_bot_right_tree = convert_right_path(folded_tree, last_bot_right_tree)
                    link_left(new_bot_bot_node, new_last_bot_bot_right_tree)
                    last_bot_right_tree = next_bot.right

                    # Set temporary right
                    # new_bot_bot_node.right = None

                    # If collision, last bottom chunk is double node
                    if next_top == next_bot:
                        new_last_bot_right_tree = convert_right_path(folded_tree, last_bot_right_tree)
                        link_right(new_bot_bot_node, new_last_bot_right_tree)
                        last_bot_right_tree = None
                        break

                    # Advance bottom node
                    next_bot = next_bot.parent

            # Check nothing is forgotten
            assert last_bot_right_tree == None
            assert new_root != None

            # Return the new root
            return new_root

        
        def convert_right_path(folded_tree: Mock_Folded_Tree, root: Many_Pointers_Red_Black_Tree.Red_Black_Node) -> Mock_Node:
            # Empty path is converted to empty node
            if root == None:
                return None
            
            # Fetch top and bottom of the path
            next_top = root
            next_bot = root
            while next_bot.right != None:
                next_bot = next_bot.right

            # Helper variables
            new_root = None
            last_path_node = None
            last_bot_left_tree = None

            # As long as next_top is on or above next_bot, continue
            while next_top.parent != next_bot:
                # ---- Top path chunk ----
                # Create node
                new_top_node = Mock_Node(folded_tree, next_top.value, is_red=next_top.is_red, is_left_path=False)
                
                if new_root is None:
                    new_root = new_top_node

                # Set parent
                if last_path_node is not None:
                    link_left(last_path_node, new_top_node)
                else:
                    new_top_node.parent = None

                # Set temporary right
                # new_top_node.right = None

                # Set left
                new_top_node_left = convert_left_path(folded_tree, next_top.left)
                link_left(new_top_node, new_top_node_left)
                
                # If collision, final lower chunk is double or triple, and this was a lower node
                if next_top == next_bot:
                    new_last_bot_left_tree = convert_left_path(folded_tree, last_bot_left_tree)
                    link_right(new_top_node, new_last_bot_left_tree)
                    last_bot_left_tree = None
                    break

                # Advance top node
                next_top = next_top.right

                # ---- Bottom path chunk ----
                # Create node
                new_bot_node = Mock_Node(folded_tree, next_bot.value, is_red=next_bot.is_red, is_left_path=False)
                last_path_node = new_bot_node

                # Set parent
                link_right(new_top_node, new_bot_node)

                # Set right
                new_last_bot_left_tree = convert_left_path(folded_tree, last_bot_left_tree)
                link_right(new_bot_node, new_last_bot_left_tree)
                last_bot_left_tree = next_bot.left

                # Set temporary left
                # new_bot_node.left = None

                # If collision, last bottom chunk is single node
                if next_top == next_bot:
                    new_last_bot_left_tree = convert_left_path(folded_tree, last_bot_left_tree)
                    link_left(new_bot_node, new_last_bot_left_tree)
                    last_bot_left_tree = None
                    break

                # Advance bottom node
                next_bot = next_bot.parent

                # If node is red, chunk needs next node
                if new_bot_node.is_red:
                    assert next_bot.is_black

                    # Create node
                    new_bot_bot_node = Mock_Node(folded_tree, next_bot.value, is_red=next_bot.is_red, is_left_path=False)
                    last_path_node = new_bot_bot_node

                    # Set parent
                    link_left(new_bot_node, new_bot_bot_node)

                    # Set right
                    new_last_bot_bot_left_tree = convert_left_path(folded_tree, last_bot_left_tree)
                    link_right(new_bot_bot_node, new_last_bot_bot_left_tree)
                    last_bot_left_tree = next_bot.left

                    # Set temporary left
                    # new_bot_bot_node.left = None

                    # If collision, last bottom chunk is double node
                    if next_top == next_bot:
                        new_last_bot_left_tree = convert_left_path(folded_tree, last_bot_left_tree)
                        link_left(new_bot_bot_node, new_last_bot_left_tree)
                        last_bot_left_tree = None
                        break

                    # Advance bottom node
                    next_bot = next_bot.parent

            # Check nothing is forgotten
            assert last_bot_left_tree == None
            assert new_root != None

            # Return the new root
            return new_root


        folded_tree = Mock_Folded_Tree()
        if main_path_is_left:
            folded_tree._root = convert_left_path(folded_tree, rb_tree._root)
        else:
            folded_tree._root = convert_right_path(folded_tree, rb_tree._root)
        folded_tree._finalized = True
        return folded_tree


    # ---------------------------------------------
    #                   Searching
    # ---------------------------------------------

    def search(self, value) -> Mock_Node|None:
        at = self._root
        while at != None:
            if at.value == value:
                return at
            elif value < at.value:
                at = at.left
            else:
                at = at.right
        return None

    @staticmethod
    def finger_search(from_node: Mock_Node, value, algorithm=Finger_Search.Version.LCA) -> Mock_Node|None:
        if algorithm == Finger_Search.Version.LCA:
            return Finger_Search.finger_search(from_node, value, algorithm=Finger_Search.Version.LCA)

        wrapped_from = Mock_Node_as_Unfolded.wrap(from_node)
        wrapped_to = Finger_Search.finger_search(wrapped_from, value, algorithm=algorithm)
        return Mock_Node_as_Unfolded.unwrap(wrapped_to)

    # ---------------------------------------------
    #                   Iterators
    # ---------------------------------------------

    def __iter__(self):
        yield from self._inorder_traversal(self._root)
    
    def _inorder_traversal(self, node: Mock_Node):
        if node == None:
            return
        yield from self._inorder_traversal(node.left)
        yield node
        yield from self._inorder_traversal(node.right)


    # ---------------------------------------------
    #                   Printing
    # ---------------------------------------------

    def _to_tuple(self, colored=False):
        def inner_to_tuple(node: Mock_Node) -> tuple:
            if node == None:
                return ()
            s = f"{node.value} ({'RL'[node.is_left_path]})"
            if colored and node.is_red:
                s = f"\033[31m{s}\033[0m"
            return (s, inner_to_tuple(node.left), inner_to_tuple(node.right))

        return inner_to_tuple(self._root)
    
    def print(self, colored=False):
        util.print_ascii_tree(
            self._to_tuple(colored=colored),
            str_len=util.visible_str_len
        )
    

    # ---------------------------------------------
    #                 Validation
    # ---------------------------------------------

    def is_valid(self, verbose=False, main_path_is_left=True) -> bool:
        a = self._all_pointers_set()
        b = self._is_sorted()
        c = self._is_valid_folded(main_path_is_left)

        if verbose:
            print(f"All pointers set: {a}")
            print(f"Sorted: {b}")
            print(f"Valid folded: {c}")
        
        return a and b and c

    def _all_pointers_set(self) -> bool:
        def all_pointers_set_from(node: Mock_Node) -> bool:
            if node == None:
                return True
            if node.left != None and node.left.parent != node or node.right != None and node.right.parent != node:
                return False
            return all_pointers_set_from(node.left) and all_pointers_set_from(node.right)

        return all_pointers_set_from(self._root)

    def _is_sorted(self) -> bool:
        def node_within_bounds(node: Mock_Node, lower_bound: float|None, upper_bound: float|None) -> bool:
            if node == None:
                return True
            if lower_bound != None and not lower_bound < node.value:
                return False
            if upper_bound != None and not node.value < upper_bound:
                return False
            
            return node_within_bounds(node.left, lower_bound, node.value) and node_within_bounds(node.right, node.value, upper_bound)
        
        return node_within_bounds(self._root, None, None)
    
    def _is_valid_folded(self, main_path_is_left: bool) -> bool:
        def correct_left_path_fold_from(path_root: Mock_Node) -> bool:
            # Empty paths are correct
            if path_root == None:
                return True
            
            # Node must be left type
            if not path_root.is_left_path:
                return False

            # Single node is correct
            if path_root.left == None:
                return True and correct_right_path_fold_from(path_root.right)

            # Traverse down the left path
            node = path_root
            while True:
                # First node must be upper
                if not node.is_upper:
                    return False
                
                # The upper node must be a left type
                if not node.is_left_path:
                    return False

                # The right child must be a valid right path
                if not correct_right_path_fold_from(node.right):
                    return False
                
                # The left path must be a lower chunk
                if node.left == None:
                    return False
                node = node.left
                if not node.is_lower:
                    return False
                
                # Traverse the lower chunk and extract the colors
                colors = []
                while node != None and node.is_lower:
                    # The node must be a left type
                    if not node.is_left_path:
                        return False

                    # Extract color
                    colors.append(node.is_red)

                    # Left subtree must be right folded
                    if not correct_right_path_fold_from(node.left):
                        return False
                    
                    # If node is upper, stop
                    if node.right == None or node.right.is_right_path:
                        break
                    node = node.right
                
                lower_len = len(colors)

                # If standing on an upper node, chunk must be not the last
                if node.is_upper:
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

                    # If three elements in chunk, and top node is black, then another fold is needed
                    if len(colors) == 3 and colors[0] == False:
                        return False

                    # Check the final right tree
                    if not correct_right_path_fold_from(node.right):
                        return False
                    
                    break

            return True

        def correct_right_path_fold_from(path_root: Mock_Node) -> bool:
            # Empty paths are correct
            if path_root == None:
                return True
            
            # Node must be right type
            if not path_root.is_right_path:
                return False

            # Single node is correct
            if path_root.right == None:
                return True and correct_left_path_fold_from(path_root.left)

            # Traverse down the right path
            node = path_root
            while True:
                # First node must be upper
                if not node.is_upper:
                    return False
                
                # The upper node must be a right type
                if not node.is_right_path:
                    return False

                # The left child must be a valid left path
                if not correct_left_path_fold_from(node.left):
                    return False
                
                # The right path must be a lower chunk
                if node.right == None:
                    return False
                node = node.right
                if not node.is_lower:
                    return False
                
                # Traverse the lower chunk and extract the colors
                colors = []
                while node != None and node.is_lower:
                    # The node must be a right type
                    if not node.is_right_path:
                        return False

                    # Extract color
                    colors.append(node.is_red)

                    # Right subtree must be left folded
                    if not correct_left_path_fold_from(node.right):
                        return False
                    
                    # If node is upper, stop
                    if node.left == None or node.left.is_left_path:
                        break
                    node = node.left
                
                lower_len = len(colors)

                # If standing on an upper node, chunk must be not the last
                if node.is_upper:
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

                    # If three elements in chunk, and top node is black, then another fold is needed
                    if len(colors) == 3 and colors[0] == False:
                        return False

                    # Check the final left tree
                    if not correct_left_path_fold_from(node.left):
                        return False
                    
                    break

            return True


        if main_path_is_left:
            return correct_left_path_fold_from(self._root)
        else:
            return correct_right_path_fold_from(self._root)



if __name__ == "__main__":
    tree = Many_Pointers_Red_Black_Tree.Red_Black_Tree()
    import random
    random.seed(42)
    values = list(range(50))
    random.shuffle(values)
    for v in values:
        tree.insert(v)
    main_path_is_left = True


    print("RB Tree:")
    tree.print(colored=True)
    print()

    folded_tree = Mock_Folded_Tree.create_folded_tree(tree, main_path_is_left=main_path_is_left)

    print("Folded Tree:")
    folded_tree.print(colored=True)
    print()

    print("Validation:")
    v = folded_tree.is_valid(verbose=True, main_path_is_left=main_path_is_left)
    print(f"Valid: {v}")
    print()


    node_7 = folded_tree.search(7)
    print("Node 7:", node_7)
    found_node = Mock_Folded_Tree.finger_search(node_7, 20)
    assert found_node.value == 20
    print("Found node:", found_node)
