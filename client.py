import socket
import threading
import rsa
import argparse
import time
from secrets import compare_digest



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
        self.s.send(self.username.encode())


    def read_handler(self):
        while True:
            message = self.s.recv(1024)#.decode()
            time.sleep(0.01)
            # message = rsa.numberblocks_to_message(decoded, rsa.alphabet, number)
            messag = rsa.decode_message(message, self.N, self.d)
            print(messag)

    def write_handler(self):
        while True:
            print("In format name|message")
            message = input()
            username = message.split('|')[0]
            self.s.send(username.encode())
            with open('public_keys.txt', 'r') as f:
                for line in f:
                    line = line.split(', ')
                    if line[0] == username:
                        N = line[1]
                        e = line[2]
            messag = message.split('|')[1]
            time.sleep(0.1)
            number = rsa.div_to(N)
            # mess = rsa.message_to_numberblocks(messag, number)
            mess = messag
            c = rsa.encode(mess, e, N, number)
            mess = b""
            for number in c:
                mess += number.to_bytes(8, "big")
            result = mess #+ "|".join(c)
            self.s.send(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    args = parser.parse_args()
    cl = Client("127.0.0.1", 9000, args.username)
    cl.init_connection()