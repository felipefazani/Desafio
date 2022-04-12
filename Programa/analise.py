import pandas as pd
import matplotlib.pyplot as plt


def maiores(dicionario, n):
    """ Recebe um dicionario e retorna um lista com n maiores """

    maior = []
    for chave in sorted(dicionario, key=dicionario.get, reverse=True):
        maior.append((chave, dicionario[chave])) if len(maior) < n else None
    return maior


def graficos(regioes):
    """ Plota os gráficos das 3 regiões com mais homicídios
        e das 3 regiões que mais aumentaram de 2020 para 2021"""

    df = pd.read_csv("dataframe.csv")
    homicidios = df.loc[df["Natureza"] == "HOMICÍDIO DOLOSO (2)", ["Regiao", "Ano", "Ocorrencias"]]
    soma_20, soma_21, soma_total, diferenca = {}, {}, {}, {}
    for regiao in regioes:
        x = homicidios.loc[(homicidios.Regiao == regiao) & (homicidios.Ano == 2020), ["Ano", "Ocorrencias"]]
        soma_20[regiao] = x.Ocorrencias.sum()
        x = homicidios.loc[(homicidios.Regiao == regiao) & (homicidios.Ano == 2021), ["Ano", "Ocorrencias"]]
        soma_21[regiao] = x.Ocorrencias.sum()

        soma_total[regiao] = soma_20[regiao] + soma_21[regiao]
        diferenca[regiao] = soma_21[regiao] - soma_20[regiao]

    maiores_3 = maiores(soma_total, 3)
    plt.bar([x[0] for x in maiores_3], [x[1] for x in maiores_3], width=0.2)
    plt.title("As 3 regiões com maiores homicídios dolosos")
    plt.grid(axis='y')
    plt.show()

    maiores_absoluto = maiores(diferenca, 3)
    plt.bar([x[0] for x in maiores_absoluto], [x[1] for x in maiores_absoluto], width=0.2)
    plt.title("As 3 regiões que mais aumentaram de 2020 para 2021")
    plt.grid(axis='y')
    plt.xticks(rotation=15)
    plt.show()