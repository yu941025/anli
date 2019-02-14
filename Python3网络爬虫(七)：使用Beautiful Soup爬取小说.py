__author__ = 'Administrator'
'''from bs4 import BeautifulSoup
html = """
<html>
<head>
<title>Jack_Cui</title>
</head>
<body>
<p class="title" name="blog"><b>My Blog</b></p>
<li><!--注释--></li>
<a href="http://blog.csdn.net/c406495762/article/details/58716886" class="sister" id="link1">Python3网络爬虫(一)：利用urllib进行简单的网页抓取</a><br/>
<a href="http://blog.csdn.net/c406495762/article/details/59095864" class="sister" id="link2">Python3网络爬虫(二)：利用urllib.urlopen发送数据</a><br/>
<a href="http://blog.csdn.net/c406495762/article/details/59488464" class="sister" id="link3">Python3网络爬虫(三)：urllib.error异常</a><br/>
</body>
</html>
"""
soup=BeautifulSoup(html,'lxml')
print(soup.title)
print(soup.head)
print(type(soup.title))
print(soup.a.attrs)
print(soup.title.string)
print(soup.attrs)


print(soup.body.contents)
print(soup.body.children)
for i in soup.body.children:
    print(i)
import re
a=soup.find_all(re.compile("^h"))
print(a)'''
'''from urllib import request
from bs4 import BeautifulSoup
if __name__=='__main__':
    url='https://www.biqukan.com/1_1094/5403177.html'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req=request.Request(url,headers=headers)
    content=request.urlopen(req)
    html=content.read()
    soup=BeautifulSoup(html,'lxml')

    h=soup.find('div',attrs={'class':'content'}).find('h1')
    a=h.string
    q=soup.find('div',class_='showtxt')
    l=q.text.replace('\xa0',' ')
    print(a)
    print(l)
    o=a+'\n'+l
    print(o)
    with open('a.txt','w',encoding='utf-8') as f:
        f.write(o)
'''
from urllib import request
from bs4 import BeautifulSoup

if __name__ == "__main__":
    download_url = 'http://www.biqukan.com/1_1094/5403177.html'
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    download_req = request.Request(url = download_url, headers = head)
    download_response = request.urlopen(download_req)
    download_html = download_response.read().decode('gbk','ignore')
    soup_texts = BeautifulSoup(download_html, 'lxml')
    texts = soup_texts.find_all(id = 'content', class_ = 'showtxt')
    soup_text = BeautifulSoup(str(texts), 'lxml')
    #将\xa0无法解码的字符删除
    o=soup_text.div.text.replace('\xa0','')
    with open('a.txt','w') as f:
        f.write(o)



