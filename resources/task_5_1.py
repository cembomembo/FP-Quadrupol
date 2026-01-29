# task_5_1.py
import numpy as np
import matplotlib.pyplot as plt
import os
from config import PRESSURE, DATA_DIR
from utils import load_spectrum, get_peak_height_robust

def run_task_5_1():
    print("--- TASK 5.1: Argon & Background Subtraction ---")
    file_bg = 'FP10_qmf260114_003_bg_sp10_em-10_p54e-6.txt'
    file_ar = 'FP10_qmf260114_004_ar_sp10_em-10_p13e-5.txt'

    m_bg, i_bg = load_spectrum(os.path.join(DATA_DIR, file_bg))
    m_ar, i_ar = load_spectrum(os.path.join(DATA_DIR, file_ar))

    if len(m_bg) == 0: return

    # Normalize
    i_bg_norm = i_bg / PRESSURE['bg']
    i_ar_norm = i_ar / PRESSURE['ar']

    # Interpolate Background to Argon grid
    i_bg_interp = np.interp(m_ar, m_bg, i_bg_norm)

    # Calculate Factor (Use window=1.5 to avoid Ar++ at 20)
    h_w_ar = get_peak_height_robust(m_ar, i_ar_norm, 18.0, 1.5)
    h_w_bg = get_peak_height_robust(m_ar, i_bg_interp, 18.0, 1.5)
    
    factor = h_w_ar / h_w_bg if h_w_bg > 0 else 1.0
    print(f"  > H2O Scaling Factor: {factor:.4f}")

    # Subtract
    i_clean = i_ar_norm - (i_bg_interp * factor)
    i_clean[i_clean < 0] = 0

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(m_ar, i_ar_norm, color='gray', alpha=0.5, ls='--', label='Argon Raw')
    plt.plot(m_ar, i_bg_interp * factor, color='orange', alpha=0.6, label='Background')
    plt.plot(m_ar, i_clean, color='blue', lw=1.5, label='Argon Corrected')

    # --- PEAK LABELS ---
    # Ar+ (40)
    plt.axvline(x=40.45, color='blue', linestyle=':', alpha=0.6, ymax=0.9)
    plt.text(39, np.max(i_clean), '$Ar^+$', ha='center', va='bottom', color='blue', fontweight='bold')
    
    # Ar++ (20)
    h = get_peak_height_robust(m_ar, i_clean, 20.0, 1.0)
    plt.axvline(x=20.1, color='blue', linestyle=':', alpha=0.6, ymax=0.21)
    plt.text(19.5, h*1.1, '$Ar^{2+}$', ha='center', va='bottom', color='blue')

    # 36Ar+ (20)
    h = get_peak_height_robust(m_ar, i_clean, 36.0, 1.0)
    plt.text(35.5, h*2, '$^{36}Ar^{+}$', ha='center', va='bottom', color='blue')

    # -- IMPURITIES --
    # N2+
    h = get_peak_height_robust(m_ar, i_clean, 28.0, 1.0)
    plt.text(27.5, h*2, '$N_{2}^{+}$', ha='center', va='bottom', color='red')
    
    plt.xlim(10, 50)
    plt.ylim(0)
    plt.title('Argon Spectrum')
    plt.xlabel('Mass-to-Charge Ratio ($m/z$)')
    plt.ylabel('Partial Pressure $1/10^{-6}hPa$')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig('task_5_1_argon.png', dpi=300)
    print("  > Saved task_5_1_argon.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_1()