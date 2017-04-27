# coding: utf-8

"""
python 中常用的包是 os, 和 pathlib(唯一的好处在于可以用 glob 的方式选择多个文件)
"""

import os

import pathlib


# 连接路径，对于 linux 用 / 链接，对于 windows 用 \ 连接。这样写的代码通用于各种操作系统
print(os.path.join("test", "test.txt"))
# 得到当前源码文件所在的目录
print(os.path.dirname(__file__))
# 得到当前源码文件的绝对路径
print(os.path.abspath(__file__))
# 得到当前源码文件的文件名
print(os.path.split(os.path.abspath(__file__))[-1])
# remove
# os.remove(<path>)
# mkdir
# os.mkdir()

p = pathlib.Path(os.path.dirname(__file__))
for file in p.glob("*demo"):
    print(file)
