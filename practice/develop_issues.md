# python practice

----

# 引用 module 的路径

- site-packages 目录
- .pth 文件
- PYTHONPATH 环境变量

查看当前 python 解释器的引用包路径

```python
import sys
print(sys.path)

# 添加路径 a 到引用 module 路径中
sys.path.append(a)
```


----

# python 安装 module

```shell
pip install <module>
```

```shell
easy_install <module>
```

```shell
tar zxvf <module>.tar.gz
cd <module>
python setup.py install
```

在一台共享的服务器上， 你不是管理员，但是你需要安装 module, 该怎么做。

- 通知服务器管理员，征得服务器管理员的同意（一般如果管理员觉得绝大多数用户都会用到这个 module 的话，管理员应该同意安装；如果只有少量用户需要用到这个 module 则不必安装），由服务器管理员代为安装 module。
- 自己创建一个 virtual python interrepter, 可以使用

```shell
pyenv <interrepter_name>
```
or
```shell
virutalenv <interrepter_name>
```
据我实践， pyenv 安装出的虚拟环境有时候不带 pip, easy_install 这些装 module 的工具，所以使用起来不方便，推荐使用 virtualenv 创建仅供个人使用的 python interrepter。


-----

# 当前目录

在写程序时常常会因为路径问题导致程序无法运行， 遵从以下规范可以避免因为路径浪费时间：
- 一个 project 中所有的可执行文件都以 project 的 root 目录作为 根目录
- python 包中不变的资源文件 使用 __file__ 变量写成相对路径
- python 包内引用使用
```python
from .[<parent_module>] import <module>
```


-----

# 测试用例



-----

# PyCharm


