from Regular_RB_tree import Node, RB_tree
from ZigZag_RB_tree import ZigZag_Node as Z_Node
from ZigZag_RB_tree import ZigZag_RB_tree as Z_tree


def link_left(parent: Z_Node, left: Z_Node) -> None:
    if parent != None: parent._left = left
    if left != None: left._parent = parent

def link_right(parent: Z_Node, right: Z_Node) -> None:
    if parent != None: parent._right = right
    if right != None: right._parent = parent


def convert_regular_to_zigzag(tree: RB_tree) -> Z_tree:
    def convert_left_path(root: Node) -> Z_Node:
        # Empty path is converted to empty node
        if root == None:
            return None

        # Fetch top and bottom of the path
        next_top = root
        next_bot = root
        while next_bot._left != None:
            next_bot = next_bot._left

        # Convert the path to Zig Zag
        new_root = None
        last_path_node = None
        last_bot_right_tree = None

        # As long as next_top is on or above next_bot, continue
        while next_top._parent != next_bot:
            # ---- Top path chunk ----
            # Create node
            new_top_node = Z_Node(next_top._key)
            new_top_node._is_red = next_top._is_red  # TODO: add to constructor?
            new_top_node.set_left_path()             # TODO: add to constructor?
            
            if new_root is None:
                new_root = new_top_node

            # Set parent
            if last_path_node is not None:
                link_right(last_path_node, new_top_node)
            else:
                new_top_node._parent = None

            # Set left
            new_top_node._left = None

            # Set right
            new_top_node_right = convert_right_path(next_top._right)
            link_right(new_top_node, new_top_node_right)
            
            # If collision, middle node is found
            if next_top == next_bot:
                new_last_bot_right_tree = convert_right_path(last_bot_right_tree)
                link_left(new_top_node, new_last_bot_right_tree)
                last_bot_right_tree = None
                break

            # Advance top node
            next_top = next_top._left

            # ---- Bottom path chunk ----
            # Create node
            new_bot_node = Z_Node(next_bot._key)
            new_bot_node._is_red = next_bot._is_red  # TODO: add to constructor?
            new_bot_node.set_left_path()             # TODO: add to constructor?

            last_path_node = new_bot_node

            # Set parent
            link_left(new_top_node, new_bot_node)

            # Set left
            new_last_bot_right_tree = convert_right_path(last_bot_right_tree)
            link_left(new_bot_node, new_last_bot_right_tree)
            last_bot_right_tree = next_bot._right

            # Set right
            new_bot_node._right = None

            # If collision, last bottom chunk is single node (red or black)
            if next_top == next_bot:
                new_last_bot_right_tree = convert_right_path(last_bot_right_tree)
                link_right(new_bot_node, new_last_bot_right_tree)
                last_bot_right_tree = None
                break

            # Advance bottom node
            next_bot = next_bot._parent

            # If node is red, chunk needs next node
            if new_bot_node.is_red():
                assert next_bot.is_black()

                # Create node
                new_bot_bot_node = Z_Node(next_bot._key)
                new_bot_bot_node._is_red = next_bot._is_red  # TODO: add to constructor?
                new_bot_bot_node.set_left_path()             # TODO: add to constructor?

                last_path_node = new_bot_bot_node

                # Set parent
                link_right(new_bot_node, new_bot_bot_node)

                # Set left
                new_last_bot_bot_right_tree = convert_right_path(last_bot_right_tree)
                link_left(new_bot_bot_node, new_last_bot_bot_right_tree)
                last_bot_right_tree = next_bot._right

                # Set right
                new_bot_bot_node._right = None

                # If collision, last bottom chunk is double node
                if next_top == next_bot:
                    new_last_bot_right_tree = convert_right_path(last_bot_right_tree)
                    link_right(new_bot_bot_node, new_last_bot_right_tree)
                    last_bot_right_tree = None
                    break

                # Advance bottom node
                next_bot = next_bot._parent

        assert last_bot_right_tree == None
        assert new_root is not None
        return new_root


    def convert_right_path(root: Node) -> Z_Node:
        # Empty path is converted to empty node
        if root == None:
            return None

        # Fetch top and bottom of the path
        next_top = root
        next_bot = root
        while next_bot._right != None:
            next_bot = next_bot._right

        # Convert the path to Zig Zag
        new_root = None
        last_path_node = None
        last_bot_left_tree = None

        # As long as next_top is on or above next_bot, continue
        while next_top._parent != next_bot:
            assert next_top != None and next_bot != None

            # ---- Top path chunk ----
            # Create node
            new_top_node = Z_Node(next_top._key)
            new_top_node._is_red = next_top._is_red  # TODO: add to constructor?
            new_top_node.set_right_path()            # TODO: add to constructor?
            
            if new_root is None:
                new_root = new_top_node

            # Set parent
            if last_path_node is not None:
                link_left(last_path_node, new_top_node)
            else:
                new_top_node._parent = None

            # Set left
            new_top_node_left = convert_left_path(next_top._left)
            link_left(new_top_node, new_top_node_left)

            # Set right
            new_top_node._right = None
            
            # If collision, middle node is found
            if next_top == next_bot:
                new_last_bot_left_tree = convert_left_path(last_bot_left_tree)
                link_right(new_top_node, new_last_bot_left_tree)
                last_bot_left_tree = None
                break

            # Advance top node
            next_top = next_top._right

            # ---- Bottom path chunk ----
            # Create node
            new_bot_node = Z_Node(next_bot._key)
            new_bot_node._is_red = next_bot._is_red  # TODO: add to constructor?
            new_bot_node.set_right_path()            # TODO: add to constructor?

            last_path_node = new_bot_node

            # Set parent
            link_right(new_top_node, new_bot_node)

            # Set left
            new_bot_node._left = None

            # Set right
            new_last_bot_left_tree = convert_left_path(last_bot_left_tree)
            link_right(new_bot_node, new_last_bot_left_tree)
            last_bot_left_tree = next_bot._left

            # If collision, last bottom chunk is single node (red or black)
            if next_top == next_bot:
                new_last_bot_left_tree = convert_left_path(last_bot_left_tree)
                link_left(new_bot_node, new_last_bot_left_tree)
                last_bot_left_tree = None
                break

            # Advance bottom node
            next_bot = next_bot._parent

            # If node is red, chunk needs next node
            if new_bot_node.is_red():
                assert next_bot.is_black()

                # Create node
                new_bot_bot_node = Z_Node(next_bot._key)
                new_bot_bot_node._is_red = next_bot._is_red  # TODO: add to constructor?
                new_bot_bot_node.set_right_path()            # TODO: add to constructor?

                last_path_node = new_bot_bot_node

                # Set parent
                link_left(new_bot_node, new_bot_bot_node)

                # Set left
                new_bot_bot_node._left = None

                # Set right
                new_last_bot_bot_left_tree = convert_left_path(last_bot_left_tree)
                link_right(new_bot_bot_node, new_last_bot_bot_left_tree)
                last_bot_left_tree = next_bot._left

                # If collision, last bottom chunk is double node
                if next_top == next_bot:
                    new_last_bot_left_tree = convert_left_path(last_bot_left_tree)
                    link_left(new_bot_bot_node, new_last_bot_left_tree)
                    last_bot_left_tree = None
                    break

                # Advance bottom node
                next_bot = next_bot._parent

        assert last_bot_left_tree == None
        assert new_root is not None
        return new_root
    

    new_tree = Z_tree()
    new_tree._root = convert_left_path(tree._root)
    return new_tree

def convert_zigzag_to_regular(tree: Z_tree) -> RB_tree:
    seen = set()

    def convert_node(node: Z_Node) -> Node:
        if node == None:
            return None
        
        if node._key in seen:
            return Node(f"!{node._key}!")
        seen.add(node._key)

        new_node = Node(node._key)
        new_node._is_red = node._is_red

        left = node._get_left_of
        right = node._get_right_of

        new_left = convert_node(left)
        new_right = convert_node(right)

        link_left(new_node, new_left)
        link_right(new_node, new_right)

        return new_node

    new_tree = RB_tree()
    new_tree._root = convert_node(tree._root)
    return new_tree
