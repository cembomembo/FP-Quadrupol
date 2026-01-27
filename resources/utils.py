# utils.py
import numpy as np
import os
from scipy.signal import find_peaks

def load_spectrum(filepath: str) -> tuple[np.ndarray, np.ndarray]:
    """Returns: mass (x), intensity (y)"""
    try:
        raw_data = np.genfromtxt(filepath, delimiter='\t', dtype=str)
        # Fix commas and convert
        clean_data = np.char.replace(raw_data, ',', '.').astype(float)
        # Col 0 = Intensity, Col 1 = Mass/10
        return clean_data[:, 1] * 10, clean_data[:, 0]
    except Exception as e:
        print(f"Error loading {os.path.basename(filepath)}: {e}")
        return np.array([]), np.array([])

def get_peak_height_robust(mass, intensity, target_mass, search_window):
    """Finds peak intensity robustly using relative prominence."""
    mask = (mass > target_mass - search_window) & (mass < target_mass + search_window)
    if not np.any(mask): return 0.0
    
    m_local = mass[mask]
    i_local = intensity[mask]
    
    # Noise threshold: 5% of local max
    local_max = np.max(i_local)
    if local_max == 0: return 0.0
    
    peaks, _ = find_peaks(i_local, prominence=(local_max * 0.05))
    
    if len(peaks) == 0:
        return float(np.max(i_local))

    # Pick the peak physically closest to the target mass
    peak_masses = m_local[peaks]
    idx = np.argmin(np.abs(peak_masses - target_mass))
    return float(i_local[peaks[idx]])