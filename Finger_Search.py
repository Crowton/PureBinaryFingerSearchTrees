"""
FINGER SEARCH ALGORITHM FOR BINARY TREES
========================================

This module implements the finger search algorithm for binary trees.
It provides different versions of the algorithm, including a paper version,
an optimized version, and a whiteboard version.

The finger search algorithm is a search algorithm that allows for efficient
searching from a given node in the tree to find a node with a specific value.
When the rank difference is 'd' the result is found in O(lg d) time.

The input binary tree must have the following properties:
- Each node must have a pointer to its parent node, left child and right child.
- For each subtree, the height of the left and right subtrees must be balanced,
  i.e., the heights are within a multiplicative constant of one another.
  Such trees are for example Red-Black trees or AVL trees.
- From each node, the predecessor and successor nodes must be accessable in O(1).

"""


from enum import Enum


class Version(Enum):
    PAPER = 0
    PAPER_OPTIMIZED = 1
    WHITEBOARD = 2
    WHITEBOARD_OPTIMIZED = 3
    LCA = 4


# ----------------------------------------------------
#              Decorators for Analysis
# ----------------------------------------------------

# Common analysis
HELPER_SEARCHES_DOWN_DONE = 0
HELPER_SEARCHES_EXP_DONE = 0

def _inc_helper_searches_down_done(f):
    def wrapper(*args, **kwargs):
        global HELPER_SEARCHES_DOWN_DONE
        result = f(*args, **kwargs)
        HELPER_SEARCHES_DOWN_DONE += 1
        return result
    return wrapper

def _inc_helper_searches_exp_done(f):
    def wrapper(*args, **kwargs):
        global HELPER_SEARCHES_EXP_DONE
        result = f(*args, **kwargs)
        HELPER_SEARCHES_EXP_DONE += 1
        return result
    return wrapper


# Paper version analysis
PAPER_VERSION_STEPS_DONE = 0

def _inc_paper_version_steps_done(f):
    def wrapper(*args, **kwargs):
        global PAPER_VERSION_STEPS_DONE
        result = f(*args, **kwargs)
        PAPER_VERSION_STEPS_DONE += 1
        return result
    return wrapper

def _paper_version_return_analysis(f):
    def wrapper(*args, return_analysis=False, **kwargs):
        global PAPER_VERSION_STEPS_DONE, HELPER_SEARCHES_DOWN_DONE
        PAPER_VERSION_STEPS_DONE = 0
        HELPER_SEARCHES_DOWN_DONE = 0
        
        result = f(*args, **kwargs)
        if not return_analysis:
            return result
        
        assert 2 * PAPER_VERSION_STEPS_DONE - 1 <= HELPER_SEARCHES_DOWN_DONE <= 2 * PAPER_VERSION_STEPS_DONE, (PAPER_VERSION_STEPS_DONE, HELPER_SEARCHES_DOWN_DONE)

        h = 2 ** (PAPER_VERSION_STEPS_DONE - 1)
        return result, h, HELPER_SEARCHES_DOWN_DONE

    return wrapper


# Whiteboard version analysis
WHITEBOARD_VERSION_CHASES_DONE = 0
WHITEBOARD_VERSION_CHASE_DOWN_WIN = 0

def _direct_inc_whiteboard_version_chases_done():
    global WHITEBOARD_VERSION_CHASES_DONE
    WHITEBOARD_VERSION_CHASES_DONE += 1

def _direct_inc_whiteboard_version_chase_down_win():
    global WHITEBOARD_VERSION_CHASE_DOWN_WIN
    WHITEBOARD_VERSION_CHASE_DOWN_WIN += 1

def _whiteboard_version_return_analysis(f):
    def wrapper(*args, return_analysis=False, **kwargs):
        global WHITEBOARD_VERSION_CHASES_DONE, WHITEBOARD_VERSION_CHASE_DOWN_WIN, HELPER_SEARCHES_EXP_DONE
        WHITEBOARD_VERSION_CHASES_DONE = 0
        WHITEBOARD_VERSION_CHASE_DOWN_WIN = 0
        HELPER_SEARCHES_EXP_DONE = 0

        result = f(*args, **kwargs)
        if not return_analysis:
            return result

        final_search_is_down = int(HELPER_SEARCHES_EXP_DONE == 0)
        return result, WHITEBOARD_VERSION_CHASES_DONE, WHITEBOARD_VERSION_CHASE_DOWN_WIN, final_search_is_down

    return wrapper

# ----------------------------------------------------
#            Main Finger Search Function
# ----------------------------------------------------

