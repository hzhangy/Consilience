#!/usr/bin/env python3
"""nea_ai_centralization_trap.py - Clean mean curve."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def build_social_graph(N, ai_coupling, seed=0):
    rng = np.random.default_rng(seed)
    A = np.zeros((N + 1, N + 1))
    for i in range(1, N+1):
        A[0, i] = 0.1 + 0.9 * ai_coupling
        A[i, 0] = 0.05
    p_human = 0.4 * (1.0 - ai_coupling)
    for i in range(1, N+1):
        for j in range(i+1, N+1):
            if rng.random() < p_human:
                A[i, j] = 0.5 + 0.5 * rng.random()
                A[j, i] = 0.3 + 0.3 * rng.random()
    for i in range(N+1):
        if A[i].sum() < 1e-3:
            j = (i+1) % (N+1)
            A[i, j] = A[j, i] = 0.05
    return A


def spectral_vitality(A):
    deg = np.maximum(A.sum(axis=1), 1e-3)
    L = np.eye(A.shape[0]) - A / deg[:, None]
    eigs = np.linalg.eigvals(L)
    return np.var(np.imag(eigs))


def run_ai_trap_audit():
    N = 30
    n_trials = 10
    couplings = np.linspace(0.0, 0.95, 20)

    xi_mean = []
    for c in couplings:
        vals = [spectral_vitality(build_social_graph(N, c, seed=s))
                for s in range(n_trials)]
        xi_mean.append(np.mean(vals))
    xi_mean = np.array(xi_mean)

    print(f"AI coupling 0.00 -> xi = {xi_mean[0]:.6e}")
    print(f"AI coupling 0.95 -> xi = {xi_mean[-1]:.6e}")
    print(f"Collapse ratio: {xi_mean[-1]/(xi_mean[0]+1e-30):.4f}")

    plt.figure(figsize=(10, 6), dpi=130)
    plt.semilogy(couplings, xi_mean, 'bo-', linewidth=2.2, markersize=8,
                 label=r'$\xi_{\rm social}$ (mean of 10 trials)')
    plt.xlabel('AI centralization degree')
    plt.ylabel(r'$\xi_{\rm social}$ (log scale)')
    plt.title('Fig 8: The AI Centralization Trap')
    plt.legend()
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_ai_trap.png', dpi=150)
    plt.close()
    print("Figure: fig_ai_trap.png")


if __name__ == "__main__":
    run_ai_trap_audit()