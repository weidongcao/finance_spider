from bs4 import BeautifulSoup
"""
BeautiSoup借助网页的结构和属性等自反性来解析网页
有了它我们不用再去写一些复杂的正则，只需要简单的
几条语句就可以完成网页中某个元素的提取。
"""
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())
# 获取HTML的title标签
print(soup.title)
# 获取HTML的title标签的对象类型
print(type(soup.title))
# 获取HTML的title标签的文本内容
print(soup.title.string)
# 获取HTML的title标签的名称
print(soup.title.name)
# 获取HTML的head标签
print(soup.head)
# 获取HTML的p标签
print(soup.p)
# 获取HTML的p标签的属性
print(soup.p.attrs)
# 获取HTML的p标签的属性
print(soup.p.attrs['name'])
print(soup.p['name'])
print(soup.p['class'])
print(soup.p.string)
