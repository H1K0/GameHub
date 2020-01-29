import socketserver
class TestServer(socketserver.BaseRequestHandler):
    def handle(self): #вызывается при подключении
        print(self.client_address)
        mode = self.request.recv(1024).decode() #получение режима
        if mode == 'join': #режим подключения
            keys = list(clients.keys()) #список клиентов
            address = self.request.recv(1024).decode()
            self.snd = address
            nf = self.request.recv(1024).decode() #получение слова
            pr = nf
            clients[self.snd] = nf
            while 1:
                if clients[self.snd] != pr: #ожидание слова
                    pos = bytes(clients[self.snd], encoding='utf-8')
                    self.request.send(pos) # отправка слова
                    nf = self.request.recv(1024).decode()
                    pr = nf
                    clients[self.snd] = nf
        elif mode == 'create':
            unus = self.client_address[0] + ' ' + str(self.client_address[1]) #создание клиента
            clients[unus] = 'open'
            pr = 'open'
            while 1:
                if clients[unus] != pr:
                    pos = bytes(clients[unus], encoding='utf-8')
                    self.request.send(pos)
                    nf = self.request.recv(1024).decode()
                    pr = nf
                    clients[unus] = nf
        elif mode == 'load_games':
            keys = list(clients.keys())
            outload = []
            for i in keys: #перебор вариантов
                info = clients[i]
                if info == 'open': #найден челик
                    outload.append(i)
            outload = '!'.join(outload)
            self.request.send(bytes(outload, encoding='utf-8'))
                    
                    
clients = {} #клиенты
if __name__ == "__main__": #создание сервера
    with socketserver.ThreadingTCPServer(("192.168.1.24", 8888), TestServer) as server:
        server.serve_forever()
