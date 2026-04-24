from operator import invert

from Crypto.Util.number import long_to_bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
from zlib import crc32
import gmpy2
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import gcd

import sys
from Crypto.Util.number import *
from random import *
sys.setrecursionlimit(2000)
################################################### part1 read pem
with open(r'F:\download\CTF\222158_certificate\private.pem', 'r') as file:
    cipher = file.readlines()[1:-1]
cipher = ''.join(cipher).replace('\n','')
print(cipher)
table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

bitstream = ""
for i in cipher:
    if(i == "?"):
        bitstream += "******"
    else:
        bitstream += bin(table.index(i))[2:].zfill(6)
print(bitstream)
################################################### part2 split params
info1 = hex(int(bitstream[:4*8],2))[2:].zfill(4*2)
print(info1) # 30（标识头） 82 027b（总⻓度）
bitstream = bitstream[4*8:]
info2 = hex(int(bitstream[:3*8],2))[2:].zfill(3*2)
bitstream = bitstream[3*8:]
print(info2)# 0201 00 （版本信息）
##### n,e
infon = hex(int(bitstream[:3*8],2))[2:].zfill(3*2)
print(infon) # 0281 81 （数据⻓度0x81字节）
bitstream = bitstream[3*8:]
n = int(bitstream[:0x81*8],2)  # 81 从37来的
print(n.bit_length())
print("n = ",hex(n))
bitstream = bitstream[0x81*8:]
infoe = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infoe) # 02 21 （数据⻓度0x21字节）
bitstream = bitstream[2*8:]
e = int(bitstream[:0x21*8],2)
print(e.bit_length())
print("e = ",hex(e))
bitstream = bitstream[0x21*8:]
###### d
infod = hex(int(bitstream[:3*8],2))[2:].zfill(3*2)
print(infod) # 0281 80 (数据⻓度0x80字节)
bitstream = bitstream[3*8:]

d = bitstream[:0x80*8]
bitstream = bitstream[0x80*8:]
###### p,q
infop = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infop) # 02 41 (数据⻓度0x41字节)
bitstream = bitstream[2*8:]
p = bitstream[:0x41*8]
# print(p)
bitstream = bitstream[0x41*8:]
infoq = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infoq) # 02 41 (数据⻓度0x41字节)
bitstream = bitstream[2*8:]
q = bitstream[:0x41*8]
bitstream = bitstream[0x41*8:]
# ##### dp,dq
infodp = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infodp) # 02 40 (数据⻓度0x40字节)
bitstream = bitstream[2*8:]
dp = int(bitstream[:0x40*8],2)
print("dp = ",dp)
bitstream = bitstream[0x40*8:]
infodq = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infodq)# 02 41 (数据⻓度0x41字节)
bitstream = bitstream[2*8:]
dq = bitstream[:0x41*8]
bitstream = bitstream[0x41*8:]
###### invert(q, p)
infodmqp = hex(int(bitstream[:2*8],2))[2:].zfill(2*2)
print(infodmqp)# 02 41 (数据⻓度0x41字节)
bitstream = bitstream[2*8:]
dmpq = bitstream[:0x41*8]
bitstream = bitstream[0x41*8:]
print(bitstream)

################################################### part3 recover the flag
cipher =82404436498466895324733436901056359489189960512493202570903960333247277400247388969097533191635462377037232768074464944681385506170855774688613792302290304494481765906529480985984818897269069587516233500512849282866396228645039453616712857020451120948641770106851301755195757766245239907077580562163260112662
p = GCD(pow(2, e*dp, n) - 2, n)
q = n // p
d = inverse(e, (p - 1) * (q - 1))
m = pow(cipher, d, n)
print(long_to_bytes(m))

