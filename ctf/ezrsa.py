from Crypto.Util.number import *
import itertools

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


nbits = 512
n = 113811568965055236591575124486758679392744553312134148909105203346767338399571149835776281246434662598568061596388663253038256689345299177200416663539845688277447346395189677568405388952270634599590543939397457325519084988358577805564978282375882831765408646889940777372958745826393653515323881370943911243589
e = 65537
c = 28637971616659975415203771281328378878549288421921080859079174552593926682380791394169267513651195690175911968893108214839850128311436983081661719981958725955998997347063633351893769712863719014753154993940174947685060864532241899917269380408066913133029163844049218414849768354727966161277243216291473824377
hint = 157624334507300300837306007943988438905196981213124202656160912356046979618961372023595598201180149465610337965346427263713514476892241848899142885213492

p,q = factor_with_reverse_xor(n, hint, nbits)
# print(isPrime(p))
# print(isPrime(q))
# print(n == p*q)

L = (p-1) *(q-1)
d = inverse(e,L)
m = pow(c,d,n)
print(long_to_bytes(m))
