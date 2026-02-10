"""
Comprehensive unit tests for all MME Calculator modules.
Run with:  python -m pytest tests/test_all.py -v
"""

import math
import pytest

from mme_calc import mechanical, thermal, phase, corrosion, casting, crystallography, composites, stress_strain


# ===================================================================
# Module 1 — Mechanical Properties
# ===================================================================

class TestMechanical:
    def test_brinell_to_tensile(self):
        assert mechanical.brinell_to_tensile(200) == pytest.approx(690.0)
        assert mechanical.brinell_to_tensile(100) == pytest.approx(345.0)

    def test_brinell_to_tensile_invalid(self):
        with pytest.raises(ValueError):
            mechanical.brinell_to_tensile(-10)

    def test_vickers_to_tensile(self):
        assert mechanical.vickers_to_tensile(200) == pytest.approx(636.0)

    def test_hrc_to_hb_and_back(self):
        hb = mechanical.hrc_to_hb(30)
        assert 280 < hb < 295
        hrc = mechanical.hb_to_hrc(hb)
        assert hrc == pytest.approx(30, abs=0.5)

    def test_hrc_out_of_range(self):
        with pytest.raises(ValueError):
            mechanical.hrc_to_hb(10)
        with pytest.raises(ValueError):
            mechanical.hrc_to_hb(60)

    def test_yield_strength(self):
        assert mechanical.yield_strength(50000, 100) == pytest.approx(500.0)

    def test_percent_elongation(self):
        assert mechanical.percent_elongation(50, 60) == pytest.approx(20.0)

    def test_percent_reduction_area(self):
        assert mechanical.percent_reduction_area(100, 80) == pytest.approx(20.0)

    def test_true_stress(self):
        # σ_t = 200 * (1 + 0.1) = 220
        assert mechanical.true_stress(200, 0.1) == pytest.approx(220.0)

    def test_true_strain(self):
        assert mechanical.true_strain(0.1) == pytest.approx(math.log(1.1))

    def test_true_strain_invalid(self):
        with pytest.raises(ValueError):
            mechanical.true_strain(-1.5)

    def test_modulus_of_resilience(self):
        # U_r = 250^2 / (2 * 200000) = 0.15625
        assert mechanical.modulus_of_resilience(250, 200000) == pytest.approx(0.15625)

    def test_basquin_fatigue(self):
        N = mechanical.basquin_fatigue_life(300, 900, -0.1)
        assert N > 0

    def test_basquin_stress(self):
        s = mechanical.basquin_stress_amplitude(900, 1e6, -0.1)
        assert s > 0

    def test_charpy_toughness(self):
        assert mechanical.charpy_toughness(30, 80) == pytest.approx(0.375)


# ===================================================================
# Module 2 — Thermal Properties
# ===================================================================

class TestThermal:
    def test_fourier_heat_flux(self):
        # q = 50 * 100 / 0.01 = 500000
        assert thermal.fourier_heat_flux(50, 100, 0.01) == pytest.approx(500000.0)

    def test_linear_expansion(self):
        # ΔL = 12e-6 * 1000 * 100 = 1.2
        assert thermal.linear_thermal_expansion(12e-6, 1000, 100) == pytest.approx(1.2)

    def test_volumetric_expansion(self):
        assert thermal.volumetric_thermal_expansion(12e-6, 1, 100) == pytest.approx(3 * 12e-6 * 100)

    def test_composite_slab(self):
        # Two layers: (0.1, 50) and (0.05, 100)
        # R = 0.1/50 + 0.05/100 = 0.002 + 0.0005 = 0.0025
        # q = 200 / 0.0025 = 80000
        assert thermal.composite_slab_heat_flux(200, [(0.1, 50), (0.05, 100)]) == pytest.approx(80000.0)

    def test_newton_cooling(self):
        assert thermal.newton_cooling(25, 2, 100, 25) == pytest.approx(25 * 2 * 75)

    def test_thermal_diffusivity(self):
        # α = 50 / (7800 * 500)
        assert thermal.thermal_diffusivity(50, 7800, 500) == pytest.approx(50 / (7800 * 500))


