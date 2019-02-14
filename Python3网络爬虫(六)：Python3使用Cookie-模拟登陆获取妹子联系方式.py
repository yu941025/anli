__author__ = 'Administrator'
from urllib import request
from http import cookiejar

# -*- coding: UTF-8 -*-
from urllib import request
from http import cookiejar

if __name__ == '__main__':

    #设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filename)
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler)
    #此处的open方法打开网页
    response = opener.open('http://www.baidu.com')
    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)


# -*- coding: UTF-8 -*-
from urllib import request
from http import cookiejar

if __name__ == '__main__':
    #设置保存cookie的文件的文件名,相对路径,也就是同级目录下
    filename = 'cookie.txt'
    #创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar()
    #从文件中读取cookie内容到变量
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler)
    #此用opener的open方法打开网页
    response = opener.open('http://www.baidu.com')
    #打印信息
    print(response.read().decode('utf-8'))

