import socket
import threading
import rsa
import argparse
from hashlib import sha256
from secrets import compare_digest

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.keys = {}

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return
        self.s.send(self.username.encode())
        print(self.username)
        p, q = rsa.generate_p_q(rsa.primes)
        e = rsa.encryption_exponent(p, q)
        d = rsa.decryption_exponent(p, q, e)
        N = p*q
        self.keys['e'] = e
        self.keys['p'] = p
        self.keys['q'] = q
        self.keys['d'] = d
        self.s.send(str(N).encode())
        self.s.send(str(e).encode())
        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()
            N = self.keys['p'] * self.keys['q']
            number = rsa.div_to(N)
            decoded = rsa.decode(message, N, self.keys['d'], number)
            message = rsa.numberblocks_to_message(decoded, rsa.alphabet, number)
            print(message)

    def write_handler(self):
        while True:
            print("In format name::message")
            message = input()
            username, messg = message.split('::')
            self.s.send(username.encode())
            N = self.s.recv(1024).decode()
            e = self.s.recv(1024).decode()
            number = rsa.div_to(N)
            mess = rsa.message_to_numberblocks(message, number)
            c = rsa.encode(mess, e, N, number)
            self.s.send(c.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    args = parser.parse_args()
    cl = Client("127.0.0.1", 9001, args.username)
    cl.init_connection()