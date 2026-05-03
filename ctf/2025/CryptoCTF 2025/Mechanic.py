from quantcrypt.kem import MLKEM_1024
from quantcrypt.cipher import KryptonKEM
from random import randint
from pathlib import *
from os import urandom

kem = MLKEM_1024()
kry = KryptonKEM(MLKEM_1024)

with open(r'F:\download\CTF\Mechanic_883a7ac0733921e7c1234ffb1d8081668caa4182\Mechanic\output.raw', 'rb') as f:
    s = f.read()

block_size = kem.param_sizes.sk_size
sk_list = [s[i*block_size:(i+1)*block_size] for i in range(len(s)//block_size)]

c = 22
for sk in sk_list[::-1]:
    ct = Path(rf'F:\download\CTF\Mechanic_883a7ac0733921e7c1234ffb1d8081668caa4182\Mechanic\flag_{c}.enc')
    pt = Path(rf'F:\download\CTF\Mechanic_883a7ac0733921e7c1234ffb1d8081668caa4182\Mechanic\flag_{c-1}.enc')
    pt.touch()
    try:
        kry.decrypt_to_file(sk, ct, pt)
        c -= 1
    except:
        continue
