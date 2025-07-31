from __future__ import annotations

from Pointer_Counting import pointer_get, pointer_set

import util


class Level_Internal_Node:
    def __init__(self, splitters=None, children=None):
        if splitters is None:
            splitters = []
        self._splitters = splitters
        self._parent = None
        if children is None:
            children = []
        self._children = children
        self._pred = None
        self._succ = None

    @property
    def splitters(self):
        return self._splitters

    @splitters.setter
    def splitters(self, splitters):
        self._splitters = splitters
    
    @property
    def parent(self):
        pointer_get()
        return self._parent

    @parent.setter
    def parent(self, parent):
        pointer_set()
        self._parent = parent

    @property
    def degree(self):
        return len(self._children)

    def get_child(self, idx):
        pointer_get()
        return self._children[idx]
    
    def set_child(self, idx, child):
        pointer_set()
        self._children[idx] = child

    def update_child_with_splitter(self, idx, child, splitter):
        pointer_set()
        self._children[idx] = child
        self._splitters[idx] = splitter

    def insert_child_with_splitter(self, idx, child, splitter):
        pointer_set()
        self._children.insert(idx, child)
        self._splitters.insert(idx, splitter)

    @property
    def pred(self):
        pointer_get()
        return self._pred
    
    @pred.setter
    def pred(self, pred):
        pointer_set()
        self._pred = pred
    
    @property
    def succ(self):
        pointer_get()
        return self._succ

    @succ.setter
    def succ(self, succ):
        pointer_set()
        self._succ = succ

    def __repr__(self):
        return f"Level_Interval_Node({self.splitters})"


class Level_Leaf_Node:
    def __init__(self, value):
        self._value = value
        self._parent = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
    
    @property
    def parent(self):
        pointer_get()
        return self._parent

    @parent.setter
    def parent(self, parent):
        pointer_set()
        self._parent = parent
    
    def __repr__(self):
        return f"Level_Leaf_Node({self.value})"


