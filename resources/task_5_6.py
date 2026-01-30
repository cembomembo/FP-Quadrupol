import numpy as np
import matplotlib.pyplot as plt
import os
from config import DATA_DIR
from utils import load_spectrum

# Import Files
FILES = [
    ('$U_{FA}=112.9, U_{B}=$' ,'FP10_qmf260114_018_air_sp10_em-10_p15e-5_ufa1129.txt', 112.9),
    ('$U_{FA}=98.1, U_{B}=$' ,'FP10_qmf260114_019_air_sp10_em-10_p15e-5_ufa981.txt', 98.1),
    ('$U_{FA}=83.0, U_{B}=$' ,'FP10_qmf260114_020_air_sp10_em-10_p15e-5_ufa830.txt', 83.0),
    ('$U_{FA}=62.9, U_{B}=$' ,'FP10_qmf260114_021_air_sp10_em-10_p15e-5_ufa629.txt', 62.9),
    ('$U_{FA}=43.1, U_{B}=$' ,'FP10_qmf260114_022_air_sp10_em-10_p15e-5_ufa431.txt', 43.1),
    ('$U_{FA}=23.1, U_{B}=$' ,'FP10_qmf260114_023_air_sp10_em-10_p15e-5_ufa231.txt', 23.1),
    ('$U_{FA}=3.0, U_{B}=$' ,'FP10_qmf260114_024_air_sp10_em-10_p15e-5_ufa30.txt', 3.0),
]

# Constants
GAIN = 1e-10
U_FR = 113 # Volts


def run_acceleration_overlay():
    print("--- TASK 5.6: Acceleration Overlay ---")

    plt.figure(figsize=(10, 6))


    for label, filename, u_fa in FILES:
        # Calculate U_B
        u_b = U_FR - u_fa


        # Add U_B to label
        label = label + f"{u_b:.1f}"

        # Create the path
        path = os.path.join(DATA_DIR, filename)
        
        # Load Data
        m, i_raw = load_spectrum(path)
        
        if len(m) == 0:
            print(f"Warning: Empty file {filename}")
            continue
        
        i_amps = i_raw * GAIN
        ground_level = np.percentile(i_amps, 10)
        i_normalized = i_amps - ground_level

        plt.plot(m, i_normalized, label=label, lw=1.2, alpha=0.8)

        # Formatting
    plt.xlabel('m/z $[Th]$')
    plt.ylabel('Partial Pressure $[10^{-6}hPa]$')
    plt.xlim(10,48)
    plt.ylim(0)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.tight_layout()
    
    save_path = 'task_5_6_acceleration_overlay.png'
    plt.savefig(save_path, dpi=300)
    print(f"  > Saved: {save_path}")
    plt.show()

if __name__ == "__main__":
    run_acceleration_overlay()