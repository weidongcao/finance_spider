"""
XPath全称为XML Path Language，即XML路径语言，它是一门在XML文档中查找信息的语言。
XPath最初设计是用来搜寻XML文档的，但是它同样适用于HTML文档的搜索。

XPath的选择功能十分强大，它提供了非常简洁明了的路径选择表达式，另外它还提供了超过100
个内建函数用于字符串、数值、时间的匹配以及节点、序列的处理。
"""
"""
首场教育LXML的etree模块，然后声明一段HTML文本，调用HTML类进行初始化，这样就成功构造了
一个XPath解析对象，在这里注意到HMTL文本中的最后一个li节点是没有闭合的，但是etree模块
可以对HTML文本进行自动修正
在这里调用tostring()方法即可输出修正后的HTML代码，但是结果是bytes类型，我们利用decode()
方法转成str类型。
"""
from lxml import etree

html = etree.parse('xpath_test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))

# 获取节点内部文本
result = html.xpath('//li[@class="item-0"]//text()')
print(result)

# 获取节点属性值
result = html.xpath('//li/a/@href')
print(result)

# 获取节点属性的多值
# contains()方法，第一参数传入属性名称，第二参数传入属性值，
# 这样只要此属性包含所有传入的属性值就可以完成完成匹配了。
result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)
