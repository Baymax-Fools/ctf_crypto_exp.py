from winreg import error

from Crypto.Util.number import bytes_to_long,long_to_bytes
from Cryptodome.Util.number import *
from Cryptodome.Cipher import AES
from pwn import xor
key_xor_iv =  91144196586662942563895769614300232343026691029427747065707381728622849079757
c = b'\x8c-\xcd\xde\xa7\xe9\x7f.b\x8aKs\xf1\xba\xc75\xc4d\x13\x07\xac\xa4&\xd6\x91\xfe\xf3\x14\x10|\xf8p'

for i in range(65536):
    key = long_to_bytes(i).rjust(2, b'\x00') * 16
    iv = long_to_bytes(bytes_to_long(key) ^ key_xor_iv).rjust(16,b'\x00')
    try:
        aes_ecb = AES.new(key, AES.MODE_CBC, iv)
        m = aes_ecb.decrypt(c)
        print(m)
        print(long_to_bytes(m), error='ignore')
    except Exception as e:
        continue
