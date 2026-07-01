import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data=pd.read_csv('Data/Kalibration der Abszisse.txt', sep=' ')

def lin_fit(x, m, c):
    return m * x + c

popt_cal, pcov_cal = curve_fit(lin_fit, data['Pixel'], data['Messuhr[mm]'])
print("Kalibration:", popt_cal)

def pixel_to_mm(pixel):
    return lin_fit(pixel, *popt_cal)

messung1 = pd.read_csv('Data/Messung1.txt', sep=' ')
messung1['x_mm'] = pixel_to_mm(messung1['pixel'])
print(messung1.head())
