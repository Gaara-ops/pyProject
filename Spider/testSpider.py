# -*- coding:utf-8 -*-

import sys
import re
import os
from bs4 import BeautifulSoup
import requests

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

'''
#传入文件句柄
#soup = BeautifulSoup(open("index.html"))#首先文档被转换成Unicode
#传入字符串
soup = BeautifulSoup(html_doc, 'html.parser')

#以漂亮的方式显示BeautifulSoup对象
print(soup.prettify())
#找到所有a标签
all_atag = soup.find_all('a')
for atag in all_atag:
    print (atag.name, atag.string) #获取标签的名称 内容
    print (atag.get('class'),atag['href']) #获取标签的属性

#通过制定的属性获取标签内容
print (soup.find(id="link3"))
#从文档中获取所有文字内容
print (soup.get_text())
'''

url = "http://tinyurl.com/ydbcvazg?raw=true"
kv = {'user-agent':'Mozilla/5.0'}
try:
    res = requests.get(url,headers = {'user-agent':'Mozilla/5.0'})
    with open('./test.png','wb') as pngsave:
        pngsave.write(res.content)
except:
    print('some thing error!')


print("over\n")
