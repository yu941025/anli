__author__ = 'Administrator'
from urllib import request
import chardet

if __name__=='__main__':
    url='https://fanyi.baidu.com/'
    rsp=request.urlopen(url)
    html=rsp.read()
    chaar=chardet.detect(html)  #获取编码
    print(chaar)
    html=html.decode('utf-8')