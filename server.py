import socket
import threading
import rsa
import time


class Client:
    def __init__(self, s, name):
        self.socket = s
        self.name = name

    def send(self, m):
        self.socket.send(m)

class Server:
    """
    To commit
    """
    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with open("public_keys.txt", "w") as file:
            ...

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            time.sleep(0.01)
            print(f"{username} tries to connect")
            self.username_lookup.append(Client(c, username))

            self.clients.append(c)

            self.broadcast(f'new person has joined: {username}')
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def send_to_client(self, client, msg):
        with open('public_keys.txt', 'r') as f:
            for line in f:
                line = line.split(', ')
                if line[0] == client.name:
                    N = line[1]
                    e = line[2]
        number = rsa.div_to(N)
        c = rsa.encode(msg, e, N, number)
        hashed = rsa.hashing(msg)
        client.send(hashed)
        time.sleep(0.01)
        mess = b""
        for number in c:
            mess += number.to_bytes(8, "big")
        client.send(mess)

    def broadcast(self, msg: str):
        for client in self.username_lookup:
            self.send_to_client(client, msg)


    def handle_client(self, c: socket, addr):
        while True:
            username = c.recv(1024).decode()
            time.sleep(0.1)
            hashed = c.recv(1024)
            time.sleep(0.1)
            receive = c.recv(1024)
            for client in self.username_lookup:
                if client.socket != c:
                    if client.name == username:
                        client.send(hashed)
                        time.sleep(0.1)
                        client.send(receive)



if __name__ == "__main__":
    s = Server(9000)
    s.start()