from Crypto.Util.number import *

N = 33267160053
c = 27093363160
import gmpy2

p = 1110426212  # p % 4 = 3
q = 2995891097  # q % 4 = 3
e = 196608  # e = 3 * 2**16


def Rabin_x(p, q, c, y):
    n = p * q
    x0 = gmpy2.invert(p, q)
    x1 = gmpy2.invert(q, p)
    cs = [c]

    for i in range(y):
        ps = []
        for c2 in cs:
            r = pow(c2, (p + 1) // 4, p)
            s = pow(c2, (q + 1) // 4, q)
            x = (r * x1 * q + s * x0 * p) % n
            y = (r * x1 * q - s * x0 * p) % n
            if x not in ps:
                ps.append(x)
            if n - x not in ps:
                ps.append(n - x)
            if y not in ps:
                ps.append(y)
            if n - y not in ps:
                ps.append(n - y)
        cs = ps
    return cs


m = Rabin_x(p, q, c, 16)
for i in m:
    print(long_to_bytes(gmpy2.iroot(i, 3)[0]))