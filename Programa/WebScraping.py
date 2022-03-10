from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class WebScraping:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def altera_regioes(self, lista_regioes):
        



