# (c) Masahiko AMANO (H1K0)
try:
    from random import choice
except:
    print('У вас не установлена библиотека "random". Установите ее, введя в командной строке "pip install random".')
    input()
    exit()
try:
    import pymorphy2
    mph = pymorphy2.MorphAnalyzer()
except:
    print('У вас не установлена библиотека "pymorphy2". Установите ее, введя в командной строке "pip install pymorphy2", а затем установите русский словарь "pip install -U pymorphy2-dicts-ru".')
    input()
    exit()
try:
    from datetime import datetime
except:
    print('У вас не установлена библиотека "datetime". Установите ее, введя в командной строке "pip install datetime".')
    input()
    exit()


def now():
    dt = datetime.today()
    return f'{dt.day}.{dt.month}.{dt.year} {dt.hour}:{dt.minute}:{dt.second}.{str(dt.microsecond)[:3]}'


def addword(word):
    global file, words
    dct = open(r'..\Database\Russian\words.txt', 'a')
    dct.write(f'\n{word}')
    dct.close()
    file = open(r'..\Database\Russian\words.txt', 'r')
    words = file.read().split('\n')


file = open(r'..\Database\Russian\words.txt', 'r')
words = list(filter(lambda word: all(map(lambda letter: word.count(letter) == 1, list(word))), file.read().split('\n')))
log = open('log.txt', 'a')
gamenum = len(list(filter(lambda line: line.startswith('='), open('log.txt', 'r').read().split('\n'))))

print(''' (c) Masahiko AMANO (H1K0)

Давайте поиграем в быков и коров!
Если вы хотите узнать правила игры, введите "?". Если правила вам уже известны и вы хотите начать игру, введите "!". Для просмотра статистики введите "123".
Для выхода введите ".".
Изначально планировалось сделать "help", "play", "stat" и "exit" соответственно, но кому не лень постоянно туда-сюда гонять раскладку клавы? :)''')
request = input('\n>>> ').lower()
gamemode = False
while request != '.':
    print()
    if request == '?':
        print('''Правила игры "Быки и коровы":

  Компьютер загадывает рандомное русское слово той длины, которую вы введете в начале игры. Далее вы будете вводить существительные в единственном числе в именительном падеже той же длины без повторяющихся букв, а компьютер будет вам отвечать.
  Один бык (1 б.) означает, что во введенном вами слове есть буква из загаданного слова, и она стоит на верной позиции.
  Одна корова (1 к.) означает, что во введенном вами слове есть буква из загаданного слова, и она стоит НЕ на верной позиции.''')
    elif request == '!' and not gamemode:
        print('Перед началом введите длину загаданного слова.')
        while 1:
            try:
                length = int(input('\n>>> '))
                if length < 3:
                    print('\nНу сказал же, НЕ МЕНЕЕ 3. Разве интересно отгадывать слово из двух букв или тем более одной? Исправьте вашу ошибку, пожалуйста.')
                    continue
                elif length not in map(len, words):
                    print('\nИзвините, в нашей базе нет слов такой длины. Попробуйте другую.')
                    continue
            except:
                print('\nВ вашем вводе допущена ошибка. Исправьте ее.')
            else:
                break
        mainword = choice(list(filter(lambda word: len(word) == length, words)))
        print('\nИгра началась!')
        gamemode = True
        log.write(f'\n\n=================== Игра №{gamenum + 1} ({now()}) ===================\n')
        count = 1
    elif request == '123':
        wins = open('log.txt', 'r').read().split('\n').count('--- ВЫИГРЫШ ---')
        loses = open('log.txt', 'r').read().split('\n').count('--- ПРОИГРЫШ ---')
        print(f'Всего сыграно: {gamenum}.\n'
              f'Выиграно: {wins}.\n'
              f'Проиграно: {loses}.')
    elif gamemode:
        try:
            word = mph.parse(request)
        except:
            print('Извините, но вы ввели какую-то абракадабру. ;) Попробуйте еще раз.')
            continue
        if not any(map(lambda parse: parse.tag.POS == 'NOUN', word)):
            print('Введенное вами слово не является существительным. Попробуйте еще раз.')
        elif not any(map(lambda parse: parse.tag.case == 'nomn', word)):
            print('Ваше слово стоит в косвенном падеже. Попробуйте еще раз.')
        elif not any(map(lambda parse: parse.tag.number == 'sing', word)):
            print('Можно использовать только единственное число.')
        elif len(request) != length:
            print('Введенное вами слово не подходит по длине. Попробуйте еще раз.')
        elif any(map(lambda letter: request.count(letter) > 1, list(request))):
            print('Ваше слово содержит повторябщиеся буквы. Попробуйте еще раз.')
        else:
            log.write(f'\n{count}. {request} ({now()})')
            if request == mainword:
                print('Поздравляю, вы выиграли! :D\nДля начала новой игры введите "!".')
                gamemode = False
                log.write('\n--- ВЫИГРЫШ ---')
                log.close()
                log = open('log.txt', 'a')
                gamenum += 1
                request = input('\n>>> ').lower()
                continue
            if request not in words:
                addword(request)
            bulls = 0
            cows = 0
            for index, letter in enumerate(request):
                if letter in mainword:
                    if mainword.index(letter) == index:
                        bulls += 1
                    else:
                        cows += 1
            print(f'{bulls} б., {cows} к.')
            log.write(f'\n   {bulls} б., {cows} к.')
            count += 1
    else:
        print('Вы не начали игру.')
    request = input('\n>>> ').lower()
    if request == '.' and gamemode:
        log.write('\n--- ПРОИГРЫШ ---')
        log.close()
        log = open('log.txt', 'a')
