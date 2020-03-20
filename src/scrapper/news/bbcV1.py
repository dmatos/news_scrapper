# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapper.util.logger import logger
from datetime import datetime as dt
import re
import os
import time
import scrapper.util.chrome_driver as chrome


class BBC2019:

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.search_page_url = 'https://www.bbc.co.uk/search?'
        self.landing_page = 'https://www.bbc.co.uk'

    def treat_link(self, href, data):
        logger.info(href)
        driver = chrome.inicializar_driver(self.download_dir)
        driver.get(href)
        try:
            artigo_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, 'orb-modules')))
            site_container = artigo_el.find_element(By.ID, 'site-container')
            logger.info(artigo_el)
            timestamp_attr = data
            logger.info(timestamp_attr)
            site_container = artigo_el.find_element(By.ID, 'page')
            # logger.debug(site_container.get_attribute('innerHTML'))
            container = site_container.find_element(By.CLASS_NAME, 'container').find_element(By.CLASS_NAME, 'column-clearfix')
            column = container.find_element(By.CLASS_NAME, 'column--primary')
            divs = column.find_elements(By.TAG_NAME, 'p')
            materia = ''
            for div in divs:
                try:
                    paragrafo = div.get_attribute('innerHTML')
                    #logger.info(paragrafo)
                    paragrafo = re.sub(r'<span>', '', paragrafo)
                    paragrafo = re.sub(r'</span>', '', paragrafo)
                    materia = materia + paragrafo
                except NoSuchElementException as ex:
                    raise
            logger.debug(materia)
            href = re.sub(r'/', '-', href)
            href = re.sub(r'\.', '-', href)
            filename = re.sub(r':', '-', href) + re.sub(r':', '-', timestamp_attr) + href
            filename_path = os.path.join(self.download_dir, filename)
            logger.info('***FILENAME: {}***'.format(filename))
            with open(filename_path, 'w') as f:
                f.write(href)
                f.write(materia)
                f.flush()
                f.close()
        except TimeoutException as ex:
            logger.debug('TimeoutException')
            logger.debug(ex)
            pass
        except NoSuchElementException as ex:
            logger.debug(ex)
            pass
        finally:
            driver.close()


    def scrap(self, termos, data_inicio, data_fim, max_paginas):

        driver = chrome.inicializar_driver(self.download_dir)

        search_url = self.search_page_url + 'q=' + termos + '&filter=news'

        logger.info(search_url)

        driver.get(search_url)

        logger.info('Iniciando raspagem dos resultados')

        try:
            next_page = True
            while next_page:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'search-results')))


            results = driver.find_elements(By.CLASS_NAME, 'search-results')

            for result in results:

                links = result.find_elements(By.TAG_NAME, 'li')

                logger.info('links {0}'.format(links))
                for link in links:
                    #logger.debug(link.get_attribute('innerHTML'))
                    data = link.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                    data = data[0:data.find('T')]
                    logger.info(data)
                    href = link.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                    #logger.info(href)
                    data_data = dt.strptime(data, '%Y-%m-%d')
                    if dt.strptime(data_inicio, '%Y-%m-%d') <= data_data <= dt.strptime(data_fim, '%Y-%m-%d'):
                        self.treat_link(href, data)
                    else:
                        logger.debug('data nao passou {0} '.format(data))
        except Exception as ex:
            raise
        finally:
            driver.close()

if __name__=='__main__':
    bbc = BBC()