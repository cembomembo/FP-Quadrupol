import numpy as np
import os
from scipy.signal import find_peaks

def load_spectrum(filepath: str) -> tuple[np.ndarray, np.ndarray]:
    """Returns: sorted_mass (x), intensity (y)"""
    try:
        # Load raw strings
        raw_data = np.genfromtxt(filepath, delimiter='\t', dtype=str)
        # Fix commas and convert
        clean_data = np.char.replace(raw_data, ',', '.').astype(float)
        
        # Extract columns (Col 1 = Mass/10, Col 0 = Intensity)
        mass = clean_data[:, 1] * 10
        intensity = clean_data[:, 0]
        
        # The QMS saves data out of order. We must sort it here.
        sort_idx = np.argsort(mass)
        return mass[sort_idx], intensity[sort_idx]
        
    except Exception as e:
        print(f"Error loading {os.path.basename(filepath)}: {e}")
        return np.array([]), np.array([])

def get_peak_height_robust(mass, intensity, target_mass, search_window):
    """Finds peak intensity robustly."""
    mask = (mass > target_mass - search_window) & (mass < target_mass + search_window)
    if not np.any(mask): return 0.0
    
    i_local = intensity[mask]
    
    # Noise threshold: 5% of local max
    local_max = np.max(i_local)
    if local_max == 0: return 0.0
    
    # Use find_peaks to ignore noise
    peaks, _ = find_peaks(i_local, prominence=(local_max * 0.05))
    
    if len(peaks) == 0:
        return float(np.max(i_local))

    # Return intensity of the peak closest to target mass
    # (Since we masked the mass/intensity arrays, we need to map peak indices back)
    m_local = mass[mask]
    peak_masses = m_local[peaks]
    idx = np.argmin(np.abs(peak_masses - target_mass))
    return float(i_local[peaks[idx]])