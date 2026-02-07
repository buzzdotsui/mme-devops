# MME-DevOps: Computational Materials Science Tool
Developed by an MME Student at FUTA.

[![MME Calculator CI](https://github.com/buzzdotsui/mme-devops/actions/workflows/main.yml/badge.svg)](https://github.com/buzzdotsui/mme-devops/actions/workflows/main.yml)
![Docker Pulls](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)

## 🔬 Project Overview
This project bridges the gap between physical metallurgy and automated software infrastructure. It provides a containerized environment for calculating key material properties and auditing design safety.

### Key Calculations:
* **Tensile Strength (UTS):** Approximation from Brinell Hardness (HB).
* **Safety Audit:** Automated Factor of Safety (FoS) check against a built-in material database (Mild Steel, Stainless 304, etc.).

---

## 🛠 Tech Stack
* **Language:** Python 3.9 (Material Logic)
* **Containerization:** Docker (Environment Portability)
* **CI/CD:** GitHub Actions (Automated Testing & Builds)
* **Registry:** GitHub Container Registry (GHCR)

---

## 🚀 Getting Started

### Prerequisites
You need **Docker** installed on your machine.

### Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/buzzdotsui/mme-devops.git](https://github.com/buzzdotsui/mme-devops.git)
   cd mme-devops