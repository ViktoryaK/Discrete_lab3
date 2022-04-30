import random


def div_to(N):
    k='90'
    while int(k+'90') < N:
        k+='90'
    return k.count('90')*2

def prime_nums_generation():
    primes = []
    for numb in range(10, 1000):
      prime = True
      for i in range(2, numb):
        if numb % i == 0:
          prime = False
      if prime:
        primes.append(numb)
    return primes

def generate_p_q(primes):
    while True:
        p = random.choice(primes)
        q = random.choice(primes)
        if p != q:
                return p, q

def encryption_exponent(p, q):
    dividers = []
    to_val = (p-1)*(q-1)
    for i in range(2, to_val):
        if to_val % i == 0:
            dividers.append(i)
    e = random.randint(2, 1000000)
    while True:
        choice = True
        for divider in dividers:
            if e % divider == 0:
                choice = False
        if choice:
            return e
        e = random.randint(2, 10000)

def decryption_exponent(p, q, e):
    module = (p-1)*(q-1)
    d = pow(e, -1, module)
    return d

def message_to_numberblocks(message, lenn):
    in_numbers = ''
    dict = alphabet_to_numbers()
    for letter in message:
        in_numbers += dict[letter]
    i=0
    result = []
    while i < len(in_numbers):
        result.append(in_numbers[i:i+lenn])
        i += lenn
    return result


def alphabet_to_numbers():
    dict = {chr(i): str(number) for number, i in enumerate(range(32, 123))}
    for value in dict:
        if len(dict[value]) == 1:
            dict[value] = '0' + dict[value]
    return dict

def encode(message, e, N, lenn):
    result = []
    for base in message:
        c = pow(int(base), e, N)
        if len(str(c)) < lenn:
            add = lenn - len(str(c))
            c = "0"*add + str(c)
        result.append(str(c))
    return result

def decode(c, N, d, lenn):
    result = []
    for block in c:
        m = pow(int(block), d, N)
        if len(str(m)) < lenn:
            add = lenn - len(str(m))
            m = "0"*add + str(m)
        result.append(str(m))
    return result

def numberblocks_to_message(num_message, diction, lenn):
    result = ""
    half = int(lenn/2)
    letters = []
    for block in num_message:
        if half<2:
            letters.append(block)
        else:
            letters.append(block[:half])
            letters.append(block[half:])
    for letter in letters:
        for key in diction:
            if diction[key] == letter:
                result += key
    return result

primes = prime_nums_generation()
# p, q = generate_p_q(primes)
# p, q = 17, 11
# print(p, q)
# e = encryption_exponent(p, q)
# print(e)
# N = p*q
# print(N)

# print(number)
# message = 'Youre freaking right'
# ulas = ['2015', '1114', '0003']
# print(ulas)
# d = decryption_exponent(p, q, e)
# print(d)
# print(alphabet_to_numbers())
# mess = message_to_numberblocks(message, number)
# print(mess)
# c = encode(mess, e, N, number)
# print(c)
# decoded = decode(c, N, d, number)
# print(decoded)
alphabet = alphabet_to_numbers()
# print(numberblocks_to_message(decoded, alphabet, number))