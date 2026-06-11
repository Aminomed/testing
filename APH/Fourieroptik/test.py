import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# TODO 1
data=pd.read_csv('Data/Kalibration der Abszisse.txt', sep=' ')

def lin_fit(x, m, c):
    return m * x + c

popt_cal, pcov_cal = curve_fit(lin_fit, data['Pixel'], data['Messuhr[mm]'])
print(f"Kalibrations-Fit: x[mm] = {popt_cal[0]:.6f} * Pixel + {popt_cal[1]:.6f}")

def pixel_to_mm(pixel):
    return lin_fit(pixel, *popt_cal)

# TODO 2
messung1 = pd.read_csv('Data/Messung1.txt', sep=' ')
messung1['x_mm'] = pixel_to_mm(messung1['pixel'])

def sinc_fit(x, I_0, a, x0, I_bg):
    return I_0 * (np.sinc(a * (x - x0) / np.pi))**2 + I_bg

x0_guess = messung1.loc[messung1['counts'].idxmax(), 'x_mm']
I_0_guess = messung1['counts'].max() - messung1['counts'].min()
I_bg_guess = messung1['counts'].min()
a_guess = 10.0 

p0 = [I_0_guess, a_guess, x0_guess, I_bg_guess]

try:
    popt_sinc, pcov_sinc = curve_fit(sinc_fit, messung1['x_mm'], messung1['counts'], p0=p0)
    print("Fit erfolgreich!")
except Exception as e:
    print("Fit fehlgeschlagen:", e)

# TODO 3
peaks, _ = find_peaks(-messung1['counts'], prominence=1, distance=10)

minima_x = messung1['x_mm'].iloc[peaks].values
minima_counts = messung1['counts'].iloc[peaks].values
x0_center = messung1.loc[messung1['counts'].idxmax(), 'x_mm']

peaks_links = np.sort([x for x in minima_x if x < x0_center])[::-1]
peaks_rechts = np.sort([x for x in minima_x if x > x0_center])

minima_x_clean = []
n_clean = []

for i, x in enumerate(peaks_links):
    n_clean.append(-(i+1))
    minima_x_clean.append(x)
    
for i, x in enumerate(peaks_rechts):
    n_clean.append(i+1)
    minima_x_clean.append(x)
    
n_clean = np.array(n_clean)
minima_x_clean = np.array(minima_x_clean)

def linear_minima(n, m, x0_):
    return m * n + x0_

popt_minima, pcov_minima = curve_fit(linear_minima, n_clean, minima_x_clean)
slope = popt_minima[0]
slope_err = np.sqrt(np.diag(pcov_minima))[0]

lambda_ = 632.8e-6 # in mm
L = 1000.0 # in mm

b = (lambda_ * L) / slope
b_err = np.abs(b) * (slope_err / np.abs(slope))

print(f"Fit-Steigung (λL/b): {slope:.4f} ± {slope_err:.4f} mm")
print(f"Berechnete Spaltbreite b: {np.abs(b):.4f} ± {b_err:.4f} mm")
