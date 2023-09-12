import pandas as pd
from unidecode import unidecode
import warnings

def tratamento_df_subprefeituras():
  warnings.filterwarnings("ignore")
  df_subprefeituras = pd.read_csv('./arquivos/subprefeituras.csv', delimiter=',')
  df_subprefeituras.rename(columns = {'nome':'BAIRRO', 'subprefeitura':'SUBPREFEITURA'}, inplace=True)
  for linha in range(df_subprefeituras.shape[0]):
    df_subprefeituras['BAIRRO'][linha] = df_subprefeituras['BAIRRO'][linha].upper()
    df_subprefeituras['SUBPREFEITURA'][linha] = df_subprefeituras['SUBPREFEITURA'][linha].upper()
    df_subprefeituras['BAIRRO'][linha] = unidecode(df_subprefeituras['BAIRRO'][linha])
    df_subprefeituras['SUBPREFEITURA'][linha] = unidecode(df_subprefeituras['SUBPREFEITURA'][linha])

  df_subprefeituras.drop_duplicates(inplace=True)
  df_subprefeituras.reset_index(inplace=True, drop=True)

  return df_subprefeituras

df_subprefeituras = tratamento_df_subprefeituras()