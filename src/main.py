# coding=utf-8

from scrapper.news.nytimes import NYTimes
from scrapper.news.elpais import ElPais
from scrapper.news.bbc import BBC
from scrapper.news.aljazeera import AlJazeera
from scrapper.util.logger import logger


def nytimes(termos):
    datainicio = '20191202'
    datafim = '20191214'
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
    aljazeera.scrap(termos, '2019-12-02', '2019-12-14')

def bbc(termos):
    bbc = BBC('/home/dmatos/Downloads/bbc')
    bbc.scrap(termos, '2019-12-02', '2019-12-14', max_paginas=30)
    #bbc.treat_link('https://www.bbc.com/news/newsbeat-50629410', '2019-01-01')
if __name__=='__main__':
    #termos = 'COP+climate+change+conference'
    termos = 'climate+change+conference'
    bbc(termos)

