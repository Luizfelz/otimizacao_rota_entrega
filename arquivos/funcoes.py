import re

def atribui_logradouro_e_numero_casa(linha, numero, endereco_split, df_escolas):
  logradouro = ' '.join(endereco_split)
  logradouro = re.sub(',','', logradouro)
  df_escolas['LOGRADOURO'][linha] = logradouro
  df_escolas['NUMERO_IMOVEL'][linha] = numero

def is_numerico_brasil(valor):
  try:
    valor = valor.replace('.', '')
    valor = int(valor)
    return True
  except:
    return False

def converte_para_numero(valor):
  if any(caracter in valor for caracter in ['-','/','~',':']):
    return valor
  else:
    valor = valor.replace('.', '')
    valor_convertido = int(valor)
    return valor_convertido