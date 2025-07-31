from Mock_FT_Folded_Tree import Mock_Folded_Tree, Mock_Node
from Many_Pointers_Red_Black_Tree import Red_Black_Tree, Red_Black_Node

from Pointer_Counting import get_pointer_count, get_compare_count, reset_counts, set_do_count

import random
import math
from itertools import count

import matplotlib.pyplot as plt


import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)



def save_and_show(name):
    plt.savefig(f"plot/{name}.png")
    plt.show()
    # plt.clf()

plt.save_and_show = save_and_show


# TODO: this is reused from the test env
def create_random_folded_tree(n, seed=None):
    tree = Red_Black_Tree()

    if seed is not None:
        random.seed(seed)
    
    values = list(range(n))
    random.shuffle(values)
    
    for v in values:
        tree.insert(v)
    
    folded_tree = Mock_Folded_Tree.create_folded_tree(tree)

    return folded_tree


# TODO: move this to some util generator file?
def create_perfect_tree(h, with_red_layers=False):
    def gen_subtree(h, label_generator) -> tuple[Red_Black_Node, Red_Black_Node, Red_Black_Node]:
        is_red = False if not with_red_layers else h % 2 == 1

        if h == 1:
            node = Red_Black_Node(value=next(label_generator), is_red=is_red)
            return node, node, node
        
        left_min, left_root, left_max = gen_subtree(h - 1, label_generator)
        node = Red_Black_Node(value=next(label_generator), is_red=is_red)
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
    
    if with_red_layers:
        assert h % 2 == 0

    tree = Red_Black_Tree()
    if h != 0:
        _, root, _ = gen_subtree(h, count(0, 1))
        tree._root = root
    
    return tree


def create_perfect_folded_tree(h, with_red_layers=False):
    tree = create_perfect_tree(h, with_red_layers=with_red_layers)
    folded_tree = Mock_Folded_Tree.create_folded_tree(tree)
    return folded_tree

# ---------------------------------------------
#                  Analysis
# ---------------------------------------------

def analyse_unfolded_access_constant(file_name, access_func, folded_tree, extra_header, is_last_lower_use_short_circuit=True):
    Mock_Node.is_last_lower = Mock_Node._is_last_lower_short_circuit if is_last_lower_use_short_circuit else Mock_Node._is_last_lower_no_short_circuit

    with open(file_name, "a") as file:
        for start_node in folded_tree:
            reset_counts()
            set_do_count(True)

            end_node = access_func(start_node)

            set_do_count(False)

            end_value = end_node.value if end_node is not None else -1
            pointer_access = get_pointer_count()
            comparisons = get_compare_count()
            assert comparisons == 0

            file.write(f"{extra_header}{start_node.value},{end_value},{pointer_access}\n")

def analyse_unfolded_access_constant_random_tree(file_name, access_func, is_last_lower_use_short_circuit=True):
    print(f"Running analysis for file {file_name}...")

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,pointer_access\n")

    n = 10_000
    
    for seed in range(10):
        print(f"Starting {seed = }...")
        
        folded_tree = create_random_folded_tree(n=n, seed=seed)

        analyse_unfolded_access_constant(
            file_name, access_func, folded_tree, f"{seed},{n},", is_last_lower_use_short_circuit=is_last_lower_use_short_circuit
        )

def analyse_unfolded_access_constant_perfect_tree(file_name, access_func, with_red_layers=False, is_last_lower_use_short_circuit=True):
    print(f"Running analysis for file {file_name}...")

    with open(file_name, "w+") as file:
        file.write("n,start_value,end_value,pointer_access\n")

    h = 16
    n = 2**h - 1
    folded_tree = create_perfect_folded_tree(h=h, with_red_layers=with_red_layers)

    analyse_unfolded_access_constant(
        file_name, access_func, folded_tree, f"{n},", is_last_lower_use_short_circuit=is_last_lower_use_short_circuit
    )


def analyse_shortest_distance_all_node_pairs(file_name):
    print(f"Running analysis for file {file_name}...")

    with open(file_name, "w+") as file:
        file.write("seed,n,start_value,end_value,rank_difference,distance\n")

        n = 1000

        for seed in range(5):
            print(f"Starting {seed = }...")

            folded_tree = create_random_folded_tree(n=n, seed=seed)
            
            # Run BFS from each node
            for start_node in folded_tree:
                start_value = start_node.value
                seen = [False] * n
                queue = [(0, start_node)]

                for dis, at in queue:
                    if at is None or seen[at.value]:
                        continue
                    seen[at.value] = True
                    
                    if start_value < at.value:
                        file.write(f"{seed},{n},{start_value},{at.value},{at.value - start_value},{dis}\n")
                    
                    queue.append((dis + 1, at.parent))
                    queue.append((dis + 1, at.left))
                    queue.append((dis + 1, at.right))


# ---------------------------------------------
#                  Plotting
# ---------------------------------------------

