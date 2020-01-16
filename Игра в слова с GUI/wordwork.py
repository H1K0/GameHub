from random import randint as rnd


class Word:
    def __init__(self, text):
        self.word = text.replace('ё', 'е')

    def __repr__(self):
        return self.word

    def __rshift__(self, other):
        w = self.word
        while w[-1] in ('ъ', 'ы', 'ь'):
            w = w[:-1]
        if w[-1] == other.word[0]:
            return True
        return False

    def __eq__(self, other):
        return self.word == other.word


class Dictionary:
    def __init__(self, path):
        self.path = path
        with open(path, encoding='utf-8') as file:
            self.dic = list(map(lambda w: Word(w), file.read().split('\n')))

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