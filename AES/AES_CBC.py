from Cryptodome.Util.number import *
from Cryptodome.Cipher import AES
from pwn import xor

c_last = '8f325d5b5c5454680628fa08746d67cf'
msg = b'Welcome to ?CTF! , I hope you can have fun!!!!!!'

hint_xor_key = 91749376808341004327450956291130629671202939702313462998246826182668975563684
hint_xor_key_bytes = hint_xor_key.to_bytes(32,'big')
hint_half = hint_xor_key_bytes[:16]
key = xor(hint_xor_key_bytes[16:],hint_half)

p1 = msg[:16]
p2 = msg[16:32]
p3 = msg[32:]

c3 = bytes.fromhex(c_last)
aes_ecb = AES.new(key, AES.MODE_ECB)
d3 = aes_ecb.decrypt(c3)        # 从后往前推
c2 = xor(d3, p3)
d2 = aes_ecb.decrypt(c2)
c1 = xor(d2, p2)
d1 = aes_ecb.decrypt(c1)
iv = xor(d1, p1)
print(iv)
