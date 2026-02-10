"""
Module 2 — Thermal Properties
Covers heat conduction (Fourier), thermal expansion, composite slab conduction,
Newton's law of cooling, and thermal diffusivity.
"""


def fourier_heat_flux(k, dt, dx):
    """
    Fourier's Law: q = -k × (dT/dx)
    Returns heat flux magnitude (W/m²).
    k  — thermal conductivity (W/m·K)
    dt — temperature difference (K or °C)
    dx — thickness / distance (m)
    """
    if dx <= 0:
        raise ValueError("Distance dx must be positive.")
    if k <= 0:
        raise ValueError("Thermal conductivity must be positive.")
    return k * abs(dt) / dx


def linear_thermal_expansion(alpha, l0, delta_t):
    """
    ΔL = α × L₀ × ΔT
    alpha  — coefficient of linear expansion (1/K)
    l0     — original length
    delta_t — temperature change
    Returns change in length (same units as l0).
    """
    if l0 <= 0:
        raise ValueError("Original length must be positive.")
    return alpha * l0 * delta_t


def volumetric_thermal_expansion(alpha, v0, delta_t):
    """
    ΔV ≈ 3α × V₀ × ΔT   (isotropic material approximation)
    Returns change in volume.
    """
    if v0 <= 0:
        raise ValueError("Original volume must be positive.")
    return 3 * alpha * v0 * delta_t


def composite_slab_heat_flux(delta_t, layers):
    """
    Steady-state heat flux through series composite slab.
    q = ΔT / Σ(L_i / k_i)

    layers — list of (thickness_m, conductivity_W_per_mK) tuples.
    Returns heat flux in W/m².
    """
    if not layers:
        raise ValueError("At least one layer is required.")
    total_resistance = sum(l / k for l, k in layers)
    if total_resistance <= 0:
        raise ValueError("Total thermal resistance must be positive.")
    return abs(delta_t) / total_resistance


def newton_cooling(h, area, t_surface, t_ambient):
    """
    Newton's Law of Cooling: Q̇ = h × A × (T_s − T_∞)
    Returns heat transfer rate (W).
    h — convective heat transfer coefficient (W/m²·K)
    """
    if area <= 0:
        raise ValueError("Surface area must be positive.")
    return h * area * (t_surface - t_ambient)


def thermal_diffusivity(k, rho, cp):
    """
    α = k / (ρ × c_p)
    k   — thermal conductivity (W/m·K)
    rho — density (kg/m³)
    cp  — specific heat capacity (J/kg·K)
    Returns thermal diffusivity (m²/s).
    """
    if rho <= 0 or cp <= 0 or k <= 0:
        raise ValueError("All parameters must be positive.")
    return k / (rho * cp)
