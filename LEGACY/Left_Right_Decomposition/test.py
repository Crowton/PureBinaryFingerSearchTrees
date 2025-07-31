import test_regular_RB_tree
import test_convert
import test_zigzag_RB_tree


# TODO: negative tests

if __name__ == "__main__":
    test_regular_RB_tree.test_all()
    test_convert.test_all()
    test_zigzag_RB_tree.test_all()

    print("All tests passed!")
