from Many_Pointers_Red_Black_Tree import Red_Black_Tree, Red_Black_Node
from Level_Linked_ab_Tree import Level_Linked_ab_Tree
from Mock_FT_Folded_Tree import Mock_Folded_Tree
import Finger_Search
from Pointer_Counting import get_pointer_count, get_compare_count, compare_wrap_value, reset_counts, set_do_count
import random

from itertools import count

import matplotlib.pyplot as plt

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)


import math

from collections import defaultdict



def save_and_show(name):
    plt.savefig(f"plot/{name}.png")
    plt.show()
    # plt.clf()

plt.save_and_show = save_and_show


# ---------------------------------------------
#                Tree creators
# ---------------------------------------------

# TODO: this is copy-pasted from the test file, should be moved to a separate file?
def create_random_tree(n, seed=42):
    tree = Red_Black_Tree()
    values = [compare_wrap_value(v) for v in range(n)]
    random.seed(seed)
    random.shuffle(values)

    for value in values:
        tree.insert(value)

    return tree


def create_perfect_tree(h):
    def gen_subtree(h, label_generator) -> tuple[Red_Black_Node, Red_Black_Node, Red_Black_Node]:
        if h == 1:
            node = Red_Black_Node(value=compare_wrap_value(next(label_generator)), is_red=False)
            return node, node, node
        
        left_min, left_root, left_max = gen_subtree(h - 1, label_generator)
        node = Red_Black_Node(value=compare_wrap_value(next(label_generator)), is_red=False)
        right_min, right_root, right_max = gen_subtree(h - 1, label_generator)

        node.left = left_root
        left_root.parent = node
        node.right = right_root
        right_root.parent = node

        node.pred = left_max
        left_max.succ = node
        node.succ = right_min
        right_min.pred = node

        return left_min, node, right_max
    

    if h == 0:
        return Red_Black_Tree()

    _, root, _ = gen_subtree(h, count(0, 1))
    tree = Red_Black_Tree()
    tree._root = root
    return tree


def create_random_level_linked_tree(n, seed=42):
    tree = Level_Linked_ab_Tree()
    values = [compare_wrap_value(v) for v in range(n)]
    random.seed(seed)
    random.shuffle(values)

    for value in values:
        tree.insert(value)
    
    return tree


# ---------------------------------------------
#                Analysis
# ---------------------------------------------

def set_inner_pred_function(use_short_circuiting):
    if use_short_circuiting:
        Finger_Search._is_the_pred_node = Finger_Search._is_the_pred_node_short_circuit
    else:
        Finger_Search._is_the_pred_node = Finger_Search._is_the_pred_node_no_short_circuit


def extract_leaves(tree):
    leaves = []
    for node in tree:
        if node.left is None and node.right is None:
            leaves.append(node)
    return leaves

def extract_all(tree):
    return list(tree)


def run_analysis_from_exp_spread_to_specific_target_set(
        file_name,
        seed, tree, n, k,
        header_write,
        run_test_func,
        target_set_generator=extract_leaves,
        inner_pred_function_use_short_circuiting=True,
        force_leaf_start=False,
    ):

    set_inner_pred_function(inner_pred_function_use_short_circuiting)

    target_set = target_set_generator(tree)

    random.seed(seed)

    with open(file_name, "a") as file:
        for end_node in random.sample(target_set, k=k):
            end_value = end_node.value.unwrap()
            d = 1
            while d < n:
                next_d = math.ceil(d * 1.3)
                for start_value, next_start in [
                    (end_value - random.randint(d, next_d - 1), lambda node: node.pred),
                    (end_value + random.randint(d, next_d - 1), lambda node: node.succ),
                ]:
                    if start_value < 0 or start_value >= n:
                        continue

                    start_node = tree.search(start_value)
                    assert start_node is not None
                    assert start_node.value.unwrap() == start_value

                    if force_leaf_start:
                        while start_node is not None and start_node.left is not None or start_node.right is not None:
                            start_node = next_start(start_node)
                        if start_node is None:
                            continue
                    
                    start_value = start_node.value.unwrap()

                    reset_counts()
                    set_do_count(True)

                    found_node, extra_info = run_test_func(start_node, end_value)

                    set_do_count(False)

                    assert found_node is not None
                    assert found_node.value.unwrap() == end_value

                    rank_difference = abs(start_value - end_value)
                    pointer_lookups = get_pointer_count()
                    compare_count = get_compare_count()

                    if extra_info is not None:
                        extra_info_str = ",".join(map(str, extra_info)) + ","
                    else:
                        extra_info_str = ""

                    file.write(f"{header_write}{start_value},{end_value},{rank_difference},{extra_info_str}{pointer_lookups},{compare_count}\n")
                
                d = next_d
    
    set_inner_pred_function(use_short_circuiting=True)


def run_paper_version_func(optimized=False):
    def run_test_func(start_node, end_value):
        found_node, h, searches = Finger_Search.finger_search_paper_version(
            start_node, end_value, optimized=optimized, return_analysis=True
        )
        return found_node, (h, searches)

    return run_test_func

def run_whiteboard_version_func(optimized=False):
    def run_test_func(start_node, end_value):
        found_node, chases, down_wins, final_search_is_down = Finger_Search.finger_search_whiteboard_version(
            start_node, end_value, optimized=optimized, return_analysis=True
        )
        return found_node, (chases, down_wins, final_search_is_down)

    return run_test_func

def run_LCA_version_func():
    def run_test_func(start_node, end_value):
        found_node = Finger_Search.finger_search_LCA_version(start_node, end_value)
        return found_node, None

    return run_test_func

def run_pred_search_from_root_func(tree):
    def run_test_func(start_node, end_value):
        found_node = tree.pred_search(end_value)
        return found_node, None

    return run_test_func

def run_mock_folded_finger_search(algorithm):
    def run_test_func(start_node, end_value):
        found_node = Mock_Folded_Tree.finger_search(start_node, end_value, algorithm=algorithm)
        return found_node, None

    return run_test_func


