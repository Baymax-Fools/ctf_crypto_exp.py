from Crypto.PublicKey import RSA

# 读取私钥
with open(r'F:\download\CTF\202012CRYPTO_PolarDN_CTF_BabyRSA\private.key', 'r') as f:
    key = RSA.import_key(f.read())

print("Modulus:", key.n)
print("Public Exponent:", key.e)
print("Private Exponent:", key.d)
print("Prime p:", key.p)
print("Prime q:", key.q)