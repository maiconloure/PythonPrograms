import os
import shutil

path = "/home/maicon/dev/python/PythonPrograms/ofl"

os.chdir(path)

for folder in os.listdir(path):
  for file in os.listdir(path + '/' + folder):
    if file.endswith('.ttf'):
      shutil.move(f'{path}/{folder}/{file}', '/home/maicon/dev/python/PythonPrograms/allfonts')