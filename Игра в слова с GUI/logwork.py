from datetime import datetime

def now(): # Получаем системное время
    dt = datetime.today()
    return f'{dt.day}.{dt.month}.{dt.year} {dt.hour}:{dt.minute}:{dt.second}.{str(dt.microsecond)[:3]}'


class Log:
    def __init__(self, un):
        self.username = un
        self.data = ''
        try:
            with open(f'..\\Users\\{self.username}\\WordGame\\log.txt', encoding='utf-8') as file:
                self.data = file.read()
        except:
            self.edited = True
            self.save()
            self.__init__(un)
        self.edited = False

    def reload(self):
        self.__init__(self.username)

    def save(self):
        if self.edited:
            with open(f'..\\Users\\{self.username}\\WordGame\\log.txt', 'w', encoding='utf-8') as file:
                file.write(self.data)

    def __len__(self):
        return len(list(filter(lambda line: line.startswith('='), self.data.split('\n'))))

    def newgame(self):
        self.data += f'\n\n{19 * "="} Игра №{len(self) + 1} ({now()}) {19 * "="}'
        self.edited = True

    def move(self, player, word):
        self.data += f'\n{player}: {word} ({now()})'
        self.edited = True

    def mistake(self, n, s=True):
        if s:
            self.data += f'\n--- ОШИБКА {n} ---'
        else:
            self.data += '\n---'
        self.edited = True

    def win(self):
        self.data += '\n--- ВЫИГРЫШ ---'
        self.edited = True

    def lose(self):
        self.data += '\n--- ПРОИГРЫШ ---'
        self.edited = True