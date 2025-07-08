import pandas as pd

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculate_wet_oxide_composition(moisture_frac, oxide_percent_dry):
    dry_mass = 1.0 - moisture_frac  # Assume 1 g total wet mass
    oxide_masses = {
        oxide: (wt / 100.0) * dry_mass for oxide, wt in oxide_percent_dry.items()
    }
    oxide_masses["H2O"] = moisture_frac
    return {oxide: m * 100.0 for oxide, m in oxide_masses.items()}  # as wt%

def main():
    print("Calculate Wet Composition from XRF Oxide Data\n")

    try:
        df = pd.read_csv("xrf_wt_percent_dry.csv")
        oxide_percent_dry = df.set_index("Oxide")["XRF_oxide_percent_dry"].to_dict()
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    moisture_frac = get_float_input("Enter moisture fraction (e.g. 0.75): ")
    result = calculate_wet_oxide_composition(moisture_frac, oxide_percent_dry)

    print("\nWet Composition (% by mass):")
    total = 0
    for oxide, wt_pct in sorted(result.items(), key=lambda x: -x[1]):
        print(f"  {oxide:>6s}: {wt_pct:7.3f} %")
        total += wt_pct

    print(f"\nTotal: {total:.3f} %")

if __name__ == "__main__":
    main()
