import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebScraping:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def download(self, lista_regioes):
        elem = self.driver.find_element(By.ID, "conteudo_btnMensal")
        elem.click()
        for regiao in lista_regioes:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "conteudo_ddlRegioes")))
            select = Select(self.driver.find_element(By.ID, "conteudo_ddlRegioes"))
            select.select_by_visible_text(regiao)
            self.driver.find_element(By.ID, "conteudo_btnExcel").click()
