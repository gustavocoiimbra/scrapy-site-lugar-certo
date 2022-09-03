import re
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
from plotly.offline import plot, iplot
import cufflinks as cf
import plotly.io as os
import pandas as pd

# Importando o dataset
df = pd.read_csv('dados_site_lugar_certo_2.csv', sep=',')

# Código para mostrar todas as colunas e linhas
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Código para retirar os dados duplicados da base de dados
df.drop_duplicates(keep='first', inplace=True)

# Retiramos caracteres especiais do dataset
df["Preço"] = df["Preço"].apply(
    lambda x: x.replace("R$", "").replace(",00", "").replace(' ', '').replace('.', '').replace(',', ''))
df["Preço"] = df["Preço"].astype(int)

# Código para retirar valores nulos e seus caracteres especiais
df.dropna(subset=["Aréa"], inplace=True)
df["Aréa"] = df["Aréa"].apply(lambda x: x.replace('m²', ''))
df["Aréa"] = df["Aréa"].astype(int)

# Criando uma coluna nova com a cidade e bairro do imóvel
df = df.assign(Cidade=[re.split(',', x)[-1].strip() for x in df["Endereço"]])
df = df.assign(Bairro=[re.split(',', x)[-2].strip() for x in df["Endereço"]])
df = df.assign(PreçoPorMetro=lambda x: x.Preço / x.Aréa)

# Retiramos todos os outliers do dataset
df.drop(df.loc[df.Preço >= 100000000].index, inplace=True)
df.drop(df.loc[df.Preço <= 10000].index, inplace=True)
df.drop(df.loc[df.Aréa < 10].index, inplace=True)
df.drop(df.loc[df.PreçoPorMetro <= 10].index, inplace=True)

cidades_met = df[(df.Cidade == "Senador Canedo - GO") | (df.Cidade == "Trindade - GO") |
                 (df.Cidade == "Goianira - GO") | (df.Cidade == "Aparecida de Goiânia - GO")]

# Cidade X Média Valor dos Imóveis

df_mediaPreco = cidades_met.groupby('Cidade').Preço.mean()
print(df_mediaPreco)
