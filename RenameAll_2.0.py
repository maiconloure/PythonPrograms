"""
    Programa para renomear em massa arquivos a partir de uma *lista,
    regras devem ser seguidas para tudo funcionar corretamente;

    >> Deve haver elementos para cada arquivo que ira ser renomeados
    >> Deve se verificar o formato do arquivo que irá renomear e incluir no final EX: mp4, mkv, srt
"""

import os
from friends import EpisodesCopy

path = 'C:/Users/Maicon/Downloads/[HorribleSubs] Naruto Shippuuden (80-426) [1080p] (Batch)'    # EX: /Users/name/AppData/Local/Programs/Python/Python38

os.chdir(path)                              # Muda o diretório para o especificado em 'path'

print(os.listdir(path))
print(os.getcwd())                          # Mostra o diretório em que o programa está rodando


"""Programa para renomear apenas legendas"""

# for file, ep in zip(os.listdir('.'), EpisodesCopy):
#     os.rename(file, ep+".srt")

"""
Programa para renomear o episodio e legenda com o mesmo nome
"""

# for file, ep in zip(os.listdir('.'), EpisodesCopy):
#     # if file.endswitch('.mkv'):
#     #     os.rename(file, ep+".mkv")
#     if file.endswitch('.srt'):
#         os.rename(file, ep+".srt")

# for file in os.listdir('.'):
#     print(file)
