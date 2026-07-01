import json

def process_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Define the new content for the cells
    cell_4_source = [
        "# TODO: Kalibration durchführen\n",
        "data=pd.read_csv('Data/Kalibration der Abszisse.txt', sep=' ')\n",
        "display(data)\n\n",
        "# Wir fitten ein lineares Modell: x_mm = m * Pixel + c\n",
        "def lin_fit(x, m, c):\n",
        "    return m * x + c\n\n",
        "popt_cal, pcov_cal = curve_fit(lin_fit, data['Pixel'], data['Messuhr[mm]'])\n",
        "print(f\"Kalibrations-Fit: x[mm] = {popt_cal[0]:.6f} * Pixel + {popt_cal[1]:.6f}\")\n\n",
        "plt.figure(figsize=(8, 5))\n",
        "plt.plot(data['Pixel'], data['Messuhr[mm]'], 'o', label='Daten')\n",
        "plt.plot(data['Pixel'], lin_fit(data['Pixel'], *popt_cal), '-', label='Fit')\n",
        "plt.xlabel('Pixel')\n",
        "plt.ylabel('Messuhr [mm]')\n",
        "plt.legend()\n",
        "plt.title('Kalibration der Abszisse')\n",
        "plt.show()\n\n",
        "plt.figure(figsize=(8, 3))\n",
        "residuals_cal = data['Messuhr[mm]'] - lin_fit(data['Pixel'], *popt_cal)\n",
        "plt.plot(data['Pixel'], residuals_cal, 'o', label='Residuen')\n",
        "plt.axhline(0, color='r', linestyle='--')\n",
        "plt.xlabel('Pixel')\n",
        "plt.ylabel('Residuen [mm]')\n",
        "plt.title('Residuen der Kalibration')\n",
        "plt.legend()\n",
        "plt.show()\n\n",
        "# Funktion zur Umrechnung von Pixel in mm\n",
        "def pixel_to_mm(pixel):\n",
        "    return lin_fit(pixel, *popt_cal)\n"
    ]

    cell_5_source = [
        "# TODO: Beugungsbild des Einzelspalts mit theoretischer Beugungsstruktur vergleichen\n",
        "messung1 = pd.read_csv('Data/Messung1.txt', sep=' ')\n",
        "# Pixel in mm umrechnen\n",
        "messung1['x_mm'] = pixel_to_mm(messung1['pixel'])\n\n",
        "# Sinc-Funktion definieren\n",
        "# I(x) = I_0 * (sin(alpha * (x - x0)) / (alpha * (x - x0)))^2 + I_bg\n",
        "def sinc_fit(x, I_0, a, x0, I_bg):\n",
        "    # np.sinc(y) berechnet sin(pi*y)/(pi*y). Daher teilen wir das innere Argument durch pi.\n",
        "    return I_0 * (np.sinc(a * (x - x0) / np.pi))**2 + I_bg\n\n",
        "# Startwerte für den Fit schätzen\n",
        "x0_guess = messung1.loc[messung1['counts'].idxmax(), 'x_mm']\n",
        "I_0_guess = messung1['counts'].max() - messung1['counts'].min()\n",
        "I_bg_guess = messung1['counts'].min()\n",
        "a_guess = 10.0 \n\n",
        "p0 = [I_0_guess, a_guess, x0_guess, I_bg_guess]\n\n",
        "try:\n",
        "    popt_sinc, pcov_sinc = curve_fit(sinc_fit, messung1['x_mm'], messung1['counts'], p0=p0)\n",
        "    print(\"Fit erfolgreich!\")\n",
        "    fit_erfolgreich = True\n",
        "except Exception as e:\n",
        "    print(\"Fit fehlgeschlagen:\", e)\n",
        "    fit_erfolgreich = False\n\n",
        "plt.figure(figsize=(10, 6))\n",
        "plt.plot(messung1['x_mm'], messung1['counts'], '.', label='Messdaten', markersize=2)\n",
        "if fit_erfolgreich:\n",
        "    x_plot = np.linspace(messung1['x_mm'].min(), messung1['x_mm'].max(), 1000)\n",
        "    plt.plot(x_plot, sinc_fit(x_plot, *popt_sinc), '-', label='Theorie-Fit', linewidth=2)\n\n",
        "plt.xlabel('Position [mm]')\n",
        "plt.ylabel('Intensität [counts]')\n",
        "plt.title('Beugungsbild Einzelspalt vs Theorie')\n",
        "plt.legend()\n",
        "plt.show()\n\n",
        "if fit_erfolgreich:\n",
        "    plt.figure(figsize=(10, 3))\n",
        "    residuals_sinc = messung1['counts'] - sinc_fit(messung1['x_mm'], *popt_sinc)\n",
        "    plt.plot(messung1['x_mm'], residuals_sinc, '.', markersize=2, label='Residuen')\n",
        "    plt.axhline(0, color='r', linestyle='--')\n",
        "    plt.xlabel('Position [mm]')\n",
        "    plt.ylabel('Residuen [counts]')\n",
        "    plt.title('Residuen: Beugungsbild Einzelspalt vs Theorie')\n",
        "    plt.legend()\n",
        "    plt.show()\n\n",
        "# Kommentar:\n",
        "# Der theoretische Fit weicht eventuell von der Messung ab, z.B. wenn die Kamera\n",
        "# eine nicht-lineare Antwort hat, an einigen Stellen gesättigt ist oder wenn es\n",
        "# störendes Hintergrundrauschen gibt. Daher ist die Methode über die Minima robuster.\n"
    ]

    cell_6_source = [
        "# TODO: Spaltbreite bestimmen\n",
        "from scipy.signal import find_peaks\n\n",
        "# Wir übergeben -counts, um die Minima (Täler) zu finden\n",
        "# prominence steuert, wie deutlich das Minimum ausgeprägt sein muss\n",
        "peaks, _ = find_peaks(-messung1['counts'], prominence=1, distance=10)\n\n",
        "minima_x = messung1['x_mm'].iloc[peaks].values\n",
        "minima_counts = messung1['counts'].iloc[peaks].values\n",
        "x0_center = messung1.loc[messung1['counts'].idxmax(), 'x_mm']\n\n",
        "peaks_links = np.sort([x for x in minima_x if x < x0_center])[::-1][:5]\n",
        "peaks_rechts = np.sort([x for x in minima_x if x > x0_center])[:5]\n\n",
        "minima_x_clean = []\n",
        "n_clean = []\n\n",
        "for i, x in enumerate(peaks_links):\n",
        "    n_clean.append(-(i+1))\n",
        "    minima_x_clean.append(x)\n",
        "    \n",
        "for i, x in enumerate(peaks_rechts):\n",
        "    n_clean.append(i+1)\n",
        "    minima_x_clean.append(x)\n",
        "    \n",
        "n_clean = np.array(n_clean)\n",
        "minima_x_clean = np.array(minima_x_clean)\n\n",
        "plt.figure(figsize=(10, 6))\n",
        "plt.plot(messung1['x_mm'], messung1['counts'], '-', label='Messung')\n",
        "plt.plot(minima_x_clean, minima_counts, 'ro', label='Gefundene Minima')\n",
        "plt.xlabel('Position [mm]')\n",
        "plt.ylabel('Intensität [counts]')\n",
        "plt.legend()\n",
        "plt.title('Identifizierte Minima zur Spaltbreitenbestimmung')\n",
        "plt.show()\n\n",
        "# linearer Zusammenhang: x_n = (lambda * L / b) * n + x_0\n",
        "def linear_minima(n, m, x0_):\n",
        "    return m * n + x0_\n\n",
        "popt_minima, pcov_minima = curve_fit(linear_minima, n_clean, minima_x_clean)\n",
        "slope = popt_minima[0]\n",
        "slope_err = np.sqrt(np.diag(pcov_minima))[0]\n\n",
        "plt.figure(figsize=(8, 5))\n",
        "plt.errorbar(n_clean, minima_x_clean, yerr=0.05, fmt='bo', label='Minima Positionen')\n",
        "n_plot = np.linspace(n_clean.min(), n_clean.max(), 100)\n",
        "plt.plot(n_plot, linear_minima(n_plot, *popt_minima), 'r-', label='Fit')\n",
        "plt.xlabel('Ordnung n')\n",
        "plt.ylabel('Position x_n [mm]')\n",
        "plt.title('Position der Minima vs Ordnung')\n",
        "plt.legend()\n",
        "plt.show()\n\n",
        "## GEMÄSS VERSUCHSAUFBAU ##\n",
        "lambda_ = 635e-6 # in mm (635 nm)\n",
        "L = 80.0 # in mm\n\n",
        "b = (lambda_ * L) / slope\n",
        "b_err = np.abs(b) * (slope_err / np.abs(slope))\n\n",
        "print(f\"Fit-Steigung (λL/b): {slope:.4f} ± {slope_err:.4f} mm\")\n",
        "print(f\"Berechnete Spaltbreite b: {np.abs(b):.4f} ± {b_err:.4f} mm\")\n",
        "print(f\"(λ={lambda_} mm, L={L} mm)\")\n"
    ]

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_text = "".join(cell['source'])
            if "TODO: Kalibration" in source_text:
                cell['source'] = cell_4_source
            elif "TODO: Beugungsbild" in source_text:
                cell['source'] = cell_5_source
            elif "TODO: Spaltbreite" in source_text:
                cell['source'] = cell_6_source

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

if __name__ == "__main__":
    process_notebook('Fourieroptik_TeilB.ipynb')
