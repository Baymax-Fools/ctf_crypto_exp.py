import gmpy2
from Crypto.Util.number import *

data=[259574080588277578527410299002867735023798216356763871244908783144610527451187, 954408432127642232121971189554605898975195279656270435479524132958262607464595, 902461413507524665418054778947872375987908929501605791883614896110219051835312, 92554599789649828855418140915311664257163346975111310560999959858873425332254]
n=1000081851369905197391900354119969103949357074708517572641608490670646955240669
value = "Welcome to HGAME 2026!"
mask = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
x = (ord(value[0]) << 7) & mask
print(x)
for c in value:
    print(c,ord(c))
print(mask,mask.bit_length())

length = len(value)
print(length)
x ^= length & mask
print(x)

x1,x2,x3,x4 = data
# pow(x3**2-x2**2,-1,n)
y = pow((x3-x2)*(pow(x3**2-x2**2,-1,n))*(x2**2-x1**2)-(x2-x1),-1,n)
b = (y*((x4-x3)*(pow(x3**2-x2**2,-1,n))*(x2**2-x1**2) - (x3-x2))) % n
a = (((x4-x3)-b*(x3-x2))*pow(x3**2-x2**2,-1,n)) % n
c = (x4-a*x3**2-b*x3) % n
# print(x2 == (a*x1**2+b*x1+c)%n)
# print(x3 == (a*x2**2+b*x2+c)%n)
# print(x4 == (a*x3**2+b*x3+c)%n)

def mod_sqrt_prime(a, p):
    """求模素数p的平方根，返回列表（可能为空）。"""
    if p == 2:
        return [a % 2]
    if a % p == 0:
        return [0]
    if pow(a, (p - 1) // 2, p) != 1:
        return []
    if p % 4 == 3:
        res = pow(a, (p + 1) // 4, p)
        return [res, p - res]
    # Tonelli-Shanks算法
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    x = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        i = 1
        while pow(t, 2**i, p) != 1:
            i += 1
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
    return [x, p - x]

D = (b**2 - 4 * a * (c - x1)) % n
sqrt_list = mod_sqrt_prime(D, n)  # 假设n是素数
solutions = []
for sqrt_D in sqrt_list:
    try:
        inv_2a = pow(2 * a, -1, n)  # 2a的模逆元
        h1 = (-b + sqrt_D) * inv_2a % n
        h2 = (-b - sqrt_D) * inv_2a % n
        if (a * h1**2 + b * h1 + c) % n == x1:
            solutions.append(h1)
        if (a * h2**2 + b * h2 + c) % n == x1:
            solutions.append(h2)
    except Exception as e:
        # 2a可能没有逆元，需要特殊处理
        print(f"2a没有逆元: {e}")
        # 可以考虑将二次方程乘以4a，转化为完全平方形式
        # (2a h + b)^2 ≡ D (mod n)
        # 然后直接求解 2a h + b ≡ sqrt(D) mod n
        # 这需要解线性同余方程，可能有多解或无解
        pass

print("解集合:", set(solutions))
h1=solutions[0]
h2=solutions[1]
print((a*h1**2+b*h1+c)%n == x1)
print((a*h2**2+b*h2+c)%n == x1)

from z3 import *

# ----------------------------
# 已知数据
# ----------------------------
value = "Welcome to HGAME 2026!"
magic_word = "I get the key now!"

# 你已经求出来的 x0（填这里）
h_target = h1   # <<< 把你算出来的 x0 放这里

MASK = (1 << 256) - 1

# ----------------------------
# 建立 z3 约束
# ----------------------------
key = BitVec('key', 70)   # key < 2^70
x = BitVecVal(ord(value[0]) << 7, 256)

for c in value:
    x = (ZeroExt(256-70, key) * x) & MASK
    x = x ^ BitVecVal(ord(c), 256)

x = x ^ BitVecVal(len(value), 256)

solver = Solver()
solver.add(x == BitVecVal(h_target, 256))

print("[*] Solving key...")
assert solver.check() == sat
model = solver.model()
key_val = model[key].as_long()
print("[+] key =", key_val)

# ----------------------------
# 计算 flag
# ----------------------------
def shash(value: str, key: int) -> int:
    mask = (1 << 256) - 1
    x = (ord(value[0]) << 7) & mask
    for c in value:
        x = (key * x) & mask ^ ord(c)
    x ^= len(value)
    return x

flag = "VIDAR{" + hex(shash(magic_word, key_val))[2:] + "}"
print("[+] flag =", flag)
