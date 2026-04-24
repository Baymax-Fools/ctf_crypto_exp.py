from Cryptodome.Util.number import *
import math
n = 145462084881728813723574366340552281785604069047381248513937024180816353963950721541845665931261230969450819680771925091152670386983240444354412170994932196142227905635227116456476835756039585419001941477905953429642459464112871080459522266599791339252614674500304621383776590313803782107531212756620796159703
e = 10463348796391625387419351013660920157452350067191419373870543363741187885528042168135531161031114295856009050029737547684735896660393845515549071092389128688718675573348847489182651631515852744312955427364280891600765444324519789452014742590962030936762237037273839906251320666705879080373711858513235704113
c = 60700608730139668338977678601901211800978306010063875269252006068222163102100346920465298044880066999492746508990629867396189713753873657197546664480233269806308415874191048149900822050054539774370134460339681949131037133783273410066318511508768512778132786573893529705068680583697574367357381635982316477364
p_q = 2456071529830122268608785635525790924856560525252760020566092363155608746534277979909142919617070274711056168120153952186905664812317049487026519113890518
# p_q = p ^ q
def fj(n: int, x: int):
    candidates = {(1, 1)}
    mask = 1
    n_low = n & mask

    for k in range(1, n.bit_length()):
        mask = (mask << 1) | 1
        n_low = n & mask
        xi = (x >> k) & 1
        options = ((0, 0), (1, 1)) if xi == 0 else ((0, 1), (1, 0))
        next_set = set()
        for (a, b) in candidates:
            for (pk, qk) in options:
                A = a | (pk << k)
                B = b | (qk << k)
                if (A * B) & mask == n_low:
                    if A <= B:
                        next_set.add((A, B))
                    else:
                        next_set.add((B, A))
        candidates = next_set

    for (p, q) in candidates:
        if p * q == n:
            return p, q

    for (p, q) in candidates:
        g = math.gcd(p, n)
        if 1 < g < n:
            return g, n // g
        g = math.gcd(q, n)
        if 1 < g < n:
            return g, n // g


p, q = fj(n, p_q)
# print(p)
# print(q)
# phi = (p - 1) * (q - 1)
# d = pow(e, -1, phi)
# m = pow(c, d, n)
# flag = long_to_bytes(m)
#
# plaintext = flag.decode()
# print(plaintext)


import itertools
"""
分解满足以下条件的n1 = a * b：
x1 = a ^ b_rev，其中b_rev是b的二进制逆序

参数:
    n1: 要分解的合数 (n1 = a * b)
    x1: 异或值 (x1 = a ^ b_rev)
    bits: 素数位数，默认为512位

返回:
    (a, b) 如果成功分解，否则返回None
"""
def factor_with_reverse_xor(n1: int, x1: int, bits: int = 512):

    # 初始化四个列表，分别存储：
    # a的低位部分, b的低位部分, a的高位部分（逆序前的）, b的高位部分（逆序前的）
    a_list, b_list, aa_list, bb_list = [0], [0], [0], [0]

    # 将x1转换为bits位二进制字符串并逆序，然后拆分为比特列表
    # x1 = a ^ b_rev，其中b_rev是b的二进制逆序
    x1_bits = [int(x) for x in f'{x1:0{bits}b}'[::-1]]

    cur_mod = 1  # 当前模数，用于检查乘积的低位
    for i in range(bits // 2):  # 需要bits//2轮，每轮处理2位（低位和高位）
        cur_mod *= 2  # 每轮模数翻倍：2, 4, 8, ..., 2^bits

        # 存储下一轮候选值
        nxt_as, nxt_bs, nxt_aas, nxt_bbs = [], [], [], []

        # 遍历当前所有候选
        for al, bl, a2, b2 in zip(a_list, b_list, aa_list, bb_list):
            # 尝试当前轮次所有可能的比特组合：ah, bh, ah2, bh2 各取0或1
            for ah, bh, ah2, bh2 in itertools.product([0, 1], repeat=4):
                # 更新各部分的当前值
                aa = ah * (cur_mod // 2) + al  # a的低位当前值
                bb = bh * (cur_mod // 2) + bl  # b的低位当前值
                aa2 = ah2 * (cur_mod // 2) + a2  # a的高位当前值（逆序前）
                bb2 = bh2 * (cur_mod // 2) + b2  # b的高位当前值（逆序前）

                # 计算高位部分的逆序（逆序后就是完整数的高位）
                # 注意：这里使用zfill确保总是bits位
                bb2_rev = int(f'{bb2:0{bits}b}'[::-1], 2)
                aa2_rev = int(f'{aa2:0{bits}b}'[::-1], 2)

                # 构造"估计界"掩码，用于范围剪枝
                # 格式：i+1个0 + (bits-2-2i)个1 + i+1个0
                ones_count = bits - 2 - 2 * i  # 中间1的个数
                if ones_count > 0:
                    gujie_bits = '0' * (i + 1) + '1' * ones_count + '0' * (i + 1)
                    gujie = int(gujie_bits, 2)
                else:
                    # 当ones_count为负时，使用全0掩码
                    gujie = 0

                # 关键约束条件判断：
                # 1. 乘法条件：a和b的低位乘积模当前模数必须匹配n1
                if (aa * bb % cur_mod != n1 % cur_mod):
                    continue

                # 2. XOR条件1：a的低位第i位 XOR b的高位第i位（即b的第bits-1-i位）必须等于x1的第i位
                if (ah ^ bh2) != x1_bits[i]:
                    continue

                # 3. XOR条件2：a的高位第i位（即a的第bits-1-i位） XOR b的低位第i位必须等于x1的第bits-1-i位
                if (ah2 ^ bh) != x1_bits[bits - 1 - i]:
                    continue

                # 4. 范围条件：当前估计值应在合理范围内
                # 计算当前估计的完整a和b
                a_est = aa2_rev + aa
                b_est = bb2_rev + bb

                # 下界条件：乘积必须≤n1
                if a_est * b_est > n1:
                    continue

                # 上界条件：加上掩码后的乘积必须≥n1（确保候选值不会偏离太远）
                if gujie > 0 and (a_est + gujie) * (b_est + gujie) < n1:
                    continue

                # 剪枝：如果候选数过多，可以限制数量
                # 这里简单限制每个列表最多保存1000个候选
                if len(nxt_as) < 1000:
                    nxt_as.append(aa)
                    nxt_bs.append(bb)
                    nxt_aas.append(aa2)
                    nxt_bbs.append(bb2)

        # 如果没有候选，提前返回失败
        if not nxt_as:
            return None

        # 更新当前候选列表
        a_list, b_list, aa_list, bb_list = nxt_as, nxt_bs, nxt_aas, nxt_bbs

    # 遍历所有最终候选，组合高低位并验证
    for a_low, b_low, a_high, b_high in zip(a_list, b_list, aa_list, bb_list):
        # 将高位部分逆序，得到完整数的高位
        a_high_rev = int(f'{a_high:0{bits}b}'[::-1], 2)
        b_high_rev = int(f'{b_high:0{bits}b}'[::-1], 2)

        # 组合高低位得到完整的a和b
        a_final = a_high_rev + a_low
        b_final = b_high_rev + b_low

        # 验证乘积是否正确
        if a_final * b_final == n1:
            # 可选：验证逆序XOR条件
            b_rev_check = int(f'{b_final:0{bits}b}'[::-1], 2)
            if (a_final ^ b_rev_check) == x1:
                return a_final, b_final

    return None