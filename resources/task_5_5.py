import numpy as np
import matplotlib.pyplot as plt
import os
from config import DATA_DIR
from utils import load_spectrum

# --- CONFIGURATION ---
FILES = [
    # Label, Filename, Gain (Electrometer Range)
    ('Res 6 (High Res)', 'FP10_qmf260114_012_air_sp10_em-10_p15e-5_res6.txt', 1e-10),
    ('Res 5',            'FP10_qmf260114_013_air_sp10_em-10_p15e-5_res5.txt', 1e-10),
    ('Res 4',            'FP10_qmf260114_014_air_sp10_em-10_p15e-5_res4.txt', 1e-10),
    ('Res 3',            'FP10_qmf260114_015_air_sp10_em-9_p15e-5_res3.txt',  1e-9),
    ('Res 2 (Low Res)',  'FP10_qmf260114_016_air_sp10_em-9_p15e-5_res2.txt',  1e-9),
]

def run_resolution_overlay():
    print("--- TASK 5.5: Resolution Overlay ---")
    
    plt.figure(figsize=(10, 6))
    
    for label, filename, gain in FILES:
        path = os.path.join(DATA_DIR, filename)
        
        # Load Data
        m, i_raw = load_spectrum(path)
        
        if len(m) == 0:
            print(f"Warning: Empty file {filename}")
            continue
        
        i_amps = i_raw * gain 
        ground_level = np.percentile(i_amps, 10)
        i_normalized = i_amps - ground_level

        plt.plot(m, i_normalized, label=label, lw=1.2, alpha=0.8)

    # Formatting
    plt.xlabel('m/z ($Th$)')
    plt.ylabel('Partial Pressure $10^{-6}hPa$')
    plt.xlim(10,48)
    plt.ylim(0)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.tight_layout()
    
    save_path = 'task_5_5_resolution_overlay.png'
    plt.savefig(save_path, dpi=300)
    print(f"  > Saved: {save_path}")
    plt.show()

if __name__ == "__main__":
    run_resolution_overlay()