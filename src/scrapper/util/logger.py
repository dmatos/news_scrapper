# coding=utf-8

import logging.config
import logging
import yaml
import coloredlogs
import os


_logger = logging.getLogger('')
_app_name = os.getenv('news_scrapper', None)
_path = 'resources/logger.yml'
_extra = {'app_name': _app_name}

if os.path.exists(_path):
    with open(_path, 'rt') as f:
        try:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            coloredlogs.install(fmt=config['formatters']['standard']['format'],
                                level=logging.DEBUG)
        except Exception as e:
            print(e)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=logging.DEBUG)
            coloredlogs.install(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)
    coloredlogs.install(level=logging.DEBUG)
    print('Failed to load configuration file. Using default configs')

logger = logging.LoggerAdapter(_logger, _extra)
