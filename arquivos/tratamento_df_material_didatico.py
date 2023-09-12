import pandas as pd
import numpy as np
import warnings

def tratamento_df_material_didatico():
  warnings.filterwarnings("ignore")
  df_material_didatico = pd.read_csv('./arquivos/material_didatico.csv', delimiter=',')
  df_material_didatico.rename(columns = {'id':'ID_INSTITUICAO', 'Quantidade':'QNTD_MATERIAL_DIDATICO'}, inplace=True)
  df_material_didatico['ID_INSTITUICAO'] = df_material_didatico['ID_INSTITUICAO'].astype(str)
  for linha in range(df_material_didatico.shape[0]):
    df_material_didatico['ID_INSTITUICAO'][linha] = df_material_didatico['ID_INSTITUICAO'][linha].zfill(3)

  for linha in range(df_material_didatico.shape[0]):
    try:
      df_material_didatico['QNTD_MATERIAL_DIDATICO'][linha] = int(df_material_didatico['QNTD_MATERIAL_DIDATICO'][linha])
    except:
      df_material_didatico['QNTD_MATERIAL_DIDATICO'][linha] = np.nan
  df_material_didatico['QNTD_MATERIAL_DIDATICO'] = df_material_didatico['QNTD_MATERIAL_DIDATICO'].astype(dtype='float')

  df_material_didatico.drop_duplicates(subset='ID_INSTITUICAO', inplace=True)
  df_material_didatico.dropna(subset='QNTD_MATERIAL_DIDATICO', inplace=True)
  df_material_didatico.reset_index(inplace=True, drop=True)

  return df_material_didatico

df_material_didatico = tratamento_df_material_didatico()