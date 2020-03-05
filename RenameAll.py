"""
    Programa para renomear em massa arquivos a partir de uma *lista,
    regras devem ser seguidas para tudo funcionar corretamente;

    >> Deve haver elementos para cada arquivos que irao ser renomeados
    >> Deve se verificar o formato do arquivo que irá renomear e incluir no final
    >> O nome dos arquivos deve haver um padrão de tamanho, ex: todos os nomes possuem 10 caracteres.
"""

import os
from friends import EpisodesCopy

path = 'arquivos que vao ser renomeados'    # EX: /Users/name/AppData/Local/Programs/Python/Python38
os.chdir('/')                               # Volta ao diretório raiz C:\
os.chdir(path)                              # Muda o diretório para o especificado em 'path'
print(os.getcwd())                          # Mostra o diretório em que o programa está rodando


"""Programa para renomear legendas"""

for file, ep in zip(os.listdir('.'), EpisodesCopy):
    os.rename(file, ep+".srt")


"""
Programa para renomear o episodio e legenda com o mesmo nome, o padrão aqui é
Nome_Episodios: 50 caracteres
Nome_Legendas: 18 caracteres
"""

for file, ep in zip(os.listdir('.'), EpisodesCopy):
    if file[46:51] == '.mkv':
        os.rename(file, ep+".mkv")
    elif file[14:18] == '.srt':
        os.rename(file, ep+".srt")

for file in os.listdir('.'):
    print(file)
