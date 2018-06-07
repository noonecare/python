import re
from typing import TypeVar


def test_comma():
    my_list = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
        ]
    assert len(my_list) == 9


def f(x: str):
    re.search(r"[0-9]+")
    print(chr(x.index('o')) * 42 + 'xxx')


VT_co = TypeVar('VT_co', covariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)

a = [
    "a",
    "b",
    "c",
    ]

b = ("in remote east, there lived a dragon. its name is China. every one "
     "drinks water from yellow river.")
