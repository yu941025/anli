__author__ = 'Administrator'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
chome_options=webdriver.ChromeOptions()
chome_options.add_argument('--headless')
driver=webdriver.Chrome(chrome_options=chome_options)
'''chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)'''
driver.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html')
html=driver.page_source
soup=BeautifulSoup(html,'lxml')
