import re
import math


# ---------------------------------------------
#               Tree Manipulation
# ---------------------------------------------

def link_left(parent, left) -> None:
    if parent != None: parent.left = left
    if left != None: left.parent = parent

def link_right(parent, right) -> None:
    if parent != None: parent.right = right
    if right != None: right.parent = parent


# ---------------------------------------------
#               Visualizations
# ---------------------------------------------

def visible_str_len(s):
    return len(s) - sum(map(len, re.findall(r"\u001b\[[0-9]*m", s)))

def print_ascii_tree(tree, str_len=len):
    anchor, lines = ascii_tree(tree, str_len=str_len)
    print(*lines, sep="\n")
    # print("\n".join(lines).replace(" ", "."))

def print_ascii_tree_side(*trees, spacing=5, **kwargs):
    spacing = " " * spacing
    blocks = [tree.str_block(**kwargs) for tree in trees]
    max_height = max(len(block) for block in blocks)
    blocks = [block + [" " * visible_str_len(block[0])] * (max_height - len(block)) for block in blocks]
    for row in zip(*blocks):
        print(spacing.join(row))

# TODO: round all centers to the left/right, to simplify the code
def ascii_tree(tree, str_len=len):
    def inner_ascii_tree(tree, is_left):
        if len(tree) == 0:
            return 0.5, ["*"]

        key, left, right = tree
        key = str(key)

        left_anchor, left_lines = inner_ascii_tree(left, True)
        right_anchor, right_lines = inner_ascii_tree(right, False)
        
        left_width = str_len(left_lines[0])
        right_width = str_len(right_lines[0])

        diff = len(right_lines) - len(left_lines)
        if diff >= 0:
            left_lines += [" " * left_width for _ in range(diff)]
        else:
            right_lines += [" " * right_width for _ in range(-diff)]

        key_width = str_len(key)
        center_space_width = 1 + max(0, 2 - left_width + math.ceil(left_anchor) - math.floor(right_anchor))
        total_width = left_width + center_space_width + right_width

        left_anchor = math.ceil(left_anchor)
        right_anchor = left_width + center_space_width + math.floor(right_anchor)
        
        anchor = (left_anchor + right_anchor) / 2
        
        key_padding_left = (math.floor if is_left else math.ceil)(anchor - key_width / 2)

        left_padding_width = 0
        right_padding_width = 0

        if key_padding_left < 0:
            left_padding_width = -key_padding_left
            key_padding_left = 0
            left_anchor += left_padding_width
            anchor += left_padding_width
            right_anchor += left_padding_width
            total_width += left_padding_width
        
        key_padding_right = total_width - (key_padding_left + key_width)
        
        if key_padding_right < 0:
            right_padding_width = -key_padding_right
            key_padding_right = 0
            total_width += right_padding_width
        
        left_padding = " " * left_padding_width
        right_padding = " " * right_padding_width

        left_under_len = math.ceil(anchor - left_anchor - 2) if is_left else math.floor(anchor - left_anchor - 1)
        right_under_len = math.floor(anchor - left_anchor - 1) if is_left else math.ceil(right_anchor - anchor - 2)

        upper_lines = [
            " " * key_padding_left + key + " " * key_padding_right,
            " " * left_anchor + "_" * left_under_len + "/ \\" + "_" * right_under_len + " " * (total_width - right_anchor),
            " " * (left_anchor - 1) + "/" + " " * (right_anchor - left_anchor) + "\\" + " " * (total_width - right_anchor - 1),
        ]

        center_space = " " * center_space_width
        lower_lines = [left_padding + l + center_space + r + right_padding for l, r in zip(left_lines, right_lines)]

        return anchor, upper_lines + lower_lines

    return inner_ascii_tree(tree, True)
