import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def plot_resolution_vs_oscillations():
    print("--- TASK 6: Plotting Resolution vs. Oscillations ---")
    
    # 1. Load Data
    csv_file = 'task_6_fwhm_results_final.csv'
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{csv_file}'. Please run the extraction script first.")
        return

    plt.figure(figsize=(10, 6))
    
    # 2. Define Theoretical Model (dm = A / n^2)
    # The resolution R ~ n^2, and R = m / dm, so dm ~ m / n^2. 
    # For a fixed mass, dm is proportional to 1/n^2.
    def theory_model(n, A):
        return A / (n**2)

    # 3. Plotting Loop
    # We plot N2+ and O2+ as requested
    ions = ['N2+', 'O2+']
    colors = {'N2+': 'blue', 'O2+': 'green'}
    
    for ion in ions:
        sub = df[df['Ion'] == ion].sort_values('Oscillations (n)')
        if sub.empty: continue
        
        n_data = sub['Oscillations (n)']
        dm_data = sub['FWHM (dm) [Th]']
        
        # Plot Measured Data
        plt.plot(n_data, dm_data, 'o', label=f'{ion} Measured', color=colors[ion], zorder=3)

    # 4. Formatting
    plt.title(r'Dependence of Peak Width on Ion Oscillations ($\Delta m$ vs. $n$)')
    plt.xlabel('Number of Oscillations $n$')
    plt.ylabel(r'$\Delta m$ [Th] (FWHM)')
    plt.legend()
    plt.grid(True, which='both', ls='-', alpha=0.2)
    plt.tight_layout()
    
    # 5. Save
    output_img = 'task_6_resolution_trend.png'
    plt.savefig(output_img, dpi=300)
    print(f"  > Plot saved to {output_img}")
    plt.show()

if __name__ == "__main__":
    plot_resolution_vs_oscillations()