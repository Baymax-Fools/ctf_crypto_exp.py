from winreg import error
from Cryptodome.Util.number import *
from Cryptodome.Cipher import AES
from pwn import xor

c=b'C4:\x86Q$\xb0\xd1\x1b\xa9L\x00\xad\xa3\xff\x96 hJ\x1b~\x1c\xd1y\x87A\xfe0\xe2\xfb\xc7\xb7\x7f^\xc8\x9aP\xdaX\xc6\xdf\x17l=K\x95\xd07'
iv=b'\xd1\xdf\x8f)\x08w\xde\xf9yX%\xca[\xcb\x18\x80'
key=b'\xa4\xa6M\xab{\xf6\x97\x94>hK\x9bBe]F'


aes_ecb = AES.new(key, AES.MODE_CBC,iv)
m=aes_ecb.decrypt(c)

print(m)
print(long_to_bytes(m),error='ignore')
# 忽视警告