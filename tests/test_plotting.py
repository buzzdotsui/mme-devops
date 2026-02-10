import pytest
from mme_calc import plotting

class TestPlotting:
    def test_stress_strain_plot(self):
        # Smoke test: ensure it runs without error (mock show/savefig if needed)
        # Using show=False to prevent blocking
        plotting.plot_stress_strain(200000, 250, 400, 0.2, show=False)
        plotting.plot_stress_strain(200000, 250, 400, 0.2, filename="test_ss.png", show=False)
        import os
        if os.path.exists("test_ss.png"):
            os.remove("test_ss.png")

    def test_cooling_curve_plot(self):
        plotting.plot_cooling_curve(1000, 25, 0.05, 100, show=False)
    
    def test_hardness_conversion_plot(self):
        plotting.plot_hardness_conversion(show=False)
