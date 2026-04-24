# 模板4：自适应beta搜索
def adaptive_coppersmith(f, modulus, root_bound, beta_range=(0.1, 0.5), steps=10):
    """
    自适应搜索最优beta
    """
    best_root = None
    best_beta = None

    beta_min, beta_max = beta_range
    step_size = (beta_max - beta_min) / steps

    for i in range(steps + 1):
        beta = beta_max - i * step_size
        beta = max(beta, beta_min)  # 确保不小于最小值

        try:
            roots = f.small_roots(X=root_bound, beta=beta)
            if roots:
                root_candidate = roots[0]
                # 简单验证：根在范围内
                if 0 <= root_candidate < root_bound:
                    best_root = root_candidate
                    best_beta = beta
                    print(f"成功! beta={beta:.3f}, 根={root_candidate}")
                    break
                else:
                    print(f"beta={beta:.3f} 找到根但超出范围")
            else:
                print(f"beta={beta:.3f} 未找到根")
        except Exception as e:
            print(f"beta={beta:.3f} 计算错误: {e}")

    return best_root, best_beta


# 使用示例
PR. < x > = PolynomialRing(Zmod(N))
f = your_polynomial(x)
f = f.monic()

root, used_beta = adaptive_coppersmith(f, N, 2 ^ 100)
if root:
    print(f"最优beta: {used_beta}")