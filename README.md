# MME-DevOps: Comprehensive Materials Engineering Calculator

Developed by an MME Student at FUTA.

[![MME Calculator CI](https://github.com/buzzdotsui/mme-devops/actions/workflows/main.yml/badge.svg)](https://github.com/buzzdotsui/mme-devops/actions/workflows/main.yml)
![Docker Pulls](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)

## 🔬 Project Overview

This project bridges the gap between physical metallurgy and automated software infrastructure. It provides a **containerized, menu-driven CLI tool** for calculating key material properties across **8 engineering domains** with **40+ calculators**.

---

## 📐 Calculator Modules

### 1. Mechanical Properties
Brinell/Vickers → Tensile Strength · HRC ↔ HB Conversion · Yield Strength · % Elongation · % Reduction in Area · True Stress/Strain · Modulus of Resilience · Basquin Fatigue Life · Charpy Impact Toughness

### 2. Thermal Properties
Fourier's Law (Heat Flux) · Linear & Volumetric Thermal Expansion · Composite Slab Conduction · Newton's Law of Cooling · Thermal Diffusivity

### 3. Phase Transformations
Lever Rule · Gibbs Phase Rule · Avrami Kinetics · Carbon Equivalent (Weldability) · Scheil Micro-segregation

### 4. Corrosion & Degradation
Corrosion Rate (mpy & mm/y) · Pilling-Bedworth Ratio · Galvanic Series Lookup · Parabolic Oxidation Kinetics

### 5. Casting & Solidification
Chvorinov's Rule · Riser Modulus · Shrinkage Allowance · Fluidity Index · Newtonian Cooling Rate

### 6. Crystallography & Defects
APF (BCC/FCC/HCP/SC) · Planar & Linear Density · ASTM Grain Size Number · Hall-Petch Equation · Burger's Vector

### 7. Composite Materials
Rule of Mixtures (Longitudinal & Transverse) · Composite Density · Critical Fiber Length · Halpin-Tsai Equation

### 8. Stress & Strain Analysis
Hooke's Law · Poisson's Ratio · Shear & Bulk Modulus · von Mises Stress · Factor of Safety · Stress Concentration · Steady-State Creep

---

## 🛠 Tech Stack
* **Language:** Python 3.9
* **Containerization:** Docker
* **CI/CD:** GitHub Actions (Test → Build → Push)
* **Registry:** GitHub Container Registry (GHCR)
* **Testing:** pytest

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ **or** Docker installed on your machine.

### Run Locally
```bash
git clone https://github.com/buzzdotsui/mme-devops.git
cd mme-devops
pip install -r requirements.txt
python main.py
```

### Run with Docker
```bash
docker build -t mme-calc .
docker run -it mme-calc
```

### Run Tests
```bash
python -m pytest tests/test_all.py -v
```

### Legacy (Hardness-only)
The original single-calculator script is still available:
```bash
python hardness.py
```

---

## 📁 Project Structure
```
mme_devops/
├── mme_calc/
│   ├── __init__.py
│   ├── menu.py              # Interactive CLI menu
│   ├── mechanical.py        # Mechanical properties
│   ├── thermal.py           # Thermal properties
│   ├── phase.py             # Phase transformations
│   ├── corrosion.py         # Corrosion & degradation
│   ├── casting.py           # Casting & solidification
│   ├── crystallography.py   # Crystal structure & defects
│   ├── composites.py        # Composite materials
│   └── stress_strain.py     # Stress-strain analysis
├── tests/
│   └── test_all.py          # Unit tests
├── main.py                  # Entry point
├── hardness.py              # Legacy calculator
├── Dockerfile
├── requirements.txt
└── .github/workflows/main.yml
```