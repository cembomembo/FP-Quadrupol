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

    # Annotations
    peaks = [
        (46, 'M+\n(46)'), 
        (45, '-H\n(45)'), 
        (31, '$CH_2OH^+$\n(31)')
    ]
    
    for mass, txt in peaks:
        h = get_peak_height_robust(m, i_norm, mass, 1.0)
        if h > 0:
            plt.annotate(txt, xy=(mass, h), xytext=(mass, h*1.5),
                         arrowprops=dict(facecolor='black', shrink=0.05), ha='center')

    plt.xlim(10, 50)
    plt.ylim(0)
    plt.title('Ethanol Spectrum')    
    plt.xlabel('Mass-to-Charge Ratio ($m/z$)')
    plt.ylabel('Partial Pressure $1/10^{-6}hPa$')
    plt.legend()
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig('task_5_3_ethanol.png', dpi=300)
    print("  > Saved task_5_3_ethanol.png")
    plt.show()

if __name__ == "__main__":
    run_task_5_3()