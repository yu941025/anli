__author__ = 'Administrator'
import requests
from bs4 import BeautifulSoup
import pymysql
def get_url():
    urls=[]
    for i in range(0,250,25):
        url='https://book.douban.com/top250?start='
        urls.append(url+str(i))
    return urls
def get_xijie(url):
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,'lxml')

    names=soup.select('div.pl2 > a')
    name=[]
    for i in names:
        name.append(i['title'])
    author=[]
    authors=soup.select('div.pl2 > span')
    for j in authors:
        author.append(j.text)
    jianjie=[]
    jianjies=soup.select('p.pl')
    #print(jianjies)
    for h in jianjies:
        jianjie.append(h.text)
    pingfen=[]
    pingfens=soup.select('div.star.clearfix > span.rating_nums')
    for k in pingfens:
        pingfen.append(k.text)
    jieshao=[]
    jieshaos=soup.select('p.quote > span')
    for l in jieshaos:
        jieshao.append(l.text)

    return zip(name,jianjie,pingfen,jieshao)
def db_connect(aaa):
    conn=pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='yuzhixiang')
    cursor=conn.cursor()
    sql='''CREATE TABLE `DOUBAN`(
    `id`  int(11)  NOT NULL AUTO_INCREMENT,
    `name` VARCHAR (250) NOT NULL ,
    `author` VARCHAR (250) NOT NULL ,
    `jianjie` VARCHAR (250) not NULL ,
    `pingfen` VARCHAR (250)NOT NULL,
    `jieshao` VARCHAR (250) NOT NULL ,
    PRIMARY KEY (`id`),
    INDEX `name`  (`name`) USING BTREE
    )
    ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    '''
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print('表已经存在')
    sql='INSERT INTO DOUBAN(name,jianjie,pingfen,jieshao) VALUES (%s,%s,%s,%s)'

    print(len(aaa))
    cursor.execute(sql,aaa)
    conn.commit()








if __name__=='__main__':
    a=0

    for i in get_url():
        h=get_xijie(i)
        for i in h :
            db_connect(i)




