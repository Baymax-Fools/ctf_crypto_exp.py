import math
from Cryptodome.Util.number import long_to_bytes

e = 65537
n = 131597024257614620869648421307952022599943625170798058722475560465555374754170467986433278540604131619940641178519954230167502146438244308999511105433219427638803460889093328223802388178143540560813587991639442439109510325931982801296494725966519902673302205827914999084293810023067168509012158443748031939483
c = 1968659140793648429069472000786965200510587960406184785982668854732724642287423003255222009970017202179772168410459767605874195614574533370563277818681668876342943583147204497260995173839443989636764614809399895977498001560095317260220383552929292480197409615426208803132661827666690467265686165715909909838
p = 11516500417019426723367143367023721121114237031914370279724222540748204265234478123246834079895657926608151549574717796604640363281423933511518846958827933
q = 11426824077836755495280357054790333684863938044257704528662235024002507215836880134548286374738252595545758498922210216905258406873430274217501038930995351

# Calculate p-1 and q-1
# 因为gcd(e,phi)!=1 且gcd(e,p-1) = e gcd(e,q-1) = e 所以尝试(p-1)在//e之后的值是否还和e不互质
p1 = p - 1
q1 = q - 1

M_p = p1 // e
M_q = q1 // e

if math.gcd(e, M_p) != 1 or math.gcd(e, M_q) != 1:
    print("Error: gcd(e, M_p) or gcd(e, M_q) is not 1. Need alternative method.")
    exit(1)

# 既然不互质了，那么在这个情况下就有 e在M_p/M_q 下有逆元
# 同时 我们有e * d_p ≡ 1 (mod M_p) 即 e * d_p = 1 + k * M_p k可以被找到
d_p = pow(e, -1, M_p)
d_q = pow(e, -1, M_q)

# x0_p/q 只是与解有关的一个值
# 实际上 x0_p^e ≡ (c^d_p)^e ≡ c^(e * d_p) ≡ c^(1 + k * M_p) ≡ c * c^(k * M_p) (mod p)
# 我们可以设 g = c^M_p
# 又因为有 M_p = p1 // e 所以我们有 g^e ≡ c^(M_p * e) ≡ c^(p-1) ≡ 1 (mod p) 所以g是一个某次单位根

'''
我们在求解x0_p/x0_q的同时就是在求m可能的一个值
因为 c=pow(m,e,n) 而 c=pow(m,e,p(q)) 求解出可能的m作为候选 再选出真正的m
正常来说 rsa的加密是:
n=p*q c=pow(m,e,n) m是明文 c是密文 而解密需要求phi=(p-1)(q-1),and gcd(e,phi)=1 and d=pow(e,-1,phi) and m=pow(c,d,n)
而这里gcd(e,phi)!=1 所以无法求出d
'''

x0_p = pow(c, d_p, p)
x0_q = pow(c, d_q, q)

# 找到各自的单位根 w 使得 w_p^e ≡ 1 (mod p)
r_p = 2
while True:
    ω_p = pow(r_p, M_p, p)
    if ω_p != 1:
        break
    r_p += 1

r_q = 2
while True:
    ω_q = pow(r_q, M_q, q)
    if ω_q != 1:
        break
    r_q += 1

# 如果x0_p是 x^e ≡ c (mod p) 的一个解 那么x0_p*w_p 也是 因为 (x0_p * ω)^e = x0_p^e * ω^e ≡ c * 1 ≡ c (mod p)
# (x0_p)^e ≡ c^(e * d_p) ≡ c^(1 + k * M_p) ≡ c * c^(k * M_p) (mod p)
# 而c^(k * M_p) ≡ (c^(M_p))^k ≡ g^k ≡ ω_p^(k * t0) 对于某个t0
# 所以(x0_p)^e ≡ c * ω_p^(k * t0) (mod p)
candidates_p = set()
for t in range(e):
    candidate_p = (x0_p * pow(ω_p, t, p)) % p
    candidates_p.add(candidate_p)

m = None

'''
根据中国剩余定理 如果 m^e ≡ c (mod p)和m^e ≡ c (mod q)
那么m^e ≡ c (mod n) 因为n = p * q
因为明文较短 所以m < min(p, q) 所以它在模p和模q下的表示就是它本身
所以我们只需要找到模p解集合和模q解集合中相同的整数值
'''

for s in range(e):
    candidate_q = (x0_q * pow(ω_q, s, q)) % q
    if candidate_q in candidates_p:
        m = candidate_q
        break

if m is None:
    print("No solution found.")
else:
    flag = long_to_bytes(m)
    print(flag.decode())