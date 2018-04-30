The seven rules of technical writing
====================================

#. 开始写的时候，专注于内容；然后整个检查一遍，整理格式。
#. 每个文档针对明确的读者。
#. 文档应该写的尽可能简单。比如一句话不要太长，一个段落不要太长等等。
#. 分主题组织文档，给每篇文档写合适的题目。选择标题时，可以想，如果读者对文档内容感兴趣，他会在 Google 中输入什么。
#. 使用统一的格式，使用模板。
#. 不要写过多的文档，特别不要在文档中写废话，开玩笑等等。
#. 示例代码，选择真实的，拿来就能运行的代码片段。


A reStructuredText Primer
=========================


段落:
.. code-block::

    =,-,:,#,+,^

列表:

.. code-block::

    *, -, #.

行内标记:

.. code-block::

    *emphasize*
    **strong emphasize**
    ``what``
    `link`_


reStructedText 和 markdown 都有个毛病，就是连续的两行中间的换行符，在生成文档时，会对应空格。这对于英文是很正确的。但是对于中文，这不对。


可以使用 Docutils 处理 reStructuredText。不过更好用的是 Sphinx ， Sphinx 扩展了 reStructuredText, 添加了很多命令。 toctree 是常用的命令，生成文档树时，会很有用。

Build the portfolio
-------------------

项目文档应该包含哪些内容


- Design
- Usage
    - Recipe, 参考 http://code.activestate.com/recipes/langs/python/
    - Tutorial, 参考
    - Module Helper，


- Operations

    - Installation and deployment documents
    - Administration documents
    - FAQ
    - Documents that explain how people can contribute, ask for help, or provide feedback

Making your own portfolio
-------------------------

不要死守模板，可能需要自己稍作改变

Building the landscape
----------------------

group and organize the documents.  其实就是要建立合理的文件目录结构，在每个层级都要有 index 页。

- Building a tree for the producers(the writers).
- Building a tree for the consumers(the readers) on top of the producer's tree.

Producer's view: 和代码一样是 module。

docs
docs/source
docs/source/design
docs/source/operations
docs/source/usage
docs/source/usage/cookbook
docs/source/usage/modules
docs/source/usage/tutorial


Consumer's view:


用户不会看 reStructured Text 源码，用户看的是编译好的 html 文件。 `Sphinx`_ 扩展了 docutils ， Sphinx 能直接从文档树种编
译出 html 文档。和 docutils 产生的 html 文档，没有 css/javascript 不同， Sphinx 生成的文档带有 css/javascript, 这使得
Sphinx 编译出的文档，比较好看且有动态效果。Sphinx 使用 `pygments` 包高亮语法。



Sphinx 对于 docutils 的扩展表现在：

#. A directive that builds a table of contents
#. A marker that can be used to register a document as a module helper
#. A marker to add an element in the index

Documenting building and continuous integration
-----------------------------------------------

