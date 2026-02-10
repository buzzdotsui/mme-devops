"""
Module 3 — Phase Transformations
Covers the Lever Rule, Gibbs Phase Rule, Avrami kinetics,
Carbon Equivalent (weldability), and Scheil micro-segregation.
"""

import math


def lever_rule(c0, c_alpha, c_beta):
    """
    Lever Rule — weight fraction of phase α in a two-phase region.
    W_α = (C_β − C₀) / (C_β − C_α)
    W_β = 1 − W_α

    c0      — overall composition
    c_alpha — composition of phase α boundary
    c_beta  — composition of phase β boundary

    Returns (W_alpha, W_beta).
    """
    denom = c_beta - c_alpha
    if denom == 0:
        raise ValueError("Phase boundary compositions must differ.")
    w_alpha = (c_beta - c0) / denom
    w_beta = 1 - w_alpha
    return w_alpha, w_beta


def gibbs_phase_rule(components, phases):
    """
    Gibbs Phase Rule: F = C − P + 2
    Returns degrees of freedom F.
    """
    if components < 1 or phases < 1:
        raise ValueError("Components and phases must be ≥ 1.")
    f = components - phases + 2
    if f < 0:
        raise ValueError("Invalid system: degrees of freedom cannot be negative.")
    return f


def avrami_fraction(k, t, n):
    """
    Avrami Equation: Y = 1 − exp(−k × t^n)
    Returns fraction transformed Y.

    k — rate constant
    t — time
    n — Avrami exponent
    """
    if t < 0:
        raise ValueError("Time must be non-negative.")
    if k < 0:
        raise ValueError("Rate constant k must be non-negative.")
    return 1 - math.exp(-k * (t ** n))


def carbon_equivalent(c, mn=0, cr=0, mo=0, v=0, ni=0, cu=0):
    """
    IIW Carbon Equivalent for weldability assessment:
    CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15

    All values in wt%.
    CE < 0.40 → good weldability
    CE 0.40–0.60 → fair (preheat recommended)
    CE > 0.60 → poor (high preheat / special procedures)
    """
    ce = c + mn / 6 + (cr + mo + v) / 5 + (ni + cu) / 15
    return ce


def scheil_equation(k, c0, fs):
    """
    Scheil Equation for micro-segregation during solidification:
    C_s = k × C₀ × (1 − f_s)^(k − 1)

    k  — partition coefficient
    c0 — initial (nominal) composition
    fs — fraction solid (0 ≤ fs < 1)

    Returns solute concentration in the solid at fraction fs.
    """
    if fs < 0 or fs >= 1:
        raise ValueError("Fraction solid must be in [0, 1).")
    if k <= 0:
        raise ValueError("Partition coefficient must be positive.")
    return k * c0 * ((1 - fs) ** (k - 1))