def finger_search(from_node, value, algorithm=None):
    if algorithm is None or algorithm == Version.PAPER:
        return finger_search_paper_version(from_node, value)

    if algorithm == Version.PAPER_OPTIMIZED:
        return finger_search_paper_version(from_node, value, optimized=True)

    if algorithm == Version.WHITEBOARD:
        return finger_search_whiteboard_version(from_node, value)

    if algorithm == Version.WHITEBOARD_OPTIMIZED:
        return finger_search_whiteboard_version(from_node, value, optimized=True)
    
    if algorithm == Version.LCA:
        return finger_search_LCA_version(from_node, value)

    raise ValueError(f"Unknown algorithm: {algorithm}")


# ----------------------------------------------------
#                  Helper Functions
# ----------------------------------------------------

def _is_the_pred_node_short_circuit(node, value):
    return node.value <= value and (node.succ is None or value < node.succ.value)

def _is_the_pred_node_no_short_circuit(node, value):
    return (node.value <= value) & (node.succ is None or value < node.succ.value)

_is_the_pred_node = _is_the_pred_node_short_circuit


@_inc_helper_searches_down_done
def _finger_search_search_down(from_node, value):
    at = from_node
    last = None
    while at is not None:
        last = at
        if _is_the_pred_node(at, value):
            return at
        if value <= at.value:
            at = at.left
        else:
            at = at.right
    
    return last


def _finger_search_search_down_no_pred_succ(from_node, value):
    at = from_node
    last = None
    while at is not None:
        if value < at.value:
            at = at.left
        else:
            last = at
            at = at.right
    
    return last


@_inc_helper_searches_exp_done
def _finger_search_search_exp_larger(from_node, value):
    at = from_node
    while at.parent is not None and at.parent.left == at:
        if value < at.parent.value:
            break
        at = at.parent

    return _finger_search_search_down(at, value)


@_inc_helper_searches_exp_done
def _finger_search_search_exp_smaller(from_node, value):
    at = from_node
    while at.parent is not None and at.parent.right == at:
        at = at.parent
        if at.value < value:
            break

    found_node = _finger_search_search_down(at, value)
    if at.parent is not None or _is_the_pred_node(found_node, value):
        return found_node
    return None


# ----------------------------------------------------
#          Version without pred/succ pointers
#         Searches for the LCA node in the tree
# Based on: https://www.cs.au.dk/~gerth/papers/finger05.pdf
#           Bottom of section 11.4.1
# ----------------------------------------------------

def finger_search_LCA_version(from_node, value):
    if from_node.value <= value:
        return _finger_search_LCA_version_search_larger(from_node, value)
    
    else:
        return _finger_search_LCA_version_search_smaller(from_node, value)


def _finger_search_LCA_version_search_larger(from_node, value):
    at = from_node
    last = None
    l = None

    # Search up the tree to find the lca of from_node and the value
    while at is not None:
        last = at

        # x = from_node.value
        # y = value
        # v = at.value

        # Case 1
        if at.value <= from_node.value:
            at = at.parent
        # Case 2
        elif at.value <= value:  # from_node.value < at.value holds
            l = at
            at = at.parent
        # Case 3
        else:                    # from_node.value < value <= at.value holds
            return _finger_search_search_down_no_pred_succ(at, value)

        # Concurent search down from last detected lca
        if l is not None:
            if l.value == value:
                return l
            if value < l.value:
                l = l.left
            else:
                l = l.right

    # At the root, search down
    # Start completing search from the last lca, only works if the value is contained in the tree
    if l is not None:
        r = _finger_search_search_down_no_pred_succ(l, value)
        if r is not None and r.value == value:
            return r

    # If not found from l, search from root
    return _finger_search_search_down_no_pred_succ(last, value)


def _finger_search_LCA_version_search_smaller(from_node, value):
    at = from_node
    last = None
    l = None

    # Search up the tree to find the lca of from_node and the value
    while at is not None:
        last = at

        # x = from_node.value
        # y = value
        # v = at.value

        # Case 1
        if at.value >= from_node.value:
            at = at.parent
        # Case 2
        elif at.value >= value:  # from_node.value > at.value holds
            l = at
            at = at.parent
        # Case 3
        else:                    # from_node.value > value >= at.value holds
            return _finger_search_search_down_no_pred_succ(at, value)

        # Concurent search down from last detected lca
        if l is not None:
            if l.value == value:
                return l
            if value < l.value:
                l = l.left
            else:
                l = l.right

    # At the root, search down
    # Start completing search from the last lca, only works if the value is contained in the tree
    if l is not None:
        r = _finger_search_search_down_no_pred_succ(l, value)
        if r is not None and r.value == value:
            return r

    # If not found from l, search from root
    return _finger_search_search_down_no_pred_succ(last, value)


