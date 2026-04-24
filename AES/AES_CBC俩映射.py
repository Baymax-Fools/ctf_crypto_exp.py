from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 已知数据
IV1 = bytes.fromhex("1e5d251ea78ef68a1282079fd028c747")
IV2 = bytes.fromhex("18777ae4c1a29f4c5db8ba6c5dfe72f1")
m1 = bytes.fromhex(
    "f560fd28ed5c5ce7d952eb44b47007e702f42dbb54540dfc78467f48933dbb01ebcf520fd3d23a211d3b4e8c06261966cb178525c25b8058ff792e0f251d3d15")
c1 = bytes.fromhex(
    "caf7bc1223c17f848aec854a87b8958d4c518f7287663bfae0b6a5a1e0f0eb95b50c9ea6789a7d77fda5f50d1b8a2183b40cab693ebacf32a9b59faf3b0084ff")
c2 = bytes.fromhex(
    "b40cab693ebacf32a9b59faf3b0084ffcaf7bc1223c17f848aec854a87b8958db50c9ea6789a7d77fda5f50d1b8a21834c518f7287663bfae0b6a5a1e0f0eb95")

# 分块
c1_blocks = [c1[i:i + 16] for i in range(0, len(c1), 16)]
c2_blocks = [c2[i:i + 16] for i in range(0, len(c2), 16)]
m1_blocks = [m1[i:i + 16] for i in range(0, len(m1), 16)]

print("c1 到 c2 的映射关系:")
c1_to_c2 = []
for i, c1_block in enumerate(c1_blocks):
    for j, c2_block in enumerate(c2_blocks):
        if c1_block == c2_block:
            c1_to_c2.append(j)
            print(f"  c1_block[{i}] = c2_block[{j}]")
            break

print(f"\n排列映射: {c1_to_c2}")

# 建立逆映射：对于每个 c2_block，找到它在 c1 中的位置
c2_to_c1 = {}
for i, j in enumerate(c1_to_c2):
    c2_to_c1[j] = i

print(f"逆映射: {c2_to_c1}")

# 重新计算 m2
m2_blocks = [b''] * 4

# 对于每个 c2 块，利用它在 c1 中的位置信息来解密
for j in range(4):
    i = c2_to_c1[j]  # c2_block[j] 在 c1 中的位置

    if i == 0:
        # c2_block[j] 是 c1 的第一个块
        # m1_blocks[0] = AES_Decrypt(key, c1_blocks[0]) ⊕ IV1
        if j == 0:
            # c2_block[0] 的加密：AES_Encrypt(key, m2_block[0] ⊕ IV2)
            # 所以：AES_Decrypt(key, c2_block[0]) = m2_block[0] ⊕ IV2
            # 因此：m1_blocks[0] = (m2_block[0] ⊕ IV2) ⊕ IV1
            m2_blocks[0] = bytes(a ^ b ^ c for a, b, c in zip(m1_blocks[0], IV2, IV1))
        else:
            # c2_block[j] 的加密：AES_Encrypt(key, m2_block[j] ⊕ c2_blocks[j-1])
            # 所以：AES_Decrypt(key, c2_block[j]) = m2_block[j] ⊕ c2_blocks[j-1]
            # 因此：m1_blocks[0] = (m2_block[j] ⊕ c2_blocks[j-1]) ⊕ IV1
            m2_blocks[j] = bytes(a ^ b ^ c for a, b, c in zip(m1_blocks[0], c2_blocks[j - 1], IV1))
    else:
        # c2_block[j] 在 c1 中不是第一个块
        # m1_blocks[i] = AES_Decrypt(key, c1_blocks[i]) ⊕ c1_blocks[i-1]
        if j == 0:
            # c2_block[0] 的加密：AES_Encrypt(key, m2_block[0] ⊕ IV2)
            # 所以：AES_Decrypt(key, c2_block[0]) = m2_block[0] ⊕ IV2
            # 因此：m1_blocks[i] = (m2_block[0] ⊕ IV2) ⊕ c1_blocks[i-1]
            m2_blocks[0] = bytes(a ^ b ^ c for a, b, c in zip(m1_blocks[i], IV2, c1_blocks[i - 1]))
        else:
            # c2_block[j] 的加密：AES_Encrypt(key, m2_block[j] ⊕ c2_blocks[j-1])
            # 所以：AES_Decrypt(key, c2_block[j]) = m2_block[j] ⊕ c2_blocks[j-1]
            # 因此：m1_blocks[i] = (m2_block[j] ⊕ c2_blocks[j-1]) ⊕ c1_blocks[i-1]
            m2_blocks[j] = bytes(a ^ b ^ c for a, b, c in zip(m1_blocks[i], c2_blocks[j - 1], c1_blocks[i - 1]))

# 组合并尝试去除填充
m2 = b''.join(m2_blocks)
print(f"\n原始解密结果: {m2}")
print(f"十六进制: {m2.hex()}")

try:
    m2_unpadded = unpad(m2, 16)
    print(f"\n去除填充后: {m2_unpadded}")
    print(f"Flag: {m2_unpadded.decode('latin-1')}")  # 使用 latin-1 避免编码错误
except Exception as e:
    print(f"\n去除填充失败: {e}")
    # 尝试手动检查
    print("手动检查最后一个字节的填充:")
    last_byte = m2[-1]
    print(f"最后一个字节: {last_byte} (0x{last_byte:02x})")

    # 手动去除填充
    if last_byte <= 16:
        potential_flag = m2[:-last_byte]
        print(f"手动去除填充后: {potential_flag}")
        try:
            print(f"Flag: {potential_flag.decode('utf-8')}")
        except:
            print(f"Flag (raw): {potential_flag}")