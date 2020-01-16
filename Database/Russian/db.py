from sqlite3 import connect

db=connect('words.db')
cur=db.cursor()
with open('words.txt',encoding='utf8') as file:
    words=file.read().split('\n')
    for i in range(len(words)):
        cur.execute(f'INSERT INTO words("word") VALUES ("{words[i]}")')
