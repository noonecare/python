#  Python 爬虫

**自动访问 url, 获取 url 资源的程序**

## 重要步骤
写 python 爬虫可以使用专门的[爬虫框架 Scrapy](http://doc.scrapy.org/en/latest/intro/tutorial.html)（现在只支持 python2）,也可以不用这个框架。 不管用不用 Scrapy ， 要做的都是以下四个步骤：

- 找到资源对应的 url
> - 工具： 浏览器，比如 chrome, IE, firefox 等。
> - 使用： [文档](https://segmentfault.com/a/1190000000683599) 简述了 chrome 的使用，我使用比较多的其中的 **Network**，查看**网页源代码**，以及 **审阅元素**的功能。其他浏览器也能完成任务，但是我不太熟悉。
> - tricky part: 查看页面源代码（不运行js代码的结果）， 审阅元素（运行js代码之后的结果）， 你当前看到的网页（运行js代码的结果） 之间的不同。

- 访问 url
> - 工具：  urllib, requests, http 等 python 包； Scrapy 通过设置中间参数（middleware）来控制访问， 不设置 middleware 的话， scrapy 会执行默认的访问 url 的操作（只要你把其他三步做好，这一步就不用管了）。
> - 使用： 我对 scrapy 并不很熟，下面的使用主要介绍 python 包的使用。
>> - [设置 Request 的 header( 包含了 Useragent 信息)](#set_request)
>> - python request 对象表示请求。
>> - 模仿 浏览器对 cookie 的操作： [接受到 cookie 后， 把 cookie 保存起来，下次访问会带着 cookie 去访问](#set_opener)。
>> - python opener 对象相对于浏览器，可以设置 IP， cookie 等。

- 解析网页
> - 工具： bs4.BeatifulSoup, lxml, re, json, xml 等。
> - 使用：
>> - json 可以把 string（如果 string 不是json的格式，解析会出错） 解析成 dict 类型，也可以把 dict 写成 string。
>> - BeatifulSoup 可以解析 html 文档， 提供 **findall, find** 函数[查找相应的标签](#parse_html)。
>> - lxml 可以解析 html 文档，可以使用 **xpath** 的语法查找相应的标签。
>> - xml 可以解析 xml 文档（没法解析 html 文档）， 可以使用 **xpath** 的语法找到相应的标签。
>> - re  正则表达式当然可以用于寻找 **特定模式** 的文本


- 下载 url 的资源
> - 文件读写操作，写入到文件。
> - 也可以直接写入到数据库。



## 好的习惯

- 记录爬取日志
- 异常处理
> - 爬取大量数据，几乎总是会被 ban， 为了让程序可以执行下去，一般要加[异常处理](#handle_exception)。



## 高效的爬虫

爬取的速度越快越好， 但是不可避免地会被禁止访问。

- 多线程提高速度。

> - 爬虫频繁地读写url指向的资源，是IO密集型的程序，用[多线程](#multiple_thread)可以明显提高爬虫爬取的速度（如果不被 ban 的话）
> - 推荐使用 **[消费者生产者模型](#multiple_thread)** 实现多线程。

- [Avoid being banned](http://doc.scrapy.org/en/latest/topics/practices.html?highlight=ban) 总体上讲，模仿**一群人访问网站**的行为。
> - User-Agent rotation（[换 user\_agent](#set_request)）
> - IP spooling （[用代理](#set_opener)； Tor project 可以实现匿名访问，我暂时不太了解 Tor）
> - follow [robots.txt](http://www.jd.com/robots.txt)（在 domain 根目录下的一个文件， 会提示一些信息）
> - [no-follow](http://baike.baidu.com/link?url=asjQBVG3I1oOonydCPnykhLCt_QIHh5NT1_sPiJmo1BAEss1tmFeKjZIixGN2upGvufYNrp73Wa3B6rjIaqW8a) 标签(honey spot)
> - disable cookies（不要用cookies。不过有些网站（比如需要账号和密码）不用 cookies 不能访问）
> - 减速，比如 random sleep some time。

## 不了解的内容

- python 可以用 selenium API 去访问 url。 selenium 会自动加载 js 代码。
- Tor 提供了匿名访问 url 的功能。

## 例子
```python
from pathlib import Path
from bs4 import BeautifulSoup
url = "http://www.zhibo8.com"
```
<span id="set_request">
```python
from urllib import request
headers = {"User-Agent": "Mozillia"}
# 设置 request
my_request = request.Request(url=url, headers=headers)
```
</span>

<span id="set_opener">
```python
from http.cookiejar import CookieJar

# 设置 opener
# 模仿浏览器处理 cookies
cj = CookieJar()

my_opener = request.build_opener(request.HTTPCookieProcessor(cj))


# 使用代理
import urllib
proxy = {'http': '27.24.158.155:84'}
proxy_support = urllib.request.ProxyHandler(proxy)
proxied_opener = request.build_opener(proxy_support)
```
</span>

```python
# opener 打开 request
with my_opener.open(my_request) as r:
        content = r.read()
        content = content.decode("utf-8")
```

<span id="parse_html">
```python
# BeautifulSoup 解析网页
# 找到XX标签， 找到属性 XX 为 YY 的标签，找到包含属性XX的标签， 找到标签的父子元素
# 获得标签的属性值，获得标签的斧子元素
# 解析 html 文档
soup = Beautiful(content)
soup.a
soup.find(a)
soup.find(lambda tag: tag.has_attr("href"))
soup.find(href="http://www.zhibo8.com")
# class 属性稍微特殊一点
soup.find(class_="prod_img")
```
</span>

```python
# lxml 解析网页， lxml 解析 html 网页还是会用到 BeautifulSoup 解析网页的 parser
from lxml import etree
# 下面一步导入可能会出错
from lxml.html import soupparser
root = etree.fromstring(soupparser)
root.xpath(<xpath_sentense>)
```
<span id=multiple_thread>
```python
from threading import Thread
from queue import Queue
class crawler(Thread):
	def __init__(self):
        super().__init__()
        self.queue = queue
	def run(self):
    	while True:
            parameter = self.queue.get()
            # crawl 就是单线程的 爬虫，包括访问 url, 解析资源，保存资源。
            crawl(parameter)
            

queue = Queue()
for i in range(100):
	t = crawler()
    t.daemon = True
    t.start()
    
# 向 queue 中填上数据，比如
for url in urls:
	queue.put(url)

queue.join()
```
</span>
<span id="handle_exception">
```python
from urllib.error import URLError

MAX_TRY_TIMES = 3
max_try_times = MAX_TRY_TIMES
    while max_try_times >= 0:
        try:
            response = opener.open(my_request, timeout=200)
            content = response.read().decode('utf-8')
            response.close()
            break

        except HTTPError as e:
            if max_try_times != 0:
                    max_try_times -= 1
                    sleep(SLEEP_PERIOD * uniform(0, 1))
                    continue
            else:
                page_num_logger.error(e.reason + ':' + sku_id)
                return

        except URLError as e:
            if max_try_times != 0:
                max_try_times -= 1
                sleep(SLEEP_PERIOD * uniform(0, 1))
                continue
            else:
                page_num_logger.error(e.reason + ':' + sku_id)
                return

        except ConnectionResetError as e:
            if max_try_times != 0:
                max_try_times -= 1
                sleep(SLEEP_PERIOD * uniform(0, 1))
                continue
            else:
                page_num_logger.error(e.reason + ':' + sku_id)
                return
```
</span>