def analyse_finger_search_paper_version_random_trees(
        file_name,
        optimized=False, inner_pred_function_use_short_circuiting=True
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,h,searches,pointer_lookups,compare_count\n")

    for seed in range(10):
        print("Starting seed", seed, "...")
        n = 100_000
        tree = create_random_tree(n, seed=seed)

        run_analysis_from_exp_spread_to_specific_target_set(
            file_name, seed, tree, n, 20, f"{seed},{n},", run_paper_version_func(optimized),
            inner_pred_function_use_short_circuiting=inner_pred_function_use_short_circuiting
        )

def analyse_finger_search_paper_version_perfect_tree(
        file_name,
        optimized=False, inner_pred_function_use_short_circuiting=True,
        force_leaf_start=False
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("n,start_value,end_value,rank_difference,h,searches,pointer_lookups,compare_count\n")

    h = 20
    n = 1048575
    tree = create_perfect_tree(h)
    
    run_analysis_from_exp_spread_to_specific_target_set(
        file_name, 42, tree, n, 50, f"{n},", run_paper_version_func(optimized),
        inner_pred_function_use_short_circuiting=inner_pred_function_use_short_circuiting,
        force_leaf_start=force_leaf_start
    )


def analyse_finger_search_whiteboard_version_random_trees(
        file_name,
        inner_pred_function_use_short_circuiting=True,
        optimized=False
    ):
    
    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,chases,down_wins,final_search_is_down,pointer_lookups,compare_count\n")

    for seed in range(10):
        print("Starting seed", seed, "...")
        n = 100_000
        tree = create_random_tree(n, seed=seed)

        run_analysis_from_exp_spread_to_specific_target_set(
            file_name, seed, tree, n, 20, f"{seed},{n},", run_whiteboard_version_func(optimized=optimized),
            inner_pred_function_use_short_circuiting=inner_pred_function_use_short_circuiting
        )

def analyse_finger_search_whiteboard_version_perfect_tree(
        file_name,
        inner_pred_function_use_short_circuiting=True,
        force_leaf_start=False
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("n,start_value,end_value,rank_difference,chases,down_wins,final_search_is_down,pointer_lookups,compare_count\n")

    h = 20
    n = 1048575
    tree = create_perfect_tree(h)
    
    run_analysis_from_exp_spread_to_specific_target_set(
        file_name, 42, tree, n, 50, f"{n},", run_whiteboard_version_func(),
        inner_pred_function_use_short_circuiting=inner_pred_function_use_short_circuiting,
        force_leaf_start=force_leaf_start
    )


def analyse_finger_search_LCA_version_random_trees(
        file_name,
    ):

    print("Running Analysis for file:", file_name)
    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,pointer_lookups,compare_count\n")
    
    for seed in range(10):
        print("Starting seed", seed, "...")
        n = 100_000
        tree = create_random_tree(n, seed=seed)

        run_analysis_from_exp_spread_to_specific_target_set(
            file_name, seed, tree, n, 20, f"{seed},{n},", run_LCA_version_func()
        )

def analyse_finger_search_LCA_version_perfect_trees_all_leaf_pairs(
        file_name,
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("n,start_value,end_value,rank_difference,lca_height,pointer_lookups,compare_count\n")

    h = 10
    n = 2**h - 1
    tree = create_perfect_tree(h)

    set_inner_pred_function(use_short_circuiting=True)

    leaves = []
    for node in tree:
        if node.left is None and node.right is None:
            leaves.append(node)

    with open(file_name, "a") as file:
        for start_node in leaves:
            start_value = start_node.value.unwrap()

            for end_node in leaves:
                if start_node == end_node:
                    continue
                
                end_value = end_node.value.unwrap()

                reset_counts()
                set_do_count(True)

                found_node = Finger_Search.finger_search_LCA_version(start_node, end_value)

                set_do_count(False)

                assert found_node is not None
                assert found_node == end_node

                assert (start_node.left is None and start_node.right is None)
                assert (found_node.left is None and found_node.right is None)
                a = start_node
                b = found_node
                lca_height = 0
                while a != b:
                    a = a.parent
                    b = b.parent
                    lca_height += 1

                rank_difference = abs(start_value - end_value)
                pointer_lookups = get_pointer_count()
                compare_count = get_compare_count()

                file.write(f"{n},{start_value},{end_value},{rank_difference},{lca_height},{pointer_lookups},{compare_count}\n")

    set_inner_pred_function(use_short_circuiting=True)


def analyse_pred_search_from_root_random_trees(
        file_name,
    ):
    
    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,pointer_lookups,compare_count\n")
    
    for seed in range(10):
        print("Starting seed", seed, "...")
        n = 100_000
        tree = create_random_tree(n, seed=seed)

        run_analysis_from_exp_spread_to_specific_target_set(
            file_name, seed, tree, n, 20, f"{seed},{n},", run_pred_search_from_root_func(tree)
        )


# TODO: refractor this function?
def analyse_finger_search_level_linked_tree_random_trees(
        file_name,
        inner_contains_function_use_short_circuiting=True
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,pointer_lookups,compare_count\n")

        for seed in range(10):
            print("Starting seed", seed, "...")

            n = 100_000
            tree = create_random_level_linked_tree(n, seed=seed)

            for start_value in random.sample(range(n), 20):
                start_node = tree.search(start_value)
                assert start_node is not None
                assert start_node.value.unwrap() == start_value

                d = 1
                while d < n:
                    next_d = math.ceil(d * 1.3)
                    for end_value in [
                        start_value - random.randint(d, next_d - 1),
                        start_value + random.randint(d, next_d - 1),
                    ]:
                        if end_value < 0 or end_value >= n:
                            continue

                        reset_counts()
                        set_do_count(True)

                        found_node = Level_Linked_ab_Tree.finger_search(start_node, end_value, use_short_circuit=inner_contains_function_use_short_circuiting)

                        set_do_count(False)

                        assert found_node is not None
                        assert found_node.value.unwrap() == end_value

                        rank_difference = abs(start_value - end_value)
                        pointer_lookups = get_pointer_count()
                        compare_count = get_compare_count()

                        file.write(f"{seed},{n},{start_value},{end_value},{rank_difference},{pointer_lookups},{compare_count}\n")
                    
                    d = next_d


def analyse_finger_search_constant_rank_diference_perfect_tree(
        file_name,
        finger_search_algorithm,
        rank_difference,
        from_leaf=False, record_lca_height=False,
        inner_pred_function_use_short_circuiting=True
    ):

    print("Running Analysis for file:", file_name)
    
    h = 15
    n = 32767
    tree = create_perfect_tree(h)

    with open(file_name, "w+") as file:
        if record_lca_height:
            lca_height_str = "lca_height,"
        else:
            lca_height_str = ""
        file.write(f"n,rank_difference,start_value,end_value,{lca_height_str}pointer_lookups,compare_count\n")

        for start_node in tree:
            if from_leaf and (start_node.left is not None or start_node.right is not None):
                continue

            start_value = start_node.value.unwrap()

            for end_value in [start_value - rank_difference, start_value + rank_difference]:
                if end_value < 0 or end_value >= n:
                    continue

                set_inner_pred_function(inner_pred_function_use_short_circuiting)
                reset_counts()
                set_do_count(True)

                found_node = finger_search_algorithm(start_node, end_value)

                set_do_count(False)
                set_inner_pred_function(True)

                assert found_node is not None
                assert found_node.value.unwrap() == end_value

                calc_rank_difference = abs(start_value - end_value)
                assert calc_rank_difference == rank_difference
                pointer_lookups = get_pointer_count()
                compare_count = get_compare_count()
                
                if record_lca_height:
                    assert (start_node.left is None and start_node.right is None)
                    assert (found_node.left is None and found_node.right is None)
                    a = start_node
                    b = found_node
                    lca_height = 0
                    while a != b:
                        a = a.parent
                        b = b.parent
                        lca_height += 1
                    lca_height_str = f"{lca_height},"
                else:
                    lca_height_str = ""

                file.write(f"{n},{rank_difference},{start_value},{end_value},{lca_height_str}{pointer_lookups},{compare_count}\n")


def analyse_finger_search_random_folded_trees(
        file_name,
        finger_search_algorithm,
        inner_pred_function_use_short_circuiting=False,
    ):

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,pointer_lookups,compare_count\n")

    for seed in range(10):
        print("Starting seed", seed, "...", end=" ")

        n = 100_000
        tree = create_random_tree(n, seed=seed)
        folded_tree = Mock_Folded_Tree.create_folded_tree(tree)

        print("Folding completed")

        run_analysis_from_exp_spread_to_specific_target_set(
            file_name, seed, folded_tree, n, 50, f"{seed},{n},",
            run_mock_folded_finger_search(finger_search_algorithm),
            target_set_generator=extract_all,
            inner_pred_function_use_short_circuiting=inner_pred_function_use_short_circuiting
        )

def analyse_finger_search_perfect_folded_trees_constant_rank_difference(
        file_name,
        finger_search_algorithm,
        rank_difference,
        inner_pred_function_use_short_circuiting=False,
    ):

    set_inner_pred_function(inner_pred_function_use_short_circuiting)

    print("Running Analysis for file:", file_name)

    with open(file_name, "w+") as file:
        file.write("n,start_value,end_value,rank_difference,pointer_lookups,compare_count\n")

        h = 15
        n = 2**h - 1
        tree = create_perfect_tree(h)
        folded_tree = Mock_Folded_Tree.create_folded_tree(tree)

        for start_node in folded_tree:
            start_value = start_node.value.unwrap()

            for end_value in [start_value - rank_difference, start_value + rank_difference]:
                if end_value < 0 or end_value >= n:
                    continue

                reset_counts()
                set_do_count(True)

                found_node = Mock_Folded_Tree.finger_search(start_node, end_value, algorithm=finger_search_algorithm)

                set_do_count(False)

                assert found_node is not None
                assert found_node.value.unwrap() == end_value

                calc_rank_difference = abs(start_value - end_value)
                assert calc_rank_difference == rank_difference
                pointer_lookups = get_pointer_count()
                compare_count = get_compare_count()

                file.write(f"{n},{start_value},{end_value},{rank_difference},{pointer_lookups},{compare_count}\n")


# ---------------------------------------------
#                  Plotting
# ---------------------------------------------

def plot(
        file_name,
        save=True, save_extra_name="",
        alpha=1,
        group_by_func=None, group_by_label_maker=None, group_filter_func=None,
        divide=True,
        leg_columns=None
    ):
    with open(file_name, "r") as f:
        lines = f.readlines()
    
    column_names = lines[0].strip().split(",")
    raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]
    
    show_legend = True
    if group_by_func is None:
        assert group_by_label_maker is None
        group_by_func = lambda _: (None,)
        group_by_label_maker = lambda _: "All"
        show_legend = False
    else:
        assert group_by_label_maker is not None
    
    if group_filter_func is None:
        group_filter_func = lambda *_: True

    fig, [ax_left, ax_right] = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(16, 6)

    for access_name, y_label, ax in [("pointer_lookups", "Pointer Access", ax_left), ("compare_count", "Comparisons", ax_right)]:
        buckets = defaultdict(list)
        for data_point in raw_data:
            rank_difference = data_point["rank_difference"]
            y_value = data_point[access_name]
            if divide and rank_difference > 1:
                y_value /= math.log2(rank_difference)
            group = group_by_func(data_point)
            buckets[group].append((rank_difference, y_value))

        for group, bucket in sorted(buckets.items()):
            if not group_filter_func(*group):
                continue
            ax.plot(*zip(*bucket), ".", alpha=alpha, label=group_by_label_maker(*group))

        ax.tick_params(reset=True, top=False, right=False)
        ax.set_xscale("log")
        ax.set_xlabel("$d$ (Rank Difference)")
        ax.set_ylabel(f"{y_label} / $\log_2(d)$" if divide else y_label)

    if show_legend:
        # leg = fig.legend(loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.25))
        handles, labels = ax_left.get_legend_handles_labels()
        # leg = fig.legend(handles, labels, ncol=len(labels), loc="upper center", bbox_to_anchor=(0.5, -0.25))
        # leg = fig.legend(handles, labels, ncol=(len(labels) if leg_columns is None else leg_columns), loc="upper center", bbox_to_anchor=(0.5, 1))
        leg = fig.legend(handles, labels, ncol=(len(labels) if leg_columns is None else leg_columns), loc="upper center")
        # leg = ax_left.legend(handles, labels, loc='lower center', ncol=len(labels), frameon=False, bbox_to_anchor=(0.5, -0.25), bbox_transform=fig.transFigure)
        
        leg.legend_handles = leg.legendHandles
        for lh in leg.legend_handles:
            lh.set_alpha(1)

    # fig.tight_layout()

    if save:
        base_file_name = file_name[5:-4]
        save_name = f"single__{base_file_name}{'__' if save_extra_name else ''}{save_extra_name}"
        plt.save_and_show(save_name)
    else:
        plt.show()


def multi_plot(
        data_sets,
        save=True, save_extra_name="", overwrite_save_name=None,
        alpha=1, divide=True
    ):

    fig, [ax_left, ax_right] = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(16, 6)

    for file_name, label in data_sets:
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        column_names = lines[0].strip().split(",")
        raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]
        
        for access_name, ax in [("pointer_lookups", ax_left), ("compare_count", ax_right)]:
            data = []
            for data_point in raw_data:
                rank_difference = data_point["rank_difference"]
                y_value = data_point[access_name]
                if divide and rank_difference > 1:
                    y_value /= math.log2(rank_difference)
                data.append((rank_difference, y_value))

            ax.plot(*zip(*data), ".", alpha=alpha, label=label)

    handles, labels = ax_left.get_legend_handles_labels()
    leg = fig.legend(handles, labels, ncol=len(labels), loc="upper center")
    
    leg.legend_handles = leg.legendHandles
    for lh in leg.legend_handles:
        lh.set_alpha(1)

    for y_label, ax in [("Pointer Access", ax_left), ("Comparisons", ax_right)]:
        ax.tick_params(reset=True, top=False, right=False)
        ax.set_xscale("log")
        ax.set_xlabel("$d$ (Rank Difference)")
        ax.set_ylabel(f"{y_label} / $\log_2(d)$" if divide else y_label)

    if save:
        if overwrite_save_name is not None:
            save_name = f"multi__{overwrite_save_name}"
        else:
            base_file_names = [file_name[5:-4] for file_name, _ in data_sets]
            save_name = f"multi__{'__'.join(base_file_names)}{'__' if save_extra_name else ''}{save_extra_name}"
        plt.save_and_show(save_name)
    else:
        plt.show()


def multi_plot_constant_rank_diff(
        data_sets,
        save=True, save_extra_name="", overwrite_save_name=None,
        alpha=1, color_intencity=False,
        divide_by_lca=False,
        show_legend=True
    ):

    fig, [ax_left, ax_right] = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(16, 6)

    for i, (file_name, label) in enumerate(data_sets, start=1):
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        column_names = lines[0].strip().split(",")
        raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]

        for access_name, ax in [("pointer_lookups", ax_left), ("compare_count", ax_right)]:
            data = []
            for data_point in raw_data:
                start_value = data_point["start_value"]
                y_value = data_point[access_name]
                if divide_by_lca:
                    y_value /= data_point["lca_height"]
                data.append((start_value, y_value))
            
            if color_intencity:
                ax.plot(*zip(*data), ".", color=f"{1 - (0.5 + 0.5 * i / len(data_sets))}", alpha=alpha, label=label)
            else:
                ax.plot(*zip(*data), ".", alpha=alpha, label=label)

    if show_legend:
        handles, labels = ax_left.get_legend_handles_labels()
        leg = fig.legend(handles, labels, ncol=len(labels), loc="upper center")

        leg.legend_handles = leg.legendHandles
        for lh in leg.legend_handles:
            lh.set_alpha(1)

    for y_label, ax in [("Pointer Access", ax_left), ("Comparisons", ax_right)]:
        ax.tick_params(reset=True, top=False, right=False)
        ax.set_xlabel("Start Value")
        ax.set_ylabel(f"{y_label} / LCA height" if divide_by_lca else y_label)

    if save:
        if overwrite_save_name is not None:
            save_name = f"multi_rank_diff__{overwrite_save_name}"
        else:
            base_file_names = [file_name[5:-4] for file_name, _ in data_sets]
            save_name = f"multi_rank_diff__{'__'.join(base_file_names)}{'__' if save_extra_name else ''}{save_extra_name}"
        plt.save_and_show(save_name)
    else:
        plt.show()


def multi_plot_constant_rank_diff_as_function_of_lca_height(
        data_sets,
        save=True, overwrite_save_name=None,
        alpha=1, color_intencity=False,
        x_shift=False,
        divide_by_lca=False,
        leg_columns=None
    ):

    fig, [ax_left, ax_right] = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(16, 6)

    max_at_lca = {
        "pointer_lookups": defaultdict(lambda: 0),
        "compare_count": defaultdict(lambda: 0)
    }

    for i, (file_name, label) in enumerate(data_sets):
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        column_names = lines[0].strip().split(",")
        raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]

        for access_name, ax in [("pointer_lookups", ax_left), ("compare_count", ax_right)]:
            data = []
            for data_point in raw_data:
                lca_height = data_point["lca_height"]
                y_value = data_point[access_name]
                if divide_by_lca:
                    y_value /= lca_height
                max_at_lca[access_name][lca_height] = max(max_at_lca[access_name][lca_height], y_value)
                if x_shift:
                    lca_height += i * (0.5 / len(data_sets)) # - 0.25
                data.append((lca_height, y_value))
            
            if color_intencity:
                ax.plot(*zip(*data), ".", color=f"{1 - (0.3 + 0.7 * (i + 1) / len(data_sets))}", alpha=alpha, label=label)
            else:
                ax.plot(*zip(*data), ".", alpha=alpha, label=label)
    
    handles, labels = ax_left.get_legend_handles_labels()
    leg = fig.legend(handles, labels, ncol=(len(labels) if leg_columns is None else leg_columns), loc="upper center")

    leg.legend_handles = leg.legendHandles
    for lh in leg.legend_handles:
        lh.set_alpha(1)

    for y_label, ax in [("Pointer Access", ax_left), ("Comparisons", ax_right)]:
        ax.tick_params(reset=True, top=False, right=False)
        ax.set_xlabel("LCA Height")
        ax.set_ylabel(f"{y_label} / LCA Height" if divide_by_lca else y_label)

    print(max_at_lca)

    # for const, ax in [(6, ax_left), (11, ax_right)]:
    #     xs = [0, 14]
    #     ys = [x * const for x in xs]
    #     ax.plot(xs, ys, "k--")

    # plt.tight_layout()

    if save:
        if overwrite_save_name is not None:
            save_name = f"multi_rank_diff__{overwrite_save_name}"
        else:
            base_file_names = [file_name[5:-4] for file_name, _ in data_sets]
            save_name = f"multi_lca_height__{'__'.join(base_file_names)}"
        plt.save_and_show(save_name)
    else:
        plt.show()


def compare_equal_experiments_plot(
        file_name_1, file_name_2,
        save=True, save_extra_name="",
        alpha=1,
        y_lim=None, fair_y_axis=False,
        has_seed=True,
        group_by_func=None, group_by_label_maker=None,
        with_line_at_equal=True,
        with_average_pr_rank_difference=False,
        group_rank_difference=False
    ):

    show_legend = True
    if group_by_func is None:
        assert group_by_label_maker is None
        group_by_func = lambda a, b: None
        group_by_label_maker = lambda _: "All"
        show_legend = False
    else:
        assert group_by_label_maker is not None

    fig, [ax_left, ax_right] = plt.subplots(nrows=1, ncols=2, sharey=True)
    fig.set_size_inches(16, 6)

    bucketed_data = []
    tree_n = None

    for file_name in [file_name_1, file_name_2]:
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        column_names = lines[0].strip().split(",")
        raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]
        
        data = {}
        for data_point in raw_data:
            key = (data_point["seed"] if has_seed else None, data_point["start_value"], data_point["end_value"])
            data[key] = data_point
        bucketed_data.append(data)

        tree_n = data_point["n"]
    
    for access_name, ax in [("pointer_lookups", ax_left), ("compare_count", ax_right)]:
        plot_data = []
        grouped_data = defaultdict(list)
        for experiment, data_point_1 in bucketed_data[0].items():
            data_point_2 = bucketed_data[1][experiment]

            rank_difference = data_point_1["rank_difference"]
            y_value_1 = data_point_1[access_name]
            y_value_2 = data_point_2[access_name]
            proc_increment = y_value_2 / y_value_1

            plot_data.append((rank_difference, proc_increment))
            grouped_data[group_by_func(data_point_1, data_point_2)].append((rank_difference, proc_increment))

        for group, points in sorted(grouped_data.items()):
            if y_lim is not None:
                y_min, y_max = y_lim
                assert all(y_min < y < y_max for _, y in points)
            ax.plot(*zip(*points), ".", alpha=alpha, label=group_by_label_maker(group))

        if with_average_pr_rank_difference:
            bucket_by_rank_difference = defaultdict(list)
            if not group_rank_difference:
                plot_type = "."
                for rank_difference, proc_increment in plot_data:
                    bucket_by_rank_difference[rank_difference].append(proc_increment)
            else:
                plot_type = "-"
                rank_cutoffs = [1]
                n = tree_n
                while rank_cutoffs[-1] < n:
                    rank_cutoffs.append(math.ceil(rank_cutoffs[-1] * 1.3))

                plot_data.sort()
                i = 1
                for rank_difference, proc_increment in plot_data:
                    if rank_difference >= rank_cutoffs[i]:
                        i += 1
                    bucket_by_rank_difference[rank_cutoffs[i-1]].append(proc_increment)

            geo_data = []
            for rank_difference, proc_increment_list in bucket_by_rank_difference.items():
                # geo_proc_increment = math.prod(proc_increment_list) ** (1 / len(proc_increment_list))
                geo_proc_increment = math.exp(sum(math.log(p) for p in proc_increment_list) / len(proc_increment_list))
                geo_data.append((rank_difference, geo_proc_increment))

            ax.plot(*zip(*geo_data), plot_type, color="black", linewidth=3)
            ax.plot(*zip(*geo_data), plot_type, color="lightgray", linewidth=2, label="Geometric Average by Rank Difference")
            # ax.plot(*zip(*geo_data), plot_type, color="gray", linewidth=4, label="Geometric Average by Rank Difference")
    
    if show_legend:
        handles, labels = ax_left.get_legend_handles_labels()
        leg = fig.legend(handles, labels, ncol=len(labels), loc="upper center")

        leg.legend_handles = leg.legendHandles
        for lh in leg.legend_handles:
            lh.set_alpha(1)

    for y_label, ax in [("Pointer Access", ax_left), ("Comparisons", ax_right)]:
        ax.tick_params(reset=True, top=False, right=False)
        ax.set_xlabel("$d$ (Rank Difference)")
        ax.set_ylabel(f"{y_label} Speed-up")
        ax.set_xscale("log")

        # TODO: fix this thing
        if fair_y_axis:
            ax.set_yscale("log")
        
        # yticks = [0.5, 1, 2, 3]  # ax.get_yticks()
        # ylabels = [f"$\\times${y}" for y in yticks]
        # ax.set_yticks(yticks, labels=ylabels)

        if y_lim is not None:
            ax_left.set_ylim(y_lim)

    if with_line_at_equal:
        ax_left.axhline(y=1, linestyle=":", color="black")
        ax_right.axhline(y=1, linestyle=":", color="black")

    if save:
        base_file_names = [file_name[5:-4] for file_name in (file_name_1, file_name_2)]
        save_name = f"compare__{'__'.join(base_file_names)}{'__' if save_extra_name else ''}{save_extra_name}"
        plt.save_and_show(save_name)
    else:
        plt.show()


