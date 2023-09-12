import pandas as pd
from arquivos.criacao_rota_entrega import pares_waypoints
from arquivos.tratamento_df_completo import exportar_df_completo

def criacao_df_final_com_rota_otimizada():
  pares_ordenados_final = []
  for i in range(len(pares_waypoints)):
    pares_ordenados = sorted(pares_waypoints[i], key=lambda x: x[0])
    pares_ordenados_final.append(pares_ordenados)

  pares_ordenados_sequencia = []
  for i in range(len(pares_ordenados_final)):
    pares_ordenados_sequencia.extend(pares_ordenados_final[i])

  pares_ordenados_sequencia_final = []
  for i in range(len(pares_ordenados_sequencia)):
    pares_ordenados_sequencia_final.append(pares_ordenados_sequencia[i][1])

  lista_indices = []
  for indice, valor in enumerate(pares_ordenados_sequencia_final):
    lista_indices.append(indice)

  df_completo = exportar_df_completo()
  df_temporario = pd.DataFrame({'ID_INSTITUICAO': pares_ordenados_sequencia_final, 'NOVO_INDICE': lista_indices})
  df_completo = df_completo.merge(df_temporario, how='left', on='ID_INSTITUICAO')
  df_completo.sort_values(by='NOVO_INDICE', ignore_index=True, inplace=True)
  df_completo.drop('NOVO_INDICE', axis=1, inplace=True)

  colunas_df_final_rota_ordenada = ['ID_INSTITUICAO','NOME_INSTITUICAO','TIPO_INSTITUICAO','LOGRADOURO','NUMERO_IMOVEL','BAIRRO','SUBPREFEITURA','LATITUDE','LONGITUDE','QNTD_MATERIAL_DIDATICO']
  df_final_rota_ordenada = df_completo[colunas_df_final_rota_ordenada]

  colunas_df_final_custo_por_subprefeitura = ['SUBPREFEITURA','QNTD_MATERIAL_DIDATICO']
  df_final_custo_por_subprefeitura = df_completo[colunas_df_final_custo_por_subprefeitura]
  df_final_custo_por_subprefeitura = df_final_custo_por_subprefeitura.groupby(by=['SUBPREFEITURA'],as_index=False).sum()

  df_final_custo_por_subprefeitura.to_csv('./otimizacao_de_rota/custo_por_subprefeitura.csv', index=False)
  df_final_rota_ordenada.to_csv('./otimizacao_de_rota/rota_entrega_otimizada.csv', index=False)