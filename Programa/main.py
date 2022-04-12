import WebScraping as Wb
import os


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def main():
    url = "http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"
    regioes = ["Capital", "Grande São Paulo (exclui a Capital)", "São José dos Campos", "Campinas",
               "Ribeirão Preto",
               "Bauru", "São José do Rio Preto", "Santos", "Sorocaba", "Presidente Prudente", "Piracicaba",
               "Araçatuba"]
    caminho = get_download_path()
    obj = Wb.WebScraping(url, regioes, caminho)
    obj.download()
    obj.organiza()


if __name__ == '__main__':
    main()
