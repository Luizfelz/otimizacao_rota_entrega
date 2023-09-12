from arquivos.tratamento_df_escolas import df_escolas
from arquivos.tratamento_df_material_didatico import df_material_didatico
from arquivos.tratamento_df_subprefeituras import df_subprefeituras
import warnings

def tratamento_df_completo():
  warnings.filterwarnings("ignore")
  df_completo = df_escolas.merge(df_subprefeituras, how='left', on='BAIRRO')
  for linha in range(df_completo.shape[0]):
    if 'FREGUESIA' in df_completo['BAIRRO'][linha]:
      if 'ILHA' in df_completo['BAIRRO'][linha]:
        df_completo['SUBPREFEITURA'][linha] = 'ILHAS'
      else:
        df_completo['SUBPREFEITURA'][linha] = 'JACAREPAGUA'

  for linha in range(df_completo.shape[0]):
    if str(df_completo['SUBPREFEITURA'][linha]).upper() == 'NAN':
      df_completo['SUBPREFEITURA'][linha] = 'SEM SUBPREFEITURA'

  df_completo = df_completo.merge(df_material_didatico, how='left', on='ID_INSTITUICAO')

  df_completo.dropna(subset='QNTD_MATERIAL_DIDATICO', inplace=True)
  df_completo.reset_index(inplace=True, drop=True)

  return df_completo

def exportar_df_completo():
  return df_completo

df_completo = tratamento_df_completo()