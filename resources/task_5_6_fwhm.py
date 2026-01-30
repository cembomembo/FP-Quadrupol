import numpy as np
import pandas as pd
import os
import glob
from config import DATA_DIR
from utils import load_spectrum, calculate_fwhm_robust

# --- PHYSICS CONSTANTS ---
U_FR = 113.825        # Formation Region Potential [V]
L_RODS = 0.100        # Length of Quadrupole Rods [m]
F_RF = 2.5e6          # RF Frequency [Hz]
E_CHARGE = 1.602e-19  # Elementary Charge [C]
U_MASS = 1.6605e-27   # Atomic Mass Unit [kg]

# --- TARGETS ---
TARGET_IONS = {
    'N2+': {'mass_u': 28.0},
    'O2+': {'mass_u': 32.0}
}

# --- FILE CONFIGURATION ---
# Mapping U_FA (Field Axis Potential) to filename patterns
# Note: Ensure these patterns match your specific file naming convention
UFA_SERIES = [
    (112.9, "*ufa1129*"),
    (98.0,  "*ufa981*"),
    (83.0,  "*ufa830*"),
    (63.0,  "*ufa629*"),
    (43.0,  "*ufa431*"),
    (23.0,  "*ufa231*"),
    (3.0,   "*ufa30*") # Sometimes labeled as 03 or similar
]

def calculate_oscillations(u_b, mass_u):
    """
    Calculates number of oscillations n based on ion energy.
    n = f * L / v_z
    v_z = sqrt(2 * E * U_B / m_kg)
    """
    if u_b <= 0: return 0 # Physical safeguard
    
    mass_kg = mass_u * U_MASS
    v_z = np.sqrt((2 * E_CHARGE * u_b) / mass_kg)
    n = F_RF * (L_RODS / v_z)
    return n

def run_task_6_analysis():
    print("--- TASK 6: FWHM & Oscillation Analysis ---")
    results = []

    for u_fa, pattern in UFA_SERIES:
        # Find file
        search_path = os.path.join(DATA_DIR, pattern + ".txt")
        files = glob.glob(search_path)
        
        if not files:
            print(f"Warning: No file found for U_FA={u_fa} V (Pattern: {pattern})")
            continue
            
        filepath = files[0] # Take first match
        u_b = U_FR - u_fa
        
        # Load Data
        m, i_raw = load_spectrum(filepath)
        if len(m) == 0: continue
        
        # Note: No specific gain mult needed if we just want width (FWHM),
        # but consistency is good. Assuming raw is proportional to Amps.
        
        for ion, props in TARGET_IONS.items():
            target_m = props['mass_u']
            
            # 1. Calculate FWHM
            # We use a slightly wider window (2.0) because peaks get broad at high U_B
            meas_m, fwhm, _ = calculate_fwhm_robust(m, i_raw, target_m, window=1.1)
            
            # 2. Calculate Oscillations (n)
            n_osc = calculate_oscillations(u_b, target_m)
            
            if fwhm:
                results.append({
                    'U_FA [V]': u_fa,
                    'U_B [V]': round(u_b, 2),
                    'Ion': ion,
                    'Mass_Target': target_m,
                    'm_meas [Th]': round(meas_m, 3),
                    'FWHM (dm) [Th]': round(fwhm, 4),
                    'Oscillations (n)': round(n_osc, 2)
                })

    # Export
    if results:
        df = pd.DataFrame(results)
        output_file = 'task_6_fwhm_results.csv'
        df.to_csv(output_file, index=False)
        print(f"  > Results saved to {output_file}")
        print("\nPreview:")
        print(df[['U_B [V]', 'Ion', 'FWHM (dm) [Th]', 'Oscillations (n)']].head(10))
    else:
        print("Error: No results generated. Check file patterns.")

if __name__ == "__main__":
    run_task_6_analysis()