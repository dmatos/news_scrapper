# coding=utf-8

from scrapper.news.nytimes import NYTimes
from scrapper.news.elpaisV0 import ElPais
from scrapper.news.bbcV2 import BBC
from scrapper.news.aljazeera import AlJazeera
from scrapper.news.folha import Folha
from scrapper.util.logger import logger


def nytimes(termos):
    datainicio = '20191125'
    datafim = '20191221'
    qparams = {'query': termos, 'startDate': datainicio, 'endDate': datafim, 'sort':  'newest'}
    nytimes = NYTimes('/home/dmatos/Downloads/nytimes')
    nytimes.scrap(qparams)


def elpais(termos):
    # TODO scrapper ElPais
    """
       datainicio = '02/12/2019'
       datafim = '14/12/2019'
       qparams = {'qt': termos, 'sd': datainicio, 'ed': datafim}
       elpais = ElPais('/home/dmatos/Downloads/elpais')
    """
    logger.error('nao implementado')


def aljazeera(termos):
    aljazeera = AlJazeera('/home/dmatos/Downloads/aljazeera')
    aljazeera.scrap(termos, '2019-11-25', '2019-12-21')


def bbc(termos):
    bbc = BBC('/home/dmatos/Downloads/bbc')
    bbc.scrap(termos, '2019-11-25', '2019-12-21', max_paginas=30)
    #bbc.treat_link('https://www.bbc.com/news/newsbeat-50629410', '2019-01-01')


def folha(termos):
    folha = Folha('/home/dmatos/Downloads/folha')
    folha.scrap(termos, '25%2F11%2F2019', '21%2F12%2F2019')


if __name__=='__main__':
    termos_en = 'climate+change+conference'
    termos_pt = 'conferência+do+clima+mudanças+climáticas'
    try:
        #folha(termos_pt)
        #nytimes(termos_en)
        aljazeera(termos_en)
        #bbc("climate+change+conference")
    except Exception as ex:
        logger.exception(ex)
        pass