# ===================================================================
# Module 3 — Phase Transformations
# ===================================================================

class TestPhase:
    def test_lever_rule(self):
        wa, wb = phase.lever_rule(35, 20, 60)
        assert wa == pytest.approx(0.625)
        assert wb == pytest.approx(0.375)
        assert wa + wb == pytest.approx(1.0)

    def test_gibbs_phase_rule(self):
        assert phase.gibbs_phase_rule(2, 3) == 1
        assert phase.gibbs_phase_rule(1, 1) == 2

    def test_avrami(self):
        # At t=0 fraction should be 0
        assert phase.avrami_fraction(1, 0, 2) == pytest.approx(0.0)
        # Fraction should be between 0 and 1
        y = phase.avrami_fraction(0.01, 10, 2)
        assert 0 < y < 1

    def test_carbon_equivalent(self):
        ce = phase.carbon_equivalent(0.15, mn=1.2, cr=0.5, mo=0.1)
        assert ce > 0

    def test_scheil(self):
        cs = phase.scheil_equation(0.5, 4.0, 0.5)
        assert cs > 0

    def test_scheil_invalid(self):
        with pytest.raises(ValueError):
            phase.scheil_equation(0.5, 4.0, 1.0)


# ===================================================================
# Module 4 — Corrosion
# ===================================================================

class TestCorrosion:
    def test_corrosion_rate_mpy(self):
        cr = corrosion.corrosion_rate_mpy(0.5, 7.87, 10, 720)
        assert cr > 0

    def test_corrosion_rate_mmpy(self):
        cr = corrosion.corrosion_rate_mmpy(0.5, 7.87, 10, 720)
        assert cr > 0

    def test_pilling_bedworth(self):
        # Al₂O₃ on Al: M_oxide=101.96, ρ_Al=2.7, n=2, M_Al=26.98, ρ_oxide=3.95
        pbr = corrosion.pilling_bedworth_ratio(101.96, 2.7, 2, 26.98, 3.95)
        assert 1.2 < pbr < 1.4  # Known PBR for Al₂O₃ ≈ 1.28

    def test_galvanic_potential(self):
        diff, anode, cathode = corrosion.galvanic_potential_diff("zinc", "copper")
        assert diff > 0
        assert anode == "zinc"
        assert cathode == "copper"

    def test_galvanic_unknown(self):
        with pytest.raises(ValueError):
            corrosion.galvanic_potential_diff("unobtanium", "copper")

    def test_parabolic_oxide(self):
        x = corrosion.parabolic_oxide_thickness(1e-10, 3600)
        assert x == pytest.approx(math.sqrt(1e-10 * 3600))


# ===================================================================
# Module 5 — Casting
# ===================================================================

class TestCasting:
    def test_chvorinov(self):
        t = casting.chvorinov_solidification_time(2e6, 0.001, 0.06, 2)
        assert t > 0

    def test_modulus(self):
        assert casting.casting_modulus(1000, 600) == pytest.approx(1000 / 600)

    def test_shrinkage(self):
        assert casting.shrinkage_allowance(100, 2.0) == pytest.approx(102.0)

    def test_fluidity(self):
        f = casting.fluidity_index(7000, 500, 50, 250000)
        assert f > 0

    def test_cooling_rate(self):
        rate = casting.newtonian_cooling_rate(100, 0.1, 7800, 500, 0.001, 800, 25)
        assert rate < 0  # cooling = negative


# ===================================================================
# Module 6 — Crystallography
# ===================================================================

