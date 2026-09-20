#!/usr/bin/env python3
"""nea_zhangsuo_layer_model.py - Layer wells produce stable plateaus."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_layer_model():
    print("=" * 66)
    print("  N.E.A. Volume C, Section 18: Zhang-Suo Layer Generation")
    print("=" * 66)

    t_max = 800
    phi_floor = 0.15
    phi_ceiling = 0.50
    layer_wells = [0.22, 0.30, 0.38, 0.45]

    np.random.seed(42)
    phi = phi_floor + 0.01
    phi_traj = []
    layer_events = []
    reset_times = []

    for t in range(t_max):
        # 基础驱动：φ 向上（缩 > 张）
        drive = 0.010 * (1 + 1.5 * phi)

        # 势阱效应：靠近层时驱动被强烈削弱
        for w in layer_wells:
            drive *= (1 - 0.92 * np.exp(-((phi - w)/0.018)**2))

        noise = 0.0025 * np.random.randn()

        f_ext = np.sqrt(max(1 - 2*phi, 0))
        phi += f_ext * (drive + noise)
        phi = max(phi_floor, min(phi_ceiling - 0.005, phi))

        # 层事件检测
        for w in layer_wells:
            if abs(phi - w) < 0.012:
                layer_events.append((t, w))

        # 崩溃
        if phi >= phi_ceiling - 0.01:
            reset_times.append(t)
            phi = phi_floor + 0.01 * np.random.randn()
            phi = max(phi_floor, phi)

        phi_traj.append(phi)

    phi_traj = np.array(phi_traj)

    print(f"Duration: {t_max} steps")
    print(f"Reset events (cycles): {len(reset_times)}")
    print(f"Layer events detected: {len(layer_events)}")
    print(f"phi range: [{phi_traj.min():.3f}, {phi_traj.max():.3f}]")

    plt.figure(figsize=(12, 6), dpi=130)
    plt.plot(phi_traj, 'b-', linewidth=1.2, label=r'$\phi$ trajectory')
    for w in layer_wells:
        plt.axhline(w, color='gray', linestyle=':', alpha=0.5)
    plt.axhline(phi_ceiling, color='red', linestyle='--',
                label=r'Horizon freeze ($\phi = 0.5$)')
    plt.title('Fig 7b: Expansion-Compression and Layer Generation')
    plt.xlabel('Time')
    plt.ylabel(r'Bandwidth deficit $\phi$')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('fig_zhangsuo_layer.png', dpi=150)
    plt.close()
    print("Figure: fig_zhangsuo_layer.png")


if __name__ == "__main__":
    run_layer_model()