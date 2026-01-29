import numpy as np
import pandas as pd
import os
from config import DATA_DIR
from utils import load_spectrum, calculate_fwhm_robust

# --- CONFIGURATION ---
# Target masses for Air components as per protocol section 5.4
TARGET_PEAKS = {
    'N+': 14.0,
    'H2O+': 18.0,
    'N2+': 28.0,
    'O2+': 32.0,
    'Ar+': 40.0
}

# Mapping filenames to their specific gain/electrometer range 
FILES = [
    ('Res 6', 'FP10_qmf260114_012_air_sp10_em-10_p15e-5_res6.txt', 1e-10),
    ('Res 5', 'FP10_qmf260114_013_air_sp10_em-10_p15e-5_res5.txt', 1e-10),
    ('Res 4', 'FP10_qmf260114_014_air_sp10_em-10_p15e-5_res4.txt', 1e-10),
    ('Res 3', 'FP10_qmf260114_015_air_sp10_em-9_p15e-5_res3.txt',  1e-9),
    ('Res 2', 'FP10_qmf260114_016_air_sp10_em-9_p15e-5_res2.txt',  1e-9),
]

def run_fwhm_table_generation():
    print("--- TASK 5.5: FWHM Extraction (utils.calculate_fwhm_robust) ---")
    results = []

    for label, filename, gain in FILES:
        path = os.path.join(DATA_DIR, filename)
        
        # Load and normalize intensity to Amperes to ensure common groundlevel
        m, i_raw = load_spectrum(path)
        if len(m) == 0: continue
        i_amps = i_raw * gain 

        for peak_name, target in TARGET_PEAKS.items():
            # Calling your robust function from utils
            actual_m, fwhm, _ = calculate_fwhm_robust(m, i_amps, target, window=1.9)
            
            if fwhm and fwhm > 0:
                results.append({
                    'Setting': label,
                    'Peak': peak_name,
                    'm_meas [Th]': round(actual_m, 3),
                    'dm [Th]': round(fwhm, 4),
                    'Resolving_Power_R': round(actual_m / fwhm, 2)
                })

    # Create and save the table
    df = pd.DataFrame(results)
    output_name = 'task_5_5_fwhm_table.csv'
    df.to_csv(output_name, index=False)
    
    print(f"  > Table saved to: {output_name}")
    print(df.to_string(index=False)) # Display in console for a quick check

if __name__ == "__main__":
    run_fwhm_table_generation()