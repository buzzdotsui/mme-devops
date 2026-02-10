"""
Module 4 — Corrosion & Degradation
Covers corrosion rate (mpy/mm-per-year), Pilling-Bedworth Ratio,
galvanic series potential, and parabolic oxidation kinetics.
"""

import math

# ---------------------------------------------------------------------------
# Corrosion Rate
# ---------------------------------------------------------------------------

def corrosion_rate_mpy(weight_loss, density, area, time_hours):
    """
    Corrosion rate in mils per year (mpy).
    CR = (K × W) / (A × T × D)

    K = 3.45 × 10⁶  (constant for mpy when W in g, A in cm², T in hours, D in g/cm³)
    weight_loss — mass loss (g)
    density     — material density (g/cm³)
    area        — exposed area (cm²)
    time_hours  — exposure time (hours)
    """
    K = 3.45e6
    if area <= 0 or time_hours <= 0 or density <= 0:
        raise ValueError("Area, time, and density must be positive.")
    return (K * weight_loss) / (area * time_hours * density)


def corrosion_rate_mmpy(weight_loss, density, area, time_hours):
    """
    Corrosion rate in mm per year (mm/y).
    CR = (8.76 × 10⁴ × W) / (A × T × D)
    Same parameter units as mpy version.
    """
    K = 8.76e4
    if area <= 0 or time_hours <= 0 or density <= 0:
        raise ValueError("Area, time, and density must be positive.")
    return (K * weight_loss) / (area * time_hours * density)


# ---------------------------------------------------------------------------
# Pilling-Bedworth Ratio
# ---------------------------------------------------------------------------

def pilling_bedworth_ratio(m_oxide, rho_metal, n, m_metal, rho_oxide):
    """
    PBR = (M_oxide × ρ_metal) / (n × M_metal × ρ_oxide)

    m_oxide   — molar mass of oxide (g/mol)
    rho_metal — density of metal (g/cm³)
    n         — number of metal atoms per formula unit of oxide
    m_metal   — molar mass of metal (g/mol)
    rho_oxide — density of oxide (g/cm³)

    PBR < 1  → porous, non-protective oxide
    PBR 1–2  → protective oxide
    PBR > 2  → oxide tends to spall / crack
    """
    denom = n * m_metal * rho_oxide
    if denom <= 0:
        raise ValueError("All parameters must be positive.")
    return (m_oxide * rho_metal) / denom


# ---------------------------------------------------------------------------
# Galvanic Series — simplified lookup
# ---------------------------------------------------------------------------

# Approximate corrosion potential in seawater (V vs SCE), more negative = more anodic
_GALVANIC_POTENTIALS = {
    "magnesium":       -1.60,
    "zinc":            -1.03,
    "aluminium":       -0.76,
    "mild_steel":      -0.60,
    "cast_iron":       -0.50,
    "stainless_304":   -0.08,
    "stainless_316":   -0.05,
    "copper":           -0.20,
    "brass":           -0.30,
    "nickel":          -0.12,
    "silver":          -0.02,
    "titanium":        -0.05,
    "gold":             0.18,
    "platinum":         0.22,
}


def galvanic_potential_diff(metal_a, metal_b):
    """
    Return the galvanic potential difference between two metals.
    The more negative metal is the anode (corrodes preferentially).

    Returns (potential_diff, anode, cathode).
    """
    a_key = metal_a.lower().replace(" ", "_")
    b_key = metal_b.lower().replace(" ", "_")
    if a_key not in _GALVANIC_POTENTIALS:
        raise ValueError(f"Unknown metal: {metal_a}. Available: {list(_GALVANIC_POTENTIALS.keys())}")
    if b_key not in _GALVANIC_POTENTIALS:
        raise ValueError(f"Unknown metal: {metal_b}. Available: {list(_GALVANIC_POTENTIALS.keys())}")

    va = _GALVANIC_POTENTIALS[a_key]
    vb = _GALVANIC_POTENTIALS[b_key]
    diff = abs(va - vb)
    anode = metal_a if va < vb else metal_b
    cathode = metal_b if va < vb else metal_a
    return diff, anode, cathode


def available_metals():
    """Return list of metals available for galvanic series lookup."""
    return list(_GALVANIC_POTENTIALS.keys())


# ---------------------------------------------------------------------------
# Parabolic Oxidation Kinetics
# ---------------------------------------------------------------------------

def parabolic_oxide_thickness(kp, time):
    """
    Parabolic oxidation: x² = k_p × t  →  x = √(k_p × t)
    kp   — parabolic rate constant (units² / time)
    time — exposure time
    Returns oxide thickness x.
    """
    if kp < 0 or time < 0:
        raise ValueError("Rate constant and time must be non-negative.")
    return math.sqrt(kp * time)
