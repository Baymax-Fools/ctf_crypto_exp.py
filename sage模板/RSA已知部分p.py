# 模板2：RSA已知p的高位或低位
def rsa_partial_p(N, known_part, unknown_bits, is_high_bits=True):
    """
    RSA部分p已知攻击
    N: RSA模数
    known_part: p的已知部分
    unknown_bits: 未知部分的位数
    is_high_bits: True=已知高位, False=已知低位
    """
    PR. < x > = PolynomialRing(Zmod(N))

    if is_high_bits:
        # p = known_part * 2^unknown_bits + x
        f = known_part * (2 ^ unknown_bits) + x
    else:
        # p = x * 2^(known_bits) + known_part
        f = x * (2 ^ (known_part.nbits())) + known_part

    f = f.monic()

    root_bound = 2 ^ unknown_bits
    beta = 0.5  # 对于标准RSA

    print(f"攻击RSA: N={N.nbits()}位, 未知部分={unknown_bits}位")

    roots = f.small_roots(X=root_bound, beta=beta)
    return roots


# 使用示例
N = 0xabcdef...  # 你的RSA N
known_p_part = 0x123456...  # p的已知部分
unknown_bits = 100  # 未知位数

roots = rsa_partial_p(N, known_p_part, unknown_bits, is_high_bits=True)
if roots:
    x = roots[0]
    if is_high_bits:
        p = known_p_part * (2 ^ unknown_bits) + x
    else:
        p = x * (2 ^ known_p_part.nbits()) + known_p_part

    if N % p == 0:
        print(f"分解成功! p = {p}")
        q = N // p
        print(f"q = {q}")