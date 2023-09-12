import os
caminho_da_pasta = os.path.join(os.getcwd(), 'otimizacao_de_rota')
if not os.path.exists(caminho_da_pasta):
    os.mkdir(caminho_da_pasta)

from main import main

main()