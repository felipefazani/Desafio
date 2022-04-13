import csv
import time
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class WebScraping:
    def __init__(self, url="http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"):
        chromedriver_autoinstaller.install()  # instala o chrome driver e o adiciona ao path
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)

    def crawler(self):
        elem = self.driver.find_element(By.ID, "conteudo_btnMensal")
        elem.click()

        region_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[2]/div/select'
        all_regions = self.all_options(region_xpath)
        all_regions.pop(0) # retira o todos
        year_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select'
        all_years = self.all_options(year_xpath)
        all_years.pop(0) # retira o todos

        for year in all_years:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, year_xpath)))
            select_year = Select(self.driver.find_element(By.XPATH, year_xpath))
            select_year.select_by_visible_text(year)

            for region in all_regions:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, region_xpath)))
                select = Select(self.driver.find_element(By.XPATH, region_xpath))
                select.select_by_visible_text(region)
                # basta pegar a tabela agora
                table_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[2]/div/div[1]/div/table'
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
                table = self.driver.find_element(By.XPATH, table_xpath)
                table_html = table.get_attribute("outerHTML")
                df = pd.read_html(table_html)
                print(region, year)
                print(df)

    def all_options(self, xpath):
        """Recebe o xpath de um select e retorna uma lista com todos os nomes de cada opcao"""
        element = self.driver.find_element(By.XPATH, xpath)
        select_element = Select(element)
        all_element_names = []
        for option in select_element.options:
            all_element_names.append(option.get_attribute("text"))

        return all_element_names
