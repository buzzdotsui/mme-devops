# MME Script: Brinell to Tensile Strength (for Steels)
def estimate_tensile(hb_value):
    # Standard approximation: UTS (MPa) ≈ 3.45 * HB
    uts = 3.45 * hb_value
    return uts

hardness = float(input("Enter Brinell Hardness (HB): "))
strength = estimate_tensile(hardness)

print(f"--- Result ---")
print(f"Estimated Tensile Strength: {strength} MPa")