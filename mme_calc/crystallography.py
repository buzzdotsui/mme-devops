"""
Module 6 — Crystallography & Defects
Covers Atomic Packing Factor, planar/linear density,
ASTM grain size number, Hall-Petch equation, and Burger's vector.
"""

import math


# ---------------------------------------------------------------------------
# Atomic Packing Factor (APF)
# ---------------------------------------------------------------------------

def apf_bcc(radius):
    """
    APF for BCC: 2 atoms per unit cell, a = 4r / √3
    APF = (2 × 4/3 πr³) / a³ ≈ 0.68
    """
    if radius <= 0:
        raise ValueError("Atomic radius must be positive.")
    a = 4 * radius / math.sqrt(3)
    v_atoms = 2 * (4 / 3) * math.pi * radius ** 3
    v_cell = a ** 3
    return v_atoms / v_cell


def apf_fcc(radius):
    """
    APF for FCC: 4 atoms per unit cell, a = 2√2 r
    APF ≈ 0.74
    """
    if radius <= 0:
        raise ValueError("Atomic radius must be positive.")
    a = 2 * math.sqrt(2) * radius
    v_atoms = 4 * (4 / 3) * math.pi * radius ** 3
    v_cell = a ** 3
    return v_atoms / v_cell


def apf_hcp(radius):
    """
    APF for ideal HCP: 6 atoms per unit cell
    APF ≈ 0.74  (same as FCC for ideal c/a ratio)
    """
    if radius <= 0:
        raise ValueError("Atomic radius must be positive.")
    a = 2 * radius
    c = (4 / math.sqrt(6)) * (2 * radius)  # ideal c/a = √(8/3)
    v_atoms = 6 * (4 / 3) * math.pi * radius ** 3
    # HCP unit cell volume = (3√3 / 2) × a² × c
    v_cell = (3 * math.sqrt(3) / 2) * a ** 2 * c
    return v_atoms / v_cell


def apf_simple_cubic(radius):
    """
    APF for Simple Cubic: 1 atom per unit cell, a = 2r
    APF ≈ 0.524
    """
    if radius <= 0:
        raise ValueError("Atomic radius must be positive.")
    a = 2 * radius
    v_atoms = (4 / 3) * math.pi * radius ** 3
    v_cell = a ** 3
    return v_atoms / v_cell


# ---------------------------------------------------------------------------
# Planar Density & Linear Density
# ---------------------------------------------------------------------------

def planar_density(atoms_on_plane, plane_area):
    """
    Planar density = number of atoms centered on a plane / area of the plane.
    Units: atoms/unit_area
    """
    if plane_area <= 0:
        raise ValueError("Plane area must be positive.")
    return atoms_on_plane / plane_area


def linear_density(atoms_on_direction, direction_length):
    """
    Linear density = number of atoms centered on a direction / length.
    Units: atoms/unit_length
    """
    if direction_length <= 0:
        raise ValueError("Direction length must be positive.")
    return atoms_on_direction / direction_length


# ---------------------------------------------------------------------------
# ASTM Grain Size Number
# ---------------------------------------------------------------------------

def astm_grain_count(n):
    """
    N = 2^(n − 1)
    Number of grains per square inch at 100× magnification.
    n — ASTM grain size number.
    """
    return 2 ** (n - 1)


def astm_grain_number_from_count(grain_count):
    """
    Solve for ASTM grain size number:  n = 1 + log₂(N)
    """
    if grain_count <= 0:
        raise ValueError("Grain count must be positive.")
    return 1 + math.log2(grain_count)


# ---------------------------------------------------------------------------
# Hall-Petch Equation
# ---------------------------------------------------------------------------

def hall_petch(sigma_0, ky, d):
    """
    Hall-Petch: σ_y = σ₀ + k_y / √d

    sigma_0 — friction stress / lattice resistance (MPa)
    ky      — Hall-Petch slope (MPa·√m or MPa·√mm)
    d       — average grain diameter (same length unit as ky)

    Returns yield strength σ_y.
    """
    if d <= 0:
        raise ValueError("Grain diameter must be positive.")
    return sigma_0 + ky / math.sqrt(d)


# ---------------------------------------------------------------------------
# Burger's Vector
# ---------------------------------------------------------------------------

def burgers_vector_magnitude(a, h, k, l):
    """
    |b| = (a/2) × √(h² + k² + l²)

    For common slip systems:
      FCC: b = (a/2)<110>  → |b| = a/√2
      BCC: b = (a/2)<111>  → |b| = a√3/2
    """
    if a <= 0:
        raise ValueError("Lattice parameter must be positive.")
    return (a / 2) * math.sqrt(h ** 2 + k ** 2 + l ** 2)
