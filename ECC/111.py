class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class ell:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
    def add(self, pA, pB):
        if pA.x == pB.x and pA.y == pB.y:
            k = mod((3 * (pA.x * pA.x) + self.a), (2 * pA.y), self.p)
        else:
            k = mod((pB.y - pA.y), (pB.x - pA.x), self.p)
        rx = k * k - pA.x - pB.x
        rx = rx % self.p
        ry = k * (pA.x - rx) - pA.y
        ry = ry % self.p
        R = point(rx, ry)
        return R
    def ne(self, n, G):
        s = str(bin(n)[::-1])
        print(s)
        sumG = None
        addPoint = G
        for i in range(len(s)):
            if s[i] == '1':
                if sumG is None:
                    sumG = addPoint
                else:
                    #此处是用来计算SUMG的累加和
                    sumG = self.add(sumG, addPoint)
            #无论是0还是1都加一次
            addPoint = self.add(addPoint, addPoint)
        return sumG
def mod(a, b, p):
    # a/b mod p
    if b < 0:
        b = -b
        a = -a
    return (a % p * pow(b, p - 2, p)) % p
p = 15424654874903
a = 16546484
b = 4548674875
ep = ell(p, a, b)
G = point(6478678675, 5636379357093)
k = 546768
flag = ep.ne(k, G)
print(flag.x + flag.y)
