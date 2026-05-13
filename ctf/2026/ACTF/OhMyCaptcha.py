#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import bytes_to_long
from math import gcd
import re
import time

context.log_level = 'warn'

HOST, PORT = "1.95.137.55", 9999
SRC = b"help('secret')#!."
MSG = bytes_to_long(SRC)
PHONES = [17625083317, 12776258639, 19732306117, 17510652739]
PHONE_LINE = " ".join(map(str, PHONES))
NEED = 12

# MSG % PHONES == [0, 9, 42, 53]. 0/9 always appear in the 10-digit permutation,
# so a connection is usable iff the captcha contains substrings "42" and "53".
assert [MSG % p for p in PHONES] == [0, 9, 42, 53]


def one_try():
    try:
        p = remote(HOST, PORT, timeout=8)
        p.recvuntil(b": ")
        p.sendline(PHONE_LINE.encode())

        data = p.recvuntil(b"valid for 1 minute.\n")
        m = re.search(rb"\] ([0-9]{10}) is your group verification code", data)
        if not m:
            p.close()
            return None
        code = m.group(1)
        if b"42" not in code or b"53" not in code:
            p.close()
            return None

        if b"> " not in data:
            data += p.recvuntil(b"> ")
        n = int(re.search(rb"n\s*=\s*(\d+)", data).group(1))

        p.sendline(str(MSG).encode())
        line = p.recvline()
        if b"Verification failed" in line:
            p.close()
            return None

        c = int(re.search(rb"[0-9a-f]+", line).group(0), 16)
        p.close()
        return n, c, code.decode()

    except (EOFError, TimeoutError, AttributeError, ValueError):
        time.sleep(0.2)
        return None


def crt(items):
    x, mod = 0, 1
    for n, c in items:
        if gcd(mod, n) != 1:
            continue
        t = ((c - x) % n) * pow(mod, -1, n) % n
        x += mod * t
        mod *= n
        x %= mod
    return x, mod


def iroot5(x):
    lo, hi = 0, 1 << ((x.bit_length() + 4) // 5 + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**5 <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo, lo**5 == x


def main():
    items, tries = [], 0
    while True:
        tries += 1
        res = one_try()
        if not res:
            if tries % 100 == 0:
                print(f"[*] tried={tries}, hits={len(items)}")
            continue

        n, c, code = res
        items.append((n, c))
        print(f"[+] hit {len(items)}/{NEED}: try={tries}, code={code}, nbits={n.bit_length()}")

        if len(items) >= NEED:
            x, mod = crt(items)
            m, ok = iroot5(x)
            if ok:
                pt = m.to_bytes((m.bit_length() + 7) // 8, "big")
                flag = re.search(rb"ACTF\{[^}]+\}", pt).group(0)
                print(flag.decode())
                return
            print(f"[-] CRT modulus too small or root not exact, bits={mod.bit_length()}")


if __name__ == "__main__":
    main()


'''
from Crypto.Util.number import *
from Crypto.Cipher import AES
import random, subprocess, os, signal, re
from secret import FLAG

assert re.fullmatch(rb'ACTF\{.{41}\}', FLAG)
valid_mobile = lambda num: [s:=str(num), len(s) == 11 and s[0] == '1'][1] and isPrime(num)
prod = lambda x: 1 if not x else x[0]*prod(x[1:])

class SandboxService:
    def __init__(self, p, q):
        self.n = p * q
        self.e = 5
    
    def encrypt(self, msg):
        return pow(bytes_to_long(msg), self.e, self.n)
    
    def run(self, template):
        output = subprocess.run(
            ['python3', '-c', template],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1,
        ).stdout
        return long_to_bytes(self.encrypt(output.strip()))

class OhMyCaptcha:
    def __init__(self):
        self.code = ''.join(random.sample("0123456789", 10))
        self.pn = None

    def verify(self, message):
        return 0 <= message < prod(self.pn) and all(str(message % p) in self.code for p in self.pn)

    def start(self):
        print("Are you human? ")
        self.pn = list(set(map(int, input("Enter phone numbers to get a group verification code: ").split())))
        assert all(valid_mobile(p) for p in self.pn) and 0 < len(self.pn) < 66
        print(f"[Azure Assassin Alliance] {self.code} is your group verification code, valid for 1 minute.")
        signal.alarm(60)

    def serve(self):
        sandbox = SandboxService(getPrime(0x137), getPrime(0x137))
        print("n =", sandbox.n)
        key, nonce = [os.urandom(8).hex() for _ in ":)"]
        cipher = AES.new(key.encode(), AES.MODE_CTR, nonce=bytes.fromhex(nonce)).encrypt(FLAG).hex()
        for _ in "AAA🤩":
            message = int(input('> '))
            template = f"key = {key!r}\ncipher_with_key_{key}_{nonce} = {cipher!r}\nprint(eval({long_to_bytes(message)}))"
            if self.verify(message):
                print(sandbox.run(template).hex())
            else:
                print("Verification failed.")

if __name__ == "__main__":
    OHC = OhMyCaptcha()
    OHC.start()
    OHC.serve()

'''