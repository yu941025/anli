__author__ = 'Administrator'
from urllib import request
import pymysql
from bs4 import BeautifulSoup
conn=pymysql.connect(user='root',password='123456',database='yuzhixiang',port=3306)
curson=conn.cursor()
sql='''CREATE TABLE proxy(
      id INT(20) PRIMARY KEY AUTO_INCREMENT,
      ip VARCHAR (100) ,
      port INT (100),
      leixing VARCHAR (100))'''
try:
    curson.execute(sql)
    conn.commit()
except:
    print('数据库表已存在')
a=1
sql='insert into proxy(ip,port,leixing) VALUES (%s,%s,%s)'

url='http://www.xicidaili.com/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

req=request.Request(url,headers=headers)
response=request.urlopen(req)
html=response.read().decode('utf-8')
soup=BeautifulSoup(html,'lxml')
h=soup.find_all(class_='odd')
all_ip=[]
all_type=[]
all_port=[]
for i in h:
    ip=i.find_all('td')[1]
    all_ip.append(ip.text)
    type=i.find_all('td')[2]
    all_type.append(type.text)
    port=i.find_all('td')[5]
    all_port.append(port.text)
h=[]
for i in range(len(all_ip)):
    h.append(i)

a=zip(all_ip,all_port,all_type)
for i in a:
    try:
        curson.execute(sql,(str(i[0]),str(i[1]),str(i[2])))
        conn.commit()
    except:
        print('error')