def plot_unfolded_access_constant(
        file_names_and_type,
        save=False, save_extra_name=None
    ):

    plt.subplots(figsize=(10, 6))

    all_access_times = []
    all_access_names = []

    for i, (file_name, access_name) in enumerate(file_names_and_type):
        with open(file_name, "r") as file:
            lines = file.readlines()
        
        column_names = lines[0].strip().split(",")
        raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]

        access_times = [data_point["pointer_access"] for data_point in raw_data]
        all_access_times.append(access_times)
        all_access_names.append(access_name)

        # plt.plot([i]*len(access_times))
    
    # plt.ylabel("Pointer Access", fontsize=12)
    plt.ylabel("Pointer Access")
    plt.boxplot(all_access_times, vert=True, labels=all_access_names, sym=".")

    plt.ylim((0, 60))

    plt.tight_layout()

    if save:
        name = "folded_unfolded_access_constant"
        if save_extra_name is not None:
            name = f"{name}__{save_extra_name}"
        plt.save_and_show(name)
    else:
        plt.show()


def plot_shortest_distance_and_rank_diff(
        file_name,
        save=True,
        divide=False,
        x_scale_log=True
    ):
    plt.subplots(figsize=(10, 6))

    with open(file_name, "r") as file:
        lines = file.readlines()
    
    column_names = lines[0].strip().split(",")
    raw_data = [dict(zip(column_names, map(int, line.strip().split(",")))) for line in lines[1:]]

    data = []
    for data_point in raw_data:
        x_value = data_point["rank_difference"]
        y_value = data_point["distance"]
        if divide and x_value > 1:
            y_value /= math.log2(x_value)
        data.append((x_value, y_value))

    plt.plot(*zip(*data), ".", alpha=0.2)
    
    if x_scale_log:
        plt.xscale("log")
    
    plt.xlabel("$d$ (Rank Difference)")
    plt.ylabel(f"Shortest Distance{'/ log($d$)' if divide else ''}")
    
    if save:
        plt.save_and_show(f"folded_compare_distance_and_rank_diff_divide_{divide}_x_scale_log_{x_scale_log}")
    else:
        plt.show()


if __name__ == "__main__":
    unfolded_access = [
        ("parent", lambda node: node.unfolded_parent),
        ("left", lambda node: node.unfolded_left),
        ("right", lambda node: node.unfolded_right),
        ("predecessor", lambda node: node.predecessor),
        ("successor", lambda node: node.successor),
    ]

    if True:
        for short_circuit in [True, False]:
            extra_str = "" if short_circuit else "_no_short_circuit"
            for name, func in unfolded_access:
                analyse_unfolded_access_constant_random_tree(
                    file_name = f"data/folded_tree_unfolded_access_constant_random_tree_{name}{extra_str}.csv",
                    access_func = func,
                    is_last_lower_use_short_circuit=short_circuit
                )
    
    if True:
        for short_circuit in [True, False]:
            extra_str = "" if short_circuit else "_no_short_circuit"
            for with_red in [False, True]:
                for name, func in unfolded_access:
                    analyse_unfolded_access_constant_perfect_tree(
                        file_name = f"data/folded_tree_unfolded_access_constant_perfect_tree_with_red_{with_red}_{name}{extra_str}.csv",
                        access_func = func,
                        with_red_layers=with_red,
                        is_last_lower_use_short_circuit=short_circuit
                    )

    if True:
        analyse_shortest_distance_all_node_pairs(
            "data/folded_tree_measure_distance_and_rank_diff.csv"
        )


    if True:
        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_random_tree_parent.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_random_tree_left.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_random_tree_right.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_random_tree_predecessor.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_random_tree_successor.csv", "Successor"),
        ], save=True, save_extra_name="random_tree")

        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_parent.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_left.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_right.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_predecessor.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_successor.csv", "Successor"),
        ], save=True, save_extra_name="perfect_tree_no_red")

        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_parent.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_left.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_right.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_predecessor.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_successor.csv", "Successor"),
        ], save=True, save_extra_name="perfect_tree_with_red")


        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_random_tree_parent_no_short_circuit.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_random_tree_left_no_short_circuit.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_random_tree_right_no_short_circuit.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_random_tree_predecessor_no_short_circuit.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_random_tree_successor_no_short_circuit.csv", "Successor"),
        ], save=True, save_extra_name="random_tree_no_short_circuit")

        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_parent_no_short_circuit.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_left_no_short_circuit.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_right_no_short_circuit.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_predecessor_no_short_circuit.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_False_successor_no_short_circuit.csv", "Successor"),
        ], save=True, save_extra_name="perfect_tree_no_red_no_short_circuit")

        plot_unfolded_access_constant([
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_parent_no_short_circuit.csv", "Parent"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_left_no_short_circuit.csv", "Left"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_right_no_short_circuit.csv", "Right"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_predecessor_no_short_circuit.csv", "Predecessor"),
            ("data/folded_tree_unfolded_access_constant_perfect_tree_with_red_True_successor_no_short_circuit.csv", "Successor"),
        ], save=True, save_extra_name="perfect_tree_with_red_no_short_circuit")


    if True:
        plot_shortest_distance_and_rank_diff(
            "data/folded_tree_measure_distance_and_rank_diff.csv",
            save=True
        )

        plot_shortest_distance_and_rank_diff(
            "data/folded_tree_measure_distance_and_rank_diff.csv",
            save=True,
            divide=True
        )

        plot_shortest_distance_and_rank_diff(
            "data/folded_tree_measure_distance_and_rank_diff.csv",
            save=True,
            x_scale_log=False
        )

        plot_shortest_distance_and_rank_diff(
            "data/folded_tree_measure_distance_and_rank_diff.csv",
            save=True,
            x_scale_log=False,
            divide=True
        )
