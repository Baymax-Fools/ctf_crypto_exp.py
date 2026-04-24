import base64
from Crypto.Cipher import AES
import sys

def decrypt():
    # 读取base64编码的结果（从标准输入或文件）
    b64 = "3XpvaycmXO/ycXW4lFfEzkeOcA6d+JDBBBODX9AFUc6L4IX7X4kHIj51/jYDjCnYfvKDBDueCg/2PrTMQZPw2HAlcUIDXioO2HTpxAShWQH3jz3aL7dOfoqv9cLChR/+HwIjyG0lqx78kwtVv4WgCN0+V0eeg1xnA8fxC/u0Gu83Cw5AeApiuVMch4r53IM+Q4+LUyUqs1LVFCemPBXeensXZHtzYREO7gvjyvdS/NvaMLfqjNYpOeKB4bB7WKrNhsKqIS2STUjxF8w42oNWbFAZ7CBlTalYaaw6blIefyqVVNwmw2kqEE8sUjgSATEyfuZAlKghZ/kBwseH5DLRIEYbfVa/TxehxMeHPas7/3l3dhq3C6/OjUvfz0bUQoj7Kh5/KpVUpXKSLFhTi7zMk02+Rmig/0RrxAys3eQNjD3sFc2quWLkUfQpPWLZCwOFC8oPJwcobjA23LxwTxO1Cv6QIAtNFnO7"
    result = base64.b64decode(b64)
    assert len(result) == 360, "解密结果长度应为360字节"

    N = 360
    key = b"lasagna!" * 2
    cipher = AES.new(key, AES.MODE_ECB)

    # 预计算所有可打印字符的AES加密结果（16字节）
    printable = range(32, 127)  # ASCII可打印字符
    precomp = {}
    for c in printable:
        ch = chr(c)
        B = cipher.encrypt(ch.encode() * 16)
        precomp[ch] = B  # 16字节

    # 初始化flag数组（长度360）
    flag = [None] * N
    # 设置已知开头：bctf{ 每个字符重复
    known = "bctf{"
    for idx, ch in enumerate(known):
        flag[2 * idx] = ch
        flag[2 * idx + 1] = ch
    # 设置已知结尾：}
    flag[358] = '}'
    flag[359] = '}'

    # current_result 记录当前已异或的中间结果
    current_result = bytearray(N)
    # count[k] 表示还有多少个影响result[k]的字符未被赋值
    count = [16] * N

    # 处理已知字符的贡献
    known_indices = list(range(10)) + [358, 359]
    for i in known_indices:
        ch = flag[i]
        B = precomp[ch]
        for j in range(16):
            k = (i + j) % N
            current_result[k] ^= B[j]
            count[k] -= 1

    # 验证已知字符处理后，已完整的k是否匹配
    for k in range(N):
        if count[k] == 0 and current_result[k] != result[k]:
            print("初始状态不一致，请检查输入或已知flag格式")
            return

    found_flag = None
    original_len = 180

    def dfs(t):
        nonlocal found_flag
        if found_flag is not None:
            return
        if t > 178:  # 所有字符已赋值
            # 最终验证
            for k in range(N):
                if count[k] != 0 or current_result[k] != result[k]:
                    return
            original = ''.join(flag[2 * i] for i in range(original_len))
            print("Found flag:", original)
            found_flag = original
            return

        # 尝试所有可打印字符
        for ch in precomp.keys():
            i1, i2 = 2 * t, 2 * t + 1
            if flag[i1] is not None or flag[i2] is not None:
                continue  # 理论上不会发生
            B = precomp[ch]
            changes = []  # 记录修改，用于回溯
            newly_zero = []  # 新变为完整的k索引

            # 处理字符对 (i1, i2)
            for i in (i1, i2):
                for j in range(16):
                    k = (i + j) % N
                    old_count = count[k]
                    current_result[k] ^= B[j]
                    count[k] -= 1
                    changes.append((k, B[j]))
                    if old_count == 1:
                        newly_zero.append(k)

            # 检查新完整的k是否匹配
            valid = True
            for k in newly_zero:
                if current_result[k] != result[k]:
                    valid = False
                    break

            if valid:
                flag[i1] = flag[i2] = ch
                dfs(t + 1)
                if found_flag is not None:
                    return
                flag[i1] = flag[i2] = None

            # 回溯：恢复current_result和count
            for k, byte_val in reversed(changes):
                current_result[k] ^= byte_val
                count[k] += 1

    # 从第6个字符开始（索引5）
    dfs(5)

    if found_flag is None:
        print("未找到flag，请确认输入正确")

if __name__ == "__main__":
    decrypt()