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
    plt.plot(m, i_norm, color='teal', label='Air Sample')

    # [cite_start]Standard Air Peaks
    # --- PEAK DATA: (Mass, Label, Is_Impurity) ---
    peak_data = [
        (44.5, '$CO_2^+$', True),
        (40.3, '$Ar^+$', False),
        (32.3, '$O_2^+$', False),
        (28.2, '$N_2^+$', False),
        (18.1, '$H_2O^+$', True),
        (17.1, '$OH^+$', True),
        (14.1, '$N^+$', False)
    ]

    # --- PLOTTING LOOP ---
    for idx, (mass, txt, is_impurity) in enumerate(peak_data):
        h = get_peak_height_robust(m, i_norm, mass, 0.6)
        
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
            
            else:
                color = 'blue'
                fontweight = 'normal'
                offset_y = 20 + (15 * (idx % 3))
                x=0
                angle=90
                arrow_style = dict(arrowstyle='->', color=color, lw=1.2)
                if mass==28.2: 
                    offset_y = 6
                    x=-20 
                    angle=0

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
    plt.title('Air Spectrum Composition')
    plt.xlabel('m/z ($Th$)')
    plt.ylabel('Partial Pressure $10^{-6}hPa$')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig('task_5_4_air.png', dpi=300)
    print("  > Saved task_5_4_air.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_4()