from test_decorators import test_main

import test_regular_RB_tree
import test_convert
import test_zigzag_RB_tree

# TODO: negative tests

@test_main
def test_all():
    test_regular_RB_tree.test_all()
    test_convert.test_all()
    test_zigzag_RB_tree.test_all()

if __name__ == "__main__":
    test_all()
