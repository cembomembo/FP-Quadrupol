# task_5_3.py
import numpy as np
import matplotlib.pyplot as plt
import os
from config import PRESSURE, DATA_DIR
from utils import load_spectrum, get_peak_height_robust

def run_task_5_3():
    print("--- TASK 5.3: Ethanol ---")
    file_bg = 'FP10_qmf260114_003_bg_sp10_em-10_p54e-6.txt'
    file_eth = 'FP10_qmf260114_009_eth_sp10_em-11_p16e-5.txt'
    m_bg, i_bg = load_spectrum(os.path.join(DATA_DIR, file_bg))
    m, i = load_spectrum(os.path.join(DATA_DIR, file_eth))

    if len(m) == 0: return

    i_bg_norm = i_bg / PRESSURE['bg']
    i_norm = i / PRESSURE['eth']

    i_bg_interp = np.interp(m, m_bg, i_bg_norm)

    plt.figure(figsize=(10, 6))    
    plt.plot(m, i_bg_interp, color='orange', alpha=0.6, label='Background')
    plt.plot(m, i_norm, color='green', label='Ethanol Sample')

    # --- PEAK DATA: (Mass, Label, Is_Impurity) ---
    peak_data = [
        # --- C2HxO+ Group (46-41) ---
        (46.7, '$CH_3CH_2OH^+$)', False), # Parent
        (45.65, '$C_2H_5O^+$', False),          # M - H
        (44.6, '$C_2H_4O^+$', False),
        (43.6, '$C_2H_3O^+$', False),
        (42.5, '$C_2H_2O^+$', False),
        (41.5, '$C_2HO^+$', False),
        (39.4, '$C_3H_3^+$', False),

        # --- Impurities ---
        (40.5, '$Ar^+$', True),                # "Aus dem vorherigen Versuch"

        # --- CHxO+ Group (31-28) ---
        (31.3, '$CH_2OH^+$', False),            # Base Peak (Primary Alcohol)
        (30.3, '$CHOH^+$', False),
        (29.3, '$COH^+/C_2H_5^+$', False),      # Overlap of COH+ and C2H5+ mentioned in text
        
        # --- Mass 28 Overlap ---
        (28.2, '$N_2^+/CO^+$', True),           # "aus der Luft" (Impurity dominant)

        # --- C2Hx+ Group (27-25) ---
        (27.3, '$C_2H_3^+$', False),
        (26.18, '$C_2H_2^+$', False),
        (25.1, '$C_2H^+$', False),

        # --- Water Group (Impurity/Mix) ---
        (18.1, '$H_2O^+$', True),               # "aus Feuchtigkeit"
        (17.1, '$OH^+$', True),                 # "Feuchtigkeit und OH-Gruppe"
        (16.1, '$O^+$', True),

        # --- Methyl Group (15-12) ---
        (15.1, '$CH_3^+$', False),
        (14.1, '$CH_2^+$', False),
        (13.1, '$CH^+$', False),
        (12.1, '$C^+$', False),
    ]

    # --- PLOTTING LOOP ---
    for idx, (mass, txt, is_impurity) in enumerate(peak_data):
        h = get_peak_height_robust(m, i_norm, mass, 0.8)
        
        if h > 0:
            # STYLE LOGIC
            if is_impurity:
                color = 'red'
                alpha = 0.7
                fontweight = 'normal'
                offset_y = 40 + (10 * (idx % 2))
                x=0
                angle=90
                arrow_style = dict(arrowstyle='->', color=color, lw=1, alpha=0.6)
                if mass==28.2: 
                    offset_y = 6
                    x=-20 
                    angle=0
            
            elif mass in [46, 31, 45]:
                # Main Peaks: Black, Bold (Parent & Base)
                color = 'blue'
                alpha = 1.0
                fontweight = 'bold'
                offset_y = 25
                x=0
                angle=90
                arrow_style = dict(arrowstyle='->', color=color, lw=2)
            
            else:
                # Minor Fragments: Dark Gray
                color = '#444444'
                alpha = 0.9
                fontweight = 'normal'
                offset_y = 20 + (15 * (idx % 3))
                x=0
                angle=90
                arrow_style = dict(arrowstyle='->', color=color, lw=1.2)

            plt.annotate(
                txt, 
                xy=(mass, h), 
                xytext=(x, offset_y), 
                textcoords='offset points',
                arrowprops=arrow_style,
                ha='center', va='bottom', fontsize=9, 
                color=color, fontweight=fontweight,
                rotation=angle if len(txt) > 8 else 0
            )

    plt.xlim(10, 50)
    plt.ylim(0)
    plt.title('Ethanol Spectrum')    
    plt.xlabel('Mass-to-Charge Ratio ($m/z$)')
    plt.ylabel('Partial Pressure $I/10^{-6}hPa$')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig('task_5_3_ethanol.png', dpi=300)
    print("  > Saved task_5_3_ethanol.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_3()