Welcome to wangmeng-python's documentation!
===========================================

一般会对软件做如下测试：

   - acceptance test

       把软件当做黑盒做测试，确保软件实现了当初设计的功能。这部分测试，不是由开发者做的，而是由 QA staff 甚至客户去做的。

   - unit test

       针对类函数功能的测试，单元测试由开发人员来写，是 TDD 的基础。

   - Functional tests

       重点测试整体的功能而不是每个代码单元。和 acceptance tests 的不同，在于 acceptance tests 完全是使用用户接口做测试。Functional tests 可以不必从用户接口做测试。比如测试 HTTP 服务器时，使用浏览器访问（模拟用户的使用）就是 acceptance tests。使用 Postman 直接整 HTTP 请求去测试，就是 Functional tests。


   - Integration tests

       重点测试不同软件部件之间是否如预期的那样交互。


   - Load and performance testing

       performance testing 很难，不同机器之间 CPU ，Memory 和 IO 性能不同会影响程序的性能。就算是同一台机器 CPU, Memory 和 IO 性能也不是一层不变的。

   - Code quality testing

       - PEP8 规范（pylint ）
       - Complexity metrics, 比如圈复杂度（flake8 可以测）
       - 代码覆盖率（coverage）
       - 编译时 warning 的数量（python 没有，Java 有）
       - 文档是否够全（这个我没有找到现成的工具去做，估计语意方面的检查只能靠人去检查）

测试过程中很用到很多`工具`_ 。下面各个小节会介绍每一方面的工具。


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pytest
   框架自带单元测试工具
   项目构建工具
   代码覆盖率
   Mock 测试环境 or Docker 虚拟测试环境
   持续集成


.. _工具: https://wiki.python.org/moin/PythonTestingToolsTaxonomy