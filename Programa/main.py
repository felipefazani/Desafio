import WebScraping as Wb

if __name__ == '__main__':
    obj = Wb.WebScraping("http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx")
    regioes = ["Capital", "Grande São Paulo (exclui a Capital)", "São José dos Campos", "Campinas", "Ribeirão Preto",
               "Bauru", "São José do Rio Preto", "Santos", "Sorocaba", "Presidente Prudente", "Piracicaba", "Araçatuba"]

    obj.download(regioes)


