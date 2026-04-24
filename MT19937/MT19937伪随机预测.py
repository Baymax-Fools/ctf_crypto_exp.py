#!/usr/bin/env python3
from pwn import *
from mt19937predictor import MT19937Predictor

ip = 'node5.buuoj.cn'
port = '25450'


def exploit():
    c = remote(ip, port)
    predictor = MT19937Predictor()

    # 使用promo code获取更多资金
    c.recvuntil(b'[3] - Exit')
    c.sendline(b'2')
    c.recvuntil(b'Enter your promocode:')
    c.sendline(b'b33_1_4m_b3333')
    c.recvuntil(b'Great!')

    # 进入老虎机
    c.recvuntil(b'[3] - Exit')
    c.sendline(b'1')
    c.recvuntil(b'$$$     all or nothing    $$$')

    collected_states = []

    # 收集624个32位随机数状态（MT19937需要624个状态来预测）
    for i in range(624):
        c.recvuntil(b'[$] - $$$SPIN$$$')
        c.sendline(b'$')
        c.recvuntil(b'It will be:')

        # 发送一个错误的猜测
        c.sendline(b'0')

        # 接收实际结果
        response = c.recvuntil(b'Nice try!')
        lines = response.split(b'\n')

        # 解析显示的随机数
        for line in lines:
            if b'|' in line and len(line) > 10:
                hex_str = line.decode().replace('|', '').strip()
                if len(hex_str) == 8:  # 确保是8个十六进制字符
                    state = int(hex_str, 16)
                    collected_states.append(state)
                    print(f"Collected state {i + 1}: {hex(state)}")
                    break

    # 训练预测器
    for state in collected_states:
        predictor.setrandbits(state, 32)

    # 进行预测并获取flag
    c.recvuntil(b'[$] - $$$SPIN$$$')
    c.sendline(b'$')
    c.recvuntil(b'It will be:')

    next_random = predictor.getrandbits(32)
    c.sendline(hex(next_random)[2:].encode())

    # 接收flag
    result = c.recvall(timeout=2)
    print(result)

    c.close()


if __name__ == "__main__":
    exploit()