# ----------------------------------------------------
#          Paper Version including Optimized
# ----------------------------------------------------

@_paper_version_return_analysis
def finger_search_paper_version(from_node, value, optimized=False):
    if from_node.value == value:
        return from_node

    if from_node.value < value:
        if from_node.succ is None:
            return from_node

        search = _finger_search_paper_version_search_larger
    
    else:
        if from_node.pred is None:
            return None

        search = _finger_search_paper_version_search_smaller
    
    start_node = from_node
    h = 1
    while True:
        found_node = search(start_node, value, h)
        if found_node is None or _is_the_pred_node(found_node, value):
            return found_node
        h *= 2
        if optimized:
            start_node = found_node


@_inc_paper_version_steps_done
def _finger_search_paper_version_search_larger(from_node, value, h):
    at = from_node

    # Skip to the bottom of the tree
    if at.right is not None:
        at = at.succ

    # Traverse up 'h' levels of the tree
    for _ in range(h):
        if at.parent is None:
            break
        at = at.parent
    
    # Search down the tree for the value
    at = _finger_search_search_down(at, value)
    if _is_the_pred_node(at, value):
        return at
    
    # Jump up to the subtree root
    at = at.succ
    if _is_the_pred_node(at, value):
        return at
    
    # Jump down to the subtree bottom
    at = at.succ

    # Traverse up 'h' levels of the tree
    for _ in range(h):
        if at.parent is None:
            break
        at = at.parent
    
    # Search down the tree for the value
    at = _finger_search_search_down(at, value)
    return at  # Return the best candidate found


@_inc_paper_version_steps_done
def _finger_search_paper_version_search_smaller(from_node, value, h):
    at = from_node

    # Skip to the bottom of the tree
    if at.left is not None:
        at = at.pred
    
    # Traverse up 'h' levels of the tree
    for _ in range(h):
        if at.parent is None:
            break
        at = at.parent
    
    # Search down the tree for the value
    at = _finger_search_search_down(at, value)
    if _is_the_pred_node(at, value):
        return at

    # Jump up to the subtree root
    at = at.pred
    if at is None or _is_the_pred_node(at, value):
        return at
    
    # Jump down to the subtree bottom
    at = at.pred

    # Traverse up 'h' levels of the tree
    for _ in range(h):
        if at.parent is None:
            break
        at = at.parent
    
    # Search down the tree for the value
    at = _finger_search_search_down(at, value)
    return at  # Return the best candidate found


# ----------------------------------------------------
#               Whiteboard Version
# ----------------------------------------------------

@_whiteboard_version_return_analysis
def finger_search_whiteboard_version(from_node, value, optimized=False):
    if _is_the_pred_node(from_node, value):
        return from_node
    
    elif from_node.value < value:
        if from_node.succ is None:
            return from_node

        if not optimized:
            return _finger_search_whiteboard_version_search_larger(from_node, value)
        else:
            return _finger_search_whiteboard_version_search_larger_optimized(from_node, value)
    
    else:
        if from_node.pred is None:
            return None

        if not optimized:
            found_node = _finger_search_whiteboard_version_search_smaller(from_node, value)
        else:
            found_node = _finger_search_whiteboard_version_search_smaller_optimized(from_node, value)

        if _is_the_pred_node(found_node, value):
            return found_node
        return None
    

def _finger_search_whiteboard_version_search_larger(from_node, value):
    at = from_node

    # Skip to the bottom of the tree
    if at.right is not None:
        at = at.succ

    while True:
        # If at is the root, search down
        if at.parent is None:
            return _finger_search_search_down(at, value)
        
        old_at = at

        # If on a left path, walk up
        if at.parent.left == at:
            at = at.parent

        # If on a right path, walk up and down in parallel, to reach the upper left path
        else:
            _direct_inc_whiteboard_version_chases_done()
            up = at
            down = at
            
            while True:
                if down.right is None:
                    _direct_inc_whiteboard_version_chase_down_win()
                    at = down.succ
                    break
                elif up.parent is None:
                    return _finger_search_search_down(up, value)
                elif up.parent.left == up:
                    at = up.parent
                    break
                else:
                    up = up.parent
                    down = down.right

        # Test if the found node has support
        if at is None:
            # Walked out of the tree, search down from the old node
            return _finger_search_search_down(old_at, value)
        elif at.right is None:
            # At constant height -> support found
            pass
        elif at.right.value <= value:
            # Support is found as the right-left-subtree
            pass
        elif at.value <= value:
            # No support, the value is to the right
            if at.succ is None or _is_the_pred_node(at, value):
                return at
            return _finger_search_search_exp_larger(at.succ, value)
        else:
            # No support, the value is to the left, from the old node
            return _finger_search_search_down(old_at, value)


