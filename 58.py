__author__ = 'Administrator'
from parse_url import url,diqu
import requests
from lxml import etree
from time import sleep
import xlrd
from xlutils.copy import copy
import re
import base64
from fontTools.ttLib import TTFont
import xlwt
def get_message():
    url_a='https://hz.58.com/hangzhou/chuzu/b2/'
    global headers

    resp=requests.get(url_a,headers=headers,timeout=5)
    if resp.status_code!=200:
        sleep(5)
        get_again()
    resp.encoding('utf-8')
    html=etree.HTML(resp.content).decode('utf-8')
    resp.encoding('utf-8')
    print(resp.text)
    class_list=html.xpath('//ul[@class="listUl"]/li')
    global list_message
    list_message={}



    for i in class_list:
        try:
            h=i.xpath('./div[@class="des"]/h2/a')[0].text.strip()
            print(h)
            #print(len(class_list))
            list_message['message']=h
            url=i.xpath('./div[@class="des"]/h2/a')[0].get('href')
            print(url)
            urls='https:'+url
            sleep(2)
            return urls

        except:
            pass

def get_detail():
    list_message={}
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url='https:'+'//hz.58.com/zufang/36749493804963x.shtml'
    resp=requests.get(url,headers=headers)
    resp.encoding='bs64'
    print(resp.text)
    html=etree.HTML(resp.text.encode('gbk'))

    jiage=html.xpath('//span[@class="c_ff552e"]/b/text()')[0]
    pattern=r"base64,(.*)format"
    pattern1=re.compile(pattern)
    jiami=pattern1.findall(resp.text)[0]
    print(jiami)
    #jiage=base64.b64encode(str(jiage))

    text=str(jiage)
    rb=xlrd.open_workbook('zhufan.xls')

    sheet1=rb.sheet_by_index(0)
    wb=copy(rb)
    sheet=wb.get_sheet(0)
    nrows=sheet1.nrows
    #print(nrows)
    with open('t2.woff','wb') as f :
        bin_date=base64.decodebytes(jiami.encode())
        f.write(bin_date)
    '''font=TTFont('t2.woff')
    font.save('text.xml')
    print(font.keys())
    from PIL import Image,ImageFont,ImageDraw
    text=jiage
    im=Image.new('RGB',(300,50),(255,255,255))
    dr=ImageDraw.Draw(im)
    font=ImageFont.truetype('t2.woff',18)
    dr.text((10,5),text,font=font,fill="#000000")
    im.show()
    im.save('t.png')'''
    def font_parse(text):#破解base64加密
        """
    解析乱码的数字
    :param rental:
    :param house_type:
    :param toward_floor:
    :return:
    """
    item_text=''
    for alpha in text:
        hex_alpha = alpha.encode('unicode_escape').decode()[2:]
        if len(hex_alpha) == 4:
            one_font = int(hex_alpha, 16)
            font = TTFont('t2.woff')
            font_dict = font['cmap'].tables[2].ttFont.tables['cmap'].tables[1].cmap
            b = font['cmap'].tables[2].ttFont.getReverseGlyphMap()
            if one_font in font_dict.keys():
                gly_font = font_dict[one_font]
                item_text+=str(b[gly_font] - 1)
            else:
                item_text = alpha
    print(item_text)



    sheet.write(nrows,0,jiage)
    wb.save('zhufan.xls')




def get_again():
    get_message()
get_detail()
'''if __name__=='__main__':
    a=input('请输入地区：')
    diqu={
    '西湖':'xihuqu',
    '拱墅':'gongshu',
    '江干':'jianggan',
    '下城':'xiacheng',
    '上城':'hzshangcheng',
    '余杭':'yuhang',
    '萧山':'xiaoshan',
    '滨江':'binjiang',
    '建德':'jiandeshi',
    '富阳':'fuyangshi',
    '临安':'linanshi',
    '桐庐':'tonglu',
    '淳安':'chunan',
    '杭州周边':'hangzhou'
}

    the_url=[str(url).format(diqu[a]) for url in url]
    #print(the_url)'''

