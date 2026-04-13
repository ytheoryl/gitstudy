
def solve():
    results = []
    # 设小长方形长为 a, 宽为 b (a > b >= 1)
    # 大长方形的长为 L, 宽为 W (L >= W >= 1)
    # 约束条件：
    # 1. 4 * a * b = L * W (面积相等)
    # 2. 2 * (L + W) = 100 => L + W = 50
    # 3. L, W 必须能被 a, b 组合出来（即拼法存在）

    for L in range(1, 50):
        W = 50 - L
        if L < W: continue # 保持 L 为长边
        
        big_area = L * W
        # 4个小长方形面积和 = L * W
        # 所以 a * b = big_area / 4
        if big_area % 4 != 0:
            continue
        small_area = big_area // 4
        
        # 寻找满足 a*b = small_area 的整数对
        for a in range(1, small_area + 1):
            if small_area % a == 0:
                b = small_area // a
                if a < b: continue # 约定 a 为长
                
                # 检查拼法可能性：
                # 拼法 1: 4个横着排或竖着排 (L=4a, W=b) 或 (L=a, W=4b) 或 (L=4b, W=a) 等
                case1 = (L == 4*a and W == b) or (L == a and W == 4*b) or (L == 4*b and W == a)
                # 拼法 2: 2x2 堆叠 (L=2a, W=2b) 或 (L=2b, W=2a)
                case2 = (L == 2*a and W == 2*b) or (L == 2*b and W == 2*a)
                # 拼法 3: 3个并列+1个垂直 (要求 a = 3b, 此时大长方形为 a x (a+b) 或 (3b) x (4b))
                # 或者 L = a+b, W = a (如果 a=3b)
                case3 = (a == 3*b and ( (L == a and W == a+b) or (L == a+b and W == a) ))
                # 还有一种拼法：中间空一个洞（或不空洞）的旋转拼法
                # 四个小长方形围成一个大长方形，外框 L x W，中间可能有空隙
                # 如果正好拼满（无空隙）：L = a + b, W = a + b 且 a + b = 25 (因为 2*(L+W)=100)
                # 这种情况下 L=W=25 (正方形)，面积 625， 625/4 不是整数，不符合要求。
                
                # 修正 case3：只需要考虑所有可能的 (L, W) 组合是否能被 4 个 (a, b) 覆盖
                # 1. 4a x b
                # 2. 2a x 2b
                # 3. a x 4b
                # 4. (a+b) x ? (比如 L=a+b, 则 W = 4ab/(a+b))
                # 检查 W 是否等于 a (如果 a=3b)
                if case1 or case2 or case3:
                    results.append({
                        "big_L": L, "big_W": W,
                        "small_a": a, "small_b": b,
                        "type": "1x4" if case1 else ("2x2" if case2 else "旋转型")
                    })
                    
    return results

if __name__ == "__main__":
    solutions = solve()
    for s in solutions:
        print(f"大长方形: {s['big_L']}x{s['big_W']}, 小长方形: {s['small_a']}x{s['small_b']}, 类型: {s['type']}")
