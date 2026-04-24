import libnum

M = isqrt(n0)
L = matrix(ZZ,[
    [M,e0,e1,e2,e3],
    [0,-n0,0,0,0],
    [0,0,-n1,0,0],
    [0,0,0,-n2,0],
    [0,0,0,0,-n3],])

d_M  = L.LLL()[0][0]
d = d_M // M
m = power_mod(c0,d,n0)
print(libnum.n2s(int(m)))
# b'NSSCTF{12514adb-2c14-4777-96ff-90e95bc2b5cb}'
