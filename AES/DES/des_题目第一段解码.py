from itertools import product
from typing import List
from Cryptodome.Util.number import *
from Cryptodome.Cipher import DES
import struct

# DES 参数定义
ROTATIONS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

__pc2 = [
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

# 在PC2盒中没出现的位置数
not_in_PC2 = [9, 18, 22, 25, 35, 38, 43, 54]

# IP 置换表
__ip = [57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6]

# 扩展置换表
__ep = [31, 0, 1, 2, 3, 4,
        3, 4, 5, 6, 7, 8,
        7, 8, 9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31, 0]

# P 置换表
__p = [15, 6, 19, 20, 28, 11, 27, 16,
       0, 14, 22, 25, 4, 17, 30, 9,
       1, 7, 23, 13, 31, 26, 2, 8,
       18, 12, 29, 5, 21, 10, 3, 24]

# S 盒
__s_box = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


# 工具函数
def bits_to_bytes(bits):
    """将比特列表转换为字节"""
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte_val = 0
        for j in range(8):
            if i + j < len(bits):
                byte_val = (byte_val << 1) | bits[i + j]
        byte_array.append(byte_val)
    return bytes(byte_array)


def bytes_to_bits(data):
    """将字节转换为比特列表"""
    bits = []
    for byte in data:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
    return bits


def IP(plain: List[int]) -> List[int]:
    return [plain[x] for x in __ip]


def EP(data: List[int]) -> List[int]:
    return [data[x] for x in __ep]


def P(data: List[int]) -> List[int]:
    return [data[x] for x in __p]


def S_box(data: List[int]) -> List[int]:
    output = []
    for i in range(0, 48, 6):
        row = data[i] * 2 + data[i + 5]
        col = (data[i + 1] << 3) | (data[i + 2] << 2) | (data[i + 3] << 1) | data[i + 4]
        s_val = __s_box[i // 6][row][col]
        output.extend([(s_val >> 3) & 1, (s_val >> 2) & 1, (s_val >> 1) & 1, s_val & 1])
    return output


def PC_2(key: List[int]) -> List[int]:
    return [key[x] for x in __pc2]


def LR(C, D, round_num):
    """逆向循环右移"""
    shift = ROTATIONS[round_num]
    # 循环右移
    C = C[-shift:] + C[:-shift]
    D = D[-shift:] + D[:-shift]
    return C, D


def encrypt_custom(plain: List[int], sub_keys: List[List[int]]) -> List[int]:
    """自定义DES加密函数"""
    plain = IP(plain)
    L, R = plain[:32], plain[32:]

    for i in range(16):
        prev_L = L
        L = R
        expanded_R = EP(R)
        xor_result = [a ^ b for a, b in zip(expanded_R, sub_keys[i])]
        substituted = S_box(xor_result)
        permuted = P(substituted)
        R = [a ^ b for a, b in zip(permuted, prev_L)]

    cipher = R + L
    # 最终置换（逆IP）
    ip_inv = [39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25,
              32, 0, 40, 8, 48, 16, 56, 24]
    cipher = [cipher[x] for x in ip_inv]
    return cipher


# 主解密逻辑
guess_8bit = list(product(range(2), repeat=8))


def re_PC2(sbkey):
    """48-bit -> 56-bit"""
    res = [0] * 56
    for i in range(len(sbkey)):
        res[__pc2[i]] = sbkey[i]
    return res


def guess_CiDi16(sbkey, t):
    res = re_PC2(sbkey)
    for i in range(8):
        res[not_in_PC2[i]] = guess_8bit[t][i]
    return res


def guess_allsbkey(roundkey, r, t):
    sbkey = [[]] * 16
    sbkey[r] = roundkey
    CiDi = guess_CiDi16(roundkey, t)
    Ci, Di = CiDi[:28], CiDi[28:]

    for i in range(r + 1, r + 16):
        Ci, Di = LR(Ci, Di, i % 16)
        sbkey[i % 16] = PC_2(Ci + Di)
        if i % 16 == 0:
            combined = Ci + Di
    return combined, sbkey


def long_des_enc(c, k):
    """使用自定义DES进行解密"""
    assert len(c) % 8 == 0
    res = b''

    for i in range(0, len(c), 8):
        block = c[i:i + 8]
        # 将字节转换为比特
        block_bits = bytes_to_bits(block)
        # 使用自定义DES解密（子密钥倒序）
        decrypted_bits = encrypt_custom(block_bits, k[::-1])
        # 将比特转换回字节
        decrypted_bytes = bits_to_bytes(decrypted_bits)
        res += decrypted_bytes

    return res


def try_des(cipher, roundkey):
    for t in range(256):
        combined, allkey = guess_allsbkey(roundkey, 15, t)
        plain = long_des_enc(cipher, allkey)
        if plain.startswith(b'Nep'):
            print("Found correct key!")
            print("Combined:", combined)
            print("Plaintext:", plain)
            return True
    return False


# 主程序
if __name__ == "__main__":
    tt = [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0,
          0,
          1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0,
          0,
          1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1,
          0,
          0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,
          1,
          0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
          0,
          1, 0]

    t_bits = tt[:64]
    t_bytes = bits_to_bytes(t_bits)

    LL = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Rr = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]

    print("Starting brute force attack...")
    found = False

    for i in range(2 ** 9 - 1, 2 ** 7, -1):
        if i % 50 == 0:
            print(f"Testing combination {i}...")

        tmp = list(bin(i)[2:].rjust(9, '0'))
        L = LL + [int(u) for u in tmp]
        R = Rr
        combined = L + R
        sub_key = PC_2(combined)

        if try_des(t_bytes, sub_key):
            found = True
            break

    if not found:
        print("Key not found in the search range")