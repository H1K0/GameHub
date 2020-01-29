import socket


def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('176.195.163.164', 8888))


def create(game):
    sock.send(bytes("create", encoding='utf-8'))
    while 1:
        inf = sock.recv(1024).decode()
        print(inf)
        ninf = input()
        sock.send(bytes(ninf, encoding='utf-8'))


def join(address):
    sock.send(bytes("join", encoding='utf-8'))
    sock.send(bytes(address, encoding='utf-8'))
    while 1:
        ninf = input()
        if ninf == 'close':
            exit()
        sock.send(bytes(ninf, encoding='utf-8'))
        inf = sock.recv(1024).decode()
        print(inf)


def load_games():
    global sock
    sock.send(bytes("load_games", encoding='utf-8'))
    users_list = sock.recv(1024).decode().split('!')[0]
    for i in users_list:
        print(i)
    print('кого выбираем?')
    choose = int(input())
    address = users_list[choose - 1]
    sock.close()
    del sock
    connect()
    join(address)


if __name__=='__main__':
    connect()
    mode = input()
    if mode == 'join':
        join()
    if mode == 'create':
        create()
    if mode == 'load_games':
        load_games()
