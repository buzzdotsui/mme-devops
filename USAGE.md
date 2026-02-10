# MME Calculator — Usage Guide

This guide explains how to use the comprehensive MME Calculator CLI tool.

## Prerequisites

- Python 3.9+ installed, **or** Docker.
- Install dependencies: `pip install -r requirements.txt`

---

## Running the Calculator

### Interactive Mode

```bash
python main.py
```

You'll see a main menu with 8 categories:

```
============================================================
  🔬 MME CALCULATOR — Metallurgical & Materials Engineering
     Developed by an MME Student at FUTA
============================================================

============================================================
  MAIN MENU — Select a Category
============================================================
  [1] Mechanical Properties
  [2] Thermal Properties
  [3] Phase Transformations
  [4] Corrosion & Degradation
  [5] Casting & Solidification
  [6] Crystallography & Defects
  [7] Composite Materials
  [8] Stress & Strain Analysis
  [0] ← Back
============================================================
  Enter choice:
```

Select a category number, then pick a specific calculator from the sub-menu.

### Example Walkthrough

```
Enter choice: 1          ← Mechanical Properties
Enter choice: 1          ← Brinell → Tensile Strength
Brinell Hardness (HB): 200

  ✅ Estimated UTS: 690 MPa
```

### File Redirection (Batch Mode)

The legacy single-calculator is still available:

```bash
# On Windows (PowerShell)
Get-Content input.txt | python hardness.py | Out-File -Encoding ASCII result.txt

# On Linux/macOS
python hardness.py < input.txt > result.txt
```

### Docker

```bash
docker build -t mme-calc .
docker run -it mme-calc
```

---

## Available Calculators

| # | Category | Calculators |
|---|----------|-------------|
| 1 | **Mechanical Properties** | Brinell→UTS, Vickers→UTS, HRC↔HB, Yield Strength, %Elongation, %RA, True Stress/Strain, Resilience, Basquin Fatigue, Charpy Toughness |
| 2 | **Thermal Properties** | Fourier Heat Flux, Linear Expansion, Vol. Expansion, Composite Slab, Newton's Cooling, Thermal Diffusivity |
| 3 | **Phase Transformations** | Lever Rule, Gibbs Phase Rule, Avrami Kinetics, Carbon Equivalent, Scheil Equation |
| 4 | **Corrosion & Degradation** | Corrosion Rate (mpy/mmpy), Pilling-Bedworth Ratio, Galvanic Series, Parabolic Oxidation |
| 5 | **Casting & Solidification** | Chvorinov's Rule, Riser Modulus, Shrinkage Allowance, Fluidity Index, Newtonian Cooling Rate |
| 6 | **Crystallography & Defects** | APF (BCC/FCC/HCP/SC), Planar Density, Linear Density, ASTM Grain Size, Hall-Petch, Burger's Vector |
| 7 | **Composite Materials** | Rule of Mixtures (Long. & Trans.), Composite Density, Critical Fiber Length, Halpin-Tsai |
| 8 | **Stress & Strain Analysis** | Hooke's Law, Poisson's Strain, Shear Modulus, Bulk Modulus, von Mises, FoS, Stress Concentration, Creep Rate |

---

## Running Tests

```bash
python -m pytest tests/test_all.py -v
```

All calculators are validated against known engineering values.
