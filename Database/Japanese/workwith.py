import pymorphy2
mph = pymorphy2.MorphAnalyzer()

iw = open('dictionary.txt', 'r').read().split('\n')
while 1:
    request = input('>>> ').lower()
    if request == 'update':
        init = open('dictionary.txt', 'w')
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
                if word not in iw:
                    iw.append(word)
        init.write('\n'.join(iw).strip())
        init.close()
        upd.close()
    elif request == 'info':
        print(f'{len(iw)} words')
    elif request == 'exit':
        break
