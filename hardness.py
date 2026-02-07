def estimate_tensile(hb_value):
    # Standard approximation: UTS (MPa) ≈ 3.45 * HB
    return 3.45 * hb_value

try:
    hardness = float(input("Enter Brinell Hardness (HB): "))
    
    # Validation: Hardest steel is usually < 1000 HB
    if hardness > 1000:
        print("Error: That hardness value is physically impossible for steel!")
    elif hardness <= 0:
        print("Error: Hardness must be a positive value.")
    else:
        strength = estimate_tensile(hardness)
        print(f"--- Result ---")
        print(f"Estimated Tensile Strength: {strength:.2f} MPa")

except ValueError:
    print("Error: Please enter a numeric value.")