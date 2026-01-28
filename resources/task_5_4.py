# task_5_4.py
import matplotlib.pyplot as plt
import os
from config import PRESSURE, DATA_DIR
from utils import load_spectrum, get_peak_height_robust

def run_task_5_4():
    print("--- TASK 5.4: Air Spectrum ---")
    file_air = 'FP10_qmf260114_011_air_sp10_em-10_p15e-5.txt'
    m, i = load_spectrum(os.path.join(DATA_DIR, file_air))
    if len(m) == 0: return

    i_norm = i / PRESSURE['air']

    plt.figure(figsize=(10, 6))
    plt.plot(m, i_norm, color='black', label='Air Sample')

    # [cite_start]Standard Air Peaks
    peaks = [
        (28, '$N_2^+$'),
        (32, '$O_2^+$'),
        (40, '$Ar^+$'),
        (44, '$CO_2^+$'),
        (18, '$H_2O^+$'),
        (14, '$N^+$')
    ]

    for mass, label in peaks:
        h = get_peak_height_robust(m, i_norm, mass, 1.0)
        if h > 0:
            plt.axvline(x=mass, color='red', linestyle=':', alpha=0.5)
            plt.text(mass, h*1.05, label, ha='center', va='bottom', color='red', fontsize=10)

    plt.xlim(10, 50)
    plt.title('Task 5.4: Air Spectrum Composition')
    plt.xlabel('Mass (amu)')
    plt.ylabel('Normalized Intensity (A/mbar)')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig('task_5_4_air.png', dpi=300)
    print("  > Saved task_5_4_air.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_4()