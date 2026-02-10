"""
Module 5 — Casting & Solidification
Covers Chvorinov's Rule, riser modulus design, shrinkage allowance,
fluidity index, and Newtonian cooling rate.
"""

import math


def chvorinov_solidification_time(B, volume, surface_area, n=2):
    """
    Chvorinov's Rule: t_s = B × (V / A)^n

    B            — mold constant (s/m² or s/cm²)
    volume       — casting volume
    surface_area — casting surface area
    n            — exponent (default 2)

    Returns solidification time.
    """
    if surface_area <= 0 or volume <= 0:
        raise ValueError("Volume and surface area must be positive.")
    if B <= 0:
        raise ValueError("Mold constant must be positive.")
    return B * (volume / surface_area) ** n


def casting_modulus(volume, surface_area):
    """
    Casting / riser modulus: M = V / A
    Used in riser design — riser modulus must exceed casting modulus.
    """
    if surface_area <= 0:
        raise ValueError("Surface area must be positive.")
    return volume / surface_area


def shrinkage_allowance(length, shrinkage_pct):
    """
    Pattern dimension with shrinkage allowance.
    Pattern length = L × (1 + shrinkage% / 100)

    Typical values:
      Cast iron     ~ 1.0%
      Steel         ~ 2.0%
      Aluminium     ~ 1.3%
      Brass/Bronze  ~ 1.5%
    """
    if length <= 0:
        raise ValueError("Length must be positive.")
    return length * (1 + shrinkage_pct / 100)


def fluidity_index(rho, cp, delta_t_superheat, latent_heat):
    """
    Simplified fluidity index:
    f = ρ × c_p × ΔT_superheat / L_f

    Higher values → better fluidity.
    """
    if latent_heat <= 0:
        raise ValueError("Latent heat must be positive.")
    return (rho * cp * delta_t_superheat) / latent_heat


def newtonian_cooling_rate(h, area, rho, cp, volume, t_current, t_ambient):
    """
    Newtonian (lumped-capacitance) cooling rate:
    dT/dt = -[h × A / (ρ × c_p × V)] × (T − T_∞)

    Returns rate of temperature change (K/s or °C/s), negative = cooling.
    """
    if volume <= 0 or rho <= 0 or cp <= 0:
        raise ValueError("Volume, density, and specific heat must be positive.")
    biot_group = (h * area) / (rho * cp * volume)
    return -biot_group * (t_current - t_ambient)
