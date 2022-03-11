import os
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebScraping:
    def __init__(self, url, lista_regioes, caminho_downloads):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.lista_regioes = lista_regioes
        self.caminho_downloads = caminho_downloads

    def download(self):
        ''' Baixa todos os csv separados por região '''
        elem = self.driver.find_element(By.ID, "conteudo_btnMensal")
        elem.click()
        for regiao in self.lista_regioes:
            baixados = [baixado for baixado in os.listdir(self.caminho_downloads) if regiao+".csv" in baixado]
            if "Mensal-Região "+regiao+".csv" not in baixados:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "conteudo_ddlRegioes")))
                select = Select(self.driver.find_element(By.ID, "conteudo_ddlRegioes"))
                select.select_by_visible_text(regiao)
                self.driver.find_element(By.ID, "conteudo_btnExcel").click()


    def organiza(self):
        for arquivo in os.listdir(self.caminho_downloads):
            for regiao in self.lista_regioes:
                if regiao+".csv" in arquivo:
                    print("Arquivo: ", arquivo, "   Regiao: ", regiao)
                    with open(self.caminho_downloads + "/" + arquivo, "r", newline='') as arq:
                        leitor = csv.reader((x.replace('\0', '') for x in arq), delimiter=' ', quotechar='|')
                        for linha in leitor:
                            print(linha)

