from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from secrets import flag
import random
import hashlib

class Niederreiter_Cryptosystem:
    def __init__(self, n, k):
        self.F = GF(2^8,repr='int')
        alpha = self.F.list()[1:]
        self.C = codes.GeneralizedReedSolomonCode(alpha, k)     # 获取校验矩阵 H  创建一个广义Reed-Solomon码
        # 计算码的纠错能力 t = (n-k)//2 = 16
        self.t = (n - k) // 2
        # 生成公钥和私钥
        self.pub, self.priv = self.gen(n, k)

    def get_recover_ability(self):
        return self.t

    def get_key(self):
        return self.priv

    def gen(self, n, k):
        # 获取GRS码的校验矩阵 H (32×255)
        H = self.C.parity_check_matrix()        # 函数sage中内有
        # 生成随机置换矩阵 P (255×255)
        P = Permutations(n).random_element().to_matrix()
        # 生成随机的可逆矩阵 S (32×32)
        S = random_matrix(self.F, n - k, n - k)
        while S.det() == 0:  # 确保S可逆
            S = random_matrix(self.F, n - k, n - k)
            # 公钥: Pub = S * H * P
        Pub = S * H * P
        # 私钥: (S, H, P)
        return Pub, (S, H, P)

    def encrypt(self, msg):
        # 将消息向量转换为GF(2^8)上的向量
        e = vector(self.F, [self.F._cache.fetch_int(x) for x in msg])       # 将普通整数转换为 GF(2⁸) 中的元素后 用fetch_int(x) 将整数x映射为GF(2⁸)中的对应元素
        # 加密: cipher = Pub * e = S * H * P * e
        return self.pub * e

    # 设置GRS码参数: n=255, k=223, 可纠正t=16个错误
    n, k = 255, 223
    # 创建Niederreiter加密器实例
    encryptor = Niederreiter_Cryptosystem(n, k)

    # 生成错误向量作为"密钥":
    # - 前16个位置是随机字节(1-255)
    # - 其余239个位置是0
    key = ([random.getrandbits(8) for _ in range(encryptor.get_recover_ability())]          # 循环16次每次生成一个随机的 0~255 整数
           + [0] * (
                n - encryptor.get_recover_ability()))       # 加 [0] * (255 - 16)
    # 随机打乱错误向量的位置
    random.shuffle(key)

    # Niederreiter加密: 用公钥加密错误向量
    # cipher = Pub * key = S * H * P * key
    cipher = encryptor.encrypt(key)

    # 获取私钥组件
    S, H, P = encryptor.get_key()

    # 用错误向量派生AES密钥:
    # 1. 将key列表转换为字符串
    # 2. 计算SHA256哈希
    # 3. 得到32字节的AES密钥
    key = hashlib.sha256(str(key).encode()).digest()

    # 使用AES-ECB模式加密flag
    aes = AES.new(key, AES.MODE_ECB)
    c = aes.encrypt(pad(flag, 16))

    # 输出加密结果
    with open('output.txt', 'w') as file:
        file.write('encrypted key: ' + str(cipher) + '\n')  # Niederreiter加密结果
        file.write('S: ' + str(S.list()) + '\n')  # 私钥组件S
        file.write('P: ' + str(P.list()) + '\n')  # 私钥组件P
        file.write('encrypted flag: ' + str(c))  # AES加密的flag



