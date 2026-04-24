from Crypto.Util.number import long_to_bytes

def sqrt_mod_p(c, p):
    return pow(c, (p + 1) // 4, p)

def all_4th_roots_mod_prime(c, p):
    sqrt_c = sqrt_mod_p(c, p)
    roots = set()
    for y in (sqrt_c, p - sqrt_c):
        sqrt_y = sqrt_mod_p(y, p)
        roots.add(sqrt_y)
        roots.add(p - sqrt_y)
    return roots

def all_4th_roots_mod_n(c, p, q):
    roots_p = all_4th_roots_mod_prime(c, p)
    roots_q = all_4th_roots_mod_prime(c, q)
    roots = set()
    for rp in roots_p:
        for rq in roots_q:
            # CRT: x ≡ rp (mod p), x ≡ rq (mod q)
            m = (rp * q * pow(q, -1, p) + rq * p * pow(p, -1, q)) % (p * q)
            roots.add(m)
    return roots

p= 302699831725480487347550089829981026739
q= 310251127743940288608112628953056785599
c= 28029583845381569999260453148298922839265818581313820186655887999877810973600
n= 93912964160731275991567737208649464206217910463145274353396977855029009131661

# 求所有四次根
candidates = all_4th_roots_mod_n(c, p, q)

print(candidates)

for m in candidates:
    print(long_to_bytes(m))