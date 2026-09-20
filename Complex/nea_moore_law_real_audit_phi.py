#!/usr/bin/env python3
"""
nea_moore_law_real_audit_phi.py

N.E.A. Volume C, §20: Moore's Law in φ coordinates.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def audit_cpu_history():
    # 真实历史数据
    cpu_data = [
        (1971, 0.74, 0.5),
        (1978, 5.0, 2.0),
        (1985, 16.0, 3.0),
        (1993, 66.0, 15.0),
        (2000, 1500.0, 50.0),
        (2004, 3800.0, 115.0),
        (2006, 2600.0, 65.0),
        (2015, 4000.0, 91.0),
    ]
    years = np.array([c[0] for c in cpu_data])
    freqs = np.array([c[1] for c in cpu_data])
    tdps = np.array([c[2] for c in cpu_data])

    # φ 演化：内耗（热密度）→ φ 上升
    # 内耗 ~ f × TDP / B_max
    f_norm = freqs / 3800.0
    p_norm = tdps / 115.0
    load = f_norm * p_norm

    # φ = 0.5 × load^0.5 (empirical mapping, calibrated at 2004)
    phi = 0.5 * np.sqrt(np.maximum(load, 0))

    print("=" * 70)
    print("  N.E.A. Volume C, §20: Moore's Law in φ coordinates")
    print("=" * 70)
    for i in range(len(years)):
        status = "CRITICAL" if phi[i] > 0.45 else "Normal"
        print(f"  {years[i]} | {freqs[i]:>7.0f} MHz | "
              f"φ = {phi[i]:.4f} | {status}")

    plt.figure(figsize=(10, 6), dpi=130)
    plt.plot(years, phi, 'k-o', label=r'CPU bandwidth deficit $\phi$')
    plt.axhline(0.5, color='r', linestyle='--',
                label=r'Horizon freeze ($\phi = 0.5$)')
    plt.axvline(2004, color='blue', alpha=0.3,
                label='2004 power wall')
    plt.annotate('Pivot to multi-core',
                 xy=(2004, 0.5), xytext=(1985, 0.55),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.title('Fig 9: Moore\'s Law — The 2004 Frequency Wall')
    plt.xlabel('Year')
    plt.ylabel(r'Bandwidth deficit $\phi$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_moore_law_phi.png', dpi=150)
    plt.close()
    print("  Figure: fig_moore_law_phi.png")


if __name__ == "__main__":
    audit_cpu_history()