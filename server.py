import socket
import threading

import rsa


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)
            print(self.clients)
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # lenn = rsa.div_to()
            # msg = rsa.message_to_numberblocks(msg, )
            # mess = rsa.encode(msg)
            # encrypt the message

            # ...

            client.send(msg.encode())

    def handle_client(self, c: socket, addr): 
        while True:
            username = c.recv(1024).decode()
            public_keys = c.send()
            for client in self.clients:
                if client.username == username:
                    c.send(client.keys)
                    client.send(messg)
            # for client in self.clients:
            #     if client != c:
            #         client.send(username)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
