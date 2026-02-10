"""
Module 9 — Visualizations
Uses Matplotlib to generate engineering plots.
"""

import math
import matplotlib.pyplot as plt
import numpy as np

def plot_stress_strain(E, sigma_y, sigma_uts, strain_failure, filename=None, show=True):
    """
    Generate a simplified engineering stress-strain curve.
    
    Curve construction:
    1. Linear elastic region: (0, 0) to (ε_y, σ_y) where ε_y = σ_y / E
    2. Plastic region: Approximated by power law σ = K * ε^n passing through yield and UTS.
       For simplicity here, we use a cubic spline or simple polynomial fit 
       from (ε_y, σ_y) to (ε_uts, σ_uts) to (ε_f, σ_fracture).
       
    SIMPLIFIED MODEL for visualization:
    - Elastic part: Straight line.
    - Plastic part: Parabolic arc to UTS, then slight drop to fracture.
    """
    
    # 1. Elastic Region
    epsilon_y = sigma_y / E
    
    # 2. Plastic Region (Simplified)
    # Assume UTS happens at 0.5 * (epsilon_y + strain_failure) or some reasonable ductility?
    # Actually, let's assume strain_failure IS the fracture point.
    # Let's assume UTS happens at roughly strain_failure if ductile, or slightly before.
    # For a generic curve, let's place UTS at 2/3 of ductility range
    epsilon_uts = epsilon_y + 0.7 * (strain_failure - epsilon_y)
    
    # Create data points
    # Elastic
    strain_elastic = np.linspace(0, epsilon_y, 20)
    stress_elastic = strain_elastic * E
    
    # Plastic to UTS (Power law hardening approximation)
    # σ = K * ε^n
    # Matched at yield: σ_y = K * ε_y^n  => K = σ_y / ε_y^n
    # Matched at UTS:   σ_uts = K * ε_uts^n
    # Divide: σ_uts / σ_y = (ε_uts / ε_y)^n  => n = log(σ_uts / σ_y) / log(ε_uts / ε_y)
    if epsilon_uts > epsilon_y and sigma_uts > sigma_y:
        try:
            n = math.log(sigma_uts / sigma_y) / math.log(epsilon_uts / epsilon_y)
            K = sigma_y / (epsilon_y ** n)
            strain_plastic1 = np.linspace(epsilon_y, epsilon_uts, 50)
            stress_plastic1 = K * (strain_plastic1 ** n)
        except ValueError:
            # Fallback linear if log fails
            strain_plastic1 = np.linspace(epsilon_y, epsilon_uts, 2)
            stress_plastic1 = np.linspace(sigma_y, sigma_uts, 2)
    else:
        # Perfectly plastic or brittle
        strain_plastic1 = np.linspace(epsilon_y, epsilon_uts, 2)
        stress_plastic1 = np.linspace(sigma_y, sigma_uts, 2)

    # Plastic post-UTS (Necking - slight drop)
    # Just a simple curve down to failure
    sigma_f = sigma_uts * 0.85 # Assume fracture stress is lower due to necking (eng stress)
    strain_necking = np.linspace(epsilon_uts, strain_failure, 20)
    # Parabolic drop
    # σ = a(ε - ε_uts)^2 + σ_uts
    # fit matching (ε_f, σ_f)
    if strain_failure > epsilon_uts:
        a = (sigma_f - sigma_uts) / ((strain_failure - epsilon_uts) ** 2)
        stress_necking = a * (strain_necking - epsilon_uts)**2 + sigma_uts
    else:
        strain_necking = np.array([epsilon_uts])
        stress_necking = np.array([sigma_uts])

    # Assemble
    strain_all = np.concatenate([strain_elastic, strain_plastic1[1:], strain_necking[1:]])
    stress_all = np.concatenate([stress_elastic, stress_plastic1[1:], stress_necking[1:]])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(strain_all, stress_all, 'b-', linewidth=2, label='Engineering Stress-Strain')
    
    # Annotate key points
    plt.plot(epsilon_y, sigma_y, 'go')
    plt.text(epsilon_y, sigma_y, f' Yield\n ({epsilon_y:.4f}, {sigma_y:.0f})', verticalalignment='top')
    
    plt.plot(epsilon_uts, sigma_uts, 'ro')
    plt.text(epsilon_uts, sigma_uts, f' UTS\n ({epsilon_uts:.4f}, {sigma_uts:.0f})', verticalalignment='bottom')
    
    plt.plot(strain_failure, sigma_f, 'kx')
    plt.text(strain_failure, sigma_f, f' Fracture\n ({strain_failure:.4f}, {sigma_f:.0f})', verticalalignment='bottom')

    plt.title(f"Theoretical Stress-Strain Curve\nE={E/1000:.1f} GPa, Yield={sigma_y} MPa, UTS={sigma_uts} MPa")
    plt.xlabel("Strain (ε)")
    plt.ylabel("Stress (MPa)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    if filename:
        plt.savefig(filename)
        print(f"  💾 Plot saved to {filename}")
        
    if show:
        plt.show()
    else:
        plt.close()


def plot_cooling_curve(T_initial, T_ambient, k_cooling, duration, filename=None, show=True):
    """
    Plot Newton's Law of Cooling: T(t) = T_inf + (T_0 - T_inf) * exp(-k*t)
    """
    t = np.linspace(0, duration, 100)
    T = T_ambient + (T_initial - T_ambient) * np.exp(-k_cooling * t)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, T, 'r-', linewidth=2, label='Temperature')
    plt.axhline(y=T_ambient, color='b', linestyle='--', label='Ambient Temp')
    
    plt.title(f"Cooling Curve (Newton's Law)\nT0={T_initial}, T_inf={T_ambient}, k={k_cooling}")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature")
    plt.grid(True, alpha=0.7)
    plt.legend()
    
    if filename:
        plt.savefig(filename)
        print(f"  💾 Plot saved to {filename}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_hardness_conversion(show_lines=True, filename=None, show=True):
    """
    Plot the empirical relationship between HRC and Brinell Hardness (HB).
    """
    # Approximate data points from standard hardness conversion tables
    # HRC values 20 to 65
    hrc_data = np.arange(20, 66, 1)
    
    def approximate_hb(hrc):
        # A rough polynomial fit for standard steel conversion tables
        return 115 + 4.8 * hrc + 0.08 * hrc**2

    hb_data = approximate_hb(hrc_data)
    
    plt.figure(figsize=(10, 6))
    plt.plot(hrc_data, hb_data, 'g-', linewidth=2, label='Approx. HRC vs HB')
    
    plt.title("Hardness Conversion Chart (Approximate)")
    plt.xlabel("Rockwell C Hardness (HRC)")
    plt.ylabel("Brinell Hardness (HB)")
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    if show_lines:
        plt.axvline(x=40, color='k', linestyle=':', alpha=0.5)
        plt.axhline(y=approximate_hb(40), color='k', linestyle=':', alpha=0.5)

    if filename:
        plt.savefig(filename)
        print(f"  💾 Plot saved to {filename}")
        
    if show:
        plt.show()
    else:
        plt.close()
