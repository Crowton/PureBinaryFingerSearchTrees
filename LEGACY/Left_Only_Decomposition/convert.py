from Regular_RB_tree import Node, RB_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_RB_tree

from util import link_left, link_right


def convert_regular_to_zigzag(tree: RB_tree) -> Z_RB_tree:
    def convert_left_path(root: Node) -> Z_Node:
        # Empty path is converted to empty node
        if root == None:
            return None
        
        # Fetch top and bottom of the path
        next_top = root
        next_bot = root
        while next_bot._left != None:
            next_bot = next_bot._left

        # Helper variables
        new_root = None
        last_path_node = None
        last_bot_right_tree = None

        # As long as next_top is on or above next_bot, continue
        while next_top._parent != next_bot:
            # ---- Top path chunk ----
            # Create node
            new_top_node = Z_Node(next_top._key, is_red=next_top._is_red())
            
            if new_root is None:
                new_root = new_top_node

            # Set parent
            if last_path_node is not None:
                link_right(last_path_node, new_top_node)
            else:
                new_top_node._parent = None

            # Set temporary left
            # new_top_node._left = None

            # Set right
            new_top_node_right = convert_left_path(next_top._right)
            link_right(new_top_node, new_top_node_right)
            
            # If collision, final lower chunk is double or triple, and this was a lower node
            if next_top == next_bot:
                new_last_bot_right_tree = convert_left_path(last_bot_right_tree)
                link_left(new_top_node, new_last_bot_right_tree)
                last_bot_right_tree = None
                break

            # Advance top node
            next_top = next_top._left

            # ---- Bottom path chunk ----
            # Create node
            new_bot_node = Z_Node(next_bot._key, is_red=next_bot._is_red())
            last_path_node = new_bot_node

            # Set parent
            link_left(new_top_node, new_bot_node)

            # Set left
            new_last_bot_right_tree = convert_left_path(last_bot_right_tree)
            link_left(new_bot_node, new_last_bot_right_tree)
            last_bot_right_tree = next_bot._right

            # Set temporary right
            # new_bot_node._right = None

            # If collision, last bottom chunk is single node
            if next_top == next_bot:
                new_last_bot_right_tree = convert_left_path(last_bot_right_tree)
                link_right(new_bot_node, new_last_bot_right_tree)
                last_bot_right_tree = None
                break

            # Advance bottom node
            next_bot = next_bot._parent

            # If node is red, chunk needs next node
            if new_bot_node._is_red():
                assert next_bot._is_black()

                # Create node
                new_bot_bot_node = Z_Node(next_bot._key, is_red=next_bot._is_red())
                last_path_node = new_bot_bot_node

                # Set parent
                link_right(new_bot_node, new_bot_bot_node)

                # Set left
                new_last_bot_bot_right_tree = convert_left_path(last_bot_right_tree)
                link_left(new_bot_bot_node, new_last_bot_bot_right_tree)
                last_bot_right_tree = next_bot._right

                # Set temporary right
                # new_bot_bot_node._right = None

                # If collision, last bottom chunk is double node
                if next_top == next_bot:
                    new_last_bot_right_tree = convert_left_path(last_bot_right_tree)
                    link_right(new_bot_bot_node, new_last_bot_right_tree)
                    last_bot_right_tree = None
                    break

                # Advance bottom node
                next_bot = next_bot._parent

        # Check nothing is forgotten
        assert last_bot_right_tree == None
        assert new_root != None

        # Return the new root
        new_root._set_path_root()
        return new_root
    

    new_tree = Z_RB_tree()
    new_tree._root = convert_left_path(tree._root)
    return new_tree


# TODO: conversion using the structure?
def convert_zigzag_to_regular(z_tree: Z_RB_tree) -> RB_tree:
    def convert_node(node: Z_Node) -> Node:
        if node == None:
            return None

        new_node = Node(node._key, is_red=node._is_red())
        link_left(new_node, convert_node(node._get_left_of))
        link_right(new_node, convert_node(node._get_right_of))
        return new_node

    tree = RB_tree()
    tree._root = convert_node(z_tree._root)
    return tree
