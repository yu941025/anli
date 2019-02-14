__author__ = 'Administrator'
from urllib import request
from urllib import parse
import json
import random,time
import hashlib
url='https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
salt=random.randint(0,10)+int(time.time()*1000)
def getsign(key,salt):
    sign='fanyideskweb'+key+str(salt)+'ebSeFb%=XZ%T[KZ)c(sy!'
    md5=hashlib.md5()
    md5.update(sign.encode('utf-8'))
    sign=md5.hexdigest()
    return sign
key=input('请输入翻译的值：')

Form_Data={}
Form_Data['i']=key
Form_Data['from']='AUTO'
Form_Data['to']='AUTO'
Form_Data['smartresult']='dict'
Form_Data['client']='fanyideskweb'
Form_Data['salt']=str(salt)
Form_Data['sign']=getsign(key,salt)
Form_Data['ts']='1543832091026'
Form_Data['bv']='ab57a166e6a56368c9f95952de6192b5'
Form_Data['doctype']='json'
Form_Data['version']='2.1'
Form_Data['keyfrom']='fanyi.web'
Form_Data['action']='FY_BY_REALTIME'
Form_Data['typoResult']='false'

data=parse.urlencode(Form_Data).encode('utf-8')
headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": len(data),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "OUTFOX_SEARCH_USER_ID=685021846@10.168.8.76; OUTFOX_SEARCH_USER_ID_NCOO=366356259.5731474; _ntes_nnid=1f61e8bddac5e72660c6d06445559ffb,1535033370622; JSESSIONID=aaaVeQTI9KXfqfVBNsXvw; ___rl__test__cookies=1535204044230",
        "Host": "fanyi.youdao.com",
        "Origin": "http://fanyi.youdao.com",
        "Referer": "http://fanyi.youdao.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
response=request.Request(url,data=data,headers=headers)
rsp=request.urlopen(response)
html=rsp.read().decode()
jsona=json.loads(html)
print(jsona)
a=jsona['translateResult'][0][0]['tgt']
print(a)
'''
# -*- coding: UTF-8 -*-
from urllib import request
from urllib import parse
import json

if __name__ == "__main__":
    #对应上图的Request URL
    Request_URL = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.baidu.com/link'
    #创建Form_Data字典，存储上图的Form Data
    Form_Data = {}
    Form_Data['type'] = 'AUTO'
    Form_Data['i'] = 'Jack'
    Form_Data['doctype'] = 'json'
    Form_Data['xmlVersion'] = '1.8'
    Form_Data['keyfrom'] = 'fanyi.web'
    Form_Data['ue'] = 'ue:UTF-8'
    Form_Data['action'] = 'FY_BY_CLICKBUTTON'
    #使用urlencode方法转换标准格式
    data = parse.urlencode(Form_Data).encode('utf-8')
    #传递Request对象和转换完格式的数据
    response = request.urlopen(Request_URL,data)
    #读取信息并解码
    html = response.read().decode('utf-8')
    #使用JSON
    translate_results = json.loads(html)
    #找到翻译结果
    translate_results = translate_results['translateResult'][0][0]['tgt']
    #打印翻译信息
    print("翻译的结果是：%s" % translate_results)
'''