import sys, os, inspect
from time import sleep

PRINT_STATE_NORMAL = 0
PRINT_STATE_DETECT = 1
PRINT_STATE_BLOCK = 2
PRINT_STATE = PRINT_STATE_NORMAL

def blockPrint():
    global PRINT_STATE
    PRINT_STATE = PRINT_STATE_BLOCK
    sys.stdout = open(os.devnull, 'w')

def detectPrint(header):
    global PRINT_STATE
    PRINT_STATE = PRINT_STATE_DETECT
    real_write = sys.stdout.write
    def new_write(string):
        global PRINT_STATE
        sys.stdout.write = real_write
        if PRINT_STATE == PRINT_STATE_DETECT:
            real_write(f"\x1b[2K\n{header}\n\n{string}")
        else:
            real_write(string)
        PRINT_STATE = PRINT_STATE_NORMAL
    sys.stdout.write = new_write

def enablePrint():
    global PRINT_STATE
    PRINT_STATE = PRINT_STATE_NORMAL
    sys.stdout = sys.__stdout__


def is_callable_with(f, *args, **kwargs):
    try:
        inspect.signature(f).bind(*args, **kwargs)
        return True
    except TypeError:
        return False


GREEN = "\u001b[32m"
RED = "\u001b[31m"
YELLOW = "\u001b[33m"
STOP = "\u001b[0m"

EXECUTING = f"[{YELLOW}EXEC{STOP}]"
PASS = f"[{GREEN}PASS{STOP}]"
FAIL = f"[{RED}FAIL{STOP}]"

CURRENT_INDENT = 0
INDENT = lambda: "   " * CURRENT_INDENT
PASS_TOTAL_COUNT = FAIL_TOTAL_COUNT = 0
PASS_FILE_COUNT = FAIL_FILE_COUNT = 0
PASS_GROUP_COUNT = FAIL_GROUP_COUNT = 0


def test(f):
    def g(*args, **kwargs):
        global PASS_TOTAL_COUNT, FAIL_TOTAL_COUNT, PASS_FILE_COUNT, FAIL_FILE_COUNT, PASS_GROUP_COUNT, FAIL_GROUP_COUNT
        name = f.__name__
        if args or kwargs:
            print_args = ", ".join([str(arg) for arg in args] + [f"{k}={v}" for k, v in kwargs.items()])
            name += f"({print_args})"
        print(f"{INDENT()}{EXECUTING} {name}\r", end="")
        
        raise_error_flag = 'raise_error' in kwargs and kwargs['raise_error']
        if raise_error_flag:
            kwargs.pop('raise_error', None)

        print_flag = 'verbose' in kwargs and kwargs['verbose']
        if print_flag:
            detectPrint(f"Print from {name}:")
        else:
            blockPrint()
        
        if not is_callable_with(f, *args, **kwargs):
            kwargs.pop('verbose', None)

        try:
            f(*args, **kwargs)
            
            if print_flag and PRINT_STATE == PRINT_STATE_NORMAL:
                print()
            
            enablePrint()
            print(f"{INDENT()}{PASS} {name}")
            
            PASS_TOTAL_COUNT += 1
            PASS_FILE_COUNT += 1
            PASS_GROUP_COUNT += 1
        
        except AssertionError:
            if print_flag and PRINT_STATE == PRINT_STATE_NORMAL:
                print()
            
            enablePrint()
            print(f"{INDENT()}{FAIL} {name}")
            
            FAIL_TOTAL_COUNT += 1
            FAIL_FILE_COUNT += 1
            FAIL_GROUP_COUNT += 1

            if raise_error_flag:
                raise
        
        except Exception:
            enablePrint()
            print(f"\n\nException occured while running test {name}:\n")
            raise 

    return g

# TODO: group in group does not work
def test_group(f):
    def g(*args, **kwargs):
        global CURRENT_INDENT, PASS_GROUP_COUNT, FAIL_GROUP_COUNT
        PASS_GROUP_COUNT = FAIL_GROUP_COUNT = 0
        print(f"{INDENT()}Running {f.__name__} ...")
        CURRENT_INDENT += 1
        f(*args, **kwargs)
        CURRENT_INDENT -= 1
        total_group_count = PASS_GROUP_COUNT + FAIL_GROUP_COUNT
        print(f"{INDENT()}{PASS if FAIL_GROUP_COUNT == 0 else FAIL} {f.__name__} ({PASS_GROUP_COUNT}/{total_group_count})")
        print()

    return g

def test_file(f):
    def g(*args, **kwargs):
        global CURRENT_INDENT, PASS_FILE_COUNT, FAIL_FILE_COUNT
        PASS_FILE_COUNT = FAIL_FILE_COUNT = 0
        name = f.__globals__['__file__'].split('/')[-1]
        print(f"Running file {name} ...")
        CURRENT_INDENT = 1
        f(*args, **kwargs)
        CURRENT_INDENT = 0
        total_file_count = PASS_FILE_COUNT + FAIL_FILE_COUNT
        print(f"{PASS if FAIL_FILE_COUNT == 0 else FAIL} File {name} ({PASS_FILE_COUNT}/{total_file_count})")
        print()
    
    return g

def test_main(f):
    def g(*args, **kwargs):
        global PASS_TOTAL_COUNT, FAIL_TOTAL_COUNT
        f(*args, **kwargs)
        total_count = PASS_TOTAL_COUNT + FAIL_TOTAL_COUNT
        print(f"{PASS if FAIL_TOTAL_COUNT == 0 else FAIL} Summary ({PASS_TOTAL_COUNT}/{total_count})")

    return g

@test
def sample_test_positive():
    assert True

@test
def sample_test_negative():
    assert False

@test
def sample_test_long():
    sleep(2)
    assert True

@test
def sample_test_may_print_long(verbose=False):
    sleep(2)
    if verbose:
        print("This is a long test")
    sleep(2)
    assert True

@test
def sample_test_positive_prints():
    print("This is a positive test")
    assert True

@test
def sample_test_negative_prints():
    print("This is a negative test")
    assert False

@test
def sample_test_with_args(a, b):
    assert a == b

@test
def sample_test_with_kwargs(i=2):
    assert True

@test
def sample_test_with_args_and_kwargs(a, b, i=2):
    assert a == b

@test_group
def sample_group():
    sample_test_positive()
    sample_test_negative()
    sample_test_long()

@test_group
def sample_group_prints():
    sample_test_positive_prints()
    sample_test_negative_prints()
    sample_test_positive_prints(verbose=True)
    sample_test_may_print_long(verbose=True)
    sample_test_may_print_long(verbose=False)

@test_group
def sample_group_with_args():
    sample_test_with_args(1, 1)
    sample_test_with_kwargs()
    sample_test_with_kwargs(i=4)
    sample_test_with_args_and_kwargs(1, 1, i=4)

@test_file
def sample_file():
    sample_group()
    sample_group_prints()
    sample_group_with_args()

@test_main
def sample_main():
    sample_file()


if __name__ == "__main__":
    sample_main()
