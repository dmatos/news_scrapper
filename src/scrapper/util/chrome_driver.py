# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os


def inicializar_driver(download_dir, headless=False, habilitar_javascript=True):
    try:
        os.mkdir(download_dir)
    except FileExistsError:
        pass
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }

    if not habilitar_javascript:
        prefs["profile.managed_default_content_settings.javascript"] = 2

    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1024, 768)
    return driver
