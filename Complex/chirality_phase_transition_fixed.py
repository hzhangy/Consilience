#!/usr/bin/env python3
"""
chirality_phase_transition_fixed.py

N.E.A. Volume C, Section 4: Chirality as Spectral Symmetry Breaking.

关键修复（相对旧版）：
  1. 使用非对称 Laplacian: L = I - D^{-1} A
  2. 使用 np.linalg.eigvals 支持复特征值
  3. vitality = Var(Im(λ))
  4. 无向图（racemic）→ 纯实谱；有向图（helix）→ 复谱

本体论：所有对象均为因果图上的虚拟记账结构，C8 不是物理空间。
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix, csr_matrix


def build_racemic_3d(L=6):
    """无向 cubic 格点：racemic 混合物，纯实谱。"""
    N = L**3
    A = lil_matrix((N, N))
    for x in range(L):
        for y in range(L):
            for z in range(L):
                u = x*L*L + y*L + z
                if x+1 < L:
                    v = (x+1)*L*L + y*L + z
                    A[u, v] = A[v, u] = 1.0
                if y+1 < L:
                    v = x*L*L + (y+1)*L + z
                    A[u, v] = A[v, u] = 1.0
                if z+1 < L:
                    v = x*L*L + y*L + (z+1)
                    A[u, v] = A[v, u] = 1.0
    return A.tocsr()


def build_helix_3d(L=6, n_chains=5):
    """有向 helical 链：homochiral，复谱。"""
    N = L**3
    A = lil_matrix((N, N))
    # 背景弱无向格
    for x in range(L):
        for y in range(L):
            for z in range(L):
                u = x*L*L + y*L + z
                if x+1 < L:
                    v = (x+1)*L*L + y*L + z
                    A[u, v] = A[v, u] = 0.1
                if y+1 < L:
                    v = x*L*L + (y+1)*L + z
                    A[u, v] = A[v, u] = 0.1
                if z+1 < L:
                    v = x*L*L + y*L + (z+1)
                    A[u, v] = A[v, u] = 0.1
    # 有向螺旋链（非对称）：A[u,v] >> A[v,u]
    np.random.seed(42)
    for _ in range(n_chains):
        x0 = np.random.randint(0, L-3)
        y0 = np.random.randint(0, L-3)
        z0 = np.random.randint(0, L-3)
        for s in range(3):
            u = (x0+s)*L*L + (y0+s)*L + (z0+s)
            v = (x0+s+1)*L*L + (y0+s+1)*L + (z0+s+1)
            A[u, v] += 3.0
            A[v, u] += 0.1
    return A.tocsr()


def compute_spectrum_asym(A):
    A = A.toarray() if hasattr(A, 'toarray') else A
    N = A.shape[0]
    deg = np.maximum(A.sum(axis=1), 1e-3)
    L = np.eye(N) - A / deg[:, None]
    eigvals = np.linalg.eigvals(L)
    return eigvals


def run_chirality_audit():
    print("=" * 66)
    print("  N.E.A. Volume C, §4: Chirality as Spectral Symmetry Breaking")
    print("=" * 66)
    print()

    L = 6
    A_race = build_racemic_3d(L)
    A_helix = build_helix_3d(L)

    eig_race = compute_spectrum_asym(A_race)
    eig_helix = compute_spectrum_asym(A_helix)

    # 复谱度量
    var_im_race = np.var(np.imag(eig_race))
    var_im_helix = np.var(np.imag(eig_helix))

    print(f"  Racemic (undirected):")
    print(f"    max |Im(λ)| = {np.max(np.abs(np.imag(eig_race))):.2e}")
    print(f"    Var(Im(λ))  = {var_im_race:.2e}")
    print()
    print(f"  Helix (directed):")
    print(f"    max |Im(λ)| = {np.max(np.abs(np.imag(eig_helix))):.2e}")
    print(f"    Var(Im(λ))  = {var_im_helix:.2e}")
    print()

    ratio = var_im_helix / (var_im_race + 1e-30)
    print(f"  Var ratio (helix / racemic) = {ratio:.2e}")
    print()

    if var_im_helix > var_im_race * 10:
        print("  >>> VERDICT: Spectral symmetry breaking confirmed.")
        print("      Racemic = real spectrum (undirected, no directed flow).")
        print("      Helix   = complex spectrum (directed flow activated).")
    else:
        print("  >>> WARNING: Complex spectrum not sufficiently emerged.")
        print("      Check directed chain strength.")

    # 绘图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=130)

    ax1.scatter(np.real(eig_race), np.imag(eig_race),
                c='black', s=12, alpha=0.6)
    ax1.axhline(0, color='gray', linewidth=0.5)
    ax1.set_title('Racemic Mixture (Real Spectrum)')
    ax1.set_xlabel('Re(λ)')
    ax1.set_ylabel('Im(λ)')
    ax1.set_ylim(-0.05, 0.05)
    ax1.grid(True, alpha=0.3)
    ax1.text(0.5, 0.9, 'No directed flow possible',
             transform=ax1.transAxes, ha='center',
             fontsize=11, color='gray', style='italic')

    ax2.scatter(np.real(eig_helix), np.imag(eig_helix),
                c='red', s=12, alpha=0.6)
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.set_title('Alpha-Helix (Complex Spectrum Emerged)')
    ax2.set_xlabel('Re(λ)')
    ax2.set_ylabel('Im(λ)')
    ax2.set_ylim(-0.05, 0.05)
    ax2.grid(True, alpha=0.3)
    ax2.text(0.5, 0.9, 'Directed flow activated',
             transform=ax2.transAxes, ha='center',
             fontsize=11, color='red', style='italic')

    plt.suptitle('Fig 1: Chirality as Spectral Symmetry Breaking',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('fig_chirality_phase_transition.png', dpi=150)
    plt.close()
    print()
    print("  Figure saved: fig_chirality_phase_transition.png")


if __name__ == "__main__":
    run_chirality_audit()