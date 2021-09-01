# -*- coding: utf-8 -*-
"""limpa_dados.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V14PLkuAh_mXojNewtuXrigZo2rtCtbK
"""


import pandas as pd
import numpy as np

def limpando_dados(dados):
    dados_limpos = preenche_tabela(dados)
    a_remover = dados_limpos.query("WINDOW=='0-2' and ICU==1")['PATIENT_VISIT_IDENTIFIER'].values
    dados_limpos = dados_limpos.query("PATIENT_VISIT_IDENTIFIER not in @a_remover")
    dados_limpos = dados_limpos.dropna()
    dados_limpos = dados_limpos.groupby("PATIENT_VISIT_IDENTIFIER").apply(prepare_window)
    dados_limpos.AGE_PERCENTIL = dados_limpos.AGE_PERCENTIL.astype("category").cat.codes
    dados_limpos.reset_index(drop=True, inplace=True)
#    dados_limpos = remove_corr_var(dados_limpos)
#    dados_limpos = dados_limpos.drop(['WINDOW', 'PATIENT_VISIT_IDENTIFIER'], axis = 1)


    return dados_limpos

def preenche_tabela(dados):
    features_continuas_colunas = dados.iloc[:, 13:-2].columns
    features_continuas = dados.groupby("PATIENT_VISIT_IDENTIFIER", as_index=False)[features_continuas_colunas].fillna(method='bfill').fillna(method='ffill')
    features_categoricas = dados.iloc[:, :13]
    saida = dados.iloc[:, -2:]
    dados_finais = pd.concat([features_categoricas, features_continuas, saida], ignore_index=True,axis=1)
    dados_finais.columns = dados.columns
    return dados_finais
        
def prepare_window(rows):
    if(np.any(rows["ICU"])):
        rows.loc[rows["WINDOW"]=="0-2", "ICU"] = 1
    return rows.loc[rows["WINDOW"] == "0-2"]

def remove_corr_var(dados, valor_corte = 0.95):

    matrix_corr = dados.iloc[:,4:-2].corr().abs()
    matrix_upper = matrix_corr.where(np.triu(np.ones(matrix_corr.shape), k=1).astype(np.bool))
    excluir = [coluna for coluna in matrix_upper.columns if any(matrix_upper[coluna] > valor_corte)]

    return dados.drop(excluir, axis=1)
