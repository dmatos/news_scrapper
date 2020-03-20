# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from scrapper.util.logger import logger
from datetime import datetime as dt
import re
import os
import scrapper.util.chrome_driver as chrome


class AlJazeera:

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.search_page_url = 'https://www.aljazeera.com/Search/?'
        self.landing_page = 'https://www.aljazeera.com'

    def treat_link(self, href, data):
        logger.info(href)
        driver = chrome.inicializar_driver(self.download_dir)
        driver.get(href)
        try:
            time_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'timeagofunction')))
            logger.info(time_el)
            timestamp_attr = data
            logger.info(timestamp_attr)
            artigo_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'article-p-wrapper')))
            divs = artigo_el.find_elements(By.TAG_NAME, 'p')
            materia = ''
            for div in divs:
                try:
                    paragrafo = div.get_attribute('innerHTML')
                    # logger.info(paragrafo)
                    paragrafo = re.sub(r'<span>', '', paragrafo)
                    paragrafo = re.sub(r'</span>', '', paragrafo)
                    materia = materia + paragrafo
                except NoSuchElementException as ex:
                    raise
            #logger.debug(materia)
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
            pass
        finally:
            driver.close()

    def scrap(self, termos, data_inicio, data_fim):

        driver = chrome.inicializar_driver(self.download_dir)

        search_url = self.search_page_url + 'q=' + termos.replace('+', ' ')

        logger.info(search_url)

        driver.get(search_url)

        logger.info('Iniciando raspagem dos resultados')

        try:
            next_page = True
            page_count = 0
            while next_page:

                driver.switch_to_active_element()

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'topics-sec-block')))

                links = driver.find_elements(By.CLASS_NAME, 'topics-sec-item')
                for link in links:
                    # logger.debug(link.get_attribute('innerHTML'))
                    data = link.find_element(By.CLASS_NAME, 'humanize-datetime').get_attribute('data-modifieddate')
                    data = data[0:data.find('T')]
                    href = link.find_elements(By.TAG_NAME, 'a')[1].get_attribute('href')
                    data_data = dt.strptime(data, '%Y-%m-%d')
                    if dt.strptime(data_inicio, '%Y-%m-%d') <= data_data <= dt.strptime(data_fim, '%Y-%m-%d'):
                        self.treat_link(href, data)
                page_count += 1
                logger.info('Terminou a pagina {}. Indo para a próxima...'.format(page_count))
                try:
                    next_link = driver.find_element(By.CLASS_NAME, 'search-result-pagination')
                    next_link = next_link.find_element(By.CLASS_NAME, 'next-page')\
                        .find_element(By.TAG_NAME, 'a').get_attribute('onclick')
                    logger.debug(next_link)
                    driver.execute_script(next_link)
                except NoSuchElementException as ex:
                    next_page = False
                    logger.error(ex)
                    pass
                except ElementClickInterceptedException as ex:
                    next_page = False
                    logger.error(ex)
                    pass
        finally:
            driver.close()
