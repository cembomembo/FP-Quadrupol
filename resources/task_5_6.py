import numpy as np
import matplotlib.pyplot as plt
import os
from config import DATA_DIR
from utils import load_spectrum

# Import Files
FILES = [
    ('$U_{FA}=112.9$' ,'FP10_qmf260114_018_air_sp10_em-10_p15e-5_ufa1129.txt', 112.9),
    ('$U_{FA}=98.1$' ,'FP10_qmf260114_019_air_sp10_em-10_p15e-5_ufa981.txt', 98.1),
    ('$U_{FA}=83.0$' ,'FP10_qmf260114_020_air_sp10_em-10_p15e-5_ufa830.txt', 83.0),
    ('$U_{FA}=62.9$' ,'FP10_qmf260114_021_air_sp10_em-10_p15e-5_ufa629.txt', 62.9),
    ('$U_{FA}=43.1$' ,'FP10_qmf260114_022_air_sp10_em-10_p15e-5_ufa431.txt', 43.1),
    ('$U_{FA}=23.1$' ,'FP10_qmf260114_023_air_sp10_em-10_p15e-5_ufa231.txt', 23.1),
    ('$U_{FA}=3.0$' ,'FP10_qmf260114_024_air_sp10_em-10_p15e-5_ufa30.txt', 3.0),
]

def run_acceleration_overlay():
    print("--- TASK 5.6: Acceleration Overlay ---")

U_FR = 113 # Volts

u_b = U_FR - u_fa