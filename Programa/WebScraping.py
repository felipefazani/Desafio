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
        """Instala o chromedriver e inicia o webdriver do chrome"""
        chromedriver_autoinstaller.install()  # instala o chrome driver e o adiciona ao path
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)

        """Atribuindo xpath utilizados"""
        self.month_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[5]/div[1]/div/a'
        self.region_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[2]/div/select'
        self.year_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[2]/div[1]/div/select'
        self.city_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[1]/div[3]/div[1]/div/select'
        self.table_xpath = '/html/body/div[3]/div/div[1]/form/div[3]/div[2]/div/div[1]/div/table'

    def crawler(self):
        """entrada saida"""

        """clica no botao de ocorrencias por mês"""
        elem = self.driver.find_element(By.XPATH, self.month_xpath)
        elem.click()

        """recebe todos os nomes de cada regiao dentro do dropdown"""
        all_regions = self.all_options(self.region_xpath)
        all_regions.pop(0)  # retira o todos

        """recebe todos os anos disponiveis dentro do dropdown"""
        all_years = self.all_options(self.year_xpath)
        all_years.pop(0)  # retira o todos

        """iteracao de todos os municipios separados por regiao de cada ano"""
        df = pd.DataFrame()
        for year in all_years:
            self.select_option_dropdown(self.year_xpath, year)

            for region in all_regions:
                self.select_option_dropdown(self.region_xpath, region)

                """recebe todos os nomes de cada municipio dentro do dropdown de cada regiao"""
                all_cities = self.all_options(self.city_xpath)
                all_cities.pop(0)  # retira o todos

                for city in all_cities:
                    self.select_option_dropdown(self.city_xpath, city)

                    df_city = self.table_html_to_df(self.table_xpath)
                    df_city['Ano'] = year
                    df_city['Cidade'] = city
                    df_city['Regiao'] = region
                    df = pd.concat([df, df_city], ignore_index=True)

        df.to_csv("all_data.csv")

    def all_options(self, xpath):
        """Recebe o xpath de um dropdown e retorna uma lista com todos os nomes de cada opcao"""
        element = self.driver.find_element(By.XPATH, xpath)
        select_element = Select(element)
        all_element_names = []
        for option in select_element.options:
            all_element_names.append(option.get_attribute("text"))

        return all_element_names

    def table_html_to_df(self, table_xpath):
        """Recebe o xpath de uma tabela em html e a transforma em dataframe"""
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        table = self.driver.find_element(By.XPATH, table_xpath)
        table_html = table.get_attribute("outerHTML")

        return pd.read_html(table_html)[0]

    def select_option_dropdown(self, dropdown_xpath, option_name):
        """Recebe xpath de um dropdown e uma opcao dentro desse e a seleciona"""
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
        select = Select(self.driver.find_element(By.XPATH, dropdown_xpath))
        select.select_by_visible_text(option_name)