def _finger_search_whiteboard_version_search_smaller(from_node, value):
    at = from_node

    # Skip to the bottom of the tree
    if at.left is not None:
        at = at.pred
    
    while True:
        # If at is the root, search down
        if at.parent is None:
            return _finger_search_search_down(at, value)
        
        old_at = at

        # If on a right path, walk up
        if at.parent.right == at:
            at = at.parent

        # If on a left path, walk up and down in parallel, to reach the upper right path
        else:
            _direct_inc_whiteboard_version_chases_done()
            up = at
            down = at
            
            while True:
                if down.left is None:
                    _direct_inc_whiteboard_version_chase_down_win()
                    at = down.pred
                    break
                elif up.parent is None:
                    return _finger_search_search_down(up, value)
                elif up.parent.right == up:
                    at = up.parent
                    break
                else:
                    up = up.parent
                    down = down.left

        # Test if the found node has support
        if at is None:
            # Walked out of the tree, search down from the old node
            return _finger_search_search_down(old_at, value)
        elif at.left is None:
            # At constant height -> support found
            pass
        elif value <= at.left.value:
            # Support is found as the left-right-subtree
            pass
        elif _is_the_pred_node(at, value):
            return at
        elif value <= at.value:
            # No support, the value is to the left
            return _finger_search_search_exp_smaller(at.pred, value)
        else:
            # No support, the value is to the right, from the old node
            return _finger_search_search_down(old_at, value)


def _finger_search_whiteboard_version_search_larger_optimized(from_node, value):
    at = from_node

    while True:
        # Test if the found node has support
        if at is None:
            # Walked out of the tree, search down from the old node
            return _finger_search_search_down(old_at, value)
        elif at.right is None:
            # At constant height -> support found
            pass
        elif at.right.value <= value:
            # Support is found as the right-left-subtree
            pass
        elif at.value <= value:
            # No support, the value is to the right
            if at.succ is None or _is_the_pred_node(at, value):
                return at
            return _finger_search_search_exp_larger(at.succ, value)
        else:
            # No support, the value is to the left, from the old node
            return _finger_search_search_down(old_at, value)

        # If at is the root, search down
        if at.parent is None:
            return _finger_search_search_down(at, value)
        
        old_at = at

        # If on a left path, walk up
        if at.parent.left == at:
            at = at.parent

        # If on a right path, walk up and down in parallel, to reach the upper left path
        else:
            _direct_inc_whiteboard_version_chases_done()
            up = at
            down = at
            
            while True:
                if down.right is None:
                    _direct_inc_whiteboard_version_chase_down_win()
                    at = down.succ
                    break
                elif up.parent is None:
                    return _finger_search_search_down(up, value)
                elif up.parent.left == up:
                    at = up.parent
                    break
                else:
                    up = up.parent
                    down = down.right


def _finger_search_whiteboard_version_search_smaller_optimized(from_node, value):
    at = from_node
    
    while True:
        # Test if the found node has support
        if at is None:
            # Walked out of the tree, search down from the old node
            return _finger_search_search_down(old_at, value)
        elif at.left is None:
            # At constant height -> support found
            pass
        elif value <= at.left.value:
            # Support is found as the left-right-subtree
            pass
        elif _is_the_pred_node(at, value):
            return at
        elif value <= at.value:
            # No support, the value is to the left
            return _finger_search_search_exp_smaller(at.pred, value)
        else:
            # No support, the value is to the right, from the old node
            return _finger_search_search_down(old_at, value)

        # If at is the root, search down
        if at.parent is None:
            return _finger_search_search_down(at, value)
        
        old_at = at

        # If on a right path, walk up
        if at.parent.right == at:
            at = at.parent

        # If on a left path, walk up and down in parallel, to reach the upper right path
        else:
            _direct_inc_whiteboard_version_chases_done()
            up = at
            down = at
            
            while True:
                if down.left is None:
                    _direct_inc_whiteboard_version_chase_down_win()
                    at = down.pred
                    break
                elif up.parent is None:
                    return _finger_search_search_down(up, value)
                elif up.parent.right == up:
                    at = up.parent
                    break
                else:
                    up = up.parent
                    down = down.left
