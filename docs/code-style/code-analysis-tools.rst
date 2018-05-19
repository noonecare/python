====================
代码检查工具
====================

:Author: 王蒙
:Tags: python 开发，编码规范，持续集成

:abstract:

    `Pylint`_ , `flake8`_ 等代码检查工具能够帮助我们写出更规范的代码。本文简述了代码检查工具常用的用法，更高级的操作，还是需要查看工具的文档。

.. contents::


Audience
========

Python 开发

Prerequisites
=============

pep8 代码规范， CI（持续集成），圈复杂度

Problem
=======

- 为什么需要代码检查工具？
- Python 主流代码检查工具？
- Pylint
- flake8
- Pycharm

Solution
========


- 为什么需要代码检查工具？

    - 能大大提高检查代码的效率。代码（规范）检查重点在于**一致性**，包含大量机械化检查的工作。
    - 能强制贯彻代码规范的执行。比如可以把代码检查放到 CI 流程，不通过代码监测不让合并到 develop 分支，这样就能保证 develop 分支中的代码都是符合规范的代码。


- Python 主流代码检查工具？

    现在，几乎所有语言都有代码检查工具。Python 中主流的代码检查工具为： **Pylint** 和 **flake8** 。

    不管哪种检查工具，都会报告被检查代码，哪些行的哪些列的代码不合哪些规范。比如如下检查结果：

    .. code-block::

        # 检查 mock_demo.py 是否符合规范
        $ pylint mock_demo.py
        No config file found, using default configuration
        ************* Module python-test-demo.mock_demo
        C: 46, 4: Missing method docstring (missing-docstring)
        C: 52, 0: Constant name "a" doesn't conform to UPPER_CASE naming style (invalid-name)
        W: 54, 0: Expression "'complex_add' in dir(a)" is assigned to nothing (expression-not-assigned)

        -----------------------------------
        Your code has been rated at 5.95/10


    上面检查结果，告诉我们：

        - 代码的第 46 行， 第 4 列的代码，缺少 module docstring 不符合规范。
        - 代码的第 52 行， 第 0 列的代码，常量 a 应该采用 UPPER_CASE 命名规范。
        - ...

    根据代码检查结果，修改代码，会让代码合乎代码规范。

    Pylint 和 flake8 各有特点，具体来说：

        - Pylint 可以自定义代码规范，非常灵活。

        - flake8 提供了计算 **圈复杂度** 的功能。


- Pylint

    - Pylint 会给被检查代码评分，根据评分可以大概估计代码质量。

        采用 Pylint 默认配置检查了 flask 代码以及一些 Python 内建包的代码，发现 Pylint 给出的评分在 7.5 以上。基本上我们写代码，如果评分达到 7 分，说明代码质量可以的（单说格式是否规范）。

    - Pylint 可以灵活配置。

        PEP 8 是 Python 推荐的代码规范。实际一个团队用 Python 开发时，可能会针对 PEP 8 没有明确规定的细节给出组内规范；也可能因为某些原因（历史原因，项目个性需求，领导强制要求等）给出违背 PEP 8 的规范。

        Pylint 可以按照定制化的代码规范检查 Python 代码，只要把规范写到 Pylint 的配置中即可。

        pylint 默认根据工作目录下的 **.pylintrc** （该文件指明了代码规范）检查代码，如果工作目录下没有 **.pylintrc** 文件，就会使用默认的代码规范检查代码。

        自定义规范一般是在默认代码规范基础上做定制。使用

            .. code-block::

                $ pylint --generate-rcfile > .pylintrc

        在工作目录生成默认规范的配置文件，修改 .pylintrc 中的选项值，就能定制代码规范（比如把 max-line-length=100 改为 max-line-length=79）。.pylintrc 中每一项配置上方有注释，说明该项配置有什么效果。


- flake8

    flake8 默认会使用 pep8 第三方包检查代码（经常会安装 mccabe 和 pyflakes，安装之后，flake8 就会提供个性的功能）。 pep8 第三方包只能检查代码是否符合 pep8 代码规范（所以 flake8 默认是使用 pep8 代码规范做检查）。

    相对于 Pylint ， flake8 提供了些个性化的功能。


        - 检查代码的 **圈复杂度** （flake8 会调用 mccabe 计算圈复杂度）。


            - 圈复杂度和 if 语句有关，选择分支越多，圈复杂度越高。

            - 圈复杂度越低越好。圈复杂度高影响代码可读性，代码容易出错。

            - flake8 官网建议圈复杂不要超过 12 。

            - 更多圈复杂度的内容插件 `圈复杂度`_ 。

                .. code-block::

                    # 检查圈复杂度
                    $ flake8 --max-complexity 1 mock_demo.py
                    mock_demo.py:62:1: C901 'calculate_inverse' is too complex (2)
                    mock_demo.py:66:80: E501 line too long (89 > 79 characters)
                    mock_demo.py:70:1: C901 'test_calculate_f' is too complex (2)
                    mock_demo.py:74:80: E501 line too long (81 > 79 characters)


                flake8 的检查结果，告诉我们 mock_demo.py 第 62 行的 calculate_inverse 的圈复杂度大于2（这里这是个列子，一般认为圈复杂度小于等于 12 都可以接受）。

        - 通过在源码中加注释，通知 flake8 不要检查该行代码。

            .. code-block:: Python

                -*- coding: utf-8 -*-
                import os
                # noqa(no quality analysis) 告诉 flake8 不要检查该行代码。
                from fabric.api import * # noqa
                from fabric.contrib.files import exists


        - flake8 使用 pyflakes(只要Python 解释器安装了 pyflakes，flake8 就会使用 pyflakes) 检查代码。pyflakes 不报告格式不规范的问题，pyflakes 只报告代码语法上的错误（pylint 也会检查代码错误，所以这一点不算特性）。


- Pycharm


    - Pycharm Ctrl+Alt+L 快捷键会自动规范代码格式。我写代码的时候，经常会点这个键。
    - Pycharm inspect code 功能会检查代码。
    - Pycharm 可以勾选 git -> before commit -> perform code-analysis 。这样在提交代码之前会自动检查代码，确保每次提交都是合乎规范的代码。

        .. image:: pycharm_analysis_before_commit.png

Reference
=========

- Pylint 文档： https://pylint.readthedocs.io/en/latest/
- flake8 文档： http://flake8.pycqa.org/en/latest/
- PEP8 文档： http://pep8.org/

.. _Pylint: https://www.pylint.org/
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _pep8: http://pep8.readthedocs.io/en/release-1.7.x/
.. _圈复杂度: 圈复杂度.rst