import socket
import threading
import rsa
import argparse

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.d = None
        self.N = None
        self.e = None

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
        self.d = d
        N = p*q
        self.N = N
        self.e = e
        with open("public_keys.txt", "a") as file:
            file.write(f"{self.username}, {N}, {e}\n")
        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            """
            line 40, in read_handler
    message = self.s.recv(1024).decode()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf6 in position 14: invalid start byte
"""
            message = self.s.recv(1024).decode()
            number = rsa.div_to(self.N)
            decoded = rsa.decode(message, self.N, self.d, number)
            message = rsa.numberblocks_to_message(decoded, rsa.alphabet, number)
            print(message)

    def write_handler(self):
        while True:
            print("In format name|message")
            message = input()
            username = message.split('|')[0]
            with open('public_keys.txt', 'r') as f:
                for line in f:
                    line = line.split(', ')
                    if line[0] == username:
                        N = line[1]
                        e = line[2]
            messag = message.split('|')[1]
            number = rsa.div_to(N)
            mess = rsa.message_to_numberblocks(messag, number)
            c = rsa.encode(mess, e, N, number)
            c = [str(i) for i in c]
            result = username + "|" + "|".join(c)
            self.s.send(result.encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    args = parser.parse_args()
    cl = Client("127.0.0.1", 9001, args.username)
    cl.init_connection()