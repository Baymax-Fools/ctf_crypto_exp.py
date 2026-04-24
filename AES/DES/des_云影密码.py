# 解题脚本
from pwn import *
import gmpy2
import string

host = '111.231.70.44'
port = 28045
block = 8
secret_len = 38
ori_padding_len = block - secret_len % block


def getCliphertext(data):
    return hex(gmpy2.iroot(int(data, 16), 12)[0])[2:]


p = connect(host, port)
dic = '0124'
padding = ['1024102', '102410', '10241', '1024', '102', '10', '1', '']
flag = ''

for i in range(secret_len):
    prob = []
    find = 0
    payload = '*' * (ori_padding_len + i + 1)

    group = i // block
    for j in range(20):
        p.recvuntil('> ')
        p.sendline('1')
        p.recvuntil('msg: ')
        p.sendline(payload)
        p.recvuntil('is : ')
        data = p.recvline()
        data = getCliphertext(data)
        print([data[i:i + 16] for i in range(0, len(data), 16)])
        print(data)
        if group == 0:
            prob.append(data[-16:])
        else:
            prob.append(data[-16 * (group + 1):-16 * (group + 1) + 16])
        prob = list(set(prob))
    print(str(i + 1) + ' prob = ' + str(prob))
    for j in dic:
        p.recvuntil('> ')
        p.sendline('1')
        p.recvuntil('msg: ')
        flag_suffix = flag[:min(len(flag), 7)]
        payload = j + flag_suffix + padding[min(len(flag_suffix), 7)]
        print(payload)
        p.sendline(payload)
        p.recvuntil('is : ')
        data = p.recvline()
        data = getCliphertext(data)
        print(data[:16])
        if data[:16] in prob:
            flag = j + flag
            print(str(i + 1) + ' flag = ' + flag)
            print()
            find = 1
            break
    if find == 0:
        print(str(i + 1) + ' cannot find!')
        break

print(flag)
# 44414440122401244401404424404421440414

/ **
*复制并使用代码请注明引用出处哦
~
*Lazzaro @ https: // lazzzaro.github.io
* /

# -*- coding:utf-8 -*-
# Author:airrudder

from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
from secret import FLAG, KEY, HINT
from itertools import *
import random


def Encode_1024sys(data, key):
    data_list = [data[i:i + 8] for i in range(0, len(data), 8)]
    k1 = DES.new(key.encode(), DES.MODE_ECB)
    k2 = DES.new(key[::-1].encode(), DES.MODE_ECB)
    data_res = ''
    for i in range(0, len(data_list)):
        k = random.choice([k1, k2])
        c = k.encrypt(data_list[i].encode())
        data_res += b2a_hex(c).decode()
    return data_res


def Encode_1024(data, key):
    len_data = len(data)
    choices = cycle('1024')
    while len_data % 8 != 0:
        data += next(choices)
        len_data = len(data)
    data_res = Encode_1024sys(data, key)
    data_out = hex(int(data_res, 16) ** 12 + random.randint(10 ** 1023, 10 ** 1024))[2:]
    return data_out


def main():
    menu = '''
1. Encode
2. Verify your FLAG
3. Exit
'''
    try:
        while True:
            print(menu)
            choice = input("> ")
            if choice == "1":
                msg = input("Please input your msg: ")
                data_out = Encode_1024(msg + FLAG, KEY)
                print("hex(Encode_1024(msg+flag)) is :", data_out)
            elif choice == "2":
                yourFLAG = input('Please input your FLAG: ')
                if yourFLAG == FLAG:
                    print(HINT)
                else:
                    print('1024, nonono..., come on!!!')
            elif choice == "3":
                print("Bye!")
                return
            else:
                print("Invalid choice!")
                continue

    except:
        print('error')


if __name__ == "__main__":
    main()

