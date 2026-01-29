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

def calculate_fwhm_robust(mass, intensity, target_mass, window=1.5):
    """
    Calculates FWHM robustly by:
    1. Correcting for local baseline offset.
    2. Searching outwards from the peak center to avoid distant noise.
    3. Using linear interpolation for sub-step precision.
    """
    # 1. Mask data to local area
    mask = (mass > target_mass - window) & (mass < target_mass + window)
    if not np.any(mask): 
        return None, None, None
    
    m_loc = mass[mask]
    i_loc = intensity[mask]
    
    # 2. Find Peak Maximum and Location
    idx_max = np.argmax(i_loc)
    i_max = i_loc[idx_max]
    m_max = m_loc[idx_max]
    
    # 3. Determine Local Baseline (Crucial for correct width)
    # We assume the lowest point in the window is the baseline
    i_base = np.min(i_loc)
    
    # Calculate Half-Max relative to baseline
    # Level = Baseline + (Height / 2)
    half_max_level = i_base + (i_max - i_base) / 2.0
    
    # 4. Search LEFT from peak center
    # We flip the left side array to search "backwards" from the peak
    left_side_i = i_loc[:idx_max][::-1]
    left_side_m = m_loc[:idx_max][::-1]
    
    # Find where it drops below half_max
    below_half_left = np.where(left_side_i < half_max_level)[0]
    if len(below_half_left) == 0:
        return m_max, None, i_max # Peak is cut off at edge
    
    # Get indices for interpolation (closest points bracketing the level)
    idx_L2 = below_half_left[0]      # First point below level (in flipped array)
    idx_L1 = idx_L2 - 1              # The point just before it (still above level)
    
    # Interpolate Left Edge
    if idx_L2 == 0: # Peak starts below half max immediately (rare)
        m_left = left_side_m[0]
    else:
        y1, y2 = left_side_i[idx_L1], left_side_i[idx_L2]
        x1, x2 = left_side_m[idx_L1], left_side_m[idx_L2]
        m_left = x1 + (half_max_level - y1) * (x2 - x1) / (y2 - y1)

    # 5. Search RIGHT from peak center
    right_side_i = i_loc[idx_max:]
    right_side_m = m_loc[idx_max:]
    
    below_half_right = np.where(right_side_i < half_max_level)[0]
    if len(below_half_right) == 0:
        return m_max, None, i_max
        
    idx_R2 = below_half_right[0]
    idx_R1 = idx_R2 - 1
    
    # Interpolate Right Edge
    if idx_R2 == 0:
        m_right = right_side_m[0]
    else:
        y1, y2 = right_side_i[idx_R1], right_side_i[idx_R2]
        x1, x2 = right_side_m[idx_R1], right_side_m[idx_R2]
        m_right = x1 + (half_max_level - y1) * (x2 - x1) / (y2 - y1)

    # 6. Result
    fwhm = m_right - m_left
    return m_max, fwhm, i_max