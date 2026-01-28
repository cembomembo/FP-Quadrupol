# task_5_3.py
import matplotlib.pyplot as plt
import os
from config import PRESSURE, DATA_DIR
from utils import load_spectrum, get_peak_height_robust

def run_task_5_3():
    print("--- TASK 5.3: Ethanol ---")
    file_eth = 'FP10_qmf260114_009_eth_sp10_em-11_p16e-5.txt'
    m, i = load_spectrum(os.path.join(DATA_DIR, file_eth))
    if len(m) == 0: return

    i_norm = i / PRESSURE['eth']

    plt.figure(figsize=(10, 6))
    plt.plot(m, i_norm, color='green', label='Ethanol Sample')

    # Annotations
    peaks = [
        (46, 'M+\n(46)'), 
        (45, '-H\n(45)'), 
        (31, '$CH_2OH^+$\n(31)')
    ]
    
    for mass, label in peaks:
        h = get_peak_height_robust(m, i_norm, mass, 1.0)
        plt.axvline(x=mass, color='green', linestyle=':', alpha=0.5)
        plt.text(mass, h*1.05, label, ha='center', va='bottom', color='green')

    # Mark Air Contamination if visible
    h_28 = get_peak_height_robust(m, i_norm, 28.0, 1.0)
    if h_28 > 0.5 * i_norm.max(): # Only if large
        plt.text(28, h_28*1.05, 'Air ($N_2$)', color='red', ha='center')

    plt.xlim(20, 50)
    plt.title('Task 5.3: Ethanol Spectrum ($C_2H_5OH$)')
    plt.xlabel('Mass (amu)')
    plt.ylabel('Normalized Intensity (A/mbar)')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig('task_5_3_ethanol.png', dpi=300)
    print("  > Saved task_5_3_ethanol.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_3()