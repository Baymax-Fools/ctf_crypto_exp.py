#!/usr/bin/env python3
from pwn import *

HOST = "challs.umdctf.io"
PORT = 32767

context.log_level = "info"

# RSA 公钥参数
n = 89496838321330017124211425752928111009238414395285545597372895783391482460166014550795440784240669454038164776392492949832230406030665778241454645944939829559549747525412818621247626093163657213524408194055221128159991890855776297338418179985226639927931716465641085590302394062423554511419578835789906477703
e = 65537

# 已知 flag 的密文 ct = flag^e mod n
ct = 7754782549233547741892262011884269269634473224225227064848605234096464292342695844400918832869742989785685496372442722948589824059885664742180188925993430350247652395812127146595142859972102395302095473677093880196683037670451512853001503582104512714892761518926915267957380484576367984853786495267989619184

# 服务端判断：
# pt = hex(m)
# if pt.startswith("0x67"):
#     触发报错
#
# 所以命中条件是：解密出来的整数 m 的十六进制最高字节是 0x67
# 若总 hex 长度固定为 256 位（不含 0x），那么满足：
#   A <= m < B
# 其中：
#   A = 0x67 * 16^254
#   B = 0x68 * 16^254
A = 103 * 16**254
B = 104 * 16**254

# 已知 flag 的前缀和总长度 这个111的长度应该是wp的作者通过测试得到flag后，直接设置为111长度的
# 所以初始时可以把 flag 限定在 [L, U) 这个整数区间里
PREFIX = b"UMDCTF{"
FLAG_LEN = 111

# 经验参数：
# ALPHA 用来控制 s_target 的大小
# 它不是严格数学常数，而是命中率 / 收缩效率之间的折中参数
ALPHA = 16

# 每轮在候选 s 区间里先粗采样 32 个点
NUM_SAMPLES = 32

# 如果一个都没命中，再更密一点采样 48 个点
DENSE_SAMPLES = 48

# 最多做多少轮 batch
MAX_BATCHES = 220


def connect():
    p = remote(HOST, PORT)
    p.recvuntil(b"Your messages:")
    return p


def query_batch(p, s_values):
    """
    一次性测试多个 s 值。

    对于每个 s，我们发送：
        ct' = ct * s^e mod n

    因为 RSA 乘法同态：
        Dec(ct') = Dec(ct) * Dec(s^e) mod n
                 = flag * s mod n

    服务端实际上在检查：
        hex(flag * s mod n).startswith("0x67")
    """

    # 把多个变形后的密文用逗号拼起来，一次发给服务端
    payload = ",".join(str((ct * pow(s, e, n)) % n) for s in s_values)
    p.sendline(payload.encode())

    # 服务端会对每个输入给一行响应，最后再次打印 "Your messages:"
    text = p.recvuntil(b"Your messages:", drop=False).decode(errors="replace")

    responses = []
    for line in text.splitlines():
        # 如果命中，服务端返回报错
        if "ERROR: BRAINROT DETECTED" in line:
            responses.append(True)

        # 否则表示没有命中
        elif "thanks you for your message" in line:
            responses.append(False)

    # 只保留那些命中的 s
    return [s for s, ok in zip(s_values, responses) if ok]


def to_bytes(x):
    """
    把整数转回字节串。
    """
    hx = hex(x)[2:]
    if len(hx) % 2:
        hx = "0" + hx
    return bytes.fromhex(hx)


# ========================
# 主逻辑（基本不变）
# ========================

