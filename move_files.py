import os
import shutil

path =  "C:/Users/Maicon/Desktop/fonts-master/apache"

for folders in os.listdir(path):
    for file in os.listdir(f'C:/Users/Maicon/Desktop/fonts-master/apache/{folders}'):
        if file.endswith('.ttf'):
            # if file already exists
            shutil.move(f"C:/Users/Maicon/Desktop/fonts-master/apache/{folders}/{file}", f'C:/Users/Maicon/Desktop/GoogleFonts/{file}')
            # or ->
            # shutil.move(os.path.join(src, filename), os.path.join(dst, filename))