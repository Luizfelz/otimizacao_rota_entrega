import pandas as pd
from unidecode import unidecode
import warnings
import re
from arquivos.funcoes import atribui_logradouro_e_numero_casa, is_numerico_brasil, converte_para_numero

def tratamento_df_escolas():
  warnings.filterwarnings("ignore")
  df_escolas = pd.read_csv('./arquivos/escolas.csv', delimiter=',')
  df_escolas.rename(columns = {'id':'ID_INSTITUICAO', 'Escolas_Postos':'ESCOLAS_POSTOS', 'ENDEREÇO ':'ENDERECO', 'lat':'LATITUDE', 'lon':'LONGITUDE'}, inplace=True)
  for linha in range(df_escolas.shape[0]):
    df_escolas['ESCOLAS_POSTOS'][linha] = df_escolas['ESCOLAS_POSTOS'][linha].upper()
    df_escolas['BAIRRO'][linha] = df_escolas['BAIRRO'][linha].upper()
    df_escolas['ENDERECO'][linha] = df_escolas['ENDERECO'][linha].upper()

  for linha in range(df_escolas.shape[0]):
    df_escolas['ESCOLAS_POSTOS'][linha] = unidecode(df_escolas['ESCOLAS_POSTOS'][linha])
    df_escolas['BAIRRO'][linha] = unidecode(df_escolas['BAIRRO'][linha])
    df_escolas['ENDERECO'][linha] = unidecode(df_escolas['ENDERECO'][linha])

  tipos_logradouro = []
  for linha in range(df_escolas.shape[0]):
    tipo_split = df_escolas.iloc[linha]['ENDERECO'].split()[0]
    tipos_logradouro.append(tipo_split)

  lista_tipos_unicos = []
  for x in tipos_logradouro:
    if x not in lista_tipos_unicos:
      lista_tipos_unicos.append(x)
  
  resultado = df_escolas[df_escolas['ENDERECO'].str.contains(r'\.')]
  palavras_com_ponto_no_final = []
  for index, row in resultado.iterrows():
    palavras_encontradas = re.findall(r'\w+\.', row['ENDERECO'])
    palavras_com_ponto_no_final.extend(palavras_encontradas)

  nomes_unicos_enderecos = []
  for x in palavras_com_ponto_no_final:
    if x not in nomes_unicos_enderecos:
      nomes_unicos_enderecos.append(x)

  # valores das listas 'lista_tipos_unicos' e 'nomes_unicos_enderecos' adicionados no dicionário abaixo para que o replace seja feito no dataframe
  tipos_unicos_dict = {'RUA':'RUA', 'R.':'RUA', 'PRACA':'PRACA', 'AVENIDA':'AVENIDA', 'AV.':'AVENIDA', 'AV':'AVENIDA', \
                     'BOULEVARD':'BOULEVARD', 'PCA.':'PRACA', 'ESTR.':'ESTRADA', 'ESTRADA':'ESTRADA', 'CAMINHO':'CAMINHO', \
                      'SEN.':'SENADOR', 'MAL.':'MARECHAL','ALM.':'ALAMEDA','ENG.':'ENGENHEIRO','SD.':'SOLDADO','CASTELO.':'CASTELO'}
  for linha in range(df_escolas.shape[0]):
    for chave in tipos_unicos_dict.keys():
      df_escolas['ENDERECO'][linha] = df_escolas['ENDERECO'][linha].replace(chave,tipos_unicos_dict.get(chave))

  for linha in range(df_escolas.shape[0]):
    df_escolas['LATITUDE'][linha] = df_escolas['LATITUDE'][linha].replace(',','.')
    df_escolas['LONGITUDE'][linha] = df_escolas['LONGITUDE'][linha].replace(',','.')
  df_escolas['LATITUDE'] = pd.to_numeric(df_escolas['LATITUDE'], errors='coerce')
  df_escolas['LONGITUDE'] = pd.to_numeric(df_escolas['LONGITUDE'], errors='coerce')
  df_escolas['LATITUDE'] = df_escolas['LATITUDE'].round(5)
  df_escolas['LONGITUDE'] = df_escolas['LONGITUDE'].round(5)

  df_escolas['ID_INSTITUICAO'] = df_escolas['ID_INSTITUICAO'].astype(str)
  for linha in range(df_escolas.shape[0]):
    df_escolas['ID_INSTITUICAO'][linha] = df_escolas['ID_INSTITUICAO'][linha].zfill(3)

  df_escolas['LOGRADOURO'] = ''
  df_escolas['NUMERO_IMOVEL'] = ''
  for linha in range(df_escolas.shape[0]):
    numero = ''
    endereco_split = df_escolas['ENDERECO'][linha].split()
    for i in range(len(endereco_split)):
      if 'S/N' in endereco_split[i]:
        numero = 'S/N'
        endereco_split.pop(i)
        break
    if numero == 'S/N':
      atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
    elif (endereco_split[-2] in ['KM','BLOCO','APARTAMENTO','APTO','AP','AP.','CONJ.','CONJ','CONJUNTO']):
      try:
        numero = converte_para_numero(endereco_split[-3])
        endereco_split.pop(-3)
      except:
        numero = 'S/N'
      atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
    elif is_numerico_brasil(endereco_split[-2]):
      numero = converte_para_numero(endereco_split[-2])
      endereco_split.pop(-2)
      atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
    elif len(endereco_split) > 4: 
      try:
        numero = converte_para_numero(endereco_split[-3])
        endereco_split.pop(-3)
        atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
      except:
        try:
          numero = converte_para_numero(endereco_split[-4])
          if is_numerico_brasil(endereco_split[-1]):
            numero = converte_para_numero(endereco_split[-1])
            endereco_split.pop(-1)
          else:
            endereco_split.pop(-4)
        except:
          try:
            numero = converte_para_numero(endereco_split[-1])
            endereco_split.pop(-1)
          except:
            numero = 'S/N'
        atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
    elif is_numerico_brasil(endereco_split[-1]):
      numero = converte_para_numero(endereco_split[-1])
      endereco_split.pop(-1)
      atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)
    else:
      numero = 'S/N'
      atribui_logradouro_e_numero_casa(linha, numero, endereco_split,df_escolas)

  tipos_instituicao = []
  for linha in range(df_escolas.shape[0]):
    tipo_split = df_escolas.iloc[linha]['ESCOLAS_POSTOS'].split()[0]
    tipos_instituicao.append(tipo_split)

  lista_tipos_unicos_instituicao = []
  for x in tipos_instituicao:
    if x not in lista_tipos_unicos_instituicao:
      lista_tipos_unicos_instituicao.append(x)

  # valores da 'lista_tipos_unicos_instituicao' adicionados no dicionário abaixo, para que o replace seja feito no dataframe
  tipos_instituicao_abreviaturas = {'EM':'ESCOLA MUNICIPAL','E.M':'ESCOLA MUNICIPAL','E.M.':'ESCOLA MUNICIPAL',\
                                    'EM.':'ESCOLA MUNICIPAL','CIEP':'CENTRO INTEGRADO DE EDUCACAO PUBLICA'}
  tipos_instituicao_completos = {'ESCOLA':'ESCOLA MUNICIPAL','COLEGIO':'COLEGIO MUNICIPAL', \
                                'CENTRO':'CENTRO INTEGRADO DE EDUCACAO PUBLICA'}
  df_escolas['TIPO_INSTITUICAO'] = ''
  df_escolas['NOME_INSTITUICAO'] = ''
  for linha in range(df_escolas.shape[0]):
    nome_split = df_escolas['ESCOLAS_POSTOS'][linha].split()
    for tipo in tipos_instituicao_abreviaturas.keys():
      if nome_split[0] == tipo:
        df_escolas['TIPO_INSTITUICAO'][linha] = tipos_instituicao_abreviaturas.get(tipo)
        nome_split.pop(0)
        df_escolas['NOME_INSTITUICAO'][linha] = ' '.join(nome_split)
        break
    for tipo in tipos_instituicao_completos.keys():
      if nome_split[0] == 'ESCOLA':
        df_escolas['TIPO_INSTITUICAO'][linha] = tipos_instituicao_completos.get('ESCOLA')
        del nome_split[0:2]
        df_escolas['NOME_INSTITUICAO'][linha] = ' '.join(nome_split)
        break
      elif nome_split[0] == 'COLEGIO':
        df_escolas['TIPO_INSTITUICAO'][linha] = tipos_instituicao_completos.get('COLEGIO')
        del nome_split[0:2]
        df_escolas['NOME_INSTITUICAO'][linha] = ' '.join(nome_split)
        break
      elif nome_split[0] == 'CENTRO':
        df_escolas['TIPO_INSTITUICAO'][linha] = tipos_instituicao_completos.get('CENTRO')
        del nome_split[0:5]
        df_escolas['NOME_INSTITUICAO'][linha] = ' '.join(nome_split)
        break

  for indice, linha in df_escolas.iterrows():
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('RECREIO','RECREIO DOS BANDEIRANTES', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('MARACANA/ VILA ISABEL','MARACANA', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('MARACANA/ TIJUCA','RECREIO DOS BANDEIRANTES', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('FREGUESIA JPA','FREGUESIA (JACAREPAGUA)', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('OSWALDO CRUZ','OSVALDO CRUZ', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('AUGUSTO VASCONCELOS','SENADOR VASCONCELOS', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('NOVA SEPETIBA','SEPETIBA', regex=True)
    df_escolas.at[indice, 'BAIRRO'] = df_escolas.at[indice, 'BAIRRO'].replace('RIO DAS PEDRAS','JACAREPAGUA', regex=True)

  df_escolas.drop_duplicates(subset='ID_INSTITUICAO', inplace=True)
  df_escolas.reset_index(inplace=True, drop=True)

  return df_escolas

df_escolas = tratamento_df_escolas()