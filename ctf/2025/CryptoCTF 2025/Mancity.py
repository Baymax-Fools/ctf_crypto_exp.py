from Crypto.Util.number import *

nbit = 256
e = 1234567891
n = 147170819334030469053514652921356515888015711942553338463409772437981228515273287953989706666936875524451626901247038180594875568558137526484665015890594045767912340169965961750130156341999306808017498374501001042628249176543370525803456692022546235595791111819909503496986338431136130272043196908119165239297
c = 77151713996168344370880352082934801122524956107256445231326053049976568087412199358725058612262271922128984783428798480191211811217854076875727477848490840660333035334309193217618178091153472265093622822195960145852562781183839474868269109313543427082414220136748700364027714272845969723750108397300867408537

def dfs(h,qh,rh):
    q_max = int(qh + '1'*(nbit-len(qh)) + '1'*nbit,2)
    q_min = int(qh + '0'*(nbit-len(qh)) + '1'*nbit,2)
    r_max = int(rh + '11'*(nbit-len(rh)//2),2)
    r_min = int(rh + "01"*(nbit-len(rh)//2),2)

    if q_max*r_max < n or r_min*q_min > n:
        return
    
    if h==nbit:
        q,r = q_max,r_max
        L = (q-1)*(r-1)
        d = inverse(e,L)
        m = pow(c,d,n)
        print(long_to_bytes(m))

    dfs(h+1,qh+"0",rh+"01")
    dfs(h+1,qh+"1",rh+"11")

dfs(1,"1","11")

'''
#!/usr/bin/env python3

from Crypto.Util.number import *
from flag import flag

def man(n):
	B = bin(n)[2:]
	M = ''
	for b in B:
		if b == '0':
			M += '01'
		else:
			M += '11'
	return int(M, 2)

def keygen(nbit):
	while True:
		p = getPrime(nbit)
		r = man(p)
		B = bin(p)[2:] + '1' * nbit
		q = int(B, 2)
		if isPrime(q) and isPrime(r):
				return q, r

nbit = 256
p, q = keygen(nbit)
m = bytes_to_long(flag)
assert m < n
e, n = 1234567891, p * q
c = pow(m, e, n)

print(f'n = {n}')
print(f'c = {c}')
'''