# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re
import os
import scrapper.util.chrome_driver as chrome


class NYTimes:

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.search_page_url = 'https://www.nytimes.com/search/?'
        self.landing_page = 'https://www.nytimes.com'

    def treat_link(self, href):
        print(href)
        driver = chrome.inicializar_driver(self.download_dir)
        driver.get(href)
        try:
            time_x_path = '/html/body/div[1]/div/div/div[2]/main/div/article/div[3]/header/div[5]/ul/li[1]/div/time'
            time_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, time_x_path)))
            timestamp_attr = time_el.get_attribute('datetime')
            print(timestamp_attr)
            artigo_x_path = '/html/body/div[1]/div/div/div[2]/main/div/article/section'
            artigo_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, artigo_x_path)))
            divs = artigo_el.find_elements(By.TAG_NAME, 'div')
            materia = ''
            for div in divs:
                try:
                    div_paragrafos = div.find_element(By.TAG_NAME, 'div')
                    paragrafos = div_paragrafos.find_elements(By.TAG_NAME, 'p')
                    for paragrafo in paragrafos:
                        materia = materia + paragrafo.get_attribute('innerHTML')
                except NoSuchElementException as ex:
                    pass
            print(materia)
            filename = re.sub(r':', '-', timestamp_attr)
            filename_path = os.path.join(self.download_dir, filename)
            print('***FILENAME: {}***'.format(filename))
            with open(filename_path, 'w') as f:
                f.write(href)
                f.write(materia)
                f.flush()
                f.close()
        except TimeoutException as ex:
            pass
        finally:
            driver.close()


    def scrap(self, qparams):

        driver = chrome.inicializar_driver(self.download_dir)

        search_url = self.search_page_url

        for k, v in qparams.items():
            search_url = search_url+k+'='+v+'&'

        print(search_url)

        driver.get(search_url)

        print('Carregando todos os resultados na página de busca...')

        try:
            el = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
        except NoSuchElementException as ex:
            print('Terminou de carregar página de busca')
            el = None
            pass

        click_counter = 0
        while el is not None:
            print(el.get_attribute('innerHTML'))
            el.click()
            click_counter += 1
            print('click_counter =  {0}'.format(click_counter))
            time.sleep(1)
            try:
                el = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            except NoSuchElementException as ex:
                print('Terminou de carregar página de busca')
                el = None
                pass

        print('Iniciando raspagem dos resultados')

        links = driver.find_elements(By.CLASS_NAME, 'css-1l4w6pd')

        try:
            for link in links:
                html_text = link.find_element(By.CLASS_NAME, 'css-2fgx4k').get_attribute('innerHTML')
                a_tag = link.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                self.treat_link(href)
        finally:
            driver.close()