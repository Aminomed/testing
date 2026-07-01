import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data=pd.read_csv('Data/Kalibration der Abszisse.txt', sep=' ')
def lin_fit(x, m, c): return m * x + c
popt_cal, pcov_cal = curve_fit(lin_fit, data['Pixel'], data['Messuhr[mm]'])
def pixel_to_mm(pixel): return lin_fit(pixel, *popt_cal)

messung1 = pd.read_csv('Data/Messung1.txt', sep=' ')
messung1['x_mm'] = pixel_to_mm(messung1['pixel'])
def sinc_fit(x, I_0, a, x0, I_bg):
    return I_0 * (np.sinc(a * (x - x0) / np.pi))**2 + I_bg

x0_guess = messung1.loc[messung1['counts'].idxmax(), 'x_mm']
I_0_guess = messung1['counts'].max() - messung1['counts'].min()
I_bg_guess = messung1['counts'].min()
a_guess = 10.0 
p0 = [I_0_guess, a_guess, x0_guess, I_bg_guess]

popt_sinc, pcov_sinc = curve_fit(sinc_fit, messung1['x_mm'], messung1['counts'], p0=p0)

plt.figure(figsize=(10, 6))
plt.plot(messung1['x_mm'], messung1['counts'], '.', label='Messdaten', markersize=2)
x_plot = np.linspace(messung1['x_mm'].min(), messung1['x_mm'].max(), 1000)
plt.plot(x_plot, sinc_fit(x_plot, *popt_sinc), '-', label='Theorie-Fit', linewidth=2)
plt.savefig('plot.png')

print("Fitted a:", popt_sinc[1])
