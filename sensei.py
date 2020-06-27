import os

path = 'C:\\Users\\Maicon\\Videos\\NARUTO\\Naruto Shippuuden'

os.chdir(path)

for episode in os.listdir():
    if len(episode) == 50:
       os.rename(episode, episode[15:])

    if len(episode) == 35:
       os.rename(episode, episode[:23] + '.mkv')

    print(episode)
    print(len(episode))



