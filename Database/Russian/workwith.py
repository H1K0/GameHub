import pymorphy2
mph = pymorphy2.MorphAnalyzer()

class Dictionary:
    def __init__(self, path):
        self.path = path
        with open(path, encoding='utf-8') as file:
            self.dic = file.read().split('\n')

    def __repr__(self):
        return self.dic

    def __str__(self):
        return str(self.dic)

    def reload(self):
        self.__init__(self.path)

    def __len__(self):
        return len(self.dic)

    @property
    def data(self):
        return self.dic[:]

    def __contains__(self, item):
        return item in self.dic

    def add(self, word):
        with open(self.path, 'a', encoding='utf-8') as file:
            file.write(f'\n{str(word)}')
        self.reload()


n = '\n'
words = Dictionary('words.txt')
while 1:
    request = input('>>> ').lower().split()
    if request[0] == 'update':
        if request[1] == 'words':
            words = open('words.txt', 'r').read().split('\n')
            init = open('words.txt', 'w')
            upd = open('update.txt', 'r')
            uw = upd.read().split('\n')
            for word in uw:
                word = word.lower()
                try:
                    wd = mph.parse(word)
                except:
                    continue
                if not any(map(lambda parse: parse.tag.POS == 'NOUN', wd)):
                    pass
                elif not any(map(lambda parse: parse.tag.case == 'nomn', wd)):
                    pass
                elif not any(map(lambda parse: parse.tag.number == 'sing', wd)):
                    pass
                else:
                    if word not in words:
                        words.append(word)
            init.write('\n'.join(words).strip())
            init.close()
            upd.close()
        elif request[1] == 'towns':
            towns = open('towns.txt', 'r').read().split('\n')
            towns = list(map(lambda wd: wd.replace('ё', 'е').replace('Ё', 'Е'), towns))
            open('towns.txt', 'w').write('\n'.join(sorted(list(set(towns)))))
        elif request[1] == 'countries':
            couns = open('countries.txt', 'r').read().split('\n')
            couns = list(map(lambda wd: wd.replace('ё', 'е').replace('Ё', 'Е'), couns))
            open('countries.txt', 'w').write('\n'.join(sorted(list(set(couns)))))
    elif request[0] == 'info':
        if request[1] == 'words':
            print(f'{len(open("words.txt", "r").read().split(n))} words')
        elif request[1] == 'towns':
            print(f'{len(open("towns.txt", "r").read().split(n))} words')
        elif request[1] == 'countries':
            print(f'{len(open("countries.txt", "r").read().split(n))} words')
    elif request[0] == 'scan':
        if request[1] == 'words':
            data = words.data
            repet = {}
            for index, word in enumerate(data):
                if not word.islower():
                    print(f'Not lowregister word {word} at position {index}')
                word = word.lower()
                if word in repet.keys():
                    repet[word].append(index)
                    print(f'Repetitive word "{word}" at positions: {", ".join(list(map(str, repet[word])))}')
                else:
                    repet[word] = [index]
            print('SCAN COMPLETED')
    elif request[0] == 'exit':
        break