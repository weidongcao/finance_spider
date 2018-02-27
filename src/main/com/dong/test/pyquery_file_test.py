"""
PyQuery是一个非常强大的网页解析库，如果你对Web有所涉猎，
如果你比较喜欢用CSS选择器，如果你对JQuery所有了解，
那么这里有一个更适合你的解析库
"""
from pyquery import PyQuery as pq

html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
doc = pq(html)

# 基本CSS选择器
print("-------------------- 基本CSS选择器 -------------------------")
print(doc('#container .list li'))
print(type(doc('#container .list li')))

print("-------------------- 查找子节点:.list -------------------------")
items = doc('.list')
print(type(items))
print(items)


print("-------------------- 查找子节点:.active -------------------------")
lis = items.children('.active')
print(lis)

print("-------------------- 查找子节点:#li -------------------------")
lis = items.find('li')
print(type(list))
print(lis)

# 初始化URL
print("-------------------- URL请求 -------------------------")
doc = pq(url='http://cuiqingcai.com')
print(doc('title'))

