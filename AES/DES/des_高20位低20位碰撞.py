"""
from Crypto.Cipher import DES
from hashlib import sha256
from numpy import *
from tqdm import *

m = b"Attack at DAWN!!"

def keygen(s):
    keys = []
    for i in range(2020):
        s = sha256(s).digest()
        keys.append(s)
    return keys

def scramble_l(x):
    ret = "".join([format(x >> 20 - 20, '020b')] * 101)
    return int(ret, 2)

def encrypt(msg, keys, sec):
    for i in range(1010):
        idx = (sec >> (2 * i)) & 3
        k = keys[i][idx * 8:idx * 8 + 8]
        cp = DES.new(k, DES.MODE_CBC, bytes(8))
        msg = cp.encrypt(msg)
    return msg

keys = keygen(b'secret_sauce_#9')
cts_enc = []
for i in tqdm(range(0, 65536)):
    SECRET_H = scramble_l(0xa0000 + i)
    cts_enc.append(bytes_to_long(encrypt(m, keys, SECRET_H)))

c = b"\x15\x08\x54\xff\x3c\xf4\xc4\xc0\xd2\x3b\xd6\x8a\x82\x34\x83\xbe"

def scramble_h(x):
    ret = "".join([format(x & 0xfffff, '020b')] * 101)
    return int(ret, 2)

def decrypt(msg, keys, sec):
    for i in range(1010):
        idx = (sec >> (2018 - 2 * i)) & 3
        k = keys[2019 - i][idx * 8:idx * 8 + 8]
        cp = DES.new(k, DES.MODE_CBC, bytes(8))
        msg = cp.decrypt(msg)
    return msg

cts_dec = []
for i in tqdm(range(0, 65536)):
    SECRET_L = scramble_h(0xe + i * 16)
    cts_dec.append(bytes_to_long(decrypt(c, keys, SECRET_L)))

# 碰撞和输出
tip, xidx, yidx = intersect1d(cts_enc, cts_dec, return_indices=True)

print("=" * 50)
print("中间相遇攻击结果:")
print("=" * 50)
print(f"碰撞的中间状态值: {tip}")
print(f"在cts_enc中的索引: {xidx}")
print(f"在cts_dec中的索引: {yidx}")

SECRET_high = 0xa0000 + xidx[0]
SECRET_low = 0xe + yidx[0] * 16
SECRET_full = (SECRET_high << 20) | SECRET_low

print(f"\nSECRET高位: {hex(SECRET_high)}")
print(f"SECRET低位: {hex(SECRET_low)}")
print(f"完整SECRET: {hex(SECRET_full)}")

# SECRET高位: 0xa4d9e
# SECRET低位: 0x3618e
# 完整SECRET: 0xa4d9e3618e
"""

import sys
from hashlib import sha256
from Crypto.Cipher import DES

SECRET = 0xa4d9e3618e
seed = b'secret_sauce_#9'


def keygen(s):
    keys = []
    for i in range(2020):
        s = sha256(s).digest()
        keys.append(s)
    return keys


def scramble(s):
    ret = "".join([format(s & 0xfffff, '020b')] * 101)
    ret += "".join([format(s >> 20, '020b')] * 101)
    return int(ret, 2)


def decrypt(keys, msg):
    dk = scramble(SECRET)
    for i in range(2020):
        idx = (dk >> (4038 - (2 * i))) & 3
        k = keys[2019 - i][idx * 8:(idx + 1) * 8]
        cp = DES.new(k, DES.MODE_CBC, bytes(8))
        msg = cp.decrypt(msg)
    return msg


keys = keygen(seed)

msg = b'\x8c\xa9\xd3\xfaXu;)\xcd\xf6\xbe\x1e{\xa9[\xc9\xd7\xb9\x15\xa4}Q\x85z\xe7\xe8\xf5\xd6\xb6 \xed$\n\x80H\xfa\xa8\x9c\x9e\x0e'

ctxt = decrypt(keys, msg)
print(ctxt)
