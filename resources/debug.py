import numpy as np
import os

DATA_DIR = './data'
file_bg = 'FP10_qmf260114_003_bg_sp10_em-10_p54e-6.txt'
file_ar = 'FP10_qmf260114_004_ar_sp10_em-10_p13e-5.txt'

def check_file(name, path):
    print(f"\n--- CHECKING {name} ---")
    try:
        # Load raw strings
        raw = np.genfromtxt(path, delimiter='\t', dtype=str)
        # Convert
        clean = np.char.replace(raw, ',', '.').astype(float)
        
        # Col 1 is Mass (we assume Mass/10 based on logbook)
        mass = clean[:, 1] * 10
        intensity = clean[:, 0]
        
        print(f"  > Data Points: {len(mass)}")
        print(f"  > Mass Range:  {mass.min():.2f}  to  {mass.max():.2f} amu")
        print(f"  > First 5 Masses: {mass[:5]}")
        print(f"  > Is sorted?   {np.all(mass[:-1] <= mass[1:])}")
        
    except Exception as e:
        print(f"  > ERROR: {e}")

check_file("BACKGROUND", os.path.join(DATA_DIR, file_bg))
check_file("ARGON", os.path.join(DATA_DIR, file_ar))