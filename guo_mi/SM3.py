import binascii
from math import ceil
from .func import rotl, bytes_to_list

IV = [
    1937774191, 1226093241, 388252375, 3666478592,
    2842636476, 372324522, 3817729613, 2969243214,
]

T_j = [
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042
]

def sm3_ff_j(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret

def sm3_gg_j(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        #ret = (X | Y) & ((2 ** 32 - 1 - X) | Z)
        ret = (x & y) | ((~ x) & z)
    return ret

def sm3_p_0(x):
    return x ^ (rotl(x, 9 % 32)) ^ (rotl(x, 17 % 32))

def sm3_p_1(x):
    return x ^ (rotl(x, 15 % 32)) ^ (rotl(x, 23 % 32))

def sm3_cf(v_i, b_i):
    w = []
    for i in range(16):  # 处理16个字
        weight = 0x1000000  # 初始权重，用于按字节组合成32位字
        data = 0  # 临时存储组合成的32位字
        # 每4个字节组成一个字（大端序）
        for k in range(i * 4, (i + 1) * 4):  # 遍历当前字的4个字节
            data = data + b_i[k] * weight  # 将字节放到对应位置
            weight = int(weight / 0x100)  # 权重右移8位（除以256）
        w.append(data)  # 添加第i个字到w[0..15]

    for j in range(16, 68):  # 生成第16到第67个字
        w.append(0)  # 为了下行数组的索引安全，先添加占位元素
        w[j] = sm3_p_1(w[j - 16] ^ w[j - 9] ^ (rotl(w[j - 3], 15 % 32))) ^ (rotl(w[j - 13], 7 % 32)) ^ w[j - 6]
        str1 = "%08x" % w[j]  # 转换为十六进制字符串（可用于调试）

    w_1 = []
    for j in range(0, 64):  # 生成64个W'字
        w_1.append(0)  # 与上个循环同理
        w_1[j] = w[j] ^ w[j + 4]
        str1 = "%08x" % w_1[j]

    a, b, c, d, e, f, g, h = v_i

    for j in range(0, 64):
        ss_1 = rotl(
            ((rotl(a, 12 % 32)) +
            e +
            (rotl(T_j[j], j % 32))) & 0xffffffff, 7 % 32
        )
        ss_2 = ss_1 ^ (rotl(a, 12 % 32))

        # w和w_1是消息扩展数组，文章后面会讲
        tt_1 = (sm3_ff_j(a, b, c, j) + d + ss_2 + w_1[j]) & 0xffffffff
        tt_2 = (sm3_gg_j(e, f, g, j) + h + ss_1 + w[j]) & 0xffffffff
        d = c
        c = rotl(b, 9 % 32)
        b = a
        a = tt_1
        h = g
        g = rotl(f, 19 % 32)
        f = e
        e = sm3_p_0(tt_2)

        a, b, c, d, e, f, g, h = map(
            lambda x:x & 0xFFFFFFFF ,[a, b, c, d, e, f, g, h])
        # 将各个字寄存器保留低32位后保存

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ v_i[i] for i in range(8)]

def sm3_hash(msg):
    # print(msg)
    len1 = len(msg)     # 计算msg的字节长
    reserve1 = len1 % 64    # 计算余数
    msg.append(0x80)    # 在msg后加上'0b10000000'
    # 这里有可能会产生一个问题，就是直接填充一个字节，如果要填充的k小于7的话，
    # 即 ( l + 1 ) % 512 > 448 ，不会产生影响吗：
    # 实际上，并不会有任何影响。
    # 因为消息msg是以字节的形式传入的，说明msg的bit位长度一定是8的倍数，
    # 如果是 448 长度的话，加上 1 就是449，需要填充一个模长
    # 最接近的是 440 长度的，k = (448 - (l+1)） = 7 % 512，刚好就是0x80中的后面七个'0'
    # 注：其实k的长度是能求出： k = 7 % 8

    reserve1 = reserve1 + 1 # 余数加上0x80这一个字节
    # 56-64, add 64 byte
    range_end = 56  # 剩下的8字节留给长度
    if reserve1 > range_end:    # 如果成立，说明要填充一整个模长（512bit）
        range_end = range_end + 64

    for i in range(reserve1, range_end):    # 填充字节
        msg.append(0x00)

    bit_length = (len1) * 8 # 转换为比特数
    bit_length_str = [bit_length % 0x100]   # 取最低8位
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)   # 依次取更高8位
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])

    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(sm3_cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

# 密钥派生函数
def sm3_kdf(z, klen): # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen/32)
    zin = [i for i in bytes.fromhex(z.decode('utf8'))]
    ha = ""
    for i in range(rcnt):
        msg = zin  + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        ha = ha + sm3_hash(msg)
        ct += 1
    return ha[0: klen * 2]
