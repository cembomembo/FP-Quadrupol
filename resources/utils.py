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

def calculate_fwhm(mass, intensity, target_mass, window=1.5):
    """
    Calculates Full Width at Half Maximum (FWHM) for a peak near target_mass.
    Returns: (peak_mass, fwhm, peak_height)
    """
    # 1. Mask data to local area
    mask = (mass > target_mass - window) & (mass < target_mass + window)
    if not np.any(mask): return None, None, None
    
    m_loc = mass[mask]
    i_loc = intensity[mask]
    
    # 2. Find Max
    i_max = np.max(i_loc)
    if i_max == 0: return None, None, None
    m_max = m_loc[np.argmax(i_loc)]
    
    # 3. Find Half Max
    half_max = i_max / 2.0
    
    # 4. Find crossings (Linear Interpolation)
    # We look for where intensity - half_max changes sign
    diff = i_loc - half_max
    crossings = np.where(np.diff(np.sign(diff)))[0]
    
    if len(crossings) < 2:
        return m_max, 0.0, i_max # Peak too narrow to resolve
        
    # Take the two crossings surrounding the peak
    # (Simplified: just take first and last in window if multiple noise crossings)
    left_idx = crossings[0]
    right_idx = crossings[-1]
    
    def get_x_at_y(idx, target_y):
        y1, y2 = i_loc[idx], i_loc[idx+1]
        x1, x2 = m_loc[idx], m_loc[idx+1]
        # Linear interp formula
        if y2 == y1: return x1
        return x1 + (target_y - y1) * (x2 - x1) / (y2 - y1)

    m_left = get_x_at_y(left_idx, half_max)
    m_right = get_x_at_y(right_idx, half_max)
    
    return m_max, (m_right - m_left), i_max