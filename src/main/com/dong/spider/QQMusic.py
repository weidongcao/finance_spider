"""
爬取QQ音乐
"""
import requests
from lxml import etree

# 1.请求列表页,并取得所有歌曲的Sessionid,歌曲url里有
def get_sessionid():
    url="https://y.qq.com/portal/player.html"
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        "Referer":"https://y.qq.com/n/yqq/song/0041EAWY2D9o9j.html"
    }
    r = requests.get(url, headers=headers)
    html=etree.HTML(r.text)
    print(r.text)

if __name__ == '__main__':
    get_sessionid()