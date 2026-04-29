import numpy as np
import matplotlib.pyplot as plt

def simulate_protein_folding():
    # 模拟 1000 种随机构型
    num_configs = 1000
    # 随机生成各向异性效率 xi (0.0=无序, 0.35=完美折叠)
    xi_samples = np.random.beta(2, 5, num_configs) * 0.4
    
    # 基础 3D 租金 (1 + 1/3)
    h_base = 1.3333
    
    # 计算每种构型的涌现焓 H = (1 + 1/d) * e^(-xi)
    h_values = h_base * np.exp(-xi_samples)
    
    # 排序以观察收敛
    sorted_h = np.sort(h_values)
    
    print(">>> N.E.A. 蛋白质折叠审计：寻找‘生命锁定点’...")
    # 找到跌破 1.25 门槛的构型
    folded_mask = sorted_h < 1.25
    num_folded = np.sum(folded_mask)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(range(num_configs), sorted_h, c='gray', alpha=0.3, label='Random Conformations')
    # 突出显示进入“生命区”的唯一态
    plt.scatter(np.where(folded_mask)[0], sorted_h[folded_mask], c='green', s=100, label='Folded Functional State (H < 1.25)')
    
    plt.axhline(y=1.25, color='red', linestyle='--', label='Life Threshold (4D Anchor)')
    plt.axhline(y=1.3333, color='blue', linestyle=':', label='3D Background')
    
    plt.title('Protein Folding: Convergence as Enthalpy Arbitrage')
    plt.xlabel('Conformation Index (Sorted by Efficiency)')
    plt.ylabel('System Enthalpy H')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

    print(f"--- 结算：在 {num_configs} 种构型中，只有 {num_folded} 个能赎回足够的带宽以维持生命。")
    print("结论：折叠是拓扑的必然选择，而非概率的随机碰撞。")

if __name__ == "__main__":
    simulate_protein_folding()