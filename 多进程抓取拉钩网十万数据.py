__author__ = 'Administrator'
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import logging
import pymongo
import time
import threading
import random
from multiprocessing import Pool
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("spam.log",encoding='utf-8')
fh.setLevel(logging.INFO)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)


# 建立一个filehandler来把日志记录在文件里，级别为INFO以上

def get_page_resp(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host':'www.lagou.com',
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests':'1',
    'cookies':'user_trace_token=20181102145432-bafe4e8f-916e-4cf3-979c-d91872be2428; _ga=GA1.2.286303898.1541141667; LGUID=20181102145433-27312db1-de6c-11e8-85c5-5254005c3644;JSESSIONID=ABAAABAAAGFABEF07F977514E63D6A2A7221543AAC1B9F5; index_location_city=%E5%85%A8%E5%9B%BD;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546053004,1546066413; X_HTTP_TOKEN=4e97bc182983c1709ed52bf67dcbf77c;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167f903300346a-00c2502816494e-454c092b-2073600-167f903300465e%22%2C%22%24device_id%22%3A%22167f903300346a-00c2502816494e-454c092b-2073600-167f903300465e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ab_test_random_num=0; LG_LOGIN_USER_ID=5639996880bad0233edbd7d6210dda730d7e7f83d2d70e8e; _putrc=12F032920E3D35DD; login=true; unick=%E4%BD%99%E6%B2%BB%E7%BF%94; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1;hasDeliver=0; _gid=GA1.2.957437360.1546393226; gate_login_token=e08e447db4da5f7ee03a7c7ddc2bd73b78ec7c9d69ebfedb; TG-TRACK-CODE=index_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546393422;LGRID=20190102094343-d679d06e-0e2f-11e9-b05a-5254005c3644'}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:

            return resp.text


    except RequestException as e:
        print(e)


def parse_index():
    url='https://www.lagou.com/'

    soup=BeautifulSoup(get_page_resp(url),'lxml')


    #logger.error('错误')

    all_positions=soup.select('div.menu_sub.dn > dl > dd > a')
    joburls=[i['href'] for i in all_positions]
    jobnames = [i.get_text() for i in all_positions]
    for joburl,jobname in zip(joburls,jobnames):
            data={'url':joburl,
                'name':jobname}
            yield data

def get_message(url,pages,mongo_table):
    ur=url+str(pages)+'/'
    logger.info('爬取网址{}'.format(ur))
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',

    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)'
    ]
    a=random.choice(user_agent_list)
    headers={
        'User-Agent':a,
        'Host':'www.lagou.com',
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests':'1',
        'cookies':'user_trace_token=20181102145432-bafe4e8f-916e-4cf3-979c-d91872be2428; _ga=GA1.2.286303898.1541141667; LGUID=20181102145433-27312db1-de6c-11e8-85c5-5254005c3644; JSESSIONID=ABAAABAAAGFABEF07F977514E63D6A2A7221543AAC1B9F5; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=4e97bc182983c1709ed52bf67dcbf77c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167f903300346a-00c2502816494e-454c092b-2073600-167f903300465e%22%2C%22%24device_id%22%3A%22167f903300346a-00c2502816494e-454c092b-2073600-167f903300465e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ab_test_random_num=0; LG_LOGIN_USER_ID=5639996880bad0233edbd7d6210dda730d7e7f83d2d70e8e; _putrc=12F032920E3D35DD; login=true; unick=%E4%BD%99%E6%B2%BB%E7%BF%94; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _gid=GA1.2.957437360.1546393226; TG-TRACK-CODE=index_navigation; PRE_UTM=; gate_login_token=f98b54b610a4951ebff2ccd97438698b747b0023f14988c1; LGSID=20190103095727-ebed5dbc-0efa-11e9-b0e4-5254005c3644; PRE_HOST=link.zhihu.com; PRE_SITE=https%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttps%253A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%253Fpx%253Dnew%2526hy%253D%2525E7%2525A7%2525BB%2525E5%25258A%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2526city%253D%2525E5%25258C%252597%2525E4%2525BA%2525AC%2523filterBox; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%3Fpx%3Dnew%26hy%3D%25E7%25A7%25BB%25E5%258A%25A8%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%26city%3D%25E5%258C%2597%25E4%25BA%25AC; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546053004,1546066413,1546480645,1546480675; SEARCH_ID=03c33f208c714080ae5c831a8892e3bf; LGRID=20190103102059-35c9a905-0efe-11e9-b0e4-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546482058'

    }

    resp=requests.get(ur,headers=headers,timeout=3)
    time.sleep(2)




    soup=BeautifulSoup(resp.text,'lxml')


    # 职位信息
    positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
    # 工作地址
    adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
    # 发布时间
    publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')
    # 薪资信息
    moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')
    # 工作需求
    needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')
    # 发布公司
    companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
    '''tags = []
    # 由于我发现有的招聘信息没有标签信息，if判断防止没有标签报错
    if soup.find('div', class_='li_b_l'):
        # 招聘信息标签'''
    tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')
    client=pymongo.MongoClient('localhost',27017)
    lagou = client['lagou']
    url_list = lagou[mongo_table]
    print(len(moneys),'\n',len(positions))
    # 公司福利
    fulis = soup.select('ul > li > div.list_item_bot > div.li_b_r')
    for position,add,publish,money,need,company,tag,fuli in \
        zip(positions,adds,publishs,moneys,needs,companys,tags,fulis):
        data = {
        'position' : position.get_text(),
        'add' : add.get_text(),
        'publish' : publish.get_text(),
        'money' : money.get_text(),
        'need' : need.get_text().split('\n')[2],
        'company' : company.get_text(),
        'tag' : tag.get_text().replace('\n','-'),
        'fuli' : fuli.get_text()
        }
        url_list.insert_one(data)
        logger.info('保存数据库成功:%s'%data)
    client.close()







from multiprocessing import Pool
def main(pages):
    datas = parse_index()
    time.sleep(2)




    for i in datas:

        url = i['url']



        #logger.info('123456')
        mongo_table = i['name']
        # 因为有的职位是以'.'开头的，比如.Net，数据库表名不能以.开头
        if mongo_table[0] == '.':
            mongo_table = mongo_table[1:]
        # 我们把之前抓取职位所有招聘信息的程序整理为parse_link()函数
        # 这个函数接收职位url，页码，和数据库表名为参数
        get_message(url, pages, mongo_table)








if __name__ == '__main__':
    '''pool = Pool(processes=1)
    pages = ([p for p in range(1, 31)])
    pool.map(main,pages)

    pool.close()
    pool.join()
    print('爬取完成')'''
    for pages in range(1,31):
        main(pages)

    '''threads=[]
    for i in range(1,31):
        thread=threading.Thread(target=main,args=(i,))
        thread.start()

        threads.append(thread)
    for i in threads:
        i.join()
    print('爬取结束')'''


