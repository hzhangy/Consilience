#!/usr/bin/env python3
"""nea_path_pruning_phi.py - Lower init, longer horizon."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_path_pruning_phi(num_futures=100, steps=120):
    phi_init = 0.10
    phi_limit = 0.5

    np.random.seed(42)
    individual_drift = np.random.normal(0.006, 0.003, num_futures)
    individual_drift = np.clip(individual_drift, 0.0005, 0.015)

    phi_states = np.full(num_futures, phi_init)
    active = np.ones(num_futures, dtype=bool)
    history = [phi_states.copy()]

    for s in range(steps):
        f_ext = np.sqrt(np.maximum(1 - 2*phi_states, 0))
        noise = np.random.normal(0, 0.008, num_futures)
        dphi = f_ext * (individual_drift + noise)

        phi_states = phi_states + dphi
        active = active & (phi_states < phi_limit)
        phi_states[~active] = np.nan
        history.append(phi_states.copy())

    history = np.array(history)
    alive_count = int(np.sum(active))

    plt.figure(figsize=(10, 6), dpi=130)
    plt.plot(history, color='gray', alpha=0.3, linewidth=0.5)
    alive_idx = np.where(active)[0]
    for i in alive_idx:
        plt.plot(history[:, i], color='green', linewidth=1.5, alpha=0.9)

    plt.axhline(phi_limit, color='red', linestyle='--',
                label=r'Horizon freeze ($\phi = 0.5$)')
    plt.title(f'Path Pruning: {alive_count} Allowed Futures '
              f'from {num_futures}')
    plt.xlabel('Causal steps')
    plt.ylabel(r'Bandwidth deficit $\phi$')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('fig_path_pruning_phi.png', dpi=150)
    plt.close()

    print(f"Initial: {num_futures}, Surviving: {alive_count}")
    print(f"Elimination rate: {(num_futures-alive_count)/num_futures:.1%}")
    print("Figure: fig_path_pruning_phi.png")


if __name__ == "__main__":
    run_path_pruning_phi()