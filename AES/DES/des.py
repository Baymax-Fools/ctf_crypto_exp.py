import string
from Cryptodome.Cipher import DES

def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = cipher.decrypt(ciphertext).decode('utf-8', errors='ignore')

    # 直接取最后一个字符的值作为原文长度
    text_length = ord(padded_text[-1])
    return padded_text[:text_length]

c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'  # 这里替换实际的密文
# 爆破3个字符的密钥
characters = string.ascii_letters + string.digits + string.punctuation

for i in range(len(characters)):
    for j in range(len(characters)):
        for k in range(len(characters)):
            key = f'ezdes{characters[i]}{characters[j]}{characters[k]}'.encode('utf-8')
            try:
                flag = decrypt(c, key)
                if flag.startswith('moectf{') and flag.endswith('}'):
                    print(f"Found: key={key.decode()}, flag={flag}")
                    break
            except:
                continue