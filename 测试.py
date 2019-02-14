__author__ = 'Administrator'
from urllib import request
import pymysql
from bs4 import BeautifulSoup
conn=pymysql.connect(user='root',password='123456',database='yuzhixiang',port=3306)
curson=conn.cursor()
sql='select * from proxy'
curson.execute(sql)
conn.commit()
a=curson.fetchall()
print(type(a))
