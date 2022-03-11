import WebScraping as Wb

if __name__ == '__main__':
    url = "http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"
    regioes = ["Capital", "Grande São Paulo (exclui a Capital)", "São José dos Campos", "Campinas", "Ribeirão Preto",
               "Bauru", "São José do Rio Preto", "Santos", "Sorocaba", "Presidente Prudente", "Piracicaba", "Araçatuba"]
    caminho = "C:/Users/Felipe/Downloads"

    obj = Wb.WebScraping(url, regioes, caminho)
    obj.download()
    obj.organiza()


