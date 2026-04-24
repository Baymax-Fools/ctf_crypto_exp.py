#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
from tqdm import tqdm
import time


def exploit():
    try:
        r = remote("node5.buuoj.cn", 28263)

        # 生成随机数据
        auth_code = urandom(16)
        token = urandom(16)
        diff = [0] * 16

        log.info("开始Padding Oracle攻击...")

        for i in reversed(range(16)):
            log.info(f"处理字节位置: {i}")
            found = False

            for b in tqdm(range(256)):
                diff[i] = b
                tmp_tk = xor(token, bytes(diff))

                r.sendlineafter(b'> ', b'1')
                r.sendlineafter(b'Enter your token > ', tmp_tk.hex().encode())
                r.sendlineafter(b'Enter your authentication code > ', auth_code.hex().encode())
                res = r.recvline(timeout=5)

                if b'out' in res:
                    log.success(f"位置 {i} 找到字节: {b:02x}")
                    if i != 0:
                        for j in range(i, 16):
                            diff[j] ^= (16 - i) ^ (16 - i + 1)
                    found = True
                    break
                elif b'oops' in res:
                    continue
                else:
                    log.warning(f"意外响应: {res}")

            if not found:
                log.error(f"位置 {i} 未找到有效字节")
                return False

        # 构造最终token
        log.info("构造最终token...")
        forged_token = xor(token, bytes(diff))
        forged_token = xor(forged_token, b'\x10' * 16)

        # 尝试所有可能的有效代码
        valid_codes = [b'SoNP#1033', b'SoNP#3329', b'SoNP#4431', b'SoNP#5052']

        for code in valid_codes:
            log.info(f"尝试代码: {code}")
            final_token = xor(forged_token, pad(code, 16))

            r.sendlineafter(b'> ', b'1')
            r.sendlineafter(b'Enter your token > ', final_token.hex().encode())
            r.sendlineafter(b'Enter your authentication code > ', auth_code.hex().encode())

            res = r.recvline(timeout=5)
            log.info(f"响应: {res}")

            if b'flag' in res or b'unlocked' in res:
                log.success("攻击成功!")
                print(res)
                r.interactive()
                return True
            elif b'oops' in res:
                log.warning("Padding错误，继续尝试下一个代码")
                continue
            else:
                log.warning(f"其他响应: {res}")

        log.error("所有代码尝试失败")
        return False

    except Exception as e:
        log.error(f"错误: {e}")
        return False


# 重试机制
for attempt in range(3):
    log.info(f"尝试第 {attempt + 1} 次攻击...")
    if exploit():
        break
    time.sleep(2)

# from secret import flag
# import string
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# from os import urandom
# import re
#
# key = urandom(16)
#
# menu = '''
# [+] WatchDog Security System
# [+] Copyright (c) 1010 by School of Natural Philosophy
#
# please select your option:
# 1. Unlock Secret Entry
# 2. Help
# 3. Exit
# '''
#
# valid_code = [1033,3329,4431,5052]
#
# auth_context_pattern = re.compile(r'^SoNP#[0-9]{4}$')
#
# def auth_context_checker(ctx : bytes):
#     for c in ctx:
#         if chr(c) not in string.printable:
#             return False
#     if auth_context_pattern.match(ctx.decode()) : return True
#
#     return False
#
# def unlock():
#     token = bytes.fromhex(input('Enter your token > '))
#     auth_code = bytes.fromhex(input('Enter your authentication code > '))
#
#     cipher = AES.new(key, AES.MODE_CBC,token)
#
#     check = cipher.decrypt(auth_code)
#     try:
#
#         msg = unpad(check, 16)
#         if auth_context_checker(msg) and int(msg[5:].decode()) in valid_code:
#             print('door unlocked, here is your reward')
#             print(flag)
#         else:
#             print('get out')
#
#     except Exception as e:
#         print('oops, something wrong')
#         print(e)
# def help():
#     print('To unlock the door, please enter your token and authentication code.')
# while True:
#     print(menu)
#     opt = input('> ')
#     try:
#         opt = int(opt)
#         if opt == 1:
#             unlock()
#         elif opt == 2:
#             help()
#         elif opt == 3:
#             break
#         else:
#             print('invalid option')
#     except:
#         print('oh no, something wrong!')
#

