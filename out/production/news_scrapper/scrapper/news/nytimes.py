# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import scrapper.util.chrome_driver as chrome

os.mkdirs'/'

_search_page_url = 'https://www.nytimes.com/search/?'

def scrap(qparams):

    driver = chrome.inicializar_driver()

    search_url = _search_page_url

    for k, v in qparams.items():
        search_url = search_url+k+'='+v+'&'

    driver.get('_search_url{0}'.format())

    html = driver.get_attribute(By.TAG, 'body')

    print(html)

if __name__=='__main__':
    termos = 'COP+climate+change+conference'
    datainicio = '20191202'
    datafim = '20191214'
    qparams = {'termos': termos,'startDate': datainicio, 'endDate': datafim, 'sort':  'newest'}