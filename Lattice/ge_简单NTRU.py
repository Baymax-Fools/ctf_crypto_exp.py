#构造格就行
h =
p =
c =

v1 = vector(ZZ, [1, h])
v2 = vector(ZZ, [0, p])
m = matrix([v1,v2]);
f, g = m.LLL()[0]
print(f, g)

#按题目推导 和ez_ntru的相同
a = f*c % p % g
m = a * inverse_mod(f, g) % g
print(bytes.fromhex(hex(m)[2:]))
