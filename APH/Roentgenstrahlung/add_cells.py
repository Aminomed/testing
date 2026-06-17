import json

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + '\n' for line in source.split('\n')[:-1]] + [source.split('\n')[-1]] if source else []
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + '\n' for line in source.split('\n')[:-1]] + [source.split('\n')[-1]] if source else []
    }

with open('Roentgenstrahlung.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells_to_add = [
    create_markdown_cell("## 5. Auswertung\n\n### 5.1 Auswertung des Nulleffekts\nVor Durchführung der eigentlichen Messreihen wurde die natürliche Hintergrundstrahlung (Nulleffekt) bei abgeschalteter Röhrenspannung ($U = 0$ kV, $I = 0$ mA) über eine Messdauer von $\\Delta t = 120$ s bestimmt.\nDie Messung ergab eine mittlere Zählrate von:\n$R_0 = 0.25$ s$^{-1}$\n\nUm die Präzision der Auswertung zu wahren und systematische Fehler bei der Bestimmung des Schwächungskoeffizienten $\\mu$ zu minimieren, wurde der Nulleffekt konsequent von allen nachfolgenden Messwerten abgezogen:\n$R_{korr} = R_{mess} - R_0$"),
    
    create_markdown_cell("### 5.2 Absorption bei unterschiedlicher Dicke\nIn diesem Abschnitt wird die Abschwächung der Röntgenstrahlung durch Aluminium untersucht. Um die reine Materialabsorption zu isolieren, wurde von allen gemessenen Intensitäten zunächst der Nulleffekt $R_0 = 0.25$ s$^{-1}$ subtrahiert."),
    
    create_code_cell("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Daten für 5.2 (Aluminium, 21 kV)
R_0 = 0.25
dicke_x = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
I_mess = np.array([786.60, 331.80, 146.70, 68.97, 31.10, 17.47, 9.00])
I_korr = I_mess - R_0
ln_I_korr = np.log(I_korr)

# DataFrame zur Darstellung
df_5_2 = pd.DataFrame({
    'Dicke x [mm]': dicke_x,
    'I_mess [1/s]': I_mess,
    'I_korr [1/s]': I_korr,
    'ln(I_korr)': np.round(ln_I_korr, 4)
})
display(df_5_2)

# Plot Intensitätsverlauf (linear)
plt.figure(figsize=(8, 6))
plt.plot(dicke_x, I_korr, 'ro-', label='Korrigierte Messwerte')
plt.xlabel('Dicke x [mm]')
plt.ylabel('Intensität I [1/s]')
plt.title('Intensitätsverlauf (linear)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()"""),

    create_markdown_cell("### Bestimmung des Schwächungskoeffizienten $\\mu$\nDie theoretische Grundlage bildet das Lambert-Beer-Gesetz:\n$I(x) = I_0 \\cdot e^{-\\mu \\cdot x}$\n\nUm den Schwächungskoeffizienten $\\mu$ experimentell zu bestimmen, wird die Gleichung logarithmiert und damit linearisiert:\n$\\ln(I_{korr}) = -\\mu \\cdot x + \\ln(I_0)$"),

    create_code_cell("""# Lineare Regression
def linear_func(x, m, b):
    return m * x + b

popt, pcov = curve_fit(linear_func, dicke_x, ln_I_korr)
m, b = popt
mu = -m

print(f"Steigung m: {m:.3f} mm^-1")
print(f"Schwächungskoeffizient mu: {mu:.3f} mm^-1")

# Halbwertsschichtdicke d_1/2 = ln(2) / mu
d_half = np.log(2) / mu
print(f"Halbwertsschichtdicke d_1/2: {d_half:.3f} mm")

# Plot Bestimmung von mu (halblogarithmisch)
plt.figure(figsize=(8, 6))
plt.plot(dicke_x, ln_I_korr, 'bs', label='Messdaten ln(I)')
plt.plot(dicke_x, linear_func(dicke_x, *popt), 'k--', label=f'Regression ($\\mu$ = {mu:.3f} $mm^{{-1}}$)')
plt.xlabel('Dicke x [mm]')
plt.ylabel('ln(I)')
plt.title('Bestimmung von $\\mu$ (halblogarithmisch)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()"""),

    create_markdown_cell("### 5.3 Absorption verschiedener Materialien\nIn diesem Teil des Versuchs wurde untersucht, wie die Materialart bei identischer Geometrie und konstanter Röhrenspannung die Schwächung der Röntgenstrahlung beeinflusst.\nDie Messungen erfolgten bei einer Schichtdicke von $d = 0.5$ mm und einer Röhrenspannung von $U = 21$ kV."),

    create_code_cell("""# Daten für 5.3
materialien = ['Luft', 'Kohlenstoff (C)', 'Aluminium (Al)', 'Eisen (Fe)', 'Kupfer (Cu)', 'Zirkonium (Zr)', 'Silber (Ag)']
Z_Werte = [7, 6, 13, 26, 29, 40, 47]
I_mess_5_3 = np.array([784.40, 764.00, 334.60, 0.23, 0.10, 2.20, 0.23])

# Wenn I_mess - R_0 <= 0 ist, verwenden wir 0.01 als Näherung, da ln(0) nicht definiert ist
I_korr_5_3 = np.where(I_mess_5_3 - R_0 <= 0, 0.01, I_mess_5_3 - R_0)

d = 0.5 # mm
I_Luft = I_korr_5_3[0]

mu_werte = -np.log(I_korr_5_3 / I_Luft) / d
mu_werte[0] = 0.000 # Für Luft manuell auf 0 setzen

df_5_3 = pd.DataFrame({
    'Material': materialien,
    'Z': Z_Werte,
    'I_mess [1/s]': I_mess_5_3,
    'I_korr [1/s]': I_korr_5_3,
    'mu [mm^-1]': np.round(mu_werte, 3)
})
display(df_5_3)""")
]

nb['cells'].extend(cells_to_add)

with open('Roentgenstrahlung.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Cells successfully added to Roentgenstrahlung.ipynb")
