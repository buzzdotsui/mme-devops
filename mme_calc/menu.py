"""
Interactive menu system for the MME Calculator.
Provides a top-level category menu and per-category sub-menus.
"""

import sys
from mme_calc import mechanical, thermal, phase, corrosion, casting, crystallography, composites, stress_strain


def _input(prompt):
    """Wrapper around input() for testability and pipe detection."""
    try:
        return input(prompt)
    except EOFError:
        sys.exit(0)


def _float(prompt):
    """Prompt for a float, retry on bad input."""
    while True:
        try:
            return float(_input(prompt))
        except ValueError:
            print("  ⚠ Please enter a numeric value.")


def _positive_float(prompt):
    """Prompt for a positive float."""
    while True:
        val = _float(prompt)
        if val > 0:
            return val
        print("  ⚠ Value must be positive.")


def _print_result(label, value, unit=""):
    """Pretty-print a result."""
    if unit:
        print(f"\n  ✅ {label}: {value:.6g} {unit}\n")
    else:
        print(f"\n  ✅ {label}: {value:.6g}\n")


def _show_menu(title, options):
    """Display a numbered menu and return the user's choice (1-indexed)."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    print(f"  [0] ← Back")
    print(f"{'='*60}")
    while True:
        try:
            choice = int(_input("  Enter choice: "))
            if 0 <= choice <= len(options):
                return choice
        except ValueError:
            pass
        print("  ⚠ Invalid choice, try again.")


# ===================================================================
# Sub-menus for each module
# ===================================================================

def menu_mechanical():
    options = [
        "Brinell Hardness → Tensile Strength",
        "Vickers Hardness → Tensile Strength",
        "HRC → HB Conversion",
        "HB → HRC Conversion",
        "Yield Strength (F / A₀)",
        "Percent Elongation",
        "Percent Reduction in Area",
        "True Stress from Engineering Stress",
        "True Strain from Engineering Strain",
        "Modulus of Resilience",
        "Basquin Fatigue Life (cycles to failure)",
        "Basquin Stress Amplitude",
        "Charpy Impact Toughness",
    ]
    while True:
        c = _show_menu("MECHANICAL PROPERTIES", options)
        if c == 0: return
        elif c == 1:
            hb = _positive_float("  Brinell Hardness (HB): ")
            _print_result("Estimated UTS", mechanical.brinell_to_tensile(hb), "MPa")
        elif c == 2:
            hv = _positive_float("  Vickers Hardness (HV): ")
            _print_result("Estimated UTS", mechanical.vickers_to_tensile(hv), "MPa")
        elif c == 3:
            hrc = _float("  Rockwell C Hardness (HRC, 20–55): ")
            try:
                _print_result("Brinell Hardness", mechanical.hrc_to_hb(hrc), "HB")
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 4:
            hb = _float("  Brinell Hardness (HB, 226–545): ")
            try:
                _print_result("Rockwell C Hardness", mechanical.hb_to_hrc(hb), "HRC")
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 5:
            f = _float("  Force (N): ")
            a = _positive_float("  Original area A₀ (mm²): ")
            _print_result("Yield Strength", mechanical.yield_strength(f, a), "MPa")
        elif c == 6:
            l0 = _positive_float("  Original gauge length L₀: ")
            lf = _float("  Final gauge length L_f: ")
            _print_result("Percent Elongation", mechanical.percent_elongation(l0, lf), "%")
        elif c == 7:
            a0 = _positive_float("  Original area A₀: ")
            af = _float("  Final area A_f: ")
            _print_result("Percent Reduction in Area", mechanical.percent_reduction_area(a0, af), "%")
        elif c == 8:
            se = _float("  Engineering stress (MPa): ")
            ee = _float("  Engineering strain: ")
            _print_result("True Stress", mechanical.true_stress(se, ee), "MPa")
        elif c == 9:
            ee = _float("  Engineering strain: ")
            try:
                _print_result("True Strain", mechanical.true_strain(ee))
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 10:
            sy = _positive_float("  Yield stress (MPa): ")
            E = _positive_float("  Young's modulus (MPa): ")
            _print_result("Modulus of Resilience", mechanical.modulus_of_resilience(sy, E), "MPa (J/m³ × 10⁻⁶)")
        elif c == 11:
            sa = _positive_float("  Stress amplitude σ_a (MPa): ")
            sf = _positive_float("  Fatigue strength coeff σ_f' (MPa): ")
            b = _float("  Basquin exponent b (negative): ")
            try:
                _print_result("Cycles to failure N", mechanical.basquin_fatigue_life(sa, sf, b), "cycles")
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 12:
            sf = _positive_float("  Fatigue strength coeff σ_f' (MPa): ")
            n = _positive_float("  Number of cycles N: ")
            b = _float("  Basquin exponent b (negative): ")
            _print_result("Stress Amplitude", mechanical.basquin_stress_amplitude(sf, n, b), "MPa")
        elif c == 13:
            E = _float("  Absorbed energy (J): ")
            A = _positive_float("  Cross-section area (mm²): ")
            _print_result("Impact Toughness", mechanical.charpy_toughness(E, A), "J/mm²")


def menu_thermal():
    options = [
        "Fourier's Law — Heat Flux",
        "Linear Thermal Expansion (ΔL)",
        "Volumetric Thermal Expansion (ΔV)",
        "Composite Slab Heat Flux",
        "Newton's Law of Cooling (Q̇)",
        "Thermal Diffusivity (α)",
    ]
    while True:
        c = _show_menu("THERMAL PROPERTIES", options)
        if c == 0: return
        elif c == 1:
            k = _positive_float("  Thermal conductivity k (W/m·K): ")
            dt = _float("  Temperature difference ΔT (K): ")
            dx = _positive_float("  Thickness dx (m): ")
            _print_result("Heat Flux", thermal.fourier_heat_flux(k, dt, dx), "W/m²")
        elif c == 2:
            a = _float("  Coeff. of linear expansion α (1/K): ")
            l0 = _positive_float("  Original length L₀: ")
            dt = _float("  Temperature change ΔT (K): ")
            _print_result("Change in Length ΔL", thermal.linear_thermal_expansion(a, l0, dt))
        elif c == 3:
            a = _float("  Coeff. of linear expansion α (1/K): ")
            v0 = _positive_float("  Original volume V₀: ")
            dt = _float("  Temperature change ΔT (K): ")
            _print_result("Change in Volume ΔV", thermal.volumetric_thermal_expansion(a, v0, dt))
        elif c == 4:
            dt = _float("  Total temperature difference ΔT (K): ")
            n = int(_positive_float("  Number of layers: "))
            layers = []
            for i in range(n):
                print(f"  --- Layer {i+1} ---")
                thickness = _positive_float(f"    Thickness (m): ")
                k = _positive_float(f"    Conductivity (W/m·K): ")
                layers.append((thickness, k))
            _print_result("Heat Flux", thermal.composite_slab_heat_flux(dt, layers), "W/m²")
        elif c == 5:
            h = _positive_float("  Convective coeff h (W/m²·K): ")
            A = _positive_float("  Surface area A (m²): ")
            ts = _float("  Surface temp T_s (°C or K): ")
            tinf = _float("  Ambient temp T_∞ (°C or K): ")
            _print_result("Heat Transfer Rate", thermal.newton_cooling(h, A, ts, tinf), "W")
        elif c == 6:
            k = _positive_float("  Thermal conductivity k (W/m·K): ")
            rho = _positive_float("  Density ρ (kg/m³): ")
            cp = _positive_float("  Specific heat c_p (J/kg·K): ")
            _print_result("Thermal Diffusivity", thermal.thermal_diffusivity(k, rho, cp), "m²/s")


def menu_phase():
    options = [
        "Lever Rule (phase fractions)",
        "Gibbs Phase Rule",
        "Avrami Equation (transformation kinetics)",
        "Carbon Equivalent (weldability)",
        "Scheil Equation (micro-segregation)",
    ]
    while True:
        c = _show_menu("PHASE TRANSFORMATIONS", options)
        if c == 0: return
        elif c == 1:
            c0 = _float("  Overall composition C₀ (wt%): ")
            ca = _float("  Phase α boundary Cα (wt%): ")
            cb = _float("  Phase β boundary Cβ (wt%): ")
            try:
                wa, wb = phase.lever_rule(c0, ca, cb)
                _print_result("Weight fraction α (Wα)", wa)
                _print_result("Weight fraction β (Wβ)", wb)
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 2:
            comp = int(_positive_float("  Number of components C: "))
            ph = int(_positive_float("  Number of phases P: "))
            try:
                _print_result("Degrees of Freedom F", phase.gibbs_phase_rule(comp, ph))
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 3:
            k = _float("  Rate constant k: ")
            t = _float("  Time t: ")
            n = _float("  Avrami exponent n: ")
            try:
                _print_result("Fraction Transformed Y", phase.avrami_fraction(k, t, n))
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 4:
            print("  Enter alloying element wt% (press Enter to skip = 0):")
            def _opt_float(prompt):
                val = _input(prompt).strip()
                return float(val) if val else 0.0
            C = _opt_float("    Carbon (C): ")
            Mn = _opt_float("    Manganese (Mn): ")
            Cr = _opt_float("    Chromium (Cr): ")
            Mo = _opt_float("    Molybdenum (Mo): ")
            V = _opt_float("    Vanadium (V): ")
            Ni = _opt_float("    Nickel (Ni): ")
            Cu = _opt_float("    Copper (Cu): ")
            ce = phase.carbon_equivalent(C, Mn, Cr, Mo, V, Ni, Cu)
            _print_result("Carbon Equivalent (CE)", ce)
            if ce < 0.40:
                print("  → Good weldability ✅")
            elif ce <= 0.60:
                print("  → Fair weldability — preheat recommended ⚠️")
            else:
                print("  → Poor weldability — special procedures needed ❌")
        elif c == 5:
            k = _positive_float("  Partition coefficient k: ")
            c0 = _float("  Nominal composition C₀ (wt%): ")
            fs = _float("  Fraction solid f_s (0–0.99): ")
            try:
                _print_result("Solid Composition C_s", phase.scheil_equation(k, c0, fs), "wt%")
            except ValueError as e:
                print(f"  ❌ {e}")


def menu_corrosion():
    options = [
        "Corrosion Rate (mils per year)",
        "Corrosion Rate (mm per year)",
        "Pilling-Bedworth Ratio",
        "Galvanic Series — Potential Difference",
        "Parabolic Oxidation — Oxide Thickness",
    ]
    while True:
        c = _show_menu("CORROSION & DEGRADATION", options)
        if c == 0: return
        elif c == 1:
            W = _float("  Weight loss (g): ")
            D = _positive_float("  Metal density (g/cm³): ")
            A = _positive_float("  Exposed area (cm²): ")
            T = _positive_float("  Exposure time (hours): ")
            _print_result("Corrosion Rate", corrosion.corrosion_rate_mpy(W, D, A, T), "mpy")
        elif c == 2:
            W = _float("  Weight loss (g): ")
            D = _positive_float("  Metal density (g/cm³): ")
            A = _positive_float("  Exposed area (cm²): ")
            T = _positive_float("  Exposure time (hours): ")
            _print_result("Corrosion Rate", corrosion.corrosion_rate_mmpy(W, D, A, T), "mm/y")
        elif c == 3:
            mo = _positive_float("  Molar mass of oxide (g/mol): ")
            rm = _positive_float("  Metal density (g/cm³): ")
            n = _positive_float("  Metal atoms per oxide formula unit: ")
            mm = _positive_float("  Molar mass of metal (g/mol): ")
            ro = _positive_float("  Oxide density (g/cm³): ")
            pbr = corrosion.pilling_bedworth_ratio(mo, rm, n, mm, ro)
            _print_result("Pilling-Bedworth Ratio", pbr)
            if pbr < 1:
                print("  → Porous / non-protective oxide ❌")
            elif pbr <= 2:
                print("  → Protective oxide ✅")
            else:
                print("  → Oxide prone to spalling / cracking ⚠️")
        elif c == 4:
            print(f"  Available metals: {', '.join(corrosion.available_metals())}")
            a = _input("  Metal A: ").strip()
            b = _input("  Metal B: ").strip()
            try:
                diff, anode, cathode = corrosion.galvanic_potential_diff(a, b)
                _print_result("Potential Difference", diff, "V")
                print(f"  → Anode (corrodes): {anode}")
                print(f"  → Cathode (protected): {cathode}")
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 5:
            kp = _float("  Parabolic rate constant k_p: ")
            t = _float("  Time: ")
            try:
                _print_result("Oxide Thickness", corrosion.parabolic_oxide_thickness(kp, t))
            except ValueError as e:
                print(f"  ❌ {e}")


def menu_casting():
    options = [
        "Chvorinov's Rule (solidification time)",
        "Casting / Riser Modulus",
        "Shrinkage Allowance",
        "Fluidity Index",
        "Newtonian Cooling Rate",
    ]
    while True:
        c = _show_menu("CASTING & SOLIDIFICATION", options)
        if c == 0: return
        elif c == 1:
            B = _positive_float("  Mold constant B: ")
            V = _positive_float("  Casting volume V: ")
            A = _positive_float("  Surface area A: ")
            n = _float("  Exponent n (default 2): ") or 2
            _print_result("Solidification Time", casting.chvorinov_solidification_time(B, V, A, n))
        elif c == 2:
            V = _positive_float("  Volume: ")
            A = _positive_float("  Surface area: ")
            _print_result("Modulus (V/A)", casting.casting_modulus(V, A))
        elif c == 3:
            L = _positive_float("  Desired casting length: ")
            s = _float("  Shrinkage % (e.g. 2.0 for steel): ")
            _print_result("Pattern Length", casting.shrinkage_allowance(L, s))
        elif c == 4:
            rho = _positive_float("  Metal density (kg/m³): ")
            cp = _positive_float("  Specific heat (J/kg·K): ")
            dt = _float("  Superheat ΔT (K): ")
            Lf = _positive_float("  Latent heat of fusion (J/kg): ")
            _print_result("Fluidity Index", casting.fluidity_index(rho, cp, dt, Lf))
        elif c == 5:
            h = _positive_float("  Heat transfer coeff h (W/m²·K): ")
            A = _positive_float("  Surface area A (m²): ")
            rho = _positive_float("  Density ρ (kg/m³): ")
            cp = _positive_float("  Specific heat c_p (J/kg·K): ")
            V = _positive_float("  Volume V (m³): ")
            Tc = _float("  Current temperature T (°C or K): ")
            Ta = _float("  Ambient temperature T_∞ (°C or K): ")
            rate = casting.newtonian_cooling_rate(h, A, rho, cp, V, Tc, Ta)
            _print_result("Cooling Rate dT/dt", rate, "K/s")


def menu_crystallography():
    options = [
        "Atomic Packing Factor — BCC",
        "Atomic Packing Factor — FCC",
        "Atomic Packing Factor — HCP",
        "Atomic Packing Factor — Simple Cubic",
        "Planar Density",
        "Linear Density",
        "ASTM Grain Size → Grain Count",
        "Grain Count → ASTM Grain Size Number",
        "Hall-Petch Equation (σ_y)",
        "Burger's Vector Magnitude",
    ]
    while True:
        c = _show_menu("CRYSTALLOGRAPHY & DEFECTS", options)
        if c == 0: return
        elif c == 1:
            r = _positive_float("  Atomic radius (any unit): ")
            _print_result("APF (BCC)", crystallography.apf_bcc(r))
        elif c == 2:
            r = _positive_float("  Atomic radius: ")
            _print_result("APF (FCC)", crystallography.apf_fcc(r))
        elif c == 3:
            r = _positive_float("  Atomic radius: ")
            _print_result("APF (HCP)", crystallography.apf_hcp(r))
        elif c == 4:
            r = _positive_float("  Atomic radius: ")
            _print_result("APF (SC)", crystallography.apf_simple_cubic(r))
        elif c == 5:
            n = _float("  Atoms centered on plane: ")
            a = _positive_float("  Plane area: ")
            _print_result("Planar Density", crystallography.planar_density(n, a), "atoms/unit²")
        elif c == 6:
            n = _float("  Atoms centered on direction: ")
            l = _positive_float("  Direction length: ")
            _print_result("Linear Density", crystallography.linear_density(n, l), "atoms/unit")
        elif c == 7:
            n = _float("  ASTM grain size number n: ")
            _print_result("Grains per sq inch at 100×", crystallography.astm_grain_count(n))
        elif c == 8:
            N = _positive_float("  Grain count N: ")
            _print_result("ASTM Grain Size Number", crystallography.astm_grain_number_from_count(N))
        elif c == 9:
            s0 = _float("  Friction stress σ₀ (MPa): ")
            ky = _float("  Hall-Petch slope k_y: ")
            d = _positive_float("  Grain diameter d: ")
            _print_result("Yield Strength σ_y", crystallography.hall_petch(s0, ky, d), "MPa")
        elif c == 10:
            a = _positive_float("  Lattice parameter a: ")
            h = _float("  Miller index h: ")
            k = _float("  Miller index k: ")
            l = _float("  Miller index l: ")
            _print_result("|b|", crystallography.burgers_vector_magnitude(a, h, k, l))


def menu_composites():
    options = [
        "Rule of Mixtures — Longitudinal (E or σ)",
        "Inverse Rule of Mixtures — Transverse (E)",
        "Composite Density",
        "Critical Fiber Length",
        "Halpin-Tsai Equation",
    ]
    while True:
        c = _show_menu("COMPOSITE MATERIALS", options)
        if c == 0: return
        elif c == 1:
            ef = _positive_float("  Fiber property (E_f or σ_f): ")
            vf = _float("  Fiber volume fraction V_f (0–1): ")
            em = _positive_float("  Matrix property (E_m or σ_m): ")
            _print_result("Composite Property (longitudinal)", composites.rule_of_mixtures_longitudinal(ef, vf, em))
        elif c == 2:
            ef = _positive_float("  Fiber modulus E_f: ")
            vf = _float("  Fiber volume fraction V_f (0–1): ")
            em = _positive_float("  Matrix modulus E_m: ")
            _print_result("Composite Modulus (transverse)", composites.rule_of_mixtures_transverse(ef, vf, em))
        elif c == 3:
            rf = _positive_float("  Fiber density ρ_f: ")
            vf = _float("  Fiber volume fraction V_f (0–1): ")
            rm = _positive_float("  Matrix density ρ_m: ")
            _print_result("Composite Density", composites.composite_density(rf, vf, rm))
        elif c == 4:
            sf = _positive_float("  Fiber ultimate strength σ_f: ")
            d = _positive_float("  Fiber diameter d: ")
            tc = _positive_float("  Interfacial shear strength τ_c: ")
            _print_result("Critical Fiber Length l_c", composites.critical_fiber_length(sf, d, tc))
        elif c == 5:
            em = _positive_float("  Matrix modulus E_m: ")
            ef = _positive_float("  Fiber modulus E_f: ")
            vf = _float("  Fiber volume fraction V_f (0–1): ")
            xi = _float("  Geometry parameter ξ (default 2): ") or 2
            _print_result("Composite Modulus (Halpin-Tsai)", composites.halpin_tsai(em, ef, vf, xi))


def menu_stress_strain():
    options = [
        "Hooke's Law — Stress from Strain",
        "Hooke's Law — Strain from Stress",
        "Poisson's Lateral Strain",
        "Shear Modulus (G)",
        "Bulk Modulus (K)",
        "von Mises Equivalent Stress",
        "Factor of Safety",
        "Stress Concentration (σ_max)",
        "Steady-State Creep Rate",
    ]
    while True:
        c = _show_menu("STRESS & STRAIN ANALYSIS", options)
        if c == 0: return
        elif c == 1:
            E = _positive_float("  Young's modulus E (GPa or MPa): ")
            e = _float("  Strain ε: ")
            _print_result("Stress σ", stress_strain.hookes_law_stress(E, e))
        elif c == 2:
            E = _positive_float("  Young's modulus E: ")
            s = _float("  Stress σ: ")
            _print_result("Strain ε", stress_strain.hookes_law_strain(E, s))
        elif c == 3:
            nu = _float("  Poisson's ratio ν: ")
            ea = _float("  Axial strain ε_axial: ")
            _print_result("Lateral Strain", stress_strain.poisson_strain(nu, ea))
        elif c == 4:
            E = _positive_float("  Young's modulus E: ")
            nu = _float("  Poisson's ratio ν: ")
            _print_result("Shear Modulus G", stress_strain.shear_modulus(E, nu))
        elif c == 5:
            E = _positive_float("  Young's modulus E: ")
            nu = _float("  Poisson's ratio ν: ")
            try:
                _print_result("Bulk Modulus K", stress_strain.bulk_modulus(E, nu))
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 6:
            s1 = _float("  Principal stress σ₁: ")
            s2 = _float("  Principal stress σ₂: ")
            s3 = _float("  Principal stress σ₃: ")
            _print_result("von Mises Stress", stress_strain.von_mises_stress(s1, s2, s3), "MPa")
        elif c == 7:
            sy = _positive_float("  Yield strength (MPa): ")
            sa = _float("  Applied stress (MPa): ")
            try:
                fos = stress_strain.factor_of_safety(sy, sa)
                _print_result("Factor of Safety", fos)
                if fos >= 1:
                    print("  → Design is SAFE ✅")
                else:
                    print("  → Design FAILS — FoS < 1 ❌")
            except ValueError as e:
                print(f"  ❌ {e}")
        elif c == 8:
            kt = _positive_float("  Stress concentration factor K_t: ")
            sn = _float("  Nominal stress σ_nom: ")
            _print_result("Max Stress σ_max", stress_strain.stress_concentration(kt, sn))
        elif c == 9:
            A = _float("  Material constant A: ")
            s = _float("  Applied stress σ: ")
            n = _float("  Stress exponent n: ")
            Q = _positive_float("  Activation energy Q (J/mol): ")
            T = _positive_float("  Temperature T (K): ")
            rate = stress_strain.creep_rate_steady_state(A, s, n, Q, 8.314, T)
            _print_result("Steady-state Creep Rate ε̇", rate, "s⁻¹")


# ===================================================================
# Main menu
# ===================================================================

CATEGORIES = [
    ("Mechanical Properties",       menu_mechanical),
    ("Thermal Properties",          menu_thermal),
    ("Phase Transformations",       menu_phase),
    ("Corrosion & Degradation",     menu_corrosion),
    ("Casting & Solidification",    menu_casting),
    ("Crystallography & Defects",   menu_crystallography),
    ("Composite Materials",         menu_composites),
    ("Stress & Strain Analysis",    menu_stress_strain),
]


def main_menu():
    """Top-level interactive menu."""
    print("\n" + "=" * 60)
    print("  🔬 MME CALCULATOR — Metallurgical & Materials Engineering")
    print("     Developed by an MME Student at FUTA")
    print("=" * 60)

    while True:
        choice = _show_menu("MAIN MENU — Select a Category", [name for name, _ in CATEGORIES])
        if choice == 0:
            print("\n  Goodbye! 👋\n")
            break
        CATEGORIES[choice - 1][1]()
