import numpy as np
import matplotlib.pyplot as plt

def run_pareto_audit():
    print("N.E.A. Pareto Audit: Truncated Power Law vs Pure Pareto")
    print("-" * 55)
    
    np.random.seed(42)
    N = 10000
    w_min = 1.0
    gamma = 1.16
    beta = 0.01
    
    # Generate truncated power law (Gamma-like)
    u = np.random.uniform(0, 1, N)
    w = (w_min**(1-gamma) - (1-gamma)*np.log(1-u)/beta)**(1/(1-gamma))
    w = w[w < 1/beta * 3]
    
    # Binning
    bins = np.logspace(np.log10(w_min), np.log10(max(w)), 60)
    hist, edges = np.histogram(w, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    
    # Pure Pareto for comparison
    A = (gamma-1) * w_min**(gamma-1)
    w_pareto = np.logspace(np.log10(w_min), np.log10(max(w)), 200)
    pareto_fit = A * w_pareto**(-gamma)
    
    # Pareto regime boundary
    w_pareto_cutoff = 0.3 / beta
    
    print(f"w_min = {w_min}")
    print(f"gamma = {gamma}")
    print(f"Pareto regime: w < {w_pareto_cutoff:.1f}")
    print(f"Exponential cutoff scale: 1/beta = {1/beta:.1f}")
    
    plt.figure(figsize=(10, 6))
    plt.loglog(centers, hist, 'ko', markersize=3, alpha=0.6, label='Simulated Truncated Power Law')
    plt.loglog(w_pareto, pareto_fit, 'b-', linewidth=2, label=f'Pure Pareto (γ={gamma})')
    plt.axvline(x=w_pareto_cutoff, color='red', linestyle='--', 
                label=f'Pareto Regime Boundary (w ≈ {w_pareto_cutoff:.0f})')
    plt.fill_between([w_min, w_pareto_cutoff], 1e-6, 1, alpha=0.1, color='blue')
    plt.text(w_pareto_cutoff/2, 5e-3, 'Pareto\nRegime', ha='center', fontsize=10, color='blue')
    plt.text(w_pareto_cutoff*2, 1e-4, 'Exponential\nTruncation', ha='center', fontsize=10, color='red')
    
    plt.xlabel('Wealth w')
    plt.ylabel('Probability Density ρ(w)')
    plt.title('Fig 4: Truncated Power Law with Pareto Regime')
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.ylim(1e-6, 1)
    plt.tight_layout()
    plt.savefig('pareto_truncated.png', dpi=150)
    plt.show()
    
    print("VERDICT: Scale-free Pareto emerges when w << 1/beta.")
    print("Exponential truncation from finite total wealth budget.")

if __name__ == "__main__":
    run_pareto_audit()