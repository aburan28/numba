from __future__ import print_function
from numba import jit, int32
from numba import unittest_support as unittest


def foo(a, b):
    return a + b


def bar(a, b):
    return cfoo(a, b) + b

@jit
def inner(x, y):
    return x + y

@jit(nopython=True)
def outer(x, y):
    return inner(x, y)


class TestInterProc(unittest.TestCase):
    def test_bar_call_foo(self):
        global cfoo
        cfoo = jit((int32, int32), nopython=True)(foo)
        cbar = jit((int32, int32), nopython=True)(bar)
        self.assertTrue(cbar(1, 2), 1 + 2 + 2)

    def test_callsite_compilation(self):
        self.assertEqual(outer(1, 2), 1 + 2)


if __name__ == '__main__':
    unittest.main()
