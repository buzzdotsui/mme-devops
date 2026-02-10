#!/usr/bin/env python3
"""
MME Calculator — Comprehensive Metallurgical & Materials Engineering Toolkit.
Entry point for the interactive calculator.

Usage:
    python main.py              # Interactive mode
    echo "1" | python main.py   # Pipe mode (select category 1)
"""

from mme_calc.menu import main_menu

if __name__ == "__main__":
    main_menu()
