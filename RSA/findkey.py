from Cryptodome.Util.number import *
from Cryptodome.Cipher import AES
from hashlib import sha256

p = 1000000007
x_val = 367608838
mod1, mod2 = 41813, 53149

# 建表: 3^k1 mod p -> k1
table = {}
val = 1
for k1 in range(mod1):
    table[val] = k1
    val = (val * 3) % p

inv5 = pow(5, -1, p)
rhs_factor = x_val

for k2 in range(mod2):
    if rhs_factor in table:
        k1 = table[rhs_factor]
        print(f"Found k1 = {k1}, k2 = {k2}")
        # CRT 解 key
        # key ≡ k1 (mod mod1)
        # key ≡ k2 (mod mod2)
        # 用 CRT 找最小正整数解
        m = mod1 * mod2
        key = (k1 * mod2 * pow(mod2, -1, mod1) + k2 * mod1 * pow(mod1, -1, mod2)) % m
        # 可能 key 很小，但 key 是 32 位，我们遍历所有可能的 key = key + t*m，且 key < 2^32
        t = 0
        while key + t * m < 2**32:
            k = key + t * m
            # 验证 f(k1,k2) 是否正确（其实已经由建表保证）
            # 但还要验证 key % mod1 == k1, key % mod2 == k2
            if k % mod1 == k1 and k % mod2 == k2:
                print(f"Possible key = {k}")
                aes_key = sha256(long_to_bytes(k)).digest()[:16]
                cipher = b'\x98\xfd\xa8\x05R\x17\xb6y%"\t\xb4\xd7\x82\xc4\'\x0b8\x14q\xff.\x13\xfb\xa4D\xb4\xde-\xd5c\xd6M\x13\x90\xdb\x81\xbd\xd0c>A\xbc)\xd0U\x7fW'
                aes = AES.new(aes_key, AES.MODE_ECB)
                flag = aes.decrypt(cipher)
                print(flag)
                # 如果 flag 格式正确，就退出
                if b'flag' in flag or b'CTF' in flag or b'{' in flag:
                    print("Flag found!")
                    exit(0)
            t += 1
    # 更新 rhs_factor = x_val * (5^{-1})^{k2+1}
    rhs_factor = (rhs_factor * inv5) % p
    if k2 % 5000 == 0:
        print(f"k2 progress: {k2}/{mod2}")

print("Done.")