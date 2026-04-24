import base64

def base64_stego_decode(lines):
    bin_str = ''
    for line in lines:
        line = line.strip()
        if not line:
            continue
        padding_count = line.count('=')
        if padding_count > 0:
            # 获取最后一个非=的字符
            last_char = line[-padding_count-1]
            # 该字符在Base64表中的索引（6位）
            index = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".index(last_char)
            # 取最后 padding_count*2 位
            if padding_count == 1:
                # 取最后2位
                bits = bin(index)[2:].zfill(6)[-2:]
                bin_str += bits
            elif padding_count == 2:
                # 取最后4位
                bits = bin(index)[2:].zfill(6)[-4:]
                bin_str += bits
            # 如果padding_count更多，按实际隐藏位数处理，但标准Base64最多2个=
    # 将二进制串转字节
    message = ''
    for i in range(0, len(bin_str), 8):
        byte = bin_str[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    return message

# 你的数据
data = """WA====
wUVw====
wQVA====
gRew====
ARZQ====
gbaQ====
QcdQ====
QZdQ====
gYaQ====
QZcg====
QadA====
wXcw====
QYbg====
wZdQ====
Qacw====
QYZw====
AbYQ====
AZaQ====
wbcg====
QZZw====
Qacw====
Qf"""

lines = data.split('\n')
print(base64_stego_decode(lines))