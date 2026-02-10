"""
Module 7 — Composite Materials
Covers Rule of Mixtures (longitudinal & transverse), composite density,
critical fiber length, and Halpin-Tsai equation.
"""


def rule_of_mixtures_longitudinal(e_fiber, v_fiber, e_matrix):
    """
    Rule of Mixtures (iso-strain / Voigt model):
    E_c = E_f × V_f + E_m × (1 − V_f)

    Also applies to strength:
    σ_c = σ_f × V_f + σ_m × (1 − V_f)
    """
    if not 0 <= v_fiber <= 1:
        raise ValueError("Fiber volume fraction must be between 0 and 1.")
    return e_fiber * v_fiber + e_matrix * (1 - v_fiber)


def rule_of_mixtures_transverse(e_fiber, v_fiber, e_matrix):
    """
    Inverse Rule of Mixtures (iso-stress / Reuss model):
    1/E_c = V_f/E_f + V_m/E_m
    """
    if not 0 <= v_fiber <= 1:
        raise ValueError("Fiber volume fraction must be between 0 and 1.")
    if e_fiber <= 0 or e_matrix <= 0:
        raise ValueError("Moduli must be positive.")
    v_matrix = 1 - v_fiber
    return 1 / (v_fiber / e_fiber + v_matrix / e_matrix)


def composite_density(rho_fiber, v_fiber, rho_matrix):
    """
    ρ_c = ρ_f × V_f + ρ_m × (1 − V_f)
    """
    if not 0 <= v_fiber <= 1:
        raise ValueError("Fiber volume fraction must be between 0 and 1.")
    return rho_fiber * v_fiber + rho_matrix * (1 - v_fiber)


def critical_fiber_length(sigma_f, d, tau_c):
    """
    Critical fiber length: l_c = (σ_f × d) / (2 × τ_c)

    sigma_f — fiber ultimate strength
    d       — fiber diameter
    tau_c   — fiber-matrix interfacial shear strength

    Fibers longer than l_c carry load effectively.
    """
    if tau_c <= 0 or d <= 0:
        raise ValueError("Fiber diameter and shear strength must be positive.")
    return (sigma_f * d) / (2 * tau_c)


def halpin_tsai(e_matrix, e_fiber, v_fiber, xi=2):
    """
    Halpin-Tsai equation for transverse / shear modulus:
    η = [(E_f/E_m) − 1] / [(E_f/E_m) + ξ]
    E_c = E_m × (1 + ξ η V_f) / (1 − η V_f)

    xi — reinforcement geometry parameter (default 2 for circular fibers, transverse).
    """
    if not 0 <= v_fiber <= 1:
        raise ValueError("Fiber volume fraction must be between 0 and 1.")
    if e_matrix <= 0 or e_fiber <= 0:
        raise ValueError("Moduli must be positive.")
    ratio = e_fiber / e_matrix
    eta = (ratio - 1) / (ratio + xi)
    return e_matrix * (1 + xi * eta * v_fiber) / (1 - eta * v_fiber)
