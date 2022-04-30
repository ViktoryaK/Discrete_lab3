import socket
import threading
import rsa
import time

class Server:
    """
    To commit
    """
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
            time.sleep(0.01)
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.username_lookup:
            with open('public_keys.txt', 'r') as f:
                for line in f:
                    line = line.split(', ')
                    if line[0] == self.username_lookup[client]:
                        N = line[1]
                        e = line[2]
            number = rsa.div_to(N)
            mess = rsa.message_to_numberblocks(msg, number)
            c = rsa.encode(mess, e, N, number)
            for client in self.username_lookup:
                if self.username_lookup[client] == self.username_lookup[client]:
                    mess = b""
                    for number in c:
                        mess += number.to_bytes(8, "big")
                    client.send(mess)

    def handle_client(self, c: socket, addr):
        while True:
            receive = c.recv(1024).decode()
            username = receive.split('|')[0]
            messg = receive.split('|')[1:]
            for client in self.username_lookup:
                if self.username_lookup[client] == username:
                    client.send("".join(messg).encode())

if __name__ == "__main__":
    s = Server(9001)
    s.start()