if __name__ == "__main__":
    # Run the analysis
    # Paper version, on random trees
    if True:
        analyse_finger_search_paper_version_random_trees(
            file_name = "data/paper_version_from_exp_spread_to_leaves.csv",
            optimized=False, inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_paper_version_random_trees(
            file_name = "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            optimized=False, inner_pred_function_use_short_circuiting=False
        )

    # Paper version, on perfect trees
    if True:
        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_from_exp_spread_to_leaves_perfect_tree.csv",
            optimized=False, inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            optimized=False, inner_pred_function_use_short_circuiting=False,
        )

        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            optimized=False, inner_pred_function_use_short_circuiting=False,
            force_leaf_start=True
        )

    # Paper version optimized, on random trees
    if True:
        analyse_finger_search_paper_version_random_trees(
            file_name = "data/paper_version_optimized_from_exp_spread_to_leaves.csv",
            optimized=True, inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_paper_version_random_trees(
            file_name = "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            optimized=True, inner_pred_function_use_short_circuiting=False
        )
    
    # Paper version optimized, on perfect trees
    if True:
        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree.csv",
            optimized=True, inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            optimized=True, inner_pred_function_use_short_circuiting=False,
        )

        analyse_finger_search_paper_version_perfect_tree(
            file_name = "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            optimized=True, inner_pred_function_use_short_circuiting=False,
            force_leaf_start=True
        )

    # Whiteboard version, on random trees
    if True:
        analyse_finger_search_whiteboard_version_random_trees(
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_whiteboard_version_random_trees(
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            inner_pred_function_use_short_circuiting=False
        )
    
    # Whiteboard version, on perfect trees
    if True:
        analyse_finger_search_whiteboard_version_perfect_tree(
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree.csv",
            inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_whiteboard_version_perfect_tree(
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            inner_pred_function_use_short_circuiting=False
        )

    # Whiteboard version optimized, on random trees
    if True:
        analyse_finger_search_whiteboard_version_random_trees(
            file_name = "data/whiteboard_optimized_version_from_exp_spread_to_leaves.csv",
            optimized=True,
            inner_pred_function_use_short_circuiting=True
        )

        analyse_finger_search_whiteboard_version_random_trees(
            file_name = "data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            optimized=True,
            inner_pred_function_use_short_circuiting=False
        )

    # LCA version, on random trees
    if True:
        analyse_finger_search_LCA_version_random_trees(
            file_name = "data/LCA_version_from_exp_spread_to_leaves.csv"
        )
    
    # LCA version, on perfect trees, all pairs
    if True:
        analyse_finger_search_LCA_version_perfect_trees_all_leaf_pairs(
            file_name = "data/LCA_version_perfect_tree_all_leaf_pairs.csv"
        )

    # Constant rank difference, on perfect trees
    if True:
        analyse_finger_search_constant_rank_diference_perfect_tree(
            file_name = "data/paper_version_rank_difference_2_perfect_tree_no_short_circuit.csv",
            finger_search_algorithm=Finger_Search.finger_search_paper_version,
            rank_difference=2,
            inner_pred_function_use_short_circuiting=False
        )

        analyse_finger_search_constant_rank_diference_perfect_tree(
            file_name = "data/whiteboard_version_rank_difference_2_perfect_tree_no_short_circuit.csv",
            finger_search_algorithm=Finger_Search.finger_search_whiteboard_version,
            rank_difference=2,
            inner_pred_function_use_short_circuiting=False
        )

        analyse_finger_search_constant_rank_diference_perfect_tree(
            file_name = "data/LCA_version_rank_difference_2_perfect_tree.csv",
            finger_search_algorithm=Finger_Search.finger_search_LCA_version,
            rank_difference=2,
        )
    
    if True:
        for rd in [2, 4, 8]:
            analyse_finger_search_constant_rank_diference_perfect_tree(
                file_name = f"data/paper_version_rank_difference_{rd}_perfect_tree_from_leaf_no_short_circuit.csv",
                finger_search_algorithm=Finger_Search.finger_search_paper_version,
                rank_difference=rd, from_leaf=True,
                inner_pred_function_use_short_circuiting=False
            )

            analyse_finger_search_constant_rank_diference_perfect_tree(
                file_name = f"data/whiteboard_version_rank_difference_{rd}_perfect_tree_from_leaf_no_short_circuit.csv",
                finger_search_algorithm=Finger_Search.finger_search_whiteboard_version,
                rank_difference=2, from_leaf=True,
                inner_pred_function_use_short_circuiting=False
            )

            analyse_finger_search_constant_rank_diference_perfect_tree(
                file_name = f"data/LCA_version_rank_difference_{rd}_perfect_tree_from_leaf.csv",
                finger_search_algorithm=Finger_Search.finger_search_LCA_version,
                rank_difference=rd, from_leaf=True,
            )
    
    if True:
        for rd in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
            analyse_finger_search_constant_rank_diference_perfect_tree(
                file_name = f"data/LCA_version_rank_difference_{rd}_perfect_tree_from_leaf_with_lca_height.csv",
                finger_search_algorithm=Finger_Search.finger_search_LCA_version,
                rank_difference=rd, from_leaf=True,
                record_lca_height=True
            )
    
    # Level linkes (2,4) trees
    if True:
        analyse_finger_search_level_linked_tree_random_trees(
            file_name = "data/level_linked_tree_from_leaves_to_exp_spread.csv",
        )

        analyse_finger_search_level_linked_tree_random_trees(
            file_name = "data/level_linked_tree_from_leaves_to_exp_spread_no_short_circuit.csv",
            inner_contains_function_use_short_circuiting=False
        )
    
    # Search from the root, random trees
    if True:
        analyse_pred_search_from_root_random_trees(
            file_name = "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
        )

    # Folded trees, random trees, search with LCA finger search
    if True:
        analyse_finger_search_random_folded_trees(
            file_name = "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            finger_search_algorithm=Finger_Search.Version.LCA
        )

    if True:
        for rd in [2, 4, 8, 16]:
            analyse_finger_search_perfect_folded_trees_constant_rank_difference(
                file_name = f"data/folded_tree_perfect_trees_LCA_version_constant_rank_diff_{rd}.csv",
                finger_search_algorithm=Finger_Search.Version.LCA,
                rank_difference=rd
            )

    # Folded trees, random trees, use paper version
    if True:
        analyse_finger_search_random_folded_trees(
            file_name = "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            finger_search_algorithm=Finger_Search.Version.PAPER
        )

        analyse_finger_search_random_folded_trees(
            file_name = "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version_no_short_circuit.csv",
            finger_search_algorithm=Finger_Search.Version.PAPER,
            inner_pred_function_use_short_circuiting=False
        )
    
    # Folded trees, random trees, use whiteboard version
    if True:
        analyse_finger_search_random_folded_trees(
            file_name = "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv",
            finger_search_algorithm=Finger_Search.Version.WHITEBOARD
        )


    # Plot the results
    # Paper version, on random trees
    if True:
        plot(
            "data/paper_version_from_exp_spread_to_leaves.csv",
            save=True
        )
        
        plot(
            "data/paper_version_from_exp_spread_to_leaves.csv",
            save_extra_name="group_h",
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["h"],),
            group_by_label_maker=lambda h: f"$h = {h}$"
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves.csv",
            save_extra_name="group_h_searches",
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"]),
            group_by_label_maker=lambda h, searches: f"$h = {h}, s = {searches}$",
            leg_columns=6
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves.csv",
            save_extra_name="group_h_searches_direc",
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"], "right" if data_point["start_value"] < data_point["end_value"] else "left"),
            group_by_label_maker=lambda h, searches, direc: f"$h = {h}, s = {searches}, direc = {direc}$",
            group_filter_func=lambda h, searches, direc: h == 8
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save_extra_name="group_h_searches_direc",
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"], "right" if data_point["start_value"] < data_point["end_value"] else "left"),
            group_by_label_maker=lambda h, searches, direc: f"$h = {h}, s = {searches}, direc = {direc}$",
            group_filter_func=lambda h, searches, direc: h == 8
        )

    # Paper version, on perfect trees
    if True:
        plot(
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree.csv",
            save=False,
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"]),
            group_by_label_maker=lambda h, searches: f"$h = {h}, s = {searches}$"
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save_extra_name="group_h_searches",
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"]),
            group_by_label_maker=lambda h, searches: f"$h = {h}, s = {searches}$",
            leg_columns=5
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"]),
            group_by_label_maker=lambda h, searches: f"$h = {h}, s = {searches}$",
            divide=False
        )

        plot(
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            save_extra_name="group_h_searches",
            group_by_func=lambda data_point: (data_point["h"], data_point["searches"]),
            group_by_label_maker=lambda h, searches: f"$h = {h}, s = {searches}$",
            leg_columns=5
        )
    
    # Paper version optimized, on random trees
    if True:
        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves.csv", "Optimized"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv", "Optimized"),
            ],
            save=True,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv", "Optimized"),
            ],
            save=False,
            alpha=0.4, divide=False
        )
    
        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            # y_lim=[0.46, 3.2], fair_y_axis=True,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            # y_lim=[0.46, 3.2], fair_y_axis=True,
            alpha=0.4,
            group_by_func=lambda data_point_1, data_point_2: data_point_2["searches"] - data_point_1["searches"],
            group_by_label_maker=lambda diff: f"{diff = }"
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            # y_lim=[0.3, 3.1], fair_y_axis=True,
            alpha=0.4,
            with_average_pr_rank_difference=True,
            group_by_func=lambda data_point_1, data_point_2: data_point_2["searches"] - data_point_1["searches"],
            group_by_label_maker=lambda diff: f"{diff = }"
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=True,
            # y_lim=[0.3, 3.1], fair_y_axis=True,
            alpha=0.4,
            with_average_pr_rank_difference=True,
            group_rank_difference=True,
            group_by_func=lambda data_point_1, data_point_2: data_point_2["searches"] - data_point_1["searches"],
            group_by_label_maker=lambda diff: f"{diff = }"
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            # y_lim=[0.46, 3.2], fair_y_axis=True,
            alpha=0.4,
            group_by_func=lambda data_point_1, data_point_2: (data_point_1["searches"], data_point_2["searches"]),
            group_by_label_maker=lambda search_tuple: f"s1 = {search_tuple[0]}, s2 = {search_tuple[1]}"
        )
    
    # Paper version optimized, on perfect trees
    if True:
        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_perfect_tree.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree.csv", "Optimized"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv", "Optimized"),
            ],
            save=True,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv", "Paper"),
                ("data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv", "Optimized"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            # y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
            with_average_pr_rank_difference=True
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            # y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )
    
        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            save=False,
            # y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            save=False,
            # y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
            with_average_pr_rank_difference=True
        )

        compare_equal_experiments_plot(
            "data/paper_version_optimized_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            "data/paper_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit_force_leaf_start.csv",
            save=True,
            # y_lim=[0.9, 2.1], fair_y_axis=True,
            alpha=0.4,
            has_seed=False,
            with_average_pr_rank_difference=True,
            group_rank_difference=True,
            group_by_func=lambda data_point_1, data_point_2: data_point_2["searches"] - data_point_1["searches"],
            group_by_label_maker=lambda diff: f"{diff = }"
        )

    # Whiteboard version, on random trees
    if True:
        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            save=False
        )

        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            save=False,
            divide=False
        )

        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=True
        )

        multi_plot(
            [
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Short Circuit"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Force Both"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
        )

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: ("right" if data_point["start_value"] < data_point["end_value"] else "left",),
            group_by_label_maker=lambda direc: f"$direc = {direc}$",
        )

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["seed"],),
            group_by_label_maker=lambda seed: f"$seed = {seed}$",
        )

        # n = 100_000
        # seeds = list(range(10))
        # root_values = [create_tree(n, seed=seed)._root.value.unwrap() for seed in seeds]
        # print(root_values)

        root_values = [48210, 56721, 43119, 38547, 34829, 60664, 58523, 54897, 46783, 59693]

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (sorted([data_point["start_value"], data_point["end_value"], root_values[data_point["seed"]]])[1] == root_values[data_point["seed"]],),
            group_by_label_maker=lambda over_root: f"$over_root = {over_root}$",
        )

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["chases"],),
            group_by_label_maker=lambda chases: f"$chases = {chases}$",
        )

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["down_wins"],),
            group_by_label_maker=lambda down_wins: f"$down_wins = {down_wins}$",
        )

        plot(
            # file_name = "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            file_name = "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save_extra_name="group_final_search_type",
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["final_search_is_down"],),
            group_by_label_maker=lambda final_search_is_down: "Downwards" if final_search_is_down else "Exponential",
        )

    if True:
        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Whiteboard"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/whiteboard_version_from_exp_spread_to_leaves.csv",
            "data/paper_version_from_exp_spread_to_leaves.csv",
            save=False,
            fair_y_axis=True,
            alpha=0.4,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Whiteboard"),
            ],
            save=True,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Whiteboard"),
            ],
            save=False,
            alpha=0.4, divide=False
        )

        compare_equal_experiments_plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            fair_y_axis=True,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            fair_y_axis=True,
            alpha=0.4,
            with_average_pr_rank_difference=True
        )

        compare_equal_experiments_plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=True,
            fair_y_axis=True,
            alpha=0.4,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )
    
    # Whiteboard version, on perfect trees
    if True:
        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree.csv",
            save=False
        )

        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False
        )
        
        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["chases"],),
            group_by_label_maker=lambda chases: f"$chases = {chases}$",
        )

        plot(
            "data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            group_by_func=lambda data_point: (data_point["down_wins"],),
            group_by_label_maker=lambda down_wins: f"$down_wins = {down_wins}$",
        )

        multi_plot(
            [
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Random"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_perfect_tree.csv", "Perfect"),
            ],
            save=False,
            alpha=0.4
        )

    # Whiteboard version optimized, on random trees
    if True:
        plot(
            "data/whiteboard_optimized_version_from_exp_spread_to_leaves.csv",
            save=False
        )

        plot(
            "data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False
        )

        multi_plot(
            [
                ("data/whiteboard_optimized_version_from_exp_spread_to_leaves.csv", "Short Circuit"),
                ("data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Force Both"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Optimized"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Unoptimized"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            with_average_pr_rank_difference=True, group_rank_difference=True
        )

    # LCA version, on random trees
    if True:
        plot(
            "data/LCA_version_from_exp_spread_to_leaves.csv",
            save=True
        )

        plot(
            "data/LCA_version_from_exp_spread_to_leaves.csv",
            save=False,
            divide=False,
        )

    if True:
        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Whiteboard"),
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "LCA"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Whiteboard"),
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "LCA"),
            ],
            save=False,
            alpha=0.4, divide=False
        )

    # LCA version, perfect tree, all leaf pairs
    if True:
        plot(
            "data/LCA_version_perfect_tree_all_leaf_pairs.csv",
            save=False,
            alpha=0.2
        )

        plot(
            "data/LCA_version_perfect_tree_all_leaf_pairs.csv",
            save=False,
            divide=False,
            alpha=0.2
        )

    # Constant rank difference, on perfect trees
    if True:
        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree.csv", "LCA"),
            ],
            save=False,
            alpha=0.4,
            show_legend=False
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf.csv", "LCA"),
            ],
            save=True,
            alpha=0.4,
            show_legend=False
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree.csv", "LCA"),
                ("data/paper_version_rank_difference_2_perfect_tree_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_rank_difference_2_perfect_tree_no_short_circuit.csv", "Whiteboard"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf.csv", "LCA"),
                ("data/paper_version_rank_difference_2_perfect_tree_from_leaf_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_rank_difference_2_perfect_tree_from_leaf_no_short_circuit.csv", "Whiteboard"),
            ],
            save=True,
            alpha=0.4
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf.csv", "LCA"),
                ("data/paper_version_rank_difference_4_perfect_tree_from_leaf_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_rank_difference_4_perfect_tree_from_leaf_no_short_circuit.csv", "Whiteboard"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf.csv", "LCA"),
                ("data/paper_version_rank_difference_8_perfect_tree_from_leaf_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_rank_difference_8_perfect_tree_from_leaf_no_short_circuit.csv", "Whiteboard"),
            ],
            save=False,
            alpha=0.4
        )

    if True:
        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8"),
            ],
            save=False,
            alpha=0.2
        )

        multi_plot_constant_rank_diff(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8"),
                ("data/LCA_version_rank_difference_16_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16"),
                ("data/LCA_version_rank_difference_32_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 32"),
                ("data/LCA_version_rank_difference_64_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 64"),
                ("data/LCA_version_rank_difference_128_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 128"),
                ("data/LCA_version_rank_difference_256_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 256"),
                ("data/LCA_version_rank_difference_512_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 512"),
                ("data/LCA_version_rank_difference_1024_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 1024"),
                ("data/LCA_version_rank_difference_2048_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2048"),
                ("data/LCA_version_rank_difference_4096_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4096"),
                ("data/LCA_version_rank_difference_8192_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8192"),
                ("data/LCA_version_rank_difference_16384_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16384"),
            ],
            save=False,
            alpha=0.2, divide_by_lca=True
        )

        multi_plot_constant_rank_diff_as_function_of_lca_height(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8"),
                ("data/LCA_version_rank_difference_16_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16"),
                ("data/LCA_version_rank_difference_32_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 32"),
                ("data/LCA_version_rank_difference_64_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 64"),
                ("data/LCA_version_rank_difference_128_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 128"),
                ("data/LCA_version_rank_difference_256_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 256"),
                ("data/LCA_version_rank_difference_512_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 512"),
                ("data/LCA_version_rank_difference_1024_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 1024"),
                ("data/LCA_version_rank_difference_2048_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2048"),
                ("data/LCA_version_rank_difference_4096_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4096"),
                ("data/LCA_version_rank_difference_8192_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8192"),
                ("data/LCA_version_rank_difference_16384_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16384"),
            ],
            save=False,
            alpha=0.2, x_shift=True
        )

        multi_plot_constant_rank_diff_as_function_of_lca_height(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8"),
                ("data/LCA_version_rank_difference_16_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16"),
                ("data/LCA_version_rank_difference_32_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 32"),
                ("data/LCA_version_rank_difference_64_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 64"),
                ("data/LCA_version_rank_difference_128_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 128"),
                ("data/LCA_version_rank_difference_256_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 256"),
                ("data/LCA_version_rank_difference_512_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 512"),
                ("data/LCA_version_rank_difference_1024_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 1024"),
                ("data/LCA_version_rank_difference_2048_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2048"),
                ("data/LCA_version_rank_difference_4096_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4096"),
                ("data/LCA_version_rank_difference_8192_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8192"),
                ("data/LCA_version_rank_difference_16384_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16384"),
            ],
            save=False,
            alpha=0.2, x_shift=True,
            color_intencity=True
        )

        multi_plot_constant_rank_diff_as_function_of_lca_height(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8"),
                ("data/LCA_version_rank_difference_16_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16"),
                ("data/LCA_version_rank_difference_32_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 32"),
                ("data/LCA_version_rank_difference_64_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 64"),
                ("data/LCA_version_rank_difference_128_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 128"),
                ("data/LCA_version_rank_difference_256_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 256"),
                ("data/LCA_version_rank_difference_512_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 512"),
                ("data/LCA_version_rank_difference_1024_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 1024"),
                ("data/LCA_version_rank_difference_2048_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 2048"),
                ("data/LCA_version_rank_difference_4096_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 4096"),
                ("data/LCA_version_rank_difference_8192_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 8192"),
                ("data/LCA_version_rank_difference_16384_perfect_tree_from_leaf_with_lca_height.csv", "Rank difference 16384"),
            ],
            save=False,
            alpha=0.2, x_shift=True,
            divide_by_lca=True
        )

        multi_plot_constant_rank_diff_as_function_of_lca_height(
            [
                ("data/LCA_version_rank_difference_2_perfect_tree_from_leaf_with_lca_height.csv", "$d = 2$"),
                ("data/LCA_version_rank_difference_4_perfect_tree_from_leaf_with_lca_height.csv", "$d = 4$"),
                ("data/LCA_version_rank_difference_8_perfect_tree_from_leaf_with_lca_height.csv", "$d = 8$"),
                ("data/LCA_version_rank_difference_16_perfect_tree_from_leaf_with_lca_height.csv", "$d = 16$"),
                ("data/LCA_version_rank_difference_32_perfect_tree_from_leaf_with_lca_height.csv", "$d = 32$"),
                ("data/LCA_version_rank_difference_64_perfect_tree_from_leaf_with_lca_height.csv", "$d = 64$"),
                ("data/LCA_version_rank_difference_128_perfect_tree_from_leaf_with_lca_height.csv", "$d = 128$"),
                ("data/LCA_version_rank_difference_256_perfect_tree_from_leaf_with_lca_height.csv", "$d = 256$"),
                ("data/LCA_version_rank_difference_512_perfect_tree_from_leaf_with_lca_height.csv", "$d = 512$"),
                ("data/LCA_version_rank_difference_1024_perfect_tree_from_leaf_with_lca_height.csv", "$d = 1024$"),
                ("data/LCA_version_rank_difference_2048_perfect_tree_from_leaf_with_lca_height.csv", "$d = 2048$"),
                ("data/LCA_version_rank_difference_4096_perfect_tree_from_leaf_with_lca_height.csv", "$d = 4096$"),
                ("data/LCA_version_rank_difference_8192_perfect_tree_from_leaf_with_lca_height.csv", "$d = 8192$"),
                ("data/LCA_version_rank_difference_16384_perfect_tree_from_leaf_with_lca_height.csv", "$d = 16384$"),
            ],
            save=True, overwrite_save_name="lca_version_by_lca_divided",
            alpha=0.2, x_shift=True,
            divide_by_lca=True,
            color_intencity=True,
            leg_columns=7
        )

        multi_plot_constant_rank_diff_as_function_of_lca_height(
            [
                ("data/LCA_version_perfect_tree_all_leaf_pairs.csv", "All")
            ],
            save=False,
            alpha=0.4,
            divide_by_lca=True
        )

    # Level linkes (2,4) trees
    if True:
        plot(
            "data/level_linked_tree_from_leaves_to_exp_spread.csv",
            save=True
        )

        plot(
            "data/level_linked_tree_from_leaves_to_exp_spread.csv",
            save=True, save_extra_name="group_direction",
            alpha=0.4,
            group_by_func=lambda data_point: ("right" if data_point["start_value"] < data_point["end_value"] else "left",),
            group_by_label_maker=lambda direc: f"$direc = {direc}$",
        )

        plot(
            "data/level_linked_tree_from_leaves_to_exp_spread_no_short_circuit.csv",
            save=True,
            alpha=0.4,
            group_by_func=lambda data_point: ("right" if data_point["start_value"] < data_point["end_value"] else "left",),
            group_by_label_maker=lambda direc: f"$direc = {direc}$",
        )

    if True:
        multi_plot(
            [
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "LCA"),
                ("data/paper_version_from_exp_spread_to_leaves.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves.csv", "Whiteboard"),
                ("data/level_linked_tree_from_leaves_to_exp_spread.csv", "Level linked tree"),
                ("data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv", "Search from Root"),
            ],
            save=True, overwrite_save_name="level_linked_compare_all",
            alpha=0.4
        )

        multi_plot(
            [
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "LCA"),
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Whiteboard"),
                ("data/level_linked_tree_from_leaves_to_exp_spread_no_short_circuit.csv", "Level linked tree"),
                ("data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv", "Search from Root"),
            ],
            save=True, overwrite_save_name="level_linked_compare_all_no_short_circuit",
            alpha=0.4
        )

        multi_plot(
            [
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "LCA"),
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Whiteboard"),
                ("data/level_linked_tree_from_leaves_to_exp_spread_no_short_circuit.csv", "Level linked tree"),
                ("data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv", "Search from Root"),
            ],
            save=False,
            alpha=0.4,
            divide=False
        )

    # Search from the root, random trees
    if True:
        plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            save=True
        )

        plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            save=True, save_extra_name="no_divide",
            divide=False
        )

        multi_plot(
            [
                ("data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Paper"),
                ("data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv", "Whiteboard"),
                ("data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv", "Search from Root"),
            ],
            save=True, overwrite_save_name="from_root_vs_all_other_no_short_circuit",
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            "data/paper_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=True,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )

        compare_equal_experiments_plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            "data/whiteboard_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=True,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )

        compare_equal_experiments_plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            "data/whiteboard_optimized_version_from_exp_spread_to_leaves_no_short_circuit.csv",
            save=False,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )

        # compare_equal_experiments_plot(
        #     "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
        #     "data/level_linked_tree_from_leaves_to_exp_spread_no_short_circuit.csv",
        #     save=False,
        #     alpha=0.4,
        #     fair_y_axis=True,
        #     with_average_pr_rank_difference=True,
        #     group_rank_difference=True
        # )

        compare_equal_experiments_plot(
            "data/pred_search_from_root_from_exp_spread_to_leaves_random_trees.csv",
            "data/LCA_version_from_exp_spread_to_leaves.csv",
            save=False,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True,
            group_rank_difference=True
        )

    # Folded trees, random trees, search with LCA finger search
    if True:
        plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            save=True
        )

        plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            save=True, save_extra_name="no_divide",
            divide=False
        )

        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv", "Folded Tree, LCA version"),
                ("data/LCA_version_from_exp_spread_to_leaves.csv", "Unfolded Tree, LCA"),
            ],
            save=False,
            alpha=0.4
        )

    if True:
        multi_plot_constant_rank_diff(
            [
                ("data/folded_tree_perfect_trees_LCA_version_constant_rank_diff_16.csv", "Folded Tree, LCA, 16"),
                ("data/folded_tree_perfect_trees_LCA_version_constant_rank_diff_8.csv", "Folded Tree, LCA, 8"),
                ("data/folded_tree_perfect_trees_LCA_version_constant_rank_diff_4.csv", "Folded Tree, LCA, 4"),
                ("data/folded_tree_perfect_trees_LCA_version_constant_rank_diff_2.csv", "Folded Tree, LCA, 2"),
            ],
            save=False,
            alpha=0.4
        )
    
    # Folded trees, random trees, paper version
    if True:
        plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            save=True
        )

        plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version_no_short_circuit.csv",
            save=False
        )

        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv", "Short circuit"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version_no_short_circuit.csv", "No short circuit"),
            ],
            save=False,
            alpha=0.4
        )

    if True:
        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv", "LCA version"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv", "Paper version"),
            ],
            save=True,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            save=False,
            alpha=0.4,
            fair_y_axis=True
        )

        compare_equal_experiments_plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            save=True,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True, group_rank_difference=True
        )
    
    # Folded trees, random trees, whiteboard version
    if True:
        plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv",
            save=True
        )

        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv", "Whiteboard version"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv", "Paper version"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv",
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv",
            save=True,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True, group_rank_difference=True
        )

        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv", "Whiteboard version"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv", "LCA version"),
            ],
            save=False,
            alpha=0.4
        )

        multi_plot(
            [
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_paper_version.csv", "Paper version"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv", "Whiteboard version"),
                ("data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv", "LCA version"),
            ],
            save=False,
            alpha=0.4
        )

        compare_equal_experiments_plot(
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_LCA_algorithm.csv",
            "data/folded_tree_random_trees_from_many_nodes_to_exp_spread_whiteboard_version.csv",
            save=True,
            alpha=0.4,
            fair_y_axis=True,
            with_average_pr_rank_difference=True, group_rank_difference=True
        )
