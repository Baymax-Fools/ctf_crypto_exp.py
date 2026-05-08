#!/usr/bin/env python3
from pwn import *
from sage.all import *
from Crypto.Util.number import *
from tqdm import trange

p = remote("node1.anna.nssctf.cn",23828)
#context.log_level = 'debug'

def ran_point():
    p.recvuntil(b'[Q]uit')
    p.sendline(b'r')
    p.recvuntil(b'E.random_point() = (')
    (x,y,_) = p.recvline().decode().strip().split(":")
    return int(x),int(y)

def get_p():
    while 1:
        x0,y0=ran_point()
        x1,y1=ran_point()
        x2,y2=ran_point()
        x3,y3=ran_point()
        x4,y4=ran_point()
        x5,y5=ran_point()
        x6,y6=ran_point()

        c0 = -(x0-x1) * ((y1**2-x1**3)-(y2**2-x2**3)) - (-(x1-x2)) * ((y0**2-x0**3)-(y1**2-x1**3)) 
        c1 = -(x1-x2) * ((y2**2-x2**3)-(y3**2-x3**3)) - (-(x2-x3)) * ((y1**2-x1**3)-(y2**2-x2**3)) 
        c2 = -(x2-x3) * ((y3**2-x3**3)-(y4**2-x4**3)) - (-(x3-x4)) * ((y2**2-x2**3)-(y3**2-x3**3)) 
        c3 = -(x3-x4) * ((y4**2-x4**3)-(y5**2-x5**3)) - (-(x4-x5)) * ((y3**2-x3**3)-(y4**2-x4**3)) 
        c4 = -(x4-x5) * ((y5**2-x5**3)-(y6**2-x6**3)) - (-(x5-x6)) * ((y4**2-x4**3)-(y5**2-x5**3)) 

        pp = gcd(c0,gcd(c1,gcd(c2,gcd(c3,c4))))
       # print(pp)
        if is_prime(pp):
            a = ((y0**2-x0**3)-(y1**2-x1**3)) * inverse((x0-x1),pp) % pp
            #print(a)
            b = y0**2-x0**3-a*x0 % pp
            #print(b)
            E = EllipticCurve(GF(pp), [a, b])
            if E.is_on_curve(x0, y0) and E.is_on_curve(x5, y5):
                return pp,a,b
                break

def G(xp,yp):
    p.recvuntil(b'[Q]uit')
    p.sendline(b'g')
    p.recvuntil(b'like x, y:')
    p.sendline((str(xp)+","+str(yp)).encode())
    p.recvuntil(b'fongi(G, H, P) = (')
    (x,y,_) = p.recvline().decode().strip().split(":")
    return x,y

i = 0
while 1:
    i += 1
    if i % 10 == 0:
        p = remote("node1.anna.nssctf.cn",23828)
    pp,a,b = get_p()
    E = EllipticCurve(GF(pp), [a, b])

    P1 = E.random_point()
    xP1, yP1 = map(ZZ, P1.xy())
    Q1 = E(G(xP1,yP1))
    R1 = E(G(xP1,pp-yP1))

    # P2
    P2 = E.random_point()
    xP2, yP2 = map(ZZ, P2.xy())
    Q2 = E(G(xP2,yP2))
    R2 = E(G(xP2,pp-yP2))
    # Might fail, try multiple times
    denom = 2 * (xP1 - xP2)
    n = E.order()
    if gcd(denom, n) != 1:
        print('Find G GG')
        continue
    G = inverse_mod(denom, n) * (Q1 + R1 - Q2 - R2)
    xG, yG = map(ZZ, G.xy())
    if gcd(yP1, n) != 1:
        print('Find H GG')
        contine
    H = inverse_mod(yP1, n) * (Q1 - xP1 * G - xG * P1)

    print(G,H)
    break

p.recvuntil(b'[Q]uit')
p.sendline(b'e')
p.recvuntil(b' = ')
c = int(p.recvline().strip().decode())

xG, yG = map(ZZ, G.xy())
xH, yH = map(ZZ, H.xy())
m = c * inverse_mod(xG * yH, pp) % pp
print(m)
print(long_to_bytes(int(m)))

p.interactive()

'''
#!/usr/bin/env sage

from Crypto.Util.number import *
from time import *
flag = open('flag.txt', 'rb').read()

import re
pattern = rb'NSSCTF\{([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\}'

match = re.search(pattern, flag)
if match:
    uuid = match.group(1).replace(b'-', b'')
    flag = uuid
else:
	print('Something wrong, tell admin.')
	exit()

def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()
	
def sc(): 
	return sys.stdin.buffer.readline()

def Ikkyu(nbit):
	p = getPrime(nbit)
	while True:
		a, b = [randint(1, p - 1) for _ in range(2)]
		E = EllipticCurve(GF(p), [a, b])
		G, H = [E.random_point() for _ in range(2)]
		try:
			I = E.lift_x(1)
		except:
			if legendre_symbol(b - a - 1, p) < 0:
				return p, E, G, H

def fongi(G, H, P):
	try:
		xG, xP, yP = G.xy()[0], P.xy()[0], P.xy()[1]
	except:
		xP = 1337
	return int(xP) * G + int(yP) * H + int(xG) * P

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, "Welcome to the Ikkyu-san challenge!! Your mission is to find the  ", border)
	pr(border, "flag with given information, have fun and good luck :)            ", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	nbit = 256
	pr(border, f'Generating parameters, please wait... ')
	p, E, G, H = Ikkyu(nbit)
	F = GF(p)
	while True:
		pr(f"{border} Options: \n{border}\t[E]ncrypted flag!\n{border}\t[R]andom point\n{border}\t[G]et Ikkyu-san point!\n{border}\t[Q]uit")
		ans = sc().decode().strip().lower()
		if ans == 'g':
			pr(border, f"Please provide your desired point `P` on elliptic curve E like x, y: ")
			xy = sc().decode()
			try:
				x, y = [F(int(_)) for _ in xy.split(',')]
				P = E(x, y)
			except:
				pr(border, f"The input you provided is not valid!")
				P = E.random_point()
			pr(border, f'{fongi(G, H, P) = }')
		elif ans == 'r':
			pr(border, f'{E.random_point() = }')
		elif ans == 'e':
			m = bytes_to_long(flag)
			assert m < p
			pr(border, f'{m * G.xy()[0] * H.xy()[1] = }')
		elif ans == 'q':
			die(border, "Quitting...")
		else:
			die(border, "Bye...")

if __name__ == '__main__':
	main()
'''