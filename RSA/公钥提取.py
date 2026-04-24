#!/usr/bin/env python3
"""
RSA Modulus 提取工具
将 OpenSSL 输出的十六进制格式转换为完整的 Modulus 值
"""


def extract_modulus():
    print("=" * 60)
    print("RSA Modulus 提取工具")
    print("=" * 60)
    print("请粘贴 OpenSSL 输出的 Modulus 十六进制数据（支持多行、冒号格式）")
    print("输入完成后，按 Enter 两次开始处理")
    print("-" * 60)

    # 读取多行输入
    lines = []
    while True:
        try:
            line = input().strip()
            if line == "":
                # 连续两个空行结束输入
                if len(lines) > 0:
                    break
                else:
                    continue
            lines.append(line)
        except EOFError:
            break

    if not lines:
        print("错误：未输入任何数据")
        return

    # 合并所有行并清理格式
    hex_data = "".join(lines)
    hex_data = hex_data.replace(":", "").replace(" ", "").replace("\t", "")

    # 验证十六进制格式
    if not all(c in "0123456789abcdefABCDEF" for c in hex_data):
        print("错误：输入包含非十六进制字符")
        return

    if len(hex_data) % 2 != 0:
        print("错误：十六进制数据长度不正确")
        return

    # 计算字节数
    byte_count = len(hex_data) // 2

    print("\n" + "=" * 60)
    print("提取结果")
    print("=" * 60)

    # 显示基本信息
    print(f"原始十六进制长度: {len(hex_data)} 字符")
    print(f"字节数: {byte_count} 字节")
    print(f"位数: {byte_count * 8} bits")

    # 转换为整数
    try:
        n = int(hex_data, 16)
        print(f"实际位数: {n.bit_length()} bits")

        # 检查是否有前导00
        if hex_data.startswith("00"):
            print("检测到前导 00 字节（ASN.1 INTEGER 正数填充）")

    except ValueError as e:
        print(f"转换错误: {e}")
        return

    print("\n" + "-" * 60)
    print("1. 完整的 Modulus (十六进制):")
    print("-" * 60)
    print(hex_data)

    print("\n" + "-" * 60)
    print("2. 不带前导00的 Modulus (十六进制):")
    print("-" * 60)
    # 去掉前导的00
    clean_hex = hex_data.lstrip('0')
    if len(clean_hex) % 2 != 0:
        clean_hex = '0' + clean_hex  # 确保长度为偶数
    print(clean_hex)

    print("\n" + "-" * 60)
    print("3. 格式化输出 (每行16字节):")
    print("-" * 60)
    formatted = ":".join(hex_data[i:i + 2] for i in range(0, len(hex_data), 2))
    # 每16字节换行
    bytes_list = formatted.split(":")
    for i in range(0, len(bytes_list), 16):
        line = " ".join(bytes_list[i:i + 8]) + "  " + " ".join(bytes_list[i + 8:i + 16])
        print(f"    {line}")

    print("\n" + "-" * 60)
    print("4. Python 使用示例:")
    print("-" * 60)
    print(f"# 完整的 modulus 值")
    print(f"modulus_hex = \"{hex_data}\"")
    print(f"n = int(modulus_hex, 16)")
    print(f"print(f\"Modulus: {{n}}\")")
    print(f"print(f\"Bit length: {{n.bit_length()}}\")")

    print("\n" + "-" * 60)
    print("5. 复制粘贴格式:")
    print("-" * 60)
    print("完整格式（带前导00）:")
    print(hex_data)
    print("\n简洁格式（无前导00）:")
    print(clean_hex)


if __name__ == "__main__":
    extract_modulus()