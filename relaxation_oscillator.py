import numpy as np
import matplotlib.pyplot as plt

def simulate_relaxation_oscillator(T=500, H_start=1.35, H_crash=2.0, 
                                    decay_rate=0.008, innovation_burst=0.15):
    t = np.arange(T)
    H = np.zeros(T)
    H[0] = H_start
    
    np.random.seed(42)
    crash_times = []
    
    for i in range(1, T):
        dH = decay_rate * (1 + 0.3 * np.random.randn())
        H[i] = H[i-1] + dH
        
        if H[i] >= H_crash:
            crash_times.append(i)
            H[i] = H_start + 0.05 * np.random.randn()
    
    return t, H, crash_times

def run_oscillator_audit():
    print("N.E.A. Relaxation Oscillator Audit: Civilizational Cycles")
    print("-" * 55)
    
    T = 500
    
    # Resilient civilization: moderate decay, strong innovation bursts
    t1, H1, crashes1 = simulate_relaxation_oscillator(
        T=T, H_start=1.35, H_crash=1.95, decay_rate=0.006, innovation_burst=0.1)
    
    # Involuted civilization: rapid decay, weak bursts
    t2, H2, crashes2 = simulate_relaxation_oscillator(
        T=T, H_start=1.35, H_crash=1.85, decay_rate=0.012, innovation_burst=0.05)
    
    print(f"Resilient system: {len(crashes1)} crashes, avg period = {T/len(crashes1):.0f} yrs")
    print(f"Involuted system: {len(crashes2)} crashes, avg period = {T/len(crashes2):.0f} yrs")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
    
    # Panel 1: Resilient
    ax1.plot(t1, H1, 'g-', linewidth=1.5, alpha=0.8)
    for ct in crashes1:
        ax1.axvline(x=ct, color='green', linestyle=':', alpha=0.3)
    ax1.axhline(y=1.95, color='darkgreen', linestyle='--', alpha=0.7, label='H_crash = 1.95 ZY')
    ax1.axhline(y=1.35, color='blue', linestyle=':', alpha=0.5, label='H_start = 1.35 ZY')
    ax1.set_ylabel('System Enthalpy H (ZY)')
    ax1.set_title('Resilient Civilization (Moderate Decay, Moderate Innovation)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.2)
    ax1.set_ylim(1.3, 2.1)
    
    # Panel 2: Involuted
    ax2.plot(t2, H2, 'r-', linewidth=1.5, alpha=0.8)
    for ct in crashes2:
        ax2.axvline(x=ct, color='red', linestyle=':', alpha=0.3)
    ax2.axhline(y=1.85, color='darkred', linestyle='--', alpha=0.7, label='H_crash = 1.85 ZY')
    ax2.axhline(y=1.35, color='blue', linestyle=':', alpha=0.5, label='H_start = 1.35 ZY')
    ax2.set_xlabel('Time (arbitrary evolutionary steps)')
    ax2.set_ylabel('System Enthalpy H (ZY)')
    ax2.set_title('Involuted Civilization (Rapid Decay, Weak Innovation)')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.2)
    ax2.set_ylim(1.3, 2.1)
    
    plt.suptitle('Fig 5: Relaxation Oscillator — Civilizational Phase Transitions', 
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('relaxation_oscillator.png', dpi=150)
    plt.show()
    
    # Phase annotation
    print("\nThree phases of each cycle:")
    print("  [1] Innovation (H decreases): anisotropic arbitrage dominates")
    print("  [2] Decay (H increases): isotropic debt accumulation")
    print("  [3] Reset (H crashes to baseline): phase transition / revolution")

if __name__ == "__main__":
    run_oscillator_audit()