class Level_Linked_ab_Tree:
    def __init__(self):
        self._root = None
    

    # ---------------------------------------------
    #                   Helpers
    # ---------------------------------------------

    def size(self):
        def inner(node):
            if node is None:
                return 0
            if isinstance(node, Level_Leaf_Node):
                return 1
            if isinstance(node, Level_Internal_Node):
                return sum(inner(node.get_child(i)) for i in range(node.degree))
            assert False

        return inner(self._root)


    # ---------------------------------------------
    #                  Query
    # ---------------------------------------------

    def search(self, value) -> Level_Leaf_Node:
        pred = self.pred_search(value)
        if pred is None or pred.value != value:
            return None
        return pred
    
    def pred_search(self, value) -> Level_Leaf_Node:
        if self._root is None:
            return None
        return Level_Linked_ab_Tree._pred_search_from(self._root, value)

    @staticmethod
    def _pred_search_from(from_node: Level_Internal_Node | Level_Leaf_Node, value) -> Level_Leaf_Node:
        current = from_node
        while isinstance(current, Level_Internal_Node):
            for i, splitter in enumerate(current.splitters[1:]):
                if value < splitter:
                    current = current.get_child(i)
                    break
            else:
                current = current.get_child(-1)
        
        assert isinstance(current, Level_Leaf_Node)
        if current.value <= value:
            return current
        return None

    @staticmethod
    def finger_search(from_node: Level_Leaf_Node, value, use_short_circuit=True) -> Level_Leaf_Node:
        # Trivial cases
        if from_node.value == value:
            return from_node
        
        if from_node.parent is None:
            if from_node.value < value:
                return from_node.succ
            else:
                return None

        # Setup functions to search left or right
        left_sibling = lambda node: node.pred
        right_sibling = lambda node: node.succ
        sibling = left_sibling if value < from_node.value else right_sibling

        if use_short_circuit:
            contains_value = lambda node: node.splitters[0] <= value and (node.succ is None or value < node.succ.splitters[0])
        else:
            contains_value = lambda node: (node.splitters[0] <= value) & (node.succ is None or value < node.succ.splitters[0])

        # Search up the tree until the current node or the sibling contains the search value
        current = from_node.parent
        while current.parent is not None:
            if contains_value(current):
                break
            sib = sibling(current)
            if sib is None:
                break
            if contains_value(sib):
                current = sib
                break
            current = current.parent

        # current now contains the value, search down
        return Level_Linked_ab_Tree._pred_search_from(current, value)


    # ---------------------------------------------
    #                  Update
    # ---------------------------------------------

    def insert(self, value) -> Level_Leaf_Node:
        # If the tree is empty, create a new leaf node and set it as the root
        if self._root is None:
            leaf = Level_Leaf_Node(value)
            self._root = leaf
            return leaf
        
        # If the root is a leaf node, we need to split it
        # and create a new internal node
        if isinstance(self._root, Level_Leaf_Node):
            if self._root.value == value:
                return self._root

            new_leaf = Level_Leaf_Node(value)
            leafs = sorted(
                [self._root, new_leaf],
                key=lambda x: x.value,
            )
            splitters = [leafs[0].value, leafs[1].value]

            root = Level_Internal_Node(splitters=splitters, children=leafs)
            self._root = root
            leafs[0].parent = root
            leafs[1].parent = root

            return new_leaf

        # Find the correct internal node to insert the new value
        # TODO: this is the same as pred_search, but we need to
        #       remember the node if the new value is the smallest
        current = self._root
        while isinstance(current, Level_Internal_Node):
            for i, splitter in enumerate(current.splitters[1:]):
                if value < splitter:
                    current = current.get_child(i)
                    break
            else:
                current = current.get_child(-1)

        assert isinstance(current, Level_Leaf_Node)

        # If the value already exists, return the existing leaf node
        if current.value == value:
            return current

        # Insert the new leaf into the tree
        parent: Level_Internal_Node = current.parent
        new_leaf = Level_Leaf_Node(value)
        new_leaf.parent = parent

        idx = parent.splitters.index(current.value)
        if current.value < value:
            idx += 1
        parent.insert_child_with_splitter(idx, new_leaf, value)
        
        # If a new minimum is found, the splitters must be updated up the tree
        # As the insert finds the pred and inserts the new leaf after that, the
        # splitters are only updated, if it is the newest smallest value.
        if idx == 0:
            at = parent
            while at.parent is not None:
                at.parent.splitters[0] = value
                at = at.parent

        # Run fixup to ensure maximum degree
        self._insert_fixup(parent)

        return new_leaf
        
    def _insert_fixup(self, node: Level_Internal_Node):
        while len(node.splitters) == 5:
            # Split the node
            left = Level_Internal_Node(
                splitters=node.splitters[:3],
                children=node._children[:3],
            )
            right = Level_Internal_Node(
                splitters=node.splitters[3:],
                children=node._children[3:],
            )

            # Update the children of the parent node
            left.get_child(0).parent = left
            left.get_child(1).parent = left
            left.get_child(2).parent = left
            right.get_child(0).parent = right
            right.get_child(1).parent = right

            # Update the pred/succ pointers
            left.pred = node.pred
            if node.pred is not None:
                node.pred.succ = left
            left.succ = right
            right.pred = left
            right.succ = node.succ
            if node.succ is not None:
                node.succ.pred = right

            # If the parent is the root, create a new root
            if node.parent is None:
                new_root = Level_Internal_Node(
                    splitters=[left.splitters[0], right.splitters[0]],
                    children=[left, right],
                )
                left.parent = new_root
                right.parent = new_root
                self._root = new_root
                return

            # Otherwise, insert the new internal node into the parent
            parent: Level_Internal_Node = node.parent
            idx = parent.splitters.index(node.splitters[0])
            parent.update_child_with_splitter(idx, left, left.splitters[0])
            parent.insert_child_with_splitter(idx + 1, right, right.splitters[0])
            left.parent = parent
            right.parent = parent
            node = parent
    

    def delete(self, value):
        raise NotImplementedError()
    
    def _delete(self, node: Level_Leaf_Node):
        raise NotImplementedError()

    def _delete_fixup(self, node: Level_Internal_Node):
        raise NotImplementedError()


    # ---------------------------------------------
    #                  Iterators
    # ---------------------------------------------

    def __iter__(self):
        if self._root is None:
            return

        if isinstance(self._root, Level_Leaf_Node):
            yield self._root
            return
        
        # Find the leftmost leaf node
        current = self._root
        while isinstance(current, Level_Internal_Node):
            current = current.get_child(0)
        current = current.parent

        # Iterate over the last layer of the tree
        while current is not None:
            for i in range(current.degree):
                yield current.get_child(i)
            current = current.succ

    # ---------------------------------------------
    #                Meta operations
    # ---------------------------------------------

    def _to_tuple(self):
        def inner(node):
            if node is None:
                return ()
            if isinstance(node, Level_Leaf_Node):
                return (node.value,)
            if isinstance(node, Level_Internal_Node):
                children = [inner(node.get_child(i)) for i in range(node.degree)]
                return (str(node.splitters), *children),
            assert False  # Unreachable

        return inner(self._root)

    def _to_double_tuple(self, with_minimum_splitter=False):
        def inner(node):
            if node is None:
                return ()
            if isinstance(node, Level_Leaf_Node):
                return (node.value, (), ())
            if isinstance(node, Level_Internal_Node):
                children = [inner(node.get_child(i)) for i in range(node.degree)] + [() for _ in range(4 - node.degree)]
                assert len(children) == 4
                splitter_values = [s.value for s in node.splitters]
                label = str(splitter_values[1:])
                if with_minimum_splitter:
                    label = f"[({splitter_values[0]}), {label[1:-1]}]"
                return (label, ("+", children[0], children[1]), ("+", children[2], children[3]))
            assert False # Unreachable
        
        return inner(self._root)

    def print(self, with_minimum_splitter=False):
        util.print_ascii_tree(self._to_double_tuple(with_minimum_splitter=with_minimum_splitter), str_len=util.visible_str_len)


    # ---------------------------------------------
    #                 Validation
    # ---------------------------------------------

    def is_valid(self, verbose=False):
        a = self._all_pointers_set()
        b = self._ab_degree()
        c = self._all_heights_equal()
        d = self._is_sorted()
        e = self._splitters_correct()

        if verbose:
            print("All pointers set:", a)
            print("a-b degree:", b)
            print("All heights equal:", c)
            print("Sorted:", d)
            print("Splitters correct:", e)
        
        return a and b and c and d and e

    def _all_pointers_set(self):
        def inner(node):
            if isinstance(node, Level_Leaf_Node):
                return True
            
            node: Level_Internal_Node = node
            # Check links to children
            for child in node._children:
                if child.parent != node:
                    return False
                if not inner(child):
                    return False
            
            # Check links to pred/succ
            if node.pred is not None:
                if node.pred.succ != node:
                    return False
            if node.succ is not None: 
                if node.succ.pred != node:
                    return False
            
            return True

        if self._root is None:
            return True
        return inner(self._root)

    def _ab_degree(self):
        def inner(node):
            if isinstance(node, Level_Leaf_Node):
                return True
            
            node: Level_Internal_Node = node
            if not (2 <= node.degree <= 4):
                return False
            
            return all(inner(child) for child in node._children)

        if self._root is None:
            return True
        return inner(self._root)

    def _all_heights_equal(self):
        def inner_height(node):
            if isinstance(node, Level_Leaf_Node):
                return 0
            
            node: Level_Internal_Node = node
            heights = [inner_height(child) for child in node._children]
            if -1 in heights or len(set(heights)) != 1:
                return -1
            return heights[0] + 1
        
        if self._root is None:
            return True
        height = inner_height(self._root)
        return height != -1

    def _is_sorted(self):
        def inner(node, minimum, maximum):
            if isinstance(node, Level_Leaf_Node):
                return (minimum is None or minimum <= node.value) and (maximum is None or node.value < maximum)
            
            node: Level_Internal_Node = node
            for i in range(node.degree - 1):
                if node.splitters[i] > node.splitters[i + 1]:
                    return False
            
            bounds = [minimum, *node.splitters[1:], maximum]
            for i in range(node.degree):
                if not inner(node.get_child(i), bounds[i], bounds[i + 1]):
                    return False
            
            return True

        if self._root is None:
            return True
        return inner(self._root, None, None)

    def _splitters_correct(self):
        def smallest_value(node):
            if isinstance(node, Level_Leaf_Node):
                return node.value
            
            node: Level_Internal_Node = node
            return node.splitters[0]

        def inner(node):
            if isinstance(node, Level_Leaf_Node):
                return True
            
            node: Level_Internal_Node = node

            should_be = [smallest_value(node.get_child(i)) for i in range(node.degree)]
            if should_be != node.splitters:
                return False
            
            if not all(inner(child) for child in node._children):
                return False
            
            return True

        if self._root is None:
            return True
        return inner(self._root)


if __name__ == "__main__":
    from random import shuffle, seed
    seed(42)

    tree = Level_Linked_ab_Tree()

    values = list(range(40))
    shuffle(values)

    for v in values:
        tree.insert(v)
    
    tree.print(with_minimum_splitter=True)

    node16 = tree.search(16)

    for v in [23, 23.5, -1, 100]:
        found_node = Level_Linked_ab_Tree.finger_search(node16, v)
        print("Looked for", v, "and found:", found_node)
