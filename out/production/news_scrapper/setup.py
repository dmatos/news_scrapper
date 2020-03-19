# coding=utf-8

from setuptools import setup, find_packages

version_file = open('VERSION')
version = version_file.read().strip()

setup(name='news_scrapper', version=version, packages=find_packages())