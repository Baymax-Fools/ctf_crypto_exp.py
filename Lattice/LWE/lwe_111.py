from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler
from sage.crypto.lwe import LWE, samples

p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
m,n = 32*4,77
esz = 2**64
F = GF(p)
V = VectorSpace(F,n)
D = DiscreteGaussianDistributionIntegerSampler(esz)

#gen private_key s
lwe = LWE(n=n, q=p, D=D)
s = lwe._LWE__s
print(s)


#primal_attack1
def primal_attack1(A,b,m,n,p,esz):
    L = block_matrix(
        [
            [matrix.identity(m)*p,matrix.zero(m, n+1)],
            [(matrix(A).T).stack(-vector(b)).change_ring(ZZ),matrix.identity(n+1)],
        ]
    )
    #print(L.dimensions())
    Q = diagonal_matrix([p//esz]*m + [1]*n + [p])
    L *= Q
    L = L.LLL()
    L /= Q
    for res in L:
        if(res[-1] == 1):
            s = vector(GF(p), res[-n-1:-1])
            return s
        elif(res[-1] == -1):
            s = -vector(GF(p), res[-n-1:-1])
            return s


#primal_attack2
def primal_attack2(A,b,m,n,p,esz):
    L = block_matrix(
        [
            [matrix(Zmod(p), A).T.echelon_form().change_ring(ZZ), 0],
            [matrix.zero(m - n, n).augment(matrix.identity(m - n) * p), 0],
            [matrix(ZZ, b), 1],
        ]
    )
    #print(L.dimensions())
    Q = diagonal_matrix([1]*m + [esz])
    L *= Q
    L = L.LLL()
    L /= Q
    res = L[0]
    if(res[-1] == 1):
        e = vector(GF(p), res[:m])
    elif(res[-1] == -1):
        e = -vector(GF(p), res[:m])
    s = matrix(Zmod(p), A).solve_right((vector(Zmod(p), b)-e))
    return s


#dual_attack1
def Dual_attack1(A,b,m,n,p):
    ker = Matrix(GF(p),A).left_kernel().basis()
    T = block_matrix(
        [
            [Matrix(ZZ,ker)],
            [identity_matrix(m)*p]
        ]
    )
    #print(T.dimensions())
    res = Matrix(ZZ,T).BKZ()[m-n]
    u = vector(GF(p),res)
    ub = u*vector(GF(p),b)
    if(ub > p//2):
        ub = p - ub
    #print(int(ub).bit_length())
    if(int(ub).bit_length() < int(p).bit_length()-5):
        return True
    else:
        return False


#dual_attack2
def Dual_attack2(A,b,m,n,p):
    ker = Matrix(GF(p),A).left_kernel().basis()
    T = block_matrix(
        [
            [Matrix(GF(p),ker).echelon_form().change_ring(ZZ)],
            [matrix.zero(n, m-n).augment(matrix.identity(n) * p)]
        ]
    )
    #print(T.dimensions())
    res = Matrix(ZZ,T).BKZ()[0]
    u = vector(GF(p),res)
    ub = u*vector(GF(p),b)
    if(ub > p//2):
        ub = p - ub
    print(int(ub).bit_length())
    if(int(ub).bit_length() < int(p).bit_length()-5):
        return True
    else:
        return False



#gen sample(LWE or random)
sample = list(zip(*samples(m=m, n=n, lwe=lwe)))
#sample = list(zip(*[[V.random_element(),(F.random_element())] for _ in range(m)]))
A,b = sample


#test
#print(primal_attack1(A,b,m,n,p,esz))
#print(primal_attack2(A,b,m,n,p,esz))
#print(Dual_attack1(A,b,m,n,p))
#print(Dual_attack2(A,b,m,n,p))