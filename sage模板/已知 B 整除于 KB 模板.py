# 模板3：类似flag题目的情况 (已知 B | KB)
def flag_style_attack(A, KB, k, C, m_bits):
    """
    类似我们flag题目的攻击模板
    A + k*m ≡ C (mod B), 且 B | KB
    """
    PR. < m > = PolynomialRing(Zmod(KB))
    f = A + k * m - C
    f = f.monic()

    root_bound = 2 ^ m_bits
    # 估计beta: 假设B大约是KB的一半大小
    beta = 0.4

    print(f"KB位数: {KB.nbits()}")
    print(f"m位数上界: {m_bits}")

    roots = f.small_roots(X=root_bound, beta=beta)

    if roots:
        m_found = roots[0]
        # 恢复B
        B = gcd(int(f(m_found)), KB)
        return m_found, B
    return None, None


# 使用示例（类似我们的题目）
A = 49327528147956...  # 你的A
KB = pow(2, 2023) - leak  # 你的KB
k = 2023
C = 2022
m_bits = 200  # m小于200位

m, B = flag_style_attack(A, KB, k, C, m_bits)
if m:
    print(f"找到m: {m}")
    print(f"找到B: {B}")

    # 转换为flag
    flag1 = bytes.fromhex(hex(int(m))[2:])
    flag2 = bytes.fromhex(hex(int(B))[2:])
    print(f"Flag1: {flag1}")
    print(f"Flag2: {flag2}")