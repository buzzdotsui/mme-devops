"""
Module 1 — Mechanical Properties
Covers hardness conversions, tensile/yield strength, ductility measures,
true stress-strain, resilience, fatigue, and impact toughness.
"""

import math

# ---------------------------------------------------------------------------
# Hardness ↔ Tensile Strength
# ---------------------------------------------------------------------------

def brinell_to_tensile(hb):
    """Estimate UTS (MPa) from Brinell Hardness: UTS ≈ 3.45 × HB."""
    if hb <= 0:
        raise ValueError("Brinell Hardness must be positive.")
    return 3.45 * hb


def vickers_to_tensile(hv):
    """Estimate UTS (MPa) from Vickers Hardness: UTS ≈ 3.18 × HV."""
    if hv <= 0:
        raise ValueError("Vickers Hardness must be positive.")
    return 3.18 * hv


# Approximate HB ↔ HRC conversion (valid for HRC 20-55 range)
_HRC_HB_TABLE = [
    (20, 226), (21, 231), (22, 237), (23, 243), (24, 247),
    (25, 253), (26, 258), (27, 264), (28, 271), (29, 279),
    (30, 286), (31, 294), (32, 301), (33, 311), (34, 319),
    (35, 327), (36, 336), (37, 344), (38, 353), (39, 362),
    (40, 371), (41, 381), (42, 390), (43, 400), (44, 409),
    (45, 421), (46, 432), (47, 442), (48, 453), (49, 465),
    (50, 477), (51, 489), (52, 500), (53, 514), (54, 528),
    (55, 545),
]


def hrc_to_hb(hrc):
    """Convert Rockwell C hardness to approximate Brinell Hardness (lookup + interpolation)."""
    if hrc < 20 or hrc > 55:
        raise ValueError("HRC must be in the range 20–55 for reliable conversion.")
    for i in range(len(_HRC_HB_TABLE) - 1):
        rc1, hb1 = _HRC_HB_TABLE[i]
        rc2, hb2 = _HRC_HB_TABLE[i + 1]
        if rc1 <= hrc <= rc2:
            frac = (hrc - rc1) / (rc2 - rc1)
            return hb1 + frac * (hb2 - hb1)
    return _HRC_HB_TABLE[-1][1]


def hb_to_hrc(hb):
    """Convert Brinell Hardness to approximate Rockwell C (lookup + interpolation)."""
    if hb < 226 or hb > 545:
        raise ValueError("HB must be in the range 226–545 for reliable HRC conversion.")
    for i in range(len(_HRC_HB_TABLE) - 1):
        rc1, hb1 = _HRC_HB_TABLE[i]
        rc2, hb2 = _HRC_HB_TABLE[i + 1]
        if hb1 <= hb <= hb2:
            frac = (hb - hb1) / (hb2 - hb1)
            return rc1 + frac * (rc2 - rc1)
    return _HRC_HB_TABLE[-1][0]


# ---------------------------------------------------------------------------
# Yield Strength
# ---------------------------------------------------------------------------

def yield_strength(force, area):
    """Calculate engineering yield strength σ_y = F / A₀ (MPa if F in N, A in mm²)."""
    if area <= 0:
        raise ValueError("Cross-sectional area must be positive.")
    return force / area


# ---------------------------------------------------------------------------
# Ductility
# ---------------------------------------------------------------------------

def percent_elongation(l0, lf):
    """Percent elongation = (L_f − L₀) / L₀ × 100."""
    if l0 <= 0:
        raise ValueError("Original gauge length must be positive.")
    return ((lf - l0) / l0) * 100


def percent_reduction_area(a0, af):
    """Percent reduction in area = (A₀ − A_f) / A₀ × 100."""
    if a0 <= 0:
        raise ValueError("Original area must be positive.")
    return ((a0 - af) / a0) * 100


# ---------------------------------------------------------------------------
# True Stress / True Strain
# ---------------------------------------------------------------------------

def true_stress(engineering_stress, engineering_strain):
    """σ_true = σ_eng × (1 + ε_eng)."""
    return engineering_stress * (1 + engineering_strain)


def true_strain(engineering_strain):
    """ε_true = ln(1 + ε_eng)."""
    if engineering_strain <= -1:
        raise ValueError("Engineering strain must be > -1.")
    return math.log(1 + engineering_strain)


# ---------------------------------------------------------------------------
# Resilience
# ---------------------------------------------------------------------------

def modulus_of_resilience(yield_stress, youngs_modulus):
    """U_r = σ_y² / (2E)  (energy per unit volume)."""
    if youngs_modulus <= 0:
        raise ValueError("Young's modulus must be positive.")
    return (yield_stress ** 2) / (2 * youngs_modulus)


# ---------------------------------------------------------------------------
# Fatigue — Basquin's Equation
# ---------------------------------------------------------------------------

def basquin_fatigue_life(stress_amplitude, sigma_f_prime, b_exponent):
    """
    Basquin's equation:  σ_a = σ_f' × (2N)^b
    Solve for N:  N = 0.5 × (σ_a / σ_f')^(1/b)
    Returns number of cycles to failure.
    """
    if sigma_f_prime <= 0 or stress_amplitude <= 0:
        raise ValueError("Stress values must be positive.")
    if b_exponent >= 0:
        raise ValueError("Basquin exponent b must be negative.")
    return 0.5 * (stress_amplitude / sigma_f_prime) ** (1 / b_exponent)


def basquin_stress_amplitude(sigma_f_prime, n_cycles, b_exponent):
    """σ_a = σ_f' × (2N)^b — given cycles, find allowable stress amplitude."""
    if n_cycles <= 0:
        raise ValueError("Number of cycles must be positive.")
    return sigma_f_prime * (2 * n_cycles) ** b_exponent


# ---------------------------------------------------------------------------
# Impact Toughness (Charpy)
# ---------------------------------------------------------------------------

def charpy_toughness(absorbed_energy, cross_section_area):
    """Impact toughness = absorbed energy / cross-section area (J/mm² or J/m²)."""
    if cross_section_area <= 0:
        raise ValueError("Cross-section area must be positive.")
    return absorbed_energy / cross_section_area
