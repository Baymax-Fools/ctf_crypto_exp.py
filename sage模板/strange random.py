# Sage 专用：修正版（处理 Sage Integer，筛选 flag{ 样式）
from math import gcd
from sage.all import GF, PolynomialRing, ZZ

# ---------- 参数 ----------
p = 12011525995131123638856398628790616238390819143793715067681777677580672053939178969642750241560824301330637775350150164841002624342957867201046659270774321
q = 11559848036543977536618779383354527465877210952129546017550474513248166778543016507802003102239650062697089674048694142164127142205998713709908639891913279
r = 9919453136128731180353641658512944982390490473148116116167240081761821921209706702557854609203013856416413229743185775260680051404176535062813533001453029
e = 1297450108
c = 254437839234710932548963084800696912447199841209292016504026652383142017227876963989808065988983617626350151358444895183944611290313513729505521630711812174923796964838915751672967332321515720258149777206328112312514688748335753179198631177743199829645308091442800427146012476434191025450662950787631144984158609948536064605299987908223963902731920237033619141863042816600729594847568654431928343565350409273886054122366132475796004834811862120850908513978375240

n = p * q * r

g_p = gcd(e, p - 1)  # 436
g_q = gcd(e, q - 1)  # 2
g_r = gcd(e, r - 1)  # 2


# ---------- 工具 ----------
def egcd(a, b):
    '''
    拓展欧几里得 令ax*by=g 其中g=gcd(a,b)
    '''
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def modinv(a, m):
    '''
    逆模 ,,其实可以有其他方法,,比如pow,但是这里加了验证gcd是否为1
    '''
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError(f"模逆不存在: gcd({a},{m})={g}")
    return x % m


'''
接下来两个都是中国剩余 但其实可以用sympy的crt,,
'''


