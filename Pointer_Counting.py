_get_pointer_count = 0
_set_pointer_count = 0
_get_bit_count = 0
_set_bit_count = 0
_compare_count = 0

_do_count = True

def set_do_count(do_count):
    global _do_count
    _do_count = do_count

def reset_get_pointer_count():
    global _get_pointer_count
    _get_pointer_count = 0

def reset_set_pointer_count():
    global _set_pointer_count
    _set_pointer_count = 0

def reset_get_bit_count():
    global _get_bit_count
    _get_bit_count = 0

def reset_set_bit_count():
    global _set_bit_count
    _set_bit_count = 0

def reset_compare_count():
    global _compare_count
    _compare_count = 0

def reset_counts():
    reset_get_pointer_count()
    reset_set_pointer_count()
    reset_get_bit_count()
    reset_set_bit_count()
    reset_compare_count()

def get_pointer_count():
    return _get_pointer_count

def set_pointer_count():
    return _set_pointer_count

def get_bit_count():
    return _get_bit_count

def set_bit_count():
    return _set_bit_count

def get_compare_count():
    return _compare_count

def total_count_pointers():
    return _get_pointer_count + _set_pointer_count + _get_bit_count + _set_bit_count

# TODO: fix decorators
# def pointer_getter(f):
#     def count():
#         if _do_count: _get_pointer_count += 1
#         return f()
#     return count

# def pointer_setter(f):
#     def count():
#         if _do_count: _set_pointer_count += 1
#         return f()
#     return count

# def bit_getter(f):
#     def count():
#         if _do_count: _get_bit_count += 1
#         return f()
#     return count

# def bit_setter(f):
#     def count():
#         if _do_count: _set_bit_count += 1
#         return f()
#     return count

def pointer_get():
    if _do_count: global _get_pointer_count; _get_pointer_count += 1

def pointer_set():
    if _do_count: global _set_pointer_count; _set_pointer_count += 1

def bit_get():
    if _do_count: global _get_bit_count; _get_bit_count += 1

def bit_set():
    if _do_count: global _set_bit_count; _set_bit_count += 1


def compare():
    if _do_count: global _compare_count; _compare_count += 1


class CompareWrap:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __lt__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value < other
    def __le__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value <= other
    def __eq__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value == other
    def __ne__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value != other
    def __gt__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value > other
    def __ge__(self, other):
        compare()
        if isinstance(other, CompareWrap):
            other = other._value
        return self._value >= other
    def __str__(self):
        return f"{self._value}"
    def __repr__(self):
        return f"CompareWrap({self._value})"

    def unwrap(self):
        return self._value

def compare_wrap_value(val):
    return CompareWrap(val)
