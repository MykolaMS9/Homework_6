import sys
from pathlib import Path
import shutil
import os
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(namef):
    word = []
    for val in namef:
        if re.findall('[а-яА-ЯіІїЇґ]', val):
            word.append(TRANS[ord(val)])
        elif re.findall('[a-zA-Z0-9]', val):
            word.append(val)
        else:
            word.append('_')
    return ''.join(word)

#     cd C:\Users\MS\OneDrive\Documents\Python\GOIT\Python_core\6_FileWork\Homework_6
#     python hw_6.py C:\Users\MS\Desktop

# Створення нових каталогів
FOLDERS = (sys.argv[1] + '\\images',
           sys.argv[1] + '\\video',
           sys.argv[1] + '\\documents',
           sys.argv[1] + '\\audio',
           sys.argv[1] + '\\archives')
EXTENSIONS = [['.jpeg', '.png', '.jpg', '.svg'],
              ['.avi', '.mp4', '.mov', '.mkv'],
              ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.ppt'],
              ['.mp3', '.ogg', '.wav', '.amr', '.flac'],
              ['.zip', '.gz', '.tar']]

def createFolders(folders):
    for val in folders:
        if not Path(val).exists():
            os.mkdir(val)
createFolders(FOLDERS)

# Пошук та перенесення файлів
newname = 1
unknownFiles = []
deletedDir = []
exFolders = [[], [], [], [], []]
exUnknown = []

def replaceFiles(p):
    global newname
    for index in range(5):
        flag = False
        for val in p.iterdir():
            if val.suffix in EXTENSIONS[index]:
                if not flag:  # для виводу шляху
                    flag = True
                    print(f'From folder {str(p)} removed to {FOLDERS[index]} next files:')
                if os.path.exists(os.path.join(FOLDERS[index], val.name)):
                    newname += 1
                    name = f'{str(val.name).replace(val.suffix, "")}_{newname}.{val.suffix}'
                else:
                    name = str(val.name).replace(val.suffix, "")
                namefile = Path(os.path.join(FOLDERS[index], f'{normalize(name)}{val.suffix}'))
                shutil.move(val, namefile)
                exFolders[index].append(val.suffix)
                if val.name == namefile.name:
                    print('{:^10}{:<40}'.format('', f'{val.name}'))
                else:
                    print('{:^10}{:<40}{:^7}{:<40}'.format('Renamed', f'{val.name}', '-->', f'{namefile.name}'))
        if flag:
            print('-' * 100)
    for val in p.iterdir():
        if val.is_dir() and not str(val) in FOLDERS:
            replaceFiles(val)
    for val in p.iterdir():
        if not val.is_dir() and not val.suffix in EXTENSIONS:
            unknownFiles.append(str(val))
            exUnknown.append(val.suffix)
    if not os.listdir(p):
        deletedDir.append(str(p))
        os.rmdir(p)

replaceFiles(Path(sys.argv[1]))

if Path(FOLDERS[0]):
    print(f'Photo:')
    for val in Path(FOLDERS[0]).iterdir():
        print('{:^10}{:<40}'.format('', f'{val.name}'))

if Path(FOLDERS[1]):
    print(f'Video:')
    for val in Path(FOLDERS[1]).iterdir():
        print('{:^10}{:<40}'.format('', f'{val.name}'))

if Path(FOLDERS[2]):
    print(f'Documents:')
    for val in Path(FOLDERS[2]).iterdir():
        print('{:^10}{:<40}'.format('', f'{val.name}'))

if Path(FOLDERS[3]):
    print(f'Music:')
    for val in Path(FOLDERS[3]).iterdir():
        print('{:^10}{:<40}'.format('', f'{val.name}'))

if Path(FOLDERS[4]):
    print(f'Archives:')
    for val in Path(FOLDERS[4]).iterdir():
        print('{:^10}{:<40}'.format('', f'{val.name}'))



if deletedDir != []:
    print(f'Next empty folder was deleted:' if len(deletedDir) == 1 else f'Next empty folders ware deleted:')
    for val in deletedDir:
        print('{:^10}{:<40}'.format('', f'{val}'))

if unknownFiles:
    print('Next unknown file:') if len(unknownFiles) == 1 else print(f'Next unknown files:')
    for val in unknownFiles:
        print('{:^10}{:<40}'.format('', f'{val}'))

if exFolders[0]:
    print(f'Image extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exFolders[0]))}'))
if exFolders[1]:
    print(f'Video extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exFolders[1]))}'))
if exFolders[2]:
    print(f'Documents extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exFolders[2]))}'))
if exFolders[3]:
    print(f'Audio extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exFolders[3]))}'))
if exFolders[4]:
    print(f'Archives extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exFolders[4]))}'))
if exUnknown:
    print('Unknown extension:') if len(exUnknown) == 1 else print(f'Unknown extensions:')
    print('{:^15}{:<50}'.format('', f'{", ".join(set(exUnknown))}'))

# розпаковка архівів
for val in Path(FOLDERS[4]).iterdir():
    if val.suffix in EXTENSIONS[4]:
        name = val.name.split('.')
        foldDir = os.path.join(FOLDERS[4], name[0])
        if not Path(foldDir).exists():
            os.mkdir(foldDir)
        shutil.unpack_archive(str(val), str(foldDir))
        if val.exists():
            os.remove(val)