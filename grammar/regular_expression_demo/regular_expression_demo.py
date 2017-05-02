import re

url = r"http://host?sku_id=123"

# 演示 group
print(re.search(r"sku_id=([0-9]+)", url).group(1))


# 演示贪婪模式和非贪婪模式
matched = re.search(r"[0-9]+?", url)
print(matched.string[matched.start(): matched.end()])

# 演示环视
money = r"总共花了 $100.00， 价值 $200.99 "

matched = re.search(r"(?<=\$)[0-9]+", money)

print(matched.string[matched.start(): matched.end()])

# 换行符, 正则表达式中的 . 默认是不会匹配换行符的。如果要匹配需要做些设置。

content = r"""走弯路好过原地踏步
可是发现自己走弯路，会伤心
原地踏步，却不会很伤心"""

print(re.search(r"(.*)", content).group(1))
print("++++++++++++++++++++++++++++++++++++")
print(re.search(r"(.*)", content, re.S).group(1))
print("++++++++++++++++++++++++++++++++++++")
print(re.search(r"((.|\n)*)", content).group(1))
