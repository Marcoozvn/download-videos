import os
from pathlib import Path
import re
from shutil import move

root_dir = 'C:\\Users\\Marcos\\Desktop\\Video'
paths = sorted(Path(root_dir).iterdir(), key=os.path.basename)

filenames = []
with open('output-titles.txt', 'r', encoding='utf-8') as f:
  for line in f:
    filenames.append(line.replace('\n', ''))
directories = []
index = 0
for file in paths:
  try:
    new_path = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', filenames[index])
    dir_path, file_path = filenames[index].split('**')
    if dir_path not in directories:
      os.mkdir(f'{root_dir}\\{dir_path}')
      directories.append(dir_path)
    os.rename(str(file), f'{root_dir}\\{dir_path}\\{file_path}.webm')
    index += 1
  except Exception as ex:
    print(ex)
    continue