def crt_pair(a1, n1, a2, n2):
    g, m1, m2 = egcd(n1, n2)
    if (a1 - a2) % g != 0:
        raise ValueError("CRT 无解")
    t = ((a2 - a1) // g) * modinv(n1 // g, n2 // g) % (n2 // g)
    x = (a1 + n1 * t) % (n1 // g * n2)
    return x


def crt(list_a, list_n):
    x, m = list_a[0], list_n[0]
    for i in range(1, len(list_a)):
        x = crt_pair(x, m, list_a[i], list_n[i])
        m = m // gcd(m, list_n[i]) * list_n[i]
    return x


# 一个无敌恶心的东西来了 以下都用p来举例
# ---------- 在单个素数上处理：自动约掉 gcd，求 a_local，并在 GF(p) 上解 x^K = a_local ----------
def process_prime_sage(name, prime, e_global, c_global, initial_g):
    print(f"\n-- 处理 {name} (p={prime}) --")
    e_local = e_global // initial_g  # 相当于 e_local = e//gcd(e,p-1)
    t_local = (prime - 1) // initial_g  # 相当于 t_local = (p-1)//gcd(e,p-1)
    print(" 初始 e_local =", e_local)
    print(" 初始 t_local =", t_local)

    removed_product = 1  # 计算在除去最大公因数之后二者剩下的公因数的乘积
    while True:
        # 使e_l and t_l 再也没有公因数 使下面可以求逆模
        g = gcd(e_local, t_local)
        if g == 1:
            break
        removed_product *= g
        e_local //= g
        t_local //= g
        print("  约掉 gcd，当前 removed_product =", removed_product, " e_local =", e_local)

    # 神秘小推导：首先 我们有 e = gcd(e,p-1) × e_local × removed_product
    # 我们又有 p-1 = gcd(e,p-1) × removed_product × t_local 一个移位 我们就有了 t_local=(p-1)/(gcd(e,p-1) × removed_product)
    # 我们又有 e_local × d_local ≡ 1 (mod t_local) 等价于 e_local × d_local = 1 + k × t_local
    # 在p的情况下 我们本来要求 m^e  ≡ c(mod p) 两边同时幂上 d_local 我们就有了m^(e × d_local) ≡ c^d_local (mod p)
    # 对左边的 e × d_local = gcd(e,p-1) × removed_product × e_local × d_local = (gcd(e,p-1) × removed_product) × (1 + k × t_local) = gcd(e,p-1) × removed_product + gcd(e,p-1) × removed_product × k × t_local
    # 再代入 t_local = (p-1)/(gcd(e,p-1) × removed_product) 我们就可以得到 e × d_local = gcd(e,p-1) × removed_product + k × (p-1)
    # 我们令 K = gcd(e,p-1) × removed_product 所以 m^(e × d_local) ≡ (m ^K) * (m^(k × (p-1))) ≡ m ^K (mod p)  ......费马小定理
    # 再对右边 因为前面的 c^d_local ≡ a_local (mod p) 所以 右边等于 a_local (mod p)
    # 所以我们整个有 m^K ≡ a_local (mod p)
    d_local = modinv(e_local, t_local)
    a_local = pow(c_global % prime, d_local, prime)
    print("  计算得到 a_local (c^d mod prime)")
    K = initial_g * removed_product
    print("  总开根次数 K =", K)

    # 在有限域上求解方程x^K = a_local，得到所有m的候选根
    # GF(prime)是 Sage 中创建 "有限域"（伽罗瓦域）的函数，prime是这个域的 "阶"（元素个数）
    # 而 F表示 "模prime的有限域"，包含 0 到prime-1的所有整数，且所有运算（加、减、乘、除）都满足 "模prime" 的规则
    F = GF(prime)
    '''
    PolynomialRing(F, 'x')是 Sage 中创建 "多项式环" 的函数，其中：
    F是多项式系数所在的域(即步骤 5.1 定义的有限域);
    'x'是多项式的变量名。
    R表示 "以F中元素为系数、以x为变量的所有多项式的集合"
    我们要求解的方程x^K ≡ a_local (mod prime)可以写成多项式形式x^K - a_local = 0
    '''
    R = PolynomialRing(F, 'x')
    # 生成基本变量'x'
    x = R.gen()
    # 构造多项式方程
    poly = x ** K - F(a_local)
    # poly.roots(multiplicities=False)是 Sage 中求多项式根的方法：
    # multiplicities=False表示只返回根的值，不返回每个根的 "重数" 即根在方程中出现的次数，例如(x-2)²=0中2的重数是 2
    # roots是所有根的列表，每个元素都是有限域F中的元素，代表满足x^K ≡ a_local (mod prime)的解。
    roots = poly.roots(multiplicities=False)
    print("  在 GF(p) 上找到根数量:", len(roots))
    # 将返回的 roots（Sage 元素）转为 int
    roots_int = [int(r) for r in roots]
    return a_local, roots_int


# ---------- 主流程 ----------
a_p, roots_p = process_prime_sage("p", p, e, c, g_p)
a_q, roots_q = process_prime_sage("q", q, e, c, g_q)
a_r, roots_r = process_prime_sage("r", r, e, c, g_r)

print("\n根数量： p:", len(roots_p), " q:", len(roots_q), " r:", len(roots_r))

# ---------- CRT 组合并直接打印flag ----------
print("\n开始CRT组合寻找flag...")
count_checked = 0
flag_found = False

for rp in roots_p:
    for rq in roots_q:
        for rr in roots_r:
            count_checked += 1
            if count_checked % 1000 == 0:
                print(f"已检查 {count_checked} 个组合...")

            try:
                # 常规crt
                m_qr = crt([rq, rr], [q, r])
                m_all = crt([rp, m_qr], [p, q * r])
            except Exception as ex:
                # CRT 合并失败则跳过
                continue

            # m_all 可能是 Python int already; 确保是 int
            m_int = int(m_all)

            # 验证
            if pow(m_int, e, n) == c:
                # 转 bytes
                bytelen = (m_int.bit_length() + 7) // 8
                mb = m_int.to_bytes(bytelen, 'big')

                # 检查是否包含flag
                if b"flag{" in mb or b"FLAG{" in mb:
                    try:
                        flag_text = mb.decode('utf-8', errors='replace')
                        print(f"\n🎉 找到flag: {flag_text}")
                        flag_found = True
                        break
                    except:
                        print(f"\n🎉 找到flag (hex): {mb.hex()}")
                        flag_found = True
                        break
        if flag_found:
            break
    if flag_found:
        break

if not flag_found:
    print("\n❌ 未找到包含flag的明文")
else:
    print(f"\n总共检查了 {count_checked} 个组合")