def main():
    # prefix_int 是前缀 "UMDCTF{" 对应的大整数
    prefix_int = int.from_bytes(PREFIX, "big")

    # 构造初始区间 [L, U)
    #
    # L: 前缀固定，后面全补 0x00
    # U: 相当于"前缀 + 1"，后面全补 0x00
    #
    # 因此所有以 PREFIX 开头、总长为 FLAG_LEN 的字符串，
    # 转成整数后都会落在 [L, U) 中
    L = prefix_int * 256 ** (FLAG_LEN - len(PREFIX))
    U = (prefix_int + 1) * 256 ** (FLAG_LEN - len(PREFIX))

    # 建立远程连接
    p = connect()

    # 进行多轮区间收缩
    for batch in range(1, MAX_BATCHES + 1):
        # 当前 flag 仍可能落在 [L, U)
        width = U - L

        # 如果区间宽度已经 <= 1，说明基本定位完成
        if width <= 1:
            break

        # 用中点近似真实 flag
        mid = (L + U) // 2

        # 选择一个"理想量级"的 s
        #
        # 设计思路：
        #   希望当前候选区间 [L, U) 乘上 s 后，
        #   宽度约为 ALPHA * (B - A)
        #
        # 即：
        #   s * (U - L) ≈ ALPHA * (B - A)
        #
        # 解得：
        #   s ≈ ALPHA * (B - A) / width
        #
        # 而这里 B - A = 16^254
        s_target = ALPHA * 16**254 // width

        # 估计对应的 k
        #
        # 命中时满足：
        #   A <= flag*s - k*n < B
        #
        # 即：
        #   flag*s ≈ k*n
        #
        # 因为 flag 不知道，就用 mid 近似：
        #   mid*s ≈ k*n
        #   k ≈ mid*s / n
        #
        # 取最近整数
        k = round(s_target * mid / n)

        # 对于固定的 k，希望存在某个 flag ∈ [L, U) 使得：
        #   A <= flag*s - k*n < B
        #
        # 改写为：
        #   k*n + A <= flag*s < k*n + B
        #
        # 又因为 flag ∈ [L, U)，所以 flag*s ∈ [L*s, U*s)
        #
        # 要让这两个区间有交集，需要 s 落在某个范围 [s_lo, s_hi]
        # 这就是下面两个式子
        s_lo = (k * n + A + U - 1) // U # 向上取整
        s_hi = (k * n + B - 1) // L # 向下取整

        # 如果范围为空，说明当前估计出的 k 不合理
        if s_hi < s_lo:
            raise RuntimeError(f"empty s-interval at batch {batch}")

        # 候选 s 区间总长度
        total = s_hi - s_lo

        # 在 [s_lo, s_hi] 中均匀采样 NUM_SAMPLES 个点
        #
        # 注意这不是枚举所有 s，只是抽样测试
        s_values = [s_lo + (total * i) // (NUM_SAMPLES - 1) for i in range(NUM_SAMPLES)]

        try:
            # 批量测试这些 s，看看哪些会触发 oracle
            hits = query_batch(p, s_values)
        except EOFError:
            # 远程有时会断连，重连后继续
            log.warning("reconnecting...")
            p.close()
            p = connect()
            hits = query_batch(p, s_values)

        # 如果粗采样一个都没中，就更密一点再试一次
        if not hits:
            s_values = [s_lo + (total * i) // (DENSE_SAMPLES - 1) for i in range(DENSE_SAMPLES)]

            try:
                hits = query_batch(p, s_values)
            except EOFError:
                log.warning("reconnecting...")
                p.close()
                p = connect()
                hits = query_batch(p, s_values)

        # 如果还是一个命中都没有，说明这一轮策略失败
        if not hits:
            raise RuntimeError(f"no positive hits at batch {batch}")

        # ========================
        # 利用命中的 s 收缩区间
        # ========================
        #
        # 对每个命中的 s，都有：
        #   A <= flag*s - k*n < B
        #
        # 于是可推出：
        #   (k*n + A)/s <= flag < (k*n + B)/s
        #
        # 再和原区间 [L, U) 取交，得到更小的新范围
        for s in hits:
            # 这里重新估计 k
            #
            # 因为真实 flag >= L，所以：
            #   k = floor(flag*s / n)
            # 至少可以先用 floor(L*s / n) 作为对应分支
            #
            # 这一步是题解/脚本里的经验写法。
            k = (s * L) // n

            # 从
            #   flag >= (k*n + A)/s
            # 得到下界，注意要向上取整
            new_L = max(L, (k * n + A + s - 1) // s)

            # 从
            #   flag < (k*n + B)/s
            # 得到上界
            #
            # 这里写成：
            #   floor((k*n + B - 1)/s) + 1
            # 是为了保持区间仍然是左闭右开 [new_L, new_U)
            new_U = min(U, (k * n + B - 1) // s + 1)

            # 如果新区间空了，说明哪步估计出了问题
            if not (new_L < new_U):
                raise RuntimeError("interval collapsed")

            # 更新当前区间
            L, U = new_L, new_U

        # 定期打印当前进度
        if batch == 1 or batch % 5 == 0:
            log.info(f"batch={batch} hits={len(hits)} bits={(U - L).bit_length()}")

    p.close()

    # 最后区间已经很小
    log.success(f"final width = {U - L}")
    log.success(f"final bits  = {(U - L).bit_length()}")

    # 在最终区间里暴力枚举，找出真正满足 m^e mod n = ct 的那个 m
    print(f'[L,U) = [{L},{U})')
    for m in range(L, U):
        if pow(m, e, n) == ct:
            flag = to_bytes(m)
            log.success(f"FLAG = {flag.decode()}")
            return

    log.error("flag not found")
    exit(1)


if __name__ == "__main__":
    main()

'''
#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long 
from secret_parameters import d, flag_bytes

# n has been specifically selected to not contain the forbidden two digit sequence.
n = 89496838321330017124211425752928111009238414395285545597372895783391482460166014550795440784240669454038164776392492949832230406030665778241454645944939829559549747525412818621247626093163657213524408194055221128159991890855776297338418179985226639927931716465641085590302394062423554511419578835789906477703 
e = 65537

flag = bytes_to_long(flag_bytes)
assert flag < n
ct = pow(flag, e, n)

print(f"Your flag: {ct}")

print("Send an encrypted message to the UMDCTF organizers!")
print("WARNING: ALL MESSAGES WILL BE SCANNED FOR SIGNS OF POTENTIAL BRAINROT ACTIVITY.")

while True:
    user_inputs = input("Your messages: ").split(',')
    for user_ct in user_inputs:
        user_ct = int(user_ct)
        if user_ct >= n or user_ct < 0:
            print("Erm that's not a valid message")
            exit()

        pt = hex(pow(user_ct, d, n))

        if pt.startswith("0x67"):
            print("ERROR: BRAINROT DETECTED. THIS INCIDENT WILL BE REPORTED.")
        else:
            print("The UMDCTF team thanks you for your message!")
        print()

'''