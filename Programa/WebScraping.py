import os
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
    def __init__(self, url, lista_regioes, caminho_downloads):
        chromedriver_autoinstaller.install()  # instala o chrome driver e o adiciona ao path
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(url)
        self.lista_regioes = lista_regioes
        self.caminho_downloads = caminho_downloads

    def download(self):
        """ Baixa todos os csv separados por região """
        elem = self.driver.find_element(By.ID, "conteudo_btnMensal")
        elem.click()
        for regiao in self.lista_regioes:
            baixados = [baixado for baixado in os.listdir(self.caminho_downloads) if regiao + ".csv" in baixado]
            if "Mensal-Região " + regiao + ".csv" not in baixados:  # apenas baixa aqueles que ainda não foram baixados
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "conteudo_ddlRegioes")))
                select = Select(self.driver.find_element(By.ID, "conteudo_ddlRegioes"))
                select.select_by_visible_text(regiao)
                self.driver.find_element(By.ID, "conteudo_btnExcel").click()
        time.sleep(5)
        self.driver.close()

    def organiza(self):
        """ Organiza todos os arquivos baixados em uma única tabela """
        matriz_organizada = []
        for arquivo in os.listdir(self.caminho_downloads):
            for regiao in self.lista_regioes:
                if regiao + ".csv" in arquivo:  # verifica se o arquivo dentro da pasta download é uma das regiões
                    with open(self.caminho_downloads + "/" + arquivo, "r", newline='\n') as arq:
                        leitor = csv.reader((x.replace('\0', '') for x in arq), delimiter=';', quotechar='|')
                        for linha in leitor:
                            if len(linha) != 0:
                                if linha[0] == '2021' or linha[0] == '2020':
                                    ano = int(linha[0])
                                    pode = True
                                elif linha[0] == '2022':
                                    pode = False
                                elif linha[0] == 'Ocorrencia' or len(linha) <= 1:
                                    continue
                                elif pode:
                                    meses = {1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
                                             7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"}
                                    natureza = linha[0]
                                    for i in range(1, 13):
                                        linha_organizada = []
                                        ocorencia_mes = linha[i]
                                        linha_organizada.append(natureza)
                                        linha_organizada.append(meses[i])
                                        linha_organizada.append(ano)
                                        linha_organizada.append(regiao)
                                        linha_organizada.append(ocorencia_mes)
                                        matriz_organizada.append(linha_organizada)

        colunas = ["Natureza", "Mes", "Ano", "Regiao", "Ocorrencias"]
        df = pd.DataFrame(matriz_organizada, columns=colunas)
        df.to_csv("dataframe.csv", index=False)
