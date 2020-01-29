with open('log.txt', encoding='utf-8') as file:
    data = file.read()
data = data.replace('--- ВЫИГРЫШ ---', '--- win ---').replace('--- ПРОИГРЫШ ---', '--- ВЫИГРЫШ ---').replace('--- win ---', '--- ПРОИГРЫШ ---')
data = data.split('\n')
for i in range(len(data)):
    if data[i].startswith('--- ОШИБКА'):
        data[i] = '---'
print('\n'.join(data[:100]))
input()
with open('log.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(data))