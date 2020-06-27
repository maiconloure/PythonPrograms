nome = 'potato.srt'
titulo = 'supernaruto.mp4'

listada = ['hidan.mp4', 'potato.srt', 'naruto.mp4', 'batataa.mp3']


for file in listada:
    if file.endswith('.srt'):
        print('É legenda!')
    elif file.endswith('.mp4'):
        print('É vídeo!')
    else:
        print('Arquivo indefinido')