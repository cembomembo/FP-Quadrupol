# task_5_2.py
import numpy as np
import matplotlib.pyplot as plt
import os
from config import PRESSURE, DATA_DIR
from utils import load_spectrum, get_peak_height_robust

def run_task_5_2():
    print("--- TASK 5.2: Acetone ---")
    file_bg = 'FP10_qmf260114_003_bg_sp10_em-10_p54e-6.txt'
    file_ac = 'FP10_qmf260114_007_ac_sp10_em-11_p14e-5.txt'
    m_bg, i_bg = load_spectrum(os.path.join(DATA_DIR, file_bg))
    m, i = load_spectrum(os.path.join(DATA_DIR, file_ac))
    
    if len(m) == 0: return

    i_bg_norm = i_bg / PRESSURE['bg']
    i_norm = i / PRESSURE['ac']
    
    i_bg_interp = np.interp(m, m_bg, i_bg_norm)
    
    plt.figure(figsize=(10, 6))
    plt.plot(m, i_bg_interp, color='orange', alpha=0.6, label='Background')
    plt.plot(m, i_norm, color='purple', label='Acetone ($CH_3COCH_3$)')
    
    # Annotate Fragments
    # 1. Main Acetone Peaks (Parent + Base + Methyl)
    # These get prominent labels (Black, bold)
    peaks = [
        (59.0, '$M^+$'),             # Acetone Parent (CH3-CO-CH3+)
        (43.6, '$CH_3CO^+$'),        # Acetone Base Peak
        (15.1, '$CH_3^+$')           # Methyl Group
    ]

    # 2. Sub-Peaks (Fragments + Impurities)
    # These get smaller labels (Blue/Red, standard font)
    sub_peaks = [
        # --- Impurities ---
        (44.6, '$CO_2^+$', True),          # Impurity
        (40.6, '$Ar^+$', True),            # Argon remnant
        (28.2, '$CO^+|N_2^+$', True),      # Fragment + Air (N2)
        (18.15, '$H_2O^+$', True),             # Fragment + Air (O2)
        (17.15, '$OH^+$', True),             # Fragment + Air (O2)
        (16.0, '$O^+$', True),             # Fragment + Air (O2)
        
        # --- C3Hx Group (Double bond split) ---
        (39.5, '$C_3H_3^+$', False),
        (38.5, '$C_3H_2^+$', False),
        (37.5, '$C_3H^+$', False),
        
        # --- Acetone Group Fragments ---
        (42.6, '$CH_2CO^+$', False),
        (41.6, '$CHCO^+$', False),
        (29.2, '$M^{2+}$', False),          # Doubly ionized Acetone (58/2 = 29)
        
        # --- C2Hx Group (C-CHx) ---
        (27.2, '$C_2H_3^+$', False),        # C-CH3+
        (26.2, '$C_2H_2^+$', False),        # C-CH2+
        (25.2, '$C_2H^+$', False),          # C-CH+
        
        # --- Small Fragments ---
        (14.1, '$CH_2^+$', False),
        (13.0, '$CH^+$', False),
        (12.0, '$C^+$', False)
    ]

    for mass, txt in peaks:
        h = get_peak_height_robust(m, i_norm, mass, 1.0)
        if h > 0:
            plt.annotate(
                txt, 
                xy=(mass, h), 
                color='blue',
                xytext=(-10, 30),              # Position text 30 points above the peak
                textcoords='offset points',  # Use relative offset instead of absolute scaling
                arrowprops=dict(
                    arrowstyle='->',         # Slimmer, cleaner arrow head
                    connectionstyle='arc3',  # Straight line
                    color='blue',           # Use 'red' for impurities
                    lw=1.2                   # Line width
                ),
                ha='center',
                va='bottom',
                fontweight='bold'
            )
    for idx, (mass, txt, is_impurity) in enumerate(sub_peaks):
            h = get_peak_height_robust(m, i_norm, mass, 0.8)
            
            # Color logic: Red for likely impurities/overlaps, Blue for pure fragments
            if is_impurity:
                # Impurity Style: Red, slightly higher label to distinguish
                color = 'red'
                alpha = 0.8
                fontweight = 'normal'
                offset_y = 35 + (10 * (idx % 2)) # Stagger slightly high
            else:
                # Minor Fragment Style: Dark Gray, standard font
                color = '#444444'
                alpha = 0.9
                fontweight = 'normal'
                offset_y = 20 + (15 * (idx % 2)) # Stagger low
            
            # Stagger heights: 20, 35, 20, 35...
            offset_y = 20 + (15 * (idx % 2)) 

            if mass==28.2:
                offset_y = 8
                x=-20 
                angle=0
            else: 
                x=0
                angle=90

            if h > 0:
                plt.annotate(
                    txt, 
                    xy=(mass, h), 
                    xytext=(x, offset_y), 
                    textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2, alpha=alpha),
                    ha='center', va='bottom', fontsize=9, 
                    color=color, fontweight=fontweight,
                    rotation=angle if len(txt) > 6 else 0
                )

    plt.xlim(10, 60)
    plt.ylim(0)
    plt.title('Acetone Spectrum')
    plt.xlabel('m/z ($Th$)')
    plt.ylabel('Partial Pressure $10^{-6}hPa$')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig('task_5_2_acetone.png', dpi=300)
    print("  > Saved task_5_2_acetone.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_2()