from Cryptodome.Util.number import *
import gmpy2
import multiprocessing as mp
import sys

# 全局参数（在子进程中重新初始化）
p_str = "10560464175631160709999383504944939280267067560378620626979040921315467798501630079655340663547895515812021911470304483075907600549587171358369476255124337"
g_str = "5572911063894340974483734192541353411838868965361107134612465011908061780180242348779533324820127053271574799429894984956163372524626786431177292215721384"
y_str = "2551976503972625362405323290468587787679347326045114894085518452627208422960190509410833573983206966744456211220857302778318665690771595372276106771043208"
c1_str = "1205617983130100879228661072981675725569095797251301660744333997969095366993470887762473783053252549837619991656838026541987751368433948599410216526314464"
c2_str = "135410793997875487972298785237681131478761447205213610635842285010164308038301697054176371628605014267489864238137735560888444688177201474949707954751577"


def worker(start, end, process_id):
    """工作进程函数"""
    # 在每个进程中重新初始化 gmpy2 对象（避免序列化问题）
    p_mpz = gmpy2.mpz(p_str)
    g_mpz = gmpy2.mpz(g_str)
    y_mpz = gmpy2.mpz(y_str)
    c1_mpz = gmpy2.mpz(c1_str)
    c2_val = int(c2_str)

    print(f"进程 {process_id} 开始搜索范围: {start} - {end}")

    for x in range(start, end):
        if gmpy2.powmod(g_mpz, x, p_mpz) == y_mpz:
            print(f"进程 {process_id} 找到私钥 x = {x}")

            # 解密
            s = gmpy2.powmod(c1_mpz, x, p_mpz)
            m = c2_val ^ int(s)
            flag = long_to_bytes(m)
            print(f"Flag: {flag.decode()}")

            # 通知其他进程停止
            return x, flag.decode()

        # 进度显示（每100万次）
        if (x - start) % 1000000 == 0 and (x - start) > 0:
            progress = (x - start) / (end - start) * 100
            print(f"进程 {process_id}: {progress:.1f}%")

    return None, None


def main():
    total_range = 2 ** 32
    num_processes = mp.cpu_count()
    chunk_size = total_range // num_processes

    print(f"使用 {num_processes} 个进程进行暴力破解")
    print(f"每个进程处理范围: {chunk_size}")

    with mp.Pool(processes=num_processes) as pool:
        results = []
        for i in range(num_processes):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_processes - 1 else total_range
            # 使用 apply_async 进行异步调用
            results.append(pool.apply_async(worker, (start, end, i)))

        # 等待结果
        for res in results:
            x, flag = res.get()
            if x is not None:
                print(f"\n成功找到私钥!")
                print(f"x = {x}")
                print(f"Flag: {flag}")

                # 终止其他进程
                pool.terminate()
                pool.join()
                return

    print("未找到私钥")


if __name__ == '__main__':
    main()

"""进程 6 找到私钥 x = 1616680587
Flag: flag{31g4m41_D15cr373_10g}"""