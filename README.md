# Pure Binary Finger Search Trees

This repository contains a mock implementation of the *Pure Binary Finger Search Trees* created by Brodal and Rysgaard, which is introduced in the paper [available here](http://doi.org/10.1137/1.9781611978315.14).

This implementation was created mainly to demonstrate the finger search algorithm the *folded tree* allows, and the implementation is therefore not a complete folded tree. Specifically, the implementaion does not permit updates on the folded trees.
In the [Legacy](Legacy/) folder, some older implementations are available, which contains an initial mock up of a folded tree, which allows insertions. However, this mock up only does left folding, and therefore does not allow finger searching.
For more details on the construction, see the paper.

The implementation contains a complete version of the linked list trees introduced in the same paper by Brodal and Rysgaard.

Additionally, new finger search algorithms have been created after publishing the paper, which are also contained in this implementation.
For more details on these, as well as a discussion of the experiments, see Section **Missing section number** of the Ph.D. Thesis of Rysgaard at **Missing link**.[^1]

## Code structure

| File | Decription |
| --- | ------ |
| __test_decorators.py | A homemade framework for creating tests using decorators, which allows for print supression, error handling and pretty printing to the terminal. |
| \_test\_\*.py | Test files for correctness. |
| \_analyse\_\*.py* | The experiments on finger searching and the distance of nodes in the folded tree. |
| FT\_\*.py | Failed attempt at creating a proper Folded Tree. |
| Finger_Search.py | Implementations of the finger search algorithms discussed in the paper, as well as the new additions. |
| Many\_Pointers\_Red\_Black\_Tree.py | A red-black tree where each node contains explicit pointers to the predesessor and successor nodes, which is the structure the folded trees emulate. Note that this structure does allow updates. |
| Mock\_FT\_Folded\_Tree.py | A mock folded tree, created by folding a red-black tree. Each node is *pure*, and traversal as if following the pointers of the unfolded tree is supported. Note that this structure does *not* allow updates. |
| util.py | Utility, consisting mainly of a function allowing for printing a binary tree as ascii art in the terminal to use in debugging. |
| Pointer\_counting.py | Software counters used to simulate time in the experiments, counting the number of read and writes to pointers and bits, as well as the number of comparisons performed. |
| SLL\_\*.py | Implementation where the metanodes use a simple linked list implementation. This is a fully functional Finger Search Tree with *almost* pure nodes, each containing only a value and two pointers. For more information, read Section 9 of the paper. |

## Citation

The paper:
```
@inproceedings{DBLP:conf/sosa/BrodalR25,
  author       = {Gerth St{\o}lting Brodal and
                  Casper Moldrup Rysgaard},
  editor       = {Ioana Oriana Bercea and
                  Rasmus Pagh},
  title        = {Pure Binary Finger Search Trees},
  booktitle    = {2025 Symposium on Simplicity in Algorithms, {SOSA} 2025, New Orleans,
                  LA, USA, January 13-15, 2025},
  pages        = {172--195},
  publisher    = {{SIAM}},
  year         = {2025},
  doi          = {10.1137/1.9781611978315.14}
}
```

This code:
```
@misc{pure_trees_impl,
  author = {Casper Moldrup Rysgaard},
  url = {https://github.com/Crowton/PureBinaryFingerSearchTrees},
  title = {Pure Binary Finger Search Trees Implementation},
  year = {2025}
}
```

[^1]: The thesis is not yet public and is therefore not linked yet.
