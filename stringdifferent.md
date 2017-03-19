### python2 和 python3 字符串类型不同

#### Python 编码问题

Python3 中 str 类就是 unicode 类。但是在 python2 中两种不同：

python2 中 str 是 bytes 串（正因为这个原因 python2 的 open 函数没法指定编码，实际上 python2 的open 只能写入读入二进制（bytes）串）。下面的代码，清楚的说明了这一点
```python
# 下面的代码，用 Python2 执行的结果和用 python3 执行的结果不一样。
with open("python2strisbytes", "wb") as f:
        f.write(str("what the hell thing is that: python2 string is bytes not text, that's something odd."))
```

python3 中的 decode 函数会把 二进制串 解码成 unicode(python3 中 unicode 和 str 是一个东西，所以也可以说是把 二进制串 解码成str)。 在 python2 中 decode 函数会把 二进制串(python2 中 二进制串和 str 是同一个东西)解码成 unicode。
下面的代码印证了上面的观点：
```python
print(type("what the hell thing is that: python2 string is bytes not text, that's something odd.".decode("utf-8").encode("gb2312")))
print(type("what the hell thing is that: python2 string is bytes not text, that's something odd.".decode("utf-8")))
```

最后 python2 和 python3 的默认编码不一样。python2 的默认编码是 ascii 码， python3 的默认编码是 utf-8。 正是默认编码的不同导致, 如果 source code 中包含中文， python2 需要明确指定 编码为 utf-8， 而 python3 不需要。关于编码声明，我需要说明的是， 编码声明声明的是当前 source file 的编码。

使用 python2 时，经常会遇见这个错误：

```bashshell
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 157: ordinal not in range(128)
```
这句错误表示，程序发生了 decode 的 操作，而且 执行 decode 时，用的编码是 ascii 码。
下面是 python2 中的三句语句，显示了什么时候会出现上面的错误。
```python
u"算你狠"
```
```python
uicode("算你狠")
```
```python
unicode("算你狠", encoding="utf-8")
```
```python
"算你狠".decode("ascii")
```
```python
"算你狠".decode("utf-8")
```
```python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
u"算你狠"
unicode("算你狠")
```

u 前缀会根据 source file 文件的编码，把字符串解码成 unicode 码。
但是 unicode(), decode() 的默认编码是根据 sys.getfaultencoding() 确定的编码决定的。要修改 sys 的默认编码可以用如下代码
```python
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
unicode("算你狠")
"算你狠".decode()
```

以上就是 python2 和 python3 的字符串的不同。


### Linux locale

执行 locale 可以看到 linux 对于本地化做的设置。
本地化的内容包括：
- 语言
- 编码
- 货币单位
- 时间格式
- 数字格式
- 时区

大致反映了 用户所在地区的使用习惯。






在C语言中，char 表示的是  编码的字符， WCHAR表示 unicode 编码的字符。


在大多数情况下，字符在内存中的表示都是 unicode 编码的。



编码译码
编码就是把 unicode 映射成二进制串，存在在文件中。译码就是把存在文件中的二进制串转成unicode码读入内存。
编码常用的方式有 utf-8, utf-16, gbk, gb2312, ANSI 等等。

文件
有的文件会用头几个数字指明文件使用的什么编码。这几个数字叫做BOM。但是也有很多文件不带BOM。通常，对于不带BOM的文件，阅读器会自动以utf-8的方式读入文件。在python中open()函数的encoding 参数，不会自动排除BOM，也就是说用 with open("file", encoding='utf-8') as f： 读入一个文件中，如果文件带有BOM，文件就不会正常读取。读取的文件头不会多出-。

读入文件有两种方式，以binary 和以 text 的方式读入文件。Python, C 都允许以这两种方式去读取文件，用 binary 读取文件，读入的是二进制数。以text 读取的文件，需要指定encoding ，而且在读取时，会进行译码，读入的是 unicode 字符串。

操作系统对文件的影响:
windows 默认的换行符是\n\r
Unix 默认的换行符是\n

这一点区别，也会对文件操作有影响。