class TestCrystallography:
    def test_apf_bcc(self):
        apf = crystallography.apf_bcc(1.0)
        assert apf == pytest.approx(0.6802, abs=0.01)

    def test_apf_fcc(self):
        apf = crystallography.apf_fcc(1.0)
        assert apf == pytest.approx(0.7405, abs=0.01)

    def test_apf_hcp(self):
        apf = crystallography.apf_hcp(1.0)
        assert apf == pytest.approx(0.7405, abs=0.01)

    def test_apf_sc(self):
        apf = crystallography.apf_simple_cubic(1.0)
        assert apf == pytest.approx(0.5236, abs=0.01)

    def test_planar_density(self):
        assert crystallography.planar_density(2, 10) == pytest.approx(0.2)

    def test_linear_density(self):
        assert crystallography.linear_density(1, 5) == pytest.approx(0.2)

    def test_astm_grain_count(self):
        assert crystallography.astm_grain_count(1) == 1
        assert crystallography.astm_grain_count(8) == 128

    def test_astm_grain_number(self):
        n = crystallography.astm_grain_number_from_count(128)
        assert n == pytest.approx(8.0)

    def test_hall_petch(self):
        sy = crystallography.hall_petch(70, 0.74, 0.01)
        assert sy == pytest.approx(70 + 0.74 / math.sqrt(0.01))

    def test_burgers_vector(self):
        # FCC <110>: |b| = a/√2
        b = crystallography.burgers_vector_magnitude(3.6, 1, 1, 0)
        assert b == pytest.approx(3.6 * math.sqrt(2) / 2, abs=0.01)


# ===================================================================
# Module 7 — Composites
# ===================================================================

class TestComposites:
    def test_rom_longitudinal(self):
        ec = composites.rule_of_mixtures_longitudinal(350, 0.6, 3.5)
        assert ec == pytest.approx(350 * 0.6 + 3.5 * 0.4)

    def test_rom_transverse(self):
        ec = composites.rule_of_mixtures_transverse(350, 0.6, 3.5)
        expected = 1 / (0.6 / 350 + 0.4 / 3.5)
        assert ec == pytest.approx(expected)

    def test_composite_density(self):
        rho = composites.composite_density(2.5, 0.6, 1.2)
        assert rho == pytest.approx(2.5 * 0.6 + 1.2 * 0.4)

    def test_critical_fiber_length(self):
        lc = composites.critical_fiber_length(3500, 0.01, 70)
        assert lc == pytest.approx(3500 * 0.01 / (2 * 70))

    def test_halpin_tsai(self):
        ec = composites.halpin_tsai(3.5, 350, 0.6, 2)
        assert ec > 3.5  # should be stiffer than matrix


# ===================================================================
# Module 8 — Stress & Strain
# ===================================================================

class TestStressStrain:
    def test_hookes_stress(self):
        assert stress_strain.hookes_law_stress(200e3, 0.001) == pytest.approx(200.0)

    def test_hookes_strain(self):
        assert stress_strain.hookes_law_strain(200e3, 200) == pytest.approx(0.001)

    def test_poisson_strain(self):
        assert stress_strain.poisson_strain(0.3, 0.01) == pytest.approx(-0.003)

    def test_shear_modulus(self):
        G = stress_strain.shear_modulus(200e3, 0.3)
        assert G == pytest.approx(200e3 / 2.6)

    def test_bulk_modulus(self):
        K = stress_strain.bulk_modulus(200e3, 0.3)
        assert K == pytest.approx(200e3 / (3 * 0.4))

    def test_von_mises(self):
        # Uniaxial: σ₁=100, σ₂=σ₃=0 → σ_vm = 100
        vm = stress_strain.von_mises_stress(100, 0, 0)
        assert vm == pytest.approx(100.0)

    def test_von_mises_hydrostatic(self):
        # Pure hydrostatic: σ₁=σ₂=σ₃=100 → σ_vm = 0
        vm = stress_strain.von_mises_stress(100, 100, 100)
        assert vm == pytest.approx(0.0)

    def test_factor_of_safety(self):
        assert stress_strain.factor_of_safety(250, 100) == pytest.approx(2.5)

    def test_factor_of_safety_zero(self):
        with pytest.raises(ValueError):
            stress_strain.factor_of_safety(250, 0)

    def test_stress_concentration(self):
        assert stress_strain.stress_concentration(2.5, 100) == pytest.approx(250.0)

    def test_creep_rate(self):
        rate = stress_strain.creep_rate_steady_state(1e10, 100, 3, 200000, 8.314, 800)
        assert rate > 0
