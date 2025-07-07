import pandas as pd

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a number.")

def convert_oxides_to_elements(oxide_wt_percent, ratios):
    """
    Converts oxide wt% to elemental wt% using given conversion ratios.
    """
    return {
        e: oxide_wt_percent[e] * ratios.get(e, 1.0)
        for e in oxide_wt_percent
    }

def calculate_normalised_wet_composition(moisture_frac, elemental_percent):
    dry_mass = 1.0 - moisture_frac  # Assume 1 g wet mass
    elemental_masses = {
        e: (wt / 100.0) * dry_mass for e, wt in elemental_percent.items()
    }
    elemental_masses["H2O"] = moisture_frac
    return {e: m * 100.0 for e, m in elemental_masses.items()}

def main():
    print("Calculate Wet Composition from XRF Data\n")

    # === Load Data ===
    try:
        xrf_df = pd.read_csv("xrf_wt_percent_dry.csv")
        oxide_wt_percent = xrf_df.set_index("Element")["XRF_wt_percent_dry"].to_dict()

        ratio_df = pd.read_csv("element_to_oxide_ratios.csv")
        conversion_ratios = ratio_df.set_index("Element")["ElementToOxideRatio"].to_dict()
    except Exception as e:
        print(f"Error loading required CSV files: {e}")
        return

    # === Convert Oxides to Elemental Composition (dry basis) ===
    elemental_percent_dry = convert_oxides_to_elements(oxide_wt_percent, conversion_ratios)

    # === Get moisture and calculate wet composition ===
    moisture_frac = get_float_input("Enter moisture fraction of Fe filter cake (e.g. 0.75): ")

    result = calculate_normalised_wet_composition(moisture_frac, elemental_percent_dry)

    # === Output ===
    print("\n Wet composition (% by mass):")
    for element, wt_pct in sorted(result.items(), key=lambda x: -x[1]):
        print(f"  {element:>4s}: {wt_pct:7.3f} %")

if __name__ == "__main__":
    main()