__author__ = 'Administrator'
import time
import os
import json
import requests
from lxml import etree
import time
header_dict={"Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    }
def get_http(load_url,header=None):
    resp=''
    try:
        req=requests.get(url=load_url,headers=header)
        resp=req.content


        try:
            resp=resp.decode(encoding='utf-8')
        except:
            resp=resp.decode(encoding='gbk')








    except Exception as e:
        print(e)
    return str(resp)
if not os.path.exists('./sina_data'):
    os.mkdir('./sina_data')
raw_file=open('./sina_data/raw.txt','w',encoding='utf-8')

json_file=open("./sina_data/555.txt","w",encoding='utf-8')
obj={'time':'',"title":"","url":"","content":""}
saved_url={"http://www.sina.com.cn/"}#记录已经爬取过的页面

url_list=["http://www.sina.com.cn/"]#url队列
while len(url_list)>0:
        url=url_list.pop()
        html_text=get_http(url,header_dict)
        if html_text=='':
            continue
        time.sleep(1)

        tree=etree.HTML(html_text)


        if url.find("html")>=0 and url.find("list")<0:
            t_xpath=["//h1[@id='main_title']/text()",
                "//h1/text()",
                "//th[@class='f24']//font/text()",
                "/html/head/title/text()"
                    ]
            title=[]
            for tx in t_xpath:
                if len(title)==0:
                    title=tree.xpath(tx)
                else:
                    break


            c_xpath= ["//div[@id='artibody']//p/text()",
                "//td[@class='l17']//p/text()",
                "//div[@class='content']//p/text()",
                "//div[@class='article']//p/text()",
                "//div[@id='article']//p/text()",
                "//div[@class='article-body main-body']//p/text()",
                "//div[@class='textbox']//p/text()"
                ]
            content=[]
            for cx in c_xpath:
                if len(content)==0:
                    content=tree.xpath(cx)
                else:
                    break
            if len(title)*len(content)==0:
                raw_file.write(html_text.replace("\n", "").replace("\r", ""))
                raw_file.write("\n")
                print("没有标题或正文"+url)
            else:

                print(html_text)
                obj["url"]=url
                obj["title"]=title[0]
                obj["content"]=" ".join(content)
                obj['time']=time.asctime()
                print(obj)

                jstr=json.dumps(obj,ensure_ascii=False)
                json_file.write(jstr)
                json_file.write("\n")

        urls=tree.xpath("//a/@href")
        for u in urls:
            flag=False
            #以下是过滤url的
            end_filter=[".apk",".iso",".jpg",".jpeg",".bmp",".cdr",".php",".exe",".dmg",".apk"]
            for f in end_filter:
                if ''.endswith(f):
                    flag=True
                    break
            if flag:
                continue
            find_filter=["vip.","guba.","lottery.","kaoshi.","club.baby","jiancai.",".cn/ku/","astro.","match.","games.","zhongce","list",
                "photo.","yangfanbook","zx.jiaju","nc.shtml","english.","download","chexian","auto","video","comfinanceweb.shtml",
                "//sax.","login","/bc.","aipai.","vip.book","talk.t","slide.","club.baby","biz.finance","blog","comment5","www.leju",
                "http://m."]
            for f in find_filter:
                if u.find(f)>=0:
                    flag=True
                    break
            if flag:
                continue
            if u.startswith('http') and u.find('.sina.')>=0:
                if u in saved_url:
                    continue
                saved_url.add(url)
                url_list.append(u)





raw_file.close()
json_file.close()