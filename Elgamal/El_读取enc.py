import msgpack
import sys

sys.setrecursionlimit(10000)

def egcd(a, b):
    if b > a:
        a, b = b, a
    if a % b == 0:
        return (b, 0, 1)
    else:
        (d, x, y) = egcd(b, (a - b * (a // b)))
        return (d, y, x - y * (a // b))


def modinv(a, N):
    (d, x, y) = egcd(N, a)
    assert d == 1
    return y % N


def npow(a, b):
    global N
    ret = 1
    if b != 0:
        if b < 0:
            ret *= modinv(pow(a, -b, N), N)
        else:
            ret *= pow(a, b, N)
    return ret


N = 23927411014020695772934916764953661641310148480977056645255098192491740356525240675906285700516357578929940114553700976167969964364149615226568689224228028461686617293534115788779955597877965044570493457567420874741357186596425753667455266870402154552439899664446413632716747644854897551940777512522044907132864905644212655387223302410896871080751768224091760934209917984213585513510597619708797688705876805464880105797829380326559399723048092175492203894468752718008631464599810632513162129223356467602508095356584405555329096159917957389834381018137378015593755767450675441331998683799788355179363368220408879117131

with open(r'F:\download\CTF\7a407f44a073442c91fd395b20594f01\msg.enc', 'rb') as f:
    msg_enc = f.read()

with open(r'F:\download\CTF\7a407f44a073442c91fd395b20594f01\msg.txt', 'r', encoding='utf-8') as f:
    msg_plain = f.read()

m = []
for i in range(0, len(msg_plain), 256):
    ms = msg_plain[i:i + 256]
    # 将字符串转换为字节然后转换为十六进制整数
    hex_val = ms.encode('utf-8').hex()
    m.append(int(hex_val, 16))

print('m:', m, len(m))

r = []
c = []
# 使用 strict_map_key=False 避免键类型检查问题

unpacked_data = msgpack.unpackb(msg_enc, strict_map_key=False, raw=True)
for r_s, c_s in unpacked_data:
    # 确保处理的是字节数据
    r.append(int(r_s.hex(), 16) if isinstance(r_s, bytes) else int(r_s))
    c.append(int(c_s.hex(), 16) if isinstance(c_s, bytes) else int(c_s))

print('r:', r, len(r))
print('c:', c, len(c))

if len(r) >= 2 and len(m) >= 2:
    _, a, b = egcd(r[0], r[1])
    k1 = (modinv(m[0], N) * c[0]) % N
    k2 = (modinv(m[1], N) * c[1]) % N
    k = npow(k1, a) * npow(k2, b) % N
    print('k:', k)

    with open(r"F:\download\CTF\7a407f44a073442c91fd395b20594f01\flag.enc", "rb") as f:
        flag_data = f.read()

    flag_unpacked = msgpack.unpackb(flag_data, strict_map_key=False, raw=True)
    r3 = int(flag_unpacked[0][0].hex(), 16) if isinstance(flag_unpacked[0][0], bytes) else flag_unpacked[0][0]
    c3 = int(flag_unpacked[0][1].hex(), 16) if isinstance(flag_unpacked[0][1], bytes) else flag_unpacked[0][1]

    m3 = (c3 * pow(modinv(k, N), r3, N)) % N

    hex_str = hex(m3)[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str

    try:
        result = bytes.fromhex(hex_str).decode('utf-8')
        print("解密结果:", result)
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试其他编码或显示原始字节
        result_bytes = bytes.fromhex(hex_str)
        print("原始字节:", result_bytes)
        # 尝试latin-1编码（不会失败）
        result = result_bytes.decode('latin-1')
        print("解密结果(latin-1):", result)
else:
    print("错误：需要至少2组明密文对")