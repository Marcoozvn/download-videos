import codecs
import os
import subprocess
import time

# decode json chunks from a text file
def json_decoder(file):
    file = open(file, 'r')
    file = file.read().replace(chr(92) * 2, chr(92))
    file = codecs.decode(file, 'unicode_escape')
    lst = file.split('\n')
    tofile = []
    for i in lst:
        if not i:
            continue
        j = i.index(':') + 2
        k = i.index('"', 50)
        tofile.append(i[j:k])
    try:
        os.remove('output.txt')
    except OSError:
        pass
    with open('output.txt', 'w') as f:
        for item in tofile:
            print(item)
            f.write(f'{item}\n')

# Download batch of links from a .txt file
def get_files(data, titles):
    file = open(data, 'r', encoding='utf-8')
    lst = file.read().split('\n')
    names = open(titles, 'r', encoding='utf-8').read().split('\n')
    index = 0
 
    for i in range(index, len(names)):
      try:
        dir_path, file_path = names[i].split('**')

        subprocess.Popen(['youtube-dl','-v','--output', f'C:\\Users\\Marcos\\Documents\\Alura-Data-Miner\\output\\{dir_path}\\{file_path}.webm', f'{lst[i]}'])
      except:
        pass

