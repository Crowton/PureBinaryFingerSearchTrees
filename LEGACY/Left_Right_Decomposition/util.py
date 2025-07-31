import math
import re


# TODO: move to Regular_RB_tree.py?
def regular_colored_node_data_formatter(key, is_red):
    return (("\u001b[31m" if is_red else "\u001b[37m") + str(key) + "\u001b[0m",)


# TODO: move to Zigzag_RB_tree.py?
def zigzag_colored_node_data_formatter(key, is_red, is_left_path):
    # return (str(key) + f"({'BR'[is_red]})({'RL'[is_left_path]})",)
    return (("\u001b[31m" if is_red else "\u001b[37m") + str(key) + "\u001b[0m" + f"({'RL'[is_left_path]})",)


def visible_str_len(s):
    # str_len = 0
    # ignore = False
    # for c in s:
    #     if ignore:
    #         if c == "m":
    #             ignore = False
    #     elif c == "\u001b":
    #         ignore = True
    #     else:
    #         str_len += 1
    # return str_len

    # return len(s) - s.count("\u001b") * 4
    
    return len(s) - sum(map(len, re.findall(r"\u001b\[[0-9]*m", s)))


# TODO: self defined len function?
def print_ascii_tree(tree, ignore_terminal_codes=False):
    anchor, lines = ascii_tree(tree, ignore_terminal_codes=ignore_terminal_codes)
    print(*lines, sep="\n")
    # print("\n".join(lines).replace(" ", "."))


def ascii_tree(tree, ignore_terminal_codes=False):
    # TODO: round all centers to the left/right, to simplify the code

    str_len = len if not ignore_terminal_codes else visible_str_len

    def inner_ascii_tree(tree, is_left):
        if len(tree) == 0:
            return 0.5, ["*"]

        key, left, right = tree
        # key = f"'{key}'"
        key = str(key)

        left_anchor, left_lines = inner_ascii_tree(left, True)
        right_anchor, right_lines = inner_ascii_tree(right, False)
        
        # left_width = len(left_lines[0])
        left_width = str_len(left_lines[0])
        # right_width = len(right_lines[0])
        right_width = str_len(right_lines[0])

        diff = len(right_lines) - len(left_lines)
        if diff >= 0:
            left_lines += [" " * left_width for _ in range(diff)]
        else:
            right_lines += [" " * right_width for _ in range(-diff)]

        # key_width = len(key)
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


if __name__ == "__main__":
    tree = ("A", (), ())
    print_ascii_tree(tree)

    print()

    tree = ("A", ("B", (), ()), ("C", (), ()))
    print_ascii_tree(tree)

    print()

    tree = ("D", ("E", ("G", (), ()), ()), ("F", (), ()))
    print_ascii_tree(tree)

    print()

    tree = ("A", ("B", (), ("C", (), ())), ("D", ("E", ("G", (), ()), ()), ("F", (), ())))
    print_ascii_tree(tree)

    print()

    tree = ("AAA", ("BB", ("D", (), ()), ()), ("C", (), ("EEEEEEE", ("FF", (), ()), ())))
    print_ascii_tree(tree)

    print()

    tree = ("A", (), ("EEEEEEE", ("FF", (), ()), ()))
    print_ascii_tree(tree)

    print()

    tree = ('\x1b[37mx_k\x1b[0m', ('\x1b[31mx_1\x1b[0m', (), ('\x1b[37mx_2\x1b[0m', ('\x1b[37mT_1\x1b[0m', (), ()), ('\x1b[37mx_k-1\x1b[0m', ('\x1b[37mx_3\x1b[0m', ('\x1b[37mT_2\x1b[0m', (), ()), ('\x1b[31mx_k-2\x1b[0m', ('\x1b[31mx_4\x1b[0m', ('\x1b[37mT_3\x1b[0m', (), ()), ('\x1b[37mx_5\x1b[0m', ('\x1b[37mT_4\x1b[0m', (), ()), ('\x1b[37mx_k-3\x1b[0m', ('\x1b[37mx_6\x1b[0m', ('\x1b[37mT_5\x1b[0m', (), ()), ('\x1b[37mx_m\x1b[0m', ('\x1b[37mT_6\x1b[0m', (), ()), ('\x1b[37mT_m\x1b[0m', (), ()))), ('\x1b[37mT_k-3\x1b[0m', (), ())))), ('\x1b[37mT_k-2\x1b[0m', (), ()))), ('\x1b[37mT_k-1\x1b[0m', (), ())))), ('\x1b[37mT_k\x1b[0m', (), ()))
    print_ascii_tree(tree, ignore_terminal_codes=True)
    
    print()
    
    tree = ('\x1b[37mx_3\x1b[0m', ('\x1b[37mT_2\x1b[0m', (), ()), ('\x1b[31mx_k-2\x1b[0m', ('\x1b[31mx_4\x1b[0m', ('\x1b[37mT_3\x1b[0m', (), ()), ('\x1b[37mx_5\x1b[0m', ('\x1b[37mT_4\x1b[0m', (), ()), ('\x1b[37mx_k-3\x1b[0m', ('\x1b[37mx_6\x1b[0m', ('\x1b[37mT_5\x1b[0m', (), ()), ('\x1b[37mx_m\x1b[0m', ('\x1b[37mT_6\x1b[0m', (), ()), ('\x1b[37mT_m\x1b[0m', (), ()))), ('\x1b[37mT_k-3\x1b[0m', (), ())))), ('\x1b[37mT_k-2\x1b[0m', (), ())))
    print_ascii_tree(tree, ignore_terminal_codes=True)
    
    print()
    
    tree = ('\x1b[31mx_k-2\x1b[0m', ('\x1b[31mx_4\x1b[0m', ('\x1b[37mT_3\x1b[0m', (), ()), ('\x1b[37mx_5\x1b[0m', ('\x1b[37mT_4\x1b[0m', (), ()), ('\x1b[37mx_k-3\x1b[0m', ('\x1b[37mx_6\x1b[0m', ('\x1b[37mT_5\x1b[0m', (), ()), ('\x1b[37mx_m\x1b[0m', ('\x1b[37mT_6\x1b[0m', (), ()), ('\x1b[37mT_m\x1b[0m', (), ()))), ('\x1b[37mT_k-3\x1b[0m', (), ())))), ('\x1b[37mT_k-2\x1b[0m', (), ()))
    print_ascii_tree(tree, ignore_terminal_codes=True)
    
    print()
    
    tree = ('\x1b[37mx_5\x1b[0m', ('\x1b[37mT_4\x1b[0m', (), ()), ('\x1b[37mx_k-3\x1b[0m', ('\x1b[37mx_6\x1b[0m', ('\x1b[37mT_5\x1b[0m', (), ()), ('\x1b[37mx_m\x1b[0m', ('\x1b[37mT_6\x1b[0m', (), ()), ('\x1b[37mT_m\x1b[0m', (), ()))), ('\x1b[37mT_k-3\x1b[0m', (), ())))
    print_ascii_tree(tree, ignore_terminal_codes=True)
