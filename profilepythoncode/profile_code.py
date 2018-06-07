"""there are three main tools for profiling python code.
cProfiler,
"""


def test_set_list_diff():
    a = range(10000)
    3 in a
    b = set(a)
    3 in b
