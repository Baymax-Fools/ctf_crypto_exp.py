#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *
from decimal import Decimal, getcontext

# 设置高精度，以防 n 太大导致浮点数精度丢失
getcontext().prec = 100

def solve_mod(A, B, D, M, first=False):
    # 辗转相除法
    # A≤(n⋅D)modM≤B

    if A > B:
        return float('inf')
    
    # 检查当前 k=0 的情况，如果存在满足条件的n直接返回（n不能为0）
    n_min = (A + D - 1) // D
    if first and n_min == 0:
        n_min = 1
    n_max = B // D
    if n_min <= n_max:
        return n_min
    
    R = M % D
    if R == 0:
        return float('inf')
    
    A_prime = (-B) % D
    B_prime = (-A) % D
    
    k = solve_mod(A_prime, B_prime, R, D, False)
    if k == float('inf'):
        return k
    
    return (k * M + A - 1) // D + 1

def solve_n(m):
    """计算使得 2^n 前缀为 m 的最小 n"""
    m_dec = Decimal(m)
    m_next = Decimal(m + 1)
    
    # 求边界的对数的小数部分
    log2 = Decimal(2).log10()               # 计算 log10(2)
    A_frac = m_dec.log10() % Decimal(1)     # 计算 log10(m) 的小数部分
    B_frac = m_next.log10() % Decimal(1)    # 计算 log10(m+1) 的小数部分
    
    # 把小数部分放大成大整数进行运算
    PRECISION = 10**80
    D = int(log2 * PRECISION)
    M = PRECISION
    
    # 使用 10**20 作为 padding 抵消边缘截断误差
    A = int(A_frac * PRECISION) - 10**20
    B = int(B_frac * PRECISION) - 10**20
    
    A_mod = A % M
    B_mod = B % M
    
    ans = solve_mod(A_mod, B_mod, D, M, True)
        
    return ans

if __name__ == "__main__":
    # 以你提供的靶机示范为测试用例
    m_test = 86101234
    print(f"[+] 正在计算 m = {m_test} ...")
    n = solve_n(m_test)
    print(f"[!] 请输入 n = {n}")
    
    # 我们可以自己用 Python 核验一下这个输出是否正确：
    # 计算 2^n 转字符串看看前缀是不是 m
    # res = str(pow(2, n))
    # print(f"2^{n} 实际前缀: {res[:len(str(m_test))]}")


p = remote("1.95.44.158",11314)
context.log_level = 'debug'

Team = b'Xp0int'
token = b'f97cfc8b121677e40378b83e14f90830'

p.recvuntil(b'Team: \n')
p.sendline(Team)
p.recvuntil(b'Token: \n')
p.sendline(token)

for i in range(8):
    p.recvuntil(b'm = ')
    m = int(p.recvline().strip())
    p.recvuntil(b'n = ')
    n = solve_n(m)
    p.sendline(str(n).encode())

p.interactive()


'''
package main

import (
    "bufio"
    "crypto/rand"
    "fmt"
    "math/big"
    "os"
    "strconv"
    "strings"
    "time"
)

func main() {
    // 对应：max.abs.array = array; array[0] = 99999999;
    max := big.NewInt(99999999)

    // 对应：v48 = crypto_rand_Int(crypto_rand_Reader, &max);
    n, err := rand.Int(rand.Reader, max)
    if err != nil {
        // 对应出错时的 fmt_Fprintln(w, v61) 并 os_Exit(2)
        fmt.Fprintln(os.Stdout, "Error: ", err)
        os.Exit(2)
    }

    // 对应：y_.abs.array = &v23 (v23 = 1); z = math_big__ptr_Int_Add(n, n, &y_);
    // 即生成一个 [1, 99999999] 范围内的随机数 m
    m := new(big.Int).Add(n, big.NewInt(1))

    // 对应：fmt_Fprintf(w_1, "m = %d\n", m)
    fmt.Fprintf(os.Stdout, "m = %d\n", m)

    // 对应：fmt_Fprint(w_2, "n = ")
    fmt.Fprint(os.Stdout, "n = ")

    // 对应：runtime_newproc((runtime_funcval *)&fn);
    // 启动一个 goroutine 执行超时检测
    go timeoutCheck()

    // 对应：bufio__ptr_Reader_ReadString(&b, 0xAu) 等初始化读取逻辑
    reader := bufio.NewReader(os.Stdin)
    input, _ := reader.ReadString('\n')

    // 对应：strings_TrimSpace(s);
    input = strings.TrimSpace(input)

    // 对应：v49 = strconv_Atoi(s_1);
    userN, err := strconv.Atoi(input)
    if err != nil {
        fmt.Fprintln(os.Stdout, "Error: ", err)
        os.Exit(2)
    }

    // 对应：x.abs.array = &n2 (n2 = 2); v7 = math_big__ptr_Int_exp(&z_, &x, &y, 0, 0);
    // 计算 2 的 userN 次方
    base := big.NewInt(2)
    exponent := big.NewInt(int64(userN))
    pow2 := new(big.Int).Exp(base, exponent, nil)

    // 将生成的 m 和计算出的 2^userN 转为十进制字符串
    // 对应：math_big_nat_itoa(..., 10) 
    var strPow2 string
    if pow2 != nil {
        strPow2 = pow2.String()
    } else {
        strPow2 = "<nil>"
    }

    var strM string
    if m != nil {
        strM = m.String()
    } else {
        strM = "<nil>"
    }

    // 对应：if ( len_3 <= len && (runtime_memequal(), v14) )
    // 判断 2^n 的长度是否大于等于 m，并且它的前缀是否和 m 的内存字节相等 (即前缀匹配)
    if len(strM) <= len(strPow2) && strings.HasPrefix(strPow2, strM) {
        fmt.Fprintf(os.Stdout, "Verified\n")
        os.Exit(0)
    } else {
        fmt.Fprintf(os.Stdout, "Failed\n")
        os.Exit(1)
    }
}

func timeoutCheck() {
    // 对应：time_Sleep(60000000000LL) => 60秒
    time.Sleep(60 * time.Second)
    // 对应：fmt_Fprintln(w, "TimeOut")
    fmt.Fprintln(os.Stdout, "TimeOut")
    os.Exit(1)
}

'''

