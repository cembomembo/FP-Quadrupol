# config.py
# Physical Constants
LENGTH_ROD = 0.1 # meters
FREQUENCY = 2.5e6 # Hz
ATOMIC_MASS = 1.66054e-27 # kg
ELECTRIC_CHARGE = 1.602e-19 # C
U_FR = 113.825   # Formation Region Voltage

# Data Directory
DATA_DIR = './data'

# Pressures (mbar)
PRESSURE = {  
    'bg': 5.4e-6,
    'ar': 1.3e-5,
    'ac': 1.4e-5,
    'eth': 1.6e-5,
    'air': 1.5e-5
}

# Voltages for Task 5.6
U_FA = {
    '112': 112.9, '98': 98.0, '83': 83.0, '63': 63.0, 
    '43': 43.0, '23': 23.0, '3': 3.0
}