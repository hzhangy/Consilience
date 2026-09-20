#!/usr/bin/env python3
"""
nea_relaxation_oscillator_phi.py

N.E.A. Volume C, §18: Civilizational cycles in φ coordinates.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def simulate_civilization(years=600, base_innovation=0.010,
                          base_decay=0.020,
                          innovation_response=0.5,
                          decay_response=0.5,
                          seed=42):
    np.random.seed(seed)
    phi = 0.20
    phi_limit = 0.5
    phi_floor = 0.15

    t_axis, phi_axis, resets = [], [], []

    for t in range(years):
        # 压力系数：phi 越高，内耗越强
        pressure = max(0.0, min(1.0,
            (phi - phi_floor) / (phi_limit - phi_floor)))

        innovation = base_innovation * (1 + innovation_response * pressure)
        decay = base_decay * (1 + decay_response * pressure)
        noise = 0.002 * np.random.randn()

        f_ext = np.sqrt(max(1 - 2*phi, 0))
        phi += f_ext * (decay - innovation + noise)

        t_axis.append(t)
        phi_axis.append(phi)

        if phi >= phi_limit:
            resets.append(t)
            phi = phi_floor + 0.02 * np.random.randn()

    return np.array(t_axis), np.array(phi_axis), resets


def run_oscillator_audit():
    print("=" * 60)
    print("  N.E.A. Volume C, §18: Relaxation Oscillator (φ)")
    print("=" * 60)

    years = 600
    t1, p1, r1 = simulate_civilization(
        years=years, base_innovation=0.012, base_decay=0.025,
        innovation_response=0.3, decay_response=0.7, seed=1)
    t2, p2, r2 = simulate_civilization(
        years=years, base_innovation=0.018, base_decay=0.022,
        innovation_response=0.8, decay_response=0.4, seed=2)

    print(f"  Involuted:  {len(r1)} crashes, period ≈ {years/max(len(r1),1):.0f} yrs")
    print(f"  Resilient:  {len(r2)} crashes, period ≈ {years/max(len(r2),1):.0f} yrs")

    fig, ax = plt.subplots(figsize=(12, 6), dpi=130)
    ax.plot(t1, p1, 'r-', label='Involuted system', alpha=0.8)
    ax.plot(t2, p2, 'g-', label='Resilient system', alpha=0.8)
    for rt in r1:
        ax.axvline(rt, color='red', linestyle=':', alpha=0.3)
    for rt in r2:
        ax.axvline(rt, color='green', linestyle=':', alpha=0.3)
    ax.axhline(0.5, color='k', linestyle='--',
               label=r'Horizon freeze ($\phi=0.5$)')
    ax.set_xlabel('Time (years)')
    ax.set_ylabel(r'Bandwidth deficit $\phi$')
    ax.set_title('Fig 7: Civilizational Relaxation Oscillator')
    ax.legend()
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('fig_relaxation_oscillator_phi.png', dpi=150)
    plt.close()
    print("  Figure: fig_relaxation_oscillator_phi.png")


if __name__ == "__main__":
    run_oscillator_audit()