import numpy as np
import matplotlib.pyplot as plt

def run_biological_audit():
    # 真实生物学数据：物种 | 体重(kg) | 静息心率(bpm) | 平均寿命(year)
    # 数据来源：生物定标律常用统计值
    mammal_data = [
        ("Mouse",    0.02,  600,   2),
        ("Rat",      0.3,   400,   4),
        ("Cat",      4.0,   150,   15),
        ("Dog",      20.0,  100,   13),
        ("Human",    70.0,  70,    80),
        ("Horse",    500.0, 40,    30),
        ("Elephant", 5000.0, 30,   70),
        ("Whale",    150000.0, 20, 90)
    ]
    
    names, mass, hr, life = zip(*mammal_data)
    mass = np.array(mass)
    hr = np.array(hr)
    life = np.array(life)

    print(">>> N.E.A. 生物带宽审计：寻找跨物种的‘生命负债常数’...")
    print("-" * 75)
    print(f"{'物种':<10} | {'体重(kg)':<10} | {'单体焓 H':<10} | {'总带宽消耗 (Relative)':<15}")
    print("-" * 75)

    # N.E.A. 逻辑：生命是三阶分形，维度 d 随质量 M 发生微弱内化
    # 利用 3/4 幂律推导：d_eff = 3 + log10(M)/constant
    # 这里我们使用 Paper IX 的公式：H = 1 + 1/d
    d_eff = 3.0 + 0.1 * np.log10(mass / 0.02 + 1)
    h_values = 1.0 + 1.0/d_eff

    # 计算总带宽消耗 = 心率 * 寿命 * 单体焓
    # 注意：心率*寿命在生物学中近似常数，但加入 H 后，我们要看它是否更稳健
    total_bandwidth = (hr * 60 * 24 * 365) * life * h_values
    
    # 归一化以便观察
    norm_bandwidth = total_bandwidth / total_bandwidth[0]

    for i in range(len(names)):
        print(f"{names[i]:<10} | {mass[i]:<10.2f} | {h_values[i]:.4f} | {norm_bandwidth[i]:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(mass, norm_bandwidth, 'go-', label='Normalized Total Bandwidth (NEA)')
    plt.xscale('log')
    plt.axhline(y=1.0, color='r', linestyle='--', label='Universal Biological Limit')
    plt.title('Biological Audit: Total Bandwidth Conservation across Mammals')
    plt.xlabel('Body Mass (kg) - Log Scale')
    plt.ylabel('Total Life Bandwidth (Relative to Mouse)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    cv = np.std(norm_bandwidth) / np.mean(norm_bandwidth)
    print("-" * 75)
    print(f"跨物种总带宽变异系数 (CV): {cv:.4f} (CV越小证明守恒律越强)")

if __name__ == "__main__":
    run_biological_audit()