# 模板1：基础小根攻击
def basic_coppersmith(poly_func, modulus, root_bound, beta=0.4):
    """
    基础Coppersmith攻击模板
    poly_func: 多项式函数
    modulus: 大模数
    root_bound: 根的上界
    beta: 小因子比例
    """
    PR. < x > = PolynomialRing(Zmod(modulus))
    f = poly_func(x)
    f = f.monic()

    print(f"模数位数: {modulus.nbits()}")
    print(f"根上界: 2^{root_bound.nbits()}")
    print(f"使用beta: {beta}")

    roots = f.small_roots(X=root_bound, beta=beta)
    return roots


# 使用示例
N = 123456789  # 你的模数
root_bound = 2 ^ 100  # 根的上界


# 定义多项式，例如: f(x) = known + x ≡ 0 (mod p)
def my_poly(x):
    known_part = 12345
    return known_part + x


roots = basic_coppersmith(my_poly, N, root_bound, beta=0.4)
if roots:
    print(f"找到根: {roots[0]}")