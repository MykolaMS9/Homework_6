import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def translate(name):
    return ''.join([TRANS[ord(val)] if val != ' ' else ' ' for val in name])




# print(translate("Дмитро Короб"))
# print(translate("Олекса Івасюк"))






print(re.findall('[а-яА-ЯіІїЇґ]','привітjap'))


# print(TRANS)
def normalize(name):


    suf = '.txt'
    print(name.replace(suf,''))


    word = []
    for val in name:
        if re.findall('[а-яА-ЯіІїЇґ]', val):
            word.append(TRANS[ord(val)])
        elif re.findall('[a-zA-Z0-9]', val):
            word.append(val)
        else:
            word.append('_')
    return ''.join(word)




    # return ''.join([TRANS[ord(val)] if val != ' ' else ' ' for val in name])

print(normalize('imageйай-*/.tttt.txt'))
print(normalize('image_2 таоІЇіЇІщі'))
print(normalize('імя папки ,54546"№%;"%"'))
print(normalize('image_4fноова папка'))