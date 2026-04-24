from gmpy2 import invert
from Cryptodome.Util.number import *
from Cryptodome.Cipher import PKCS1_v1_5
import binascii

n = 86934482296048119190666062003494800588905656017203025617216654058378322103517
e = 65537
p = 285960468890451637935629440372639283459
q = 304008741604601924494328155975272418463

L = (p-1)*(q-1)
d = invert(e, L)

# 读取密文
with open(r"F:\download\CTF\0eaf8d6c-3fe5-4549-9e81-94ac42535e7b\flag.enc", 'rb') as file:
    ciphertext = file.read()

# 将密文转换为整数
ciphertext_int = bytes_to_long(ciphertext)

# 使用原始 RSA 解密（无填充）
plaintext_int = pow(ciphertext_int, d, n)
plaintext_bytes = long_to_bytes(plaintext_int)

print("解密结果:", plaintext_bytes)

# 如果是 PKCS#1 v1.5 填充，需要去除填充
try:
    # 尝试解析 PKCS#1 v1.5 填充
    if plaintext_bytes[0:1] == b'\x00' and plaintext_bytes[1:2] == b'\x02':
        # 找到分隔符 0x00
        separator_index = plaintext_bytes.find(b'\x00', 2)
        if separator_index != -1:
            actual_data = plaintext_bytes[separator_index+1:]
            print("去除填充后的明文:", actual_data)
            print("Flag:", actual_data.decode('utf-8'))
except Exception as e:
    print("解析填充时出错:", e)