"""
了解Requests库的基本使用方法
准备工作：
    请确保已经正确安装好了Requests库
"""
import requests

r = requests.get('http://httpbin.org/get')

print(type(r))
print(r.status_code)
print(type(r.text))
print(r.text)
print(r.cookies)

print("-------------------------- GET请求 -----------------------------------")
# GET请求
data={
    'name': 'dong',
    'age': 22
}

r = requests.get("http://httpbin.org/get", params=data)
print(r.text)

print("-------------------------- POST请求 -----------------------------------")
# POST请求
data = {
    'name': 'dong',
    'age': 28
}
r = requests.post("http://httpbin.org/post", data=data)
print(r.text)


print("-------------------------- Cookies -----------------------------------")
r = requests.get('https://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
    print(key + ' = ' + value)
    
