from libnum import primes
from sympy.ntheory.modular import crt
from sympy import primerange
from Crypto.Util.number import long_to_bytes

primes = list(primerange(2,114514))

c = [1, 2, 2, 4, 0, 2, 11, 11, 8, 23, 1, 30, 35, 0, 18, 30, 55, 60, 29, 42, 8, 13, 49, 11, 69, 26, 8, 73, 84, 67, 100, 9, 77, 72, 127, 49, 57, 74, 70, 129, 146, 45, 35, 180, 196, 101, 100, 146, 100, 194, 2, 161, 35, 155]

moduli = primes[:len(c)]

n,_ = crt(moduli,c)

print(n)
print(long_to_bytes(n))


