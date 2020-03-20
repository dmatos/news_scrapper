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
import time
import scrapper.util.chrome_driver as chrome


class Folha:

    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.search_page_url = 'https://search.folha.uol.com.br/search?'
        self.landing_page = 'https://www.folha.uol.com.br/'

    def treat_link(self, href):
        logger.info('=== Acessando {} ==='.format(href))
        driver = chrome.inicializar_driver(self.download_dir, headless=False, habilitar_javascript=False)
        try:
            driver.get(href)

            data_el = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'c-more-options__header')))

            data_el = data_el.find_element(By.CLASS_NAME, "c-more-options__published-date")

            try:
                logger.debug('=== innerHtml: {} ==='.format(data_el.get_attribute('innerHTML')))
            except Exception as ex:
                data_el = data_el.find_element(By.CLASS_NAME, "c-more-options__published-date")
                pass

            data = data_el.get_attribute('datetime')

            data = dt.strptime(data, '%Y-%m-%d %H:%M:%S')
            logger.info('=== DATA {} ==='.format(data))
            conteudo = None
            try:
                conteudo = driver.find_element(By.CLASS_NAME, 'c-news__content')
            except NoSuchElementException as nse:
                logger.exception(nse)
                try:
                    conteudo = conteudo.find_element(By.CLASS_NAME, 'c-news__body')
                except NoSuchElementException as nxe:
                    logger.exception(nxe)
                    raise
                pass

            paragrafos = conteudo.find_elements(By.TAG_NAME, 'p')

            logger.info('=== Numero de parágrafos: {} ==='.format(len(paragrafos)))

            materia = ''
            for p in paragrafos:
                materia = materia + p.get_attribute('innerHTML')
            filename = re.sub(r'/', '-', href) + re.sub(r':', '-', data.strftime('%Y-%m-%d %H:%M:%S'))
            filename_path = os.path.join(self.download_dir, filename)
            logger.info('***FILENAME: {}***'.format(filename))
            with open(filename_path, 'w') as f:
                f.write(href)
                f.write(materia)
                f.flush()
                f.close()
        except Exception as ex:
            logger.exception(ex)
        finally:
            driver.close()

    def scrap(self, termos, data_inicio, data_fim):

        driver = chrome.inicializar_driver(self.download_dir)

        search_url = self.search_page_url + 'q=' + termos + '&' \
                                                            'periodo=personalizado' \
                                                            '&sd='+data_inicio+'&ed='+data_fim+'&site=sitefolha'

        logger.info(search_url)

        driver.get(search_url)

        logger.info('Iniciando raspagem do resultado')

        try:
            next_page = True
            page_count = 1
            while next_page:
                logger.info('=== Inicializando raspagem na página {} ==== '.format(page_count))
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "c-search")))
                lista_links = driver.find_element(By.TAG_NAME, 'ol')
                links = lista_links.find_elements(By.TAG_NAME, 'li')

                for link in links:
                    a_tag = link.find_element(By.TAG_NAME, 'a')
                    href = a_tag.get_attribute('href')
                    logger.info('=== href: {}'.format(href))
                    self.treat_link(href)
                try:
                    arrows = driver.find_elements(By.CLASS_NAME, 'c-pagination__arrows')
                    if len(arrows) == 1:
                        arrow_index = 0
                    elif len(arrows) > 1:
                        arrow_index = 1
                    else:
                        break
                        next_page = False
                    arrow_count = 0
                    for arrow in arrows:
                        if arrow_count == arrow_index:
                            arrow.click()
                        arrow_count += 1
                except NoSuchElementException as ex:
                    next_page = False
                    logger.error(ex)
                    pass
                page_count += 1

        except Exception as ex:
            logger.exception(ex)


if __name__=='__main__':
    folha = Folha('/home/dmatos/Downloads/folha')
    folha.treat_link('https://www1.folha.uol.com.br/opiniao/2019/12/cop-25-a-agenda-do-clima-e-o-acordo-ambiental-sao-paulo.shtml')