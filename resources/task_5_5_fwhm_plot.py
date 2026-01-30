import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_resolution_trends(csv_path='task_5_5_fwhm_table_final.csv'):
    # Load the extracted data
    df = pd.read_csv(csv_path)
    
    # Define order and colors for consistency with previous plots
    setting_order = ['Res 6', 'Res 5', 'Res 4', 'Res 3', 'Res 2']
    available_settings = [s for s in setting_order if s in df['Setting'].unique()]
    
    plt.figure(figsize=(10, 6))
    
    for setting in available_settings:
        sub = df[df['Setting'] == setting].sort_values('m_meas [Th]')
        m = sub['m_meas [Th]']
        dm = sub['dm [Th]']
        
        # Plot data points with markers
        line, = plt.plot(m, dm, 'o--', label=f'{setting} Setting', markersize=6)
        
        # Optional: Add a light trendline to guide the eye
        if len(m) > 1:
            z = np.polyfit(m, dm, 1)
            p = np.poly1d(z)
            plt.plot(m, p(m), color=line.get_color(), alpha=0.9, ls='-')

    # Styling for report-ready quality
    plt.xlabel('$m$ [Th]')
    plt.ylabel('$\Delta m$ [Th] (FWHM)')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend(title="Resolution Config")
    plt.tight_layout()

    # Save for the report
    save_path = 'task_5_5_resolution_trend.png'
    plt.savefig(save_path, dpi=300)
    print(f"  > Trend plot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    plot_resolution_trends()