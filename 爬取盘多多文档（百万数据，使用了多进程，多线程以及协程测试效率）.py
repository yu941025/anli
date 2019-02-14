__author__ = 'Administrator'
import requests
from multiprocessing import Pool
import multiprocessing
from bs4 import BeautifulSoup
import pymysql
import time
import logging
import gevent
import aiohttp
import asyncio
import threading
start_url='http://www.panduoduo.net/c/4/16'
logger=logging.getLogger('get_data')
logger.setLevel(logging.INFO)
hander=logging.FileHandler('123.log',encoding='utf-8')
formata=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hander.setFormatter(formata)
hander.setLevel(logging.INFO)
logger.addHandler(hander)
a=0
def get_data(urls):
    #url='http://www.panduoduo.net/c/4/16'
    requests.adapters.DEFAULT_RETRIES = 5#增加重试连接次数

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    resp=requests.get(urls,headers=headers,timeout=10)
    #print(resp.text)
    s = requests.session()
    s.keep_alive = False#关闭多余的连接
    soup=BeautifulSoup(resp.text,'lxml')
    allas=soup.find_all('a',class_="blue")
    #print(allas)

    for i in allas:
        url=i.get('href')
        url='http://www.panduoduo.net'+url
        title=i.get('title')

        baocunshuju(url,title)



def main(page):
    url='http://www.panduoduo.net/c/4/{}'.format(page)
    print('爬取第{}页'.format(page)+url)
    logger.info('爬取第{}页'.format(page)+url)

    get_data(url)

def baocunshuju(url,title):
    global a
    conn=pymysql.connect(host='localhost',user='root',password='123456',database='yuzhixiang',port=3306)
    cursor=conn.cursor()
    sql='''
  CREATE TABLE `wangpan`(
    `id`  INT (100) NOT NULL AUTO_INCREMENT,#主键自动增长
    `title` VARCHAR (255) DEFAULT  NULL ,
    `url` VARCHAR (100) DEFAULT  NULL ,
    PRIMARY KEY (`id`),
    INDEX `url` (`url`) USING BTREE
    )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;'''#AUTO_INCREMENT=1，id从1开始
    '''cursor.execute(sql)
    conn.commit()'''
    try:
        cursor.execute(sql)
        conn.commit()
        print('创建成功')
    except:
        pass
    sql1='insert into  wangpan(title,url) VALUES (%s,%s)'

    try:
        cursor.execute(sql1,(title,url))
        conn.commit()
        print(r'插入成功(%s,%s)'%(title,url))
        logger.info('插入成功(%s,%s)'%(title,url))
        a+=1
    except:
        print('插入失败')
        time.sleep(10)
        cursor.execute(sql1,(title,url))
        conn.commit()
        print(r'重新插入成功(%s,%s)'%(title,url))
        logger.info('重新插入成功(%s,%s)'%(title,url))
        a+=1



    print(a)

'''for i in range(1,88301):
    main(i)'''


if __name__=='__main__':


    '''start_time=time.time()
    pool=Pool(processes=1)
    pool.map_async(main,range(1,86151))
    pool.close()
    pool.join()
    end_time=time.time( )
    print(end_time-start_time)'''
    '''pool = Pool(multiprocessing.cpu_count())
    for url in range(1,86151):
        pool.apply_async(main,(url,))
    # pool.map(detailPage, urls)
    pool.close()
    pool.join()'''


    '''global cursor
    global conn
    sem=threading.Semaphore(4)
    threads=[]
    for i in range(1,88301):
        while sem:
            thread=threading.Thread(target=main,args=(i,))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()
    cursor.close()
    conn.close()'''
    for i in range(1,10000):
        g1=gevent.spawn(main,i)
    for j in range(10000,20000):
        g2=gevent.spawn(main,j)
    for k in range(20000,40000):
        g3=gevent.spawn(main,k)
    gevent.joinall([g1,g2,g3])


    '''task=[asyncio.ensure_future(main())for _ in range(1,80000)]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))'''


