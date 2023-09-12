from arquivos.plotagem_rota_entrega import plotagem_rota_entrega
from arquivos.tratamento_df_completo import tratamento_df_completo
from arquivos.tratamento_df_escolas import tratamento_df_escolas
from arquivos.tratamento_df_material_didatico import tratamento_df_material_didatico
from arquivos.tratamento_df_subprefeituras import tratamento_df_subprefeituras
from arquivos.criacao_rota_entrega import criacao_rota_entrega
from arquivos.criacao_df_final_com_rota_otimizada import criacao_df_final_com_rota_otimizada

def main():
  # passo 1
  tratamento_df_escolas()

  # passo 2
  tratamento_df_material_didatico()

  # passo 3
  tratamento_df_subprefeituras()

  # passo 4
  tratamento_df_completo()

  # passo 5
  criacao_rota_entrega()

  # passo 6
  criacao_df_final_com_rota_otimizada()

  # passo 7
  plotagem_rota_entrega()

  # passo 8
  print('\nEXECUÇÃO FINALIZADA! Arquivos salvos na pasta "otimizacao_de_rota".\n')