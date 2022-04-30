import socket
import threading
import rsa


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.keys = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            N = c.recv(1024).decode()
            e = c.recv(1024).decode()
            self.keys[username] = [N, e]
            self.username_lookup[c] = username
            self.clients.append(c)
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for username in self.keys:
            N = self.keys[username][0]
            e = self.keys[username][1]
            number = rsa.div_to(N)
            mess = rsa.message_to_numberblocks(msg, number)
            c = rsa.encode(mess, e, N, number)
            for client in self.clients:
                if client.username == username:
                    client.send(c.encode())

    def handle_client(self, c: socket, addr):
        while True:
            username = c.recv(1024).decode()
            for key in self.username_lookup:
                if self.username_lookup[key] == username:
                    N = key.keys['p'] * key.keys['q']
                    c.send(str(N)).encode()
                    c.send(str(key.keys['e'])).encode()
            messg = c.recv(1024).decode()
            for client in self.clients:
                if client.username == username:
                    client.send(messg)


if __name__ == "__main__":
    s = Server(9001)
    s.start()
