from Regular_RB_tree import Node, RB_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_tree


def regular_tree_equality(tree_a: RB_tree, tree_b: RB_tree):
    def node_equality(node_a: Node, node_b: Node):
        if node_a == None and node_b == None:
            return True
        if node_a == None or node_b == None:
            return False
        return node_a._key == node_b._key and node_a._is_red_bool == node_b._is_red_bool and \
            node_equality(node_a._left, node_b._left) and node_equality(node_a._right, node_b._right)

    return node_equality(tree_a._root, tree_b._root)

def zigzag_tree_equality(tree_a: Z_tree, tree_b: Z_tree):
    def node_equality(node_a: Z_Node, node_b: Z_Node):
        if node_a == None and node_b == None:
            return True
        if node_a == None or node_b == None:
            return False
        res = node_a._key == node_b._key and node_a._is_red_bool == node_b._is_red_bool and node_a._is_path_root_bool == node_b._is_path_root_bool and \
            node_equality(node_a._left, node_b._left) and node_equality(node_a._right, node_b._right)
        # if not res:
        #     left = node_equality(node_a._left, node_b._left)
        #     right = node_equality(node_a._right, node_b._right)
        #     print("Fails at nodes:", node_a._key, node_b._key)
        #     print(node_a._key == node_b._key,
        #                 node_a._is_red_bool == node_b._is_red_bool,
        #                 node_a._is_path_root_bool == node_b._is_path_root_bool,
        #                 left,
        #                 right
        #     )
        return res

    return node_equality(tree_a._root, tree_b._root)

def regular_and_zigzag_tree_equality(tree_a: RB_tree, tree_b: Z_tree):
    def node_equality(node_a: Node, node_b: Z_Node):
        if node_a == None and node_b == None:
            return True
        if node_a == None or node_b == None:
            return False
        return node_a._key == node_b._key and node_a._is_red_bool == node_b._is_red_bool and \
            node_equality(node_a._left, node_b._get_left_of) and node_equality(node_a._right, node_b._get_right_of)

    return node_equality(tree_a._root, tree_b._root)
