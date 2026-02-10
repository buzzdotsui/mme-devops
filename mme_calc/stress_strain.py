"""
Module 8 — Stress & Strain Analysis
Covers Hooke's Law, Poisson's ratio, shear modulus, von Mises stress,
Factor of Safety, stress concentration, and steady-state creep.
"""

import math


def hookes_law_stress(E, strain):
    """σ = E × ε  (Hooke's Law — uniaxial)."""
    return E * strain


def hookes_law_strain(E, stress):
    """ε = σ / E  (Hooke's Law — solve for strain)."""
    if E <= 0:
        raise ValueError("Young's modulus must be positive.")
    return stress / E


def poisson_strain(nu, axial_strain):
    """
    Lateral strain from Poisson's ratio:
    ε_lateral = −ν × ε_axial
    """
    return -nu * axial_strain


def shear_modulus(E, nu):
    """
    G = E / [2(1 + ν)]
    Relationship between Young's modulus, shear modulus, and Poisson's ratio.
    """
    if (1 + nu) == 0:
        raise ValueError("(1 + ν) must not be zero.")
    return E / (2 * (1 + nu))


def bulk_modulus(E, nu):
    """
    K = E / [3(1 − 2ν)]
    """
    denom = 3 * (1 - 2 * nu)
    if denom == 0:
        raise ValueError("(1 − 2ν) must not be zero (ν ≠ 0.5).")
    return E / denom


def von_mises_stress(s1, s2, s3):
    """
    von Mises equivalent stress (principal stresses):
    σ_vm = √(½[(σ₁−σ₂)² + (σ₂−σ₃)² + (σ₃−σ₁)²])
    """
    return math.sqrt(0.5 * ((s1 - s2)**2 + (s2 - s3)**2 + (s3 - s1)**2))


def factor_of_safety(yield_strength, applied_stress):
    """
    FoS = σ_yield / σ_applied
    FoS > 1 → safe;  FoS < 1 → failure expected.
    """
    if applied_stress == 0:
        raise ValueError("Applied stress must not be zero.")
    return yield_strength / applied_stress


def stress_concentration(kt, nominal_stress):
    """
    σ_max = K_t × σ_nom
    kt — stress concentration factor (from geometry / charts).
    """
    return kt * nominal_stress


def creep_rate_steady_state(A, stress, n, Q, R, T):
    """
    Norton / power-law creep (steady-state):
    ε̇ = A × σⁿ × exp(−Q / RT)

    A — material constant
    n — stress exponent
    Q — activation energy (J/mol)
    R — gas constant (8.314 J/mol·K)
    T — absolute temperature (K)
    """
    if T <= 0:
        raise ValueError("Temperature must be positive (Kelvin).")
    return A * (stress ** n) * math.exp(-Q / (R